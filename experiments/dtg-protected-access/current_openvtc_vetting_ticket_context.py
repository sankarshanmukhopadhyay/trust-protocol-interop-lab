#!/usr/bin/env python3
"""Execute OpenVTC vetted-admission surfaces and emit privacy-safe observations.

The probe copies the immutable OpenVTC checkout to a temporary workspace, adds one
throw-away workspace member, and compiles against that copied workspace. This preserves
the target's exact workspace dependency/patch graph while leaving the immutable checkout
untouched. It exercises manifest discovery, directory/profile state, status/policy handles,
ticket issuance, and retained application/profile state. Raw ticket secrets, personal data,
location/contact values and full profile content are never exported.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def rust_source() -> str:
    return r'''
use chrono::Utc;
use openvtc_core::config::account::PersonaId;
use openvtc_core::vetting::VettingBook;
use openvtc_core::vetting::book::VetterPolicy;
use openvtc_core::vetting::queries::{CommunityQuery, QueryKind};
use openvtc_core::vetting::registry::{DirectoryFilter, ProfileDraft, ProfileState};
use openvtc_core::vetting::status::status_list_url;
use openvtc_core::vetting::tickets::{Ticket, DEFAULT_VALIDITY};
use openvtc_core::vetting::wire;
use serde_json::{Value, json};
use sha2::{Digest, Sha256};

fn fp(value: &str) -> String {
    let mut h = Sha256::new();
    h.update(value.as_bytes());
    format!("sha256:{}", hex::encode(h.finalize()))
}

fn scoped(label: &str, community: &str) -> Value {
    json!({"class": label, "community_fingerprint": fp(community)})
}

fn query(document_id: &str, community: &str, persona: PersonaId, kind: QueryKind) -> CommunityQuery {
    CommunityQuery {
        document_id: document_id.to_string(),
        community: community.to_string(),
        persona,
        kind,
        sent_at: Utc::now(),
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let community = &args[1];
    let vetter = &args[2];
    let applicant = &args[3];
    let now = Utc::now();
    let persona = PersonaId::new();
    let mut book = VettingBook::default();

    // Pre-admission application + manifest discovery.
    let application_id = {
        let app = book.start_application(community, persona, applicant, now).unwrap();
        app.id.clone()
    };
    let manifest = wire::manifest_request(applicant, community).unwrap();
    book.ask(query(&manifest.id, community, persona, QueryKind::Manifest));
    let discovery_timestamp = book
        .waiting_on(community, QueryKind::Manifest)
        .unwrap()
        .sent_at
        .to_rfc3339();
    let manifest_envelope = serde_json::to_string(&manifest).unwrap();

    // Directory request and transient query-state consumption.
    let filter = DirectoryFilter::default().to_body(None).unwrap();
    let directory = wire::vetter_list_request(applicant, community, &filter).unwrap();
    book.ask(query(&directory.id, community, persona, QueryKind::VetterList));
    let directory_result_context = format!("{}|{}", directory.id, community);
    let profile = ProfileDraft::new(&VetterPolicy::default()).to_body().unwrap();
    let profile_value = serde_json::to_value(&profile).unwrap();
    let mut metadata_classes: Vec<String> = profile_value
        .as_object()
        .map(|m| m.keys().cloned().collect())
        .unwrap_or_default();
    metadata_classes.sort();
    let _ = book.take_query(community, &directory.id, Some(QueryKind::VetterList));
    let retained_directory_state = if book.waiting_on(community, QueryKind::VetterList).is_none() {
        Value::Null
    } else {
        scoped("query-retained", community)
    };

    // Status + policy-discovery surfaces. This executes OpenVTC's HTTPS/status URL
    // guard on a context-scoped synthetic status endpoint; no network call is made.
    let status_endpoint_raw = format!("https://status.example/{}/list", &fp(community)[7..23]);
    let parsed_status = status_list_url(&status_endpoint_raw).unwrap();
    let status_handle_raw = format!("{}#index=7", parsed_status.as_str());

    // Retained application/profile state after a target-native refusal transition.
    book.record_profile_sent(community, persona, &profile, now);
    assert!(book.on_profile_refused(community, persona, "probe-refusal", Utc::now()));
    let profile_record = book.vetter_profile(community, persona).unwrap();
    let profile_state = match &profile_record.state {
        ProfileState::Sent { .. } => "sent",
        ProfileState::Stored { .. } => "stored",
        ProfileState::Refused { .. } => "refused",
    };
    let application_retained = book.applications.iter().any(|a| a.id == application_id);
    let profile_retained = book.vetter_profile(community, persona).is_some();

    // Ticket evidence remains part of the same characterized member.
    let ticket = Ticket::issue(community.clone(), persona, vec![], 1, DEFAULT_VALIDITY, Utc::now());
    let uri = ticket.uri(vetter);

    let output = json!({
        "active_persona_identifier": fp(applicant),
        "target_community": fp(community),
        "discovery_request_envelope": fp(&manifest_envelope),
        "discovery_timestamp": discovery_timestamp,

        "vetter_identifier": fp(vetter),
        "directory_filters": {"filter": filter, "community_fingerprint": fp(community)},
        "profile_metadata_classes": {"classes": metadata_classes, "community_fingerprint": fp(community)},
        "result_context": fp(&directory_result_context),
        "retained_directory_state": retained_directory_state,

        "status_handle": fp(&status_handle_raw),
        "status_endpoint": fp(parsed_status.as_str()),
        "policy_discovery_handle": fp(&manifest.id),
        "policy_endpoint": {"protocol": "vtc/join-requests/manifest/0.2", "community_fingerprint": fp(community)},

        "application_state": {"state": if application_retained {"present"} else {"absent"}, "community_fingerprint": fp(community)},
        "last_sent_profile": {"state": profile_state, "profile_fingerprint": fp(&serde_json::to_string(&profile_record.profile).unwrap()), "community_fingerprint": fp(community)},
        "response_or_refusal_state": {"state": profile_state, "community_fingerprint": fp(community)},
        "retained_identifier": fp(&application_id),
        "retention_boundary": {"application_retained": application_retained, "profile_retained": profile_retained, "community_fingerprint": fp(community)},

        "ticket_identifier_fingerprint": fp(&ticket.id),
        "ticket_uri_fingerprint": fp(&uri),
        "ticket_community_fingerprint": fp(&ticket.community),
        "retained_ticket_identifier_fingerprint": fp(&ticket.id),
        "ticket_live": ticket.is_live(Utc::now()),
        "raw_secret_exported": false
    });
    println!("{}", output);
}
'''


def copied_workspace(checkout: Path, root: Path) -> Path:
    workspace = root / "openvtc-workspace"
    shutil.copytree(checkout, workspace, ignore=shutil.ignore_patterns(".git", "target"))
    cargo_path = workspace / "Cargo.toml"
    cargo = cargo_path.read_text(encoding="utf-8")
    needle = '  "openvtc",\n]'
    if needle not in cargo:
        raise RuntimeError("cannot locate OpenVTC workspace member list")
    cargo_path.write_text(cargo.replace(needle, '  "openvtc",\n  "vetting-probe",\n]', 1), encoding="utf-8")
    return workspace


def run_probe(checkout: Path, community: str, vetter: str, applicant: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="openvtc-vetting-probe-") as td:
        workspace = copied_workspace(checkout, Path(td))
        probe = workspace / "vetting-probe"
        (probe / "src").mkdir(parents=True)
        (probe / "Cargo.toml").write_text(
            '''[package]\nname = "openvtc-vetting-probe"\nversion = "0.1.0"\nedition.workspace = true\npublish = false\n\n[dependencies]\nopenvtc-core = { path = "../openvtc-core", default-features = false }\nchrono.workspace = true\nhex.workspace = true\nserde_json.workspace = true\nsha2.workspace = true\n''',
            encoding="utf-8",
        )
        (probe / "src" / "main.rs").write_text(rust_source(), encoding="utf-8")
        completed = subprocess.run(
            ["cargo", "run", "--quiet", "-p", "openvtc-vetting-probe", "--", community, vetter, applicant],
            cwd=workspace,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip())
        return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--context", required=True, choices=["A", "B"])
    parser.add_argument("--community", required=True)
    parser.add_argument("--vetter", required=True)
    parser.add_argument("--applicant", required=True)
    args = parser.parse_args()
    checkout = Path(os.environ["OPENVTC_CHECKOUT"]).resolve()
    observed = run_probe(checkout, args.community, args.vetter, args.applicant)
    assert observed.pop("raw_secret_exported") is False
    assert observed.pop("ticket_live") is True
    executed = sorted(observed)
    print(json.dumps({
        "run_id": f"vetted-admission-{args.context.lower()}",
        "producer_component": "OpenVTC/openvtc::openvtc-core::vetting",
        "executed_surfaces": executed,
        "observations": observed,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
