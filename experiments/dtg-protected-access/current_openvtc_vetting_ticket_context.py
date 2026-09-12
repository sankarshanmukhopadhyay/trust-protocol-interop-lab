#!/usr/bin/env python3
"""Execute a minimal OpenVTC vetting-ticket probe and emit privacy-safe observations.

The probe copies the immutable OpenVTC checkout to a temporary workspace, adds one
throw-away workspace member, and compiles against that copied workspace. This preserves
the target's exact workspace dependency/patch graph while leaving the immutable checkout
untouched. It never emits raw ticket codes, ids, secrets, or URIs.
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
use openvtc_core::vetting::tickets::{Ticket, DEFAULT_VALIDITY};
use sha2::{Digest, Sha256};
use serde_json::json;

fn fp(value: &str) -> String {
    let mut h = Sha256::new();
    h.update(value.as_bytes());
    format!("sha256:{:x}", h.finalize())
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let community = &args[1];
    let vetter = &args[2];
    let ticket = Ticket::issue(community.clone(), PersonaId::new(), vec![], 1, DEFAULT_VALIDITY, Utc::now());
    let uri = ticket.uri(vetter);
    let output = json!({
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


def run_probe(checkout: Path, community: str, vetter: str) -> dict:
    with tempfile.TemporaryDirectory(prefix="openvtc-vetting-probe-") as td:
        workspace = copied_workspace(checkout, Path(td))
        probe = workspace / "vetting-probe"
        (probe / "src").mkdir(parents=True)
        (probe / "Cargo.toml").write_text(
            '''[package]\nname = "openvtc-vetting-probe"\nversion = "0.1.0"\nedition.workspace = true\npublish = false\n\n[dependencies]\nopenvtc-core = { path = "../openvtc-core", default-features = false }\nchrono.workspace = true\nserde_json.workspace = true\nsha2.workspace = true\n''',
            encoding="utf-8",
        )
        (probe / "src" / "main.rs").write_text(rust_source(), encoding="utf-8")
        completed = subprocess.run(
            ["cargo", "run", "--quiet", "-p", "openvtc-vetting-probe", "--", community, vetter],
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
    args = parser.parse_args()
    checkout = Path(os.environ["OPENVTC_CHECKOUT"]).resolve()
    observed = run_probe(checkout, args.community, args.vetter)
    assert observed.pop("raw_secret_exported") is False
    assert observed.pop("ticket_live") is True
    print(json.dumps({
        "run_id": f"vetted-admission-{args.context.lower()}",
        "producer_component": "OpenVTC/openvtc::openvtc-core::vetting::tickets",
        "executed_surfaces": [
            "ticket_identifier_fingerprint",
            "ticket_uri_fingerprint",
            "ticket_community_fingerprint",
            "retained_ticket_identifier_fingerprint",
        ],
        "observations": observed,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
