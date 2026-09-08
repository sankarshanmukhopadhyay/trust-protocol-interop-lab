#!/usr/bin/env python3
"""Execute one bounded Track-A observation against the current pinned OpenVTC revision.

This adapter is intentionally separate from the historical Dogwood adapter. It executes
current VTI E2E test support through an additive temporary probe, records only surfaces
materially exercised by that path, and makes no privacy judgment. Null values are paired
with an explicit executed_surfaces list so the A/B capture contract can distinguish
absence from an unexecuted surface.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap
import uuid

OPENVTC_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
OPENVTC_REVISION = "72bf5794071971da506eb7a5af8e4765c35c137c"
MARKER = "RAHP_RUNTIME_OBSERVATION="

PROBE_TEMPLATE = r'''use ed25519_dalek::SigningKey;
use serde_json::json;
use vta_sdk::did_key::ed25519_multibase_pubkey;
use vta_sdk::didcomm_session::DIDCommSession;

mod common;
use common::test_vta_responder::{ResponderReply, TestVtaResponder};

fn did_key_from_seed(seed_byte: u8) -> (String, String) {
    let seed = [seed_byte; 32];
    let sk = SigningKey::from_bytes(&seed);
    let pk = sk.verifying_key().to_bytes();
    let did = format!("did:key:{}", ed25519_multibase_pubkey(&pk));
    let mut buf = vec![0x80, 0x26];
    buf.extend_from_slice(&seed);
    let priv_mb = multibase::encode(multibase::Base::Base58Btc, &buf);
    (did, priv_mb)
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn rahp_current_track_a_observation() {
    common::init_tracing();
    let verifier = std::env::var("RAHP_VERIFIER").expect("RAHP_VERIFIER");
    let purpose = std::env::var("RAHP_PURPOSE").expect("RAHP_PURPOSE");
    let challenge = std::env::var("RAHP_CHALLENGE").expect("RAHP_CHALLENGE");
    let (client_did, client_priv) = did_key_from_seed(__CLIENT_SEED__);

    let (mediator, responder) =
        TestVtaResponder::spawn_with_mediator(vec![client_did.clone()], |msg_type, _body| {
            if msg_type.ends_with("/list-keys") {
                ResponderReply::ok(format!("{msg_type}-result"), json!({"keys": [], "total": 0}))
            } else {
                ResponderReply::problem_report("e.p.msg.not-found", "no handler")
            }
        }).await.expect("current VTI responder spawns with mediator");

    let session = DIDCommSession::connect(&client_did, &client_priv, responder.did(), mediator.did())
        .await.expect("current VTI DIDComm session connects");
    let message_type = "https://firstperson.network/protocols/key-management/1.0/list-keys";
    let response_type = "https://firstperson.network/protocols/key-management/1.0/list-keys-result";
    let resp: serde_json::Value = session.send_and_wait(
        message_type, json!({"offset": 0, "limit": 10}), response_type, 10,
    ).await.expect("current VTI round-trip returns responder body");

    let observation = json!({"observations": {
        "relationship_did": null,
        "edge_identifier": null,
        "equivalent_relationship_binder": client_did,
        "status_handle": null,
        "status_endpoint": null,
        "policy_discovery_handle": null,
        "policy_endpoint": null,
        "task_identifier": null,
        "thread_identifier": null,
        "retained_relationship_evidence": null,
        "retained_outcome_evidence": null,
        "verifier_transcript": format!("client={};responder={};mediator={};type={};response={};total={}", client_did, responder.did(), mediator.did(), message_type, response_type, resp["total"]),
        "challenge": challenge,
        "purpose": purpose,
        "transaction_context": verifier,
        "deliberate_join_attempt": format!("{}|{}|{}", client_did, responder.did(), message_type)
    }});
    println!("RAHP_RUNTIME_OBSERVATION={}", observation);
    session.shutdown().await;
    responder.shutdown().await;
    mediator.shutdown();
    mediator.join().await.expect("mediator joins");
}
'''


def run(*args: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, env=env, text=True, capture_output=True, check=False)


def verify_checkout(checkout: Path) -> None:
    if not (checkout / ".git").exists():
        raise ValueError(f"OpenVTC checkout is not a git repository: {checkout}")
    head = run("git", "rev-parse", "HEAD", cwd=checkout)
    if head.returncode != 0:
        raise RuntimeError(head.stderr.strip() or "cannot resolve OpenVTC checkout HEAD")
    actual = head.stdout.strip()
    if actual != OPENVTC_REVISION:
        raise ValueError(f"OpenVTC checkout must be pinned to {OPENVTC_REVISION}; observed {actual}")


def execute_context(checkout: Path, context: str, verifier: str, purpose: str, challenge: str, client_seed: int) -> dict[str, object]:
    verify_checkout(checkout)
    probe = checkout / "tests" / "e2e" / "tests" / "rahp_current_track_a_observation.rs"
    if probe.exists():
        raise ValueError(f"refusing to overwrite existing upstream file: {probe}")
    probe.write_text(PROBE_TEMPLATE.replace("__CLIENT_SEED__", f"0x{client_seed:02x}"), encoding="utf-8")
    env = os.environ.copy()
    env.update({"RAHP_VERIFIER": verifier, "RAHP_PURPOSE": purpose, "RAHP_CHALLENGE": challenge, "RUST_LOG": env.get("RUST_LOG", "warn")})
    try:
        completed = run("cargo", "test", "-p", "vti-e2e-tests", "--test", "rahp_current_track_a_observation", "--", "--nocapture", cwd=checkout, env=env)
    finally:
        probe.unlink(missing_ok=True)
    if completed.returncode != 0:
        detail = "\n".join(part for part in (completed.stdout.strip(), completed.stderr.strip()) if part)
        raise RuntimeError(f"current OpenVTC runtime probe failed:\n{detail[-12000:]}")
    marker_lines = [line for line in completed.stdout.splitlines() if MARKER in line]
    if len(marker_lines) != 1:
        raise RuntimeError(f"expected exactly one {MARKER} marker, observed {len(marker_lines)}")
    doc = json.loads(marker_lines[0].split(MARKER, 1)[1].strip())
    observations = doc.get("observations") if isinstance(doc, dict) else None
    if not isinstance(observations, dict):
        raise RuntimeError("current OpenVTC observation marker has no observations mapping")
    return {
        "run_id": f"current-openvtc-{context.lower()}-{uuid.uuid4()}",
        "implementation_repository": OPENVTC_REPOSITORY,
        "implementation_revision": OPENVTC_REVISION,
        "context": {"label": context, "verifier": verifier, "purpose": purpose, "challenge": challenge},
        "executed_surfaces": ["relationship_did", "edge_identifier", "equivalent_relationship_binder", "verifier_transcript", "challenge", "purpose", "transaction_context", "deliberate_join_attempt"],
        "observations": observations,
        "producer_component": OPENVTC_REPOSITORY,
        "assurance_boundary": "Current pinned VTI crates/test support executed. Status/policy and Trust Task surfaces are not marked executed by this path, so they remain not-evidenced rather than absent. No privacy conclusion is made."
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", type=Path, default=Path(os.environ.get("OPENVTC_CHECKOUT", "build/current-openvtc")))
    parser.add_argument("--context", choices=["A", "B"], required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--challenge", required=True)
    parser.add_argument("--client-seed", type=lambda value: int(value, 0), required=True)
    args = parser.parse_args()
    if not 0 <= args.client_seed <= 255:
        raise ValueError("--client-seed must fit in one byte")
    print(json.dumps(execute_context(args.checkout.resolve(), args.context, args.verifier, args.purpose, args.challenge, args.client_seed), sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(textwrap.fill(f"ERROR: {exc}", width=120), file=sys.stderr)
        raise SystemExit(2)
