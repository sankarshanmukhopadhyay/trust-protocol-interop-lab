#!/usr/bin/env python3
"""Execute one attributable Dogwood RC-1 observation context.

This is a deliberately narrow target adapter for Interop Lab issue #64. It verifies
an immutable upstream checkout, adds a temporary integration-test *probe* alongside
Dogwood's own E2E tests, executes that probe against the pinned Dogwood crates and
test-support surface, captures the explicit runtime observation marker, and then
removes the probe source.

The adapter does not modify Dogwood production code and does not make a privacy
judgment. A null surface means that surface is absent from this deliberately bounded
Dogwood execution path; it is not a claim that the surface can never exist elsewhere
in VTI or in a wider composition.
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

DOGWOOD_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
DOGWOOD_REVISION = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"
MARKER = "RAHP_RUNTIME_OBSERVATION="

PROBE = r'''use ed25519_dalek::SigningKey;
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
async fn rahp_runtime_observation() {
    common::init_tracing();

    let verifier = std::env::var("RAHP_VERIFIER").expect("RAHP_VERIFIER");
    let purpose = std::env::var("RAHP_PURPOSE").expect("RAHP_PURPOSE");
    let challenge = std::env::var("RAHP_CHALLENGE").expect("RAHP_CHALLENGE");

    // Deliberately keep the same deterministic client DID in both runs. This is
    // the bounded "same underlying relationship" anchor and is intentionally
    // observable so the A/B harness can detect a durable join surface.
    let (client_did, client_priv) = did_key_from_seed(0x11);

    let (mediator, responder) =
        TestVtaResponder::spawn_with_mediator(vec![client_did.clone()], |msg_type, _body| {
            if msg_type.ends_with("/list-keys") {
                ResponderReply::ok(
                    format!("{msg_type}-result"),
                    json!({"keys": [], "total": 0}),
                )
            } else {
                ResponderReply::problem_report("e.p.msg.not-found", "no handler")
            }
        })
        .await
        .expect("responder spawns with mediator");

    let session = DIDCommSession::connect(
        &client_did,
        &client_priv,
        responder.did(),
        mediator.did(),
    )
    .await
    .expect("Dogwood DIDComm session connects");

    let message_type = "https://firstperson.network/protocols/key-management/1.0/list-keys";
    let response_type = "https://firstperson.network/protocols/key-management/1.0/list-keys-result";
    let resp: serde_json::Value = session
        .send_and_wait(
            message_type,
            json!({"offset": 0, "limit": 10}),
            response_type,
            10,
        )
        .await
        .expect("Dogwood round-trip returns responder body");

    let observation = json!({
        "observations": {
            // Dogwood does not expose a named relationship-DID/edge-ID in this
            // bounded path, but its protocol-visible client DID is an equivalent
            // durable relationship binder and is therefore intentionally retained.
            "relationship_did": null,
            "edge_identifier": null,
            "equivalent_relationship_binder": client_did,

            // This selected Dogwood DIDComm list-keys execution performs no
            // status or policy-discovery operation. These are bounded execution
            // absences, not global VTI claims.
            "status_handle": null,
            "status_endpoint": null,
            "policy_discovery_handle": null,
            "policy_endpoint": null,

            // The selected Dogwood path is not a Trust Task execution. Again,
            // absence is scoped to this execution rather than the wider DTG composition.
            "task_identifier": null,
            "thread_identifier": null,
            "retained_relationship_evidence": null,
            "retained_outcome_evidence": null,

            // Direct runtime/context observations from the executed upstream path.
            "verifier_transcript": format!(
                "client={};responder={};mediator={};type={};response={};total={}",
                client_did,
                responder.did(),
                mediator.did(),
                message_type,
                response_type,
                resp["total"]
            ),
            "challenge": challenge,
            "purpose": purpose,
            "transaction_context": verifier,
            "deliberate_join_attempt": format!("{}|{}|{}", client_did, responder.did(), message_type)
        }
    });

    println!("RAHP_RUNTIME_OBSERVATION={}", observation);

    session.shutdown().await;
    responder.shutdown().await;
    mediator.shutdown();
    mediator.join().await.expect("mediator joins");
}
'''


def run(*args: str, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args), cwd=cwd, env=env, text=True, capture_output=True, check=False
    )


def verify_checkout(checkout: Path) -> None:
    if not (checkout / ".git").exists():
        raise ValueError(f"Dogwood checkout is not a git repository: {checkout}")
    head = run("git", "rev-parse", "HEAD", cwd=checkout)
    if head.returncode != 0:
        raise RuntimeError(head.stderr.strip() or "cannot resolve Dogwood checkout HEAD")
    actual = head.stdout.strip()
    if actual != DOGWOOD_REVISION:
        raise ValueError(
            f"Dogwood checkout must be pinned to {DOGWOOD_REVISION}; observed {actual}"
        )


def execute_context(
    checkout: Path, context: str, verifier: str, purpose: str, challenge: str
) -> dict[str, object]:
    verify_checkout(checkout)
    probe = checkout / "tests" / "e2e" / "tests" / "rahp_runtime_observation.rs"
    if probe.exists():
        raise ValueError(f"refusing to overwrite existing upstream file: {probe}")
    probe.write_text(PROBE, encoding="utf-8")
    env = os.environ.copy()
    env.update(
        {
            "RAHP_VERIFIER": verifier,
            "RAHP_PURPOSE": purpose,
            "RAHP_CHALLENGE": challenge,
            "RUST_LOG": env.get("RUST_LOG", "warn"),
        }
    )
    try:
        completed = run(
            "cargo",
            "test",
            "-p",
            "vti-e2e-tests",
            "--test",
            "rahp_runtime_observation",
            "--",
            "--nocapture",
            cwd=checkout,
            env=env,
        )
    finally:
        probe.unlink(missing_ok=True)

    if completed.returncode != 0:
        detail = "\n".join(
            part for part in (completed.stdout.strip(), completed.stderr.strip()) if part
        )
        raise RuntimeError(f"Dogwood runtime probe failed:\n{detail[-12000:]}")

    marker_lines = [line for line in completed.stdout.splitlines() if MARKER in line]
    if len(marker_lines) != 1:
        raise RuntimeError(
            f"expected exactly one {MARKER} marker, observed {len(marker_lines)}"
        )
    raw = marker_lines[0].split(MARKER, 1)[1].strip()
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Dogwood observation marker was not JSON: {exc}") from exc
    observations = doc.get("observations") if isinstance(doc, dict) else None
    if not isinstance(observations, dict):
        raise RuntimeError("Dogwood observation marker has no observations mapping")

    return {
        "run_id": f"dogwood-{context.lower()}-{uuid.uuid4()}",
        "implementation_repository": DOGWOOD_REPOSITORY,
        "implementation_revision": DOGWOOD_REVISION,
        "context": {
            "label": context,
            "verifier": verifier,
            "purpose": purpose,
            "challenge": challenge,
        },
        "observations": observations,
        "assurance_boundary": (
            "Actual pinned Dogwood crates/test support executed. The additive probe is an "
            "observer, not a production-code modification. Null surfaces are bounded "
            "absences from this selected execution, not global VTI claims, and no privacy "
            "conclusion is made."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        type=Path,
        default=Path(os.environ.get("DOGWOOD_CHECKOUT", "build/dogwood-rc1")),
    )
    parser.add_argument("--context", choices=["A", "B"], required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--challenge", required=True)
    args = parser.parse_args()
    result = execute_context(
        args.checkout.resolve(), args.context, args.verifier, args.purpose, args.challenge
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(textwrap.fill(f"ERROR: {exc}", width=120), file=sys.stderr)
        raise SystemExit(2)
