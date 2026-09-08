#!/usr/bin/env python3
"""Capture target-generated Trust Task / retained relationship evidence from OpenVTC.

The observer transiently instruments the target's existing relationship integration test
only to print values that the target itself generates and already asserts over. The file
is restored byte-for-byte after execution. No production code is changed and the target
checkout must be clean before and after the run.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

OPENVTC_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
OPENVTC_REVISION = "72bf5794071971da506eb7a5af8e4765c35c137c"
MARKER = "RAHP_TRACK_B_TASK="
TARGET_TEST = Path("vtc-service/tests/relationships.rs")
MECHANICAL_LOCKFILES = {"Cargo.lock", "vtc-service/admin-ui/package-lock.json"}
NEEDLE = '        assert_eq!(body["recipient"], did_for(MEMBER));\n'
INJECTION = r'''        assert_eq!(body["recipient"], did_for(MEMBER));

        let mut rahp_audit_vrc_id: Option<String> = None;
        for (_k, raw) in fix.audit_ks.prefix_iter_raw(Vec::new()).await.unwrap() {
            let env: AuditEnvelope = serde_json::from_slice(&raw).unwrap();
            if let AuditEvent::VrcPublished(d) = env.event {
                rahp_audit_vrc_id = Some(d.vrc_id);
            }
        }
        let rahp_observation = json!({
            "task_identifier": body["id"],
            "thread_identifier": body["threadId"],
            "retained_relationship_evidence": body["payload"]["id"],
            "retained_outcome_evidence": rahp_audit_vrc_id,
        });
        println!("RAHP_TRACK_B_TASK={}", rahp_observation);
'''


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, text=True, capture_output=True, check=False)


def verify_checkout(checkout: Path) -> None:
    head = run("git", "rev-parse", "HEAD", cwd=checkout)
    if head.returncode != 0:
        raise RuntimeError(head.stderr.strip() or "cannot resolve OpenVTC checkout HEAD")
    if head.stdout.strip() != OPENVTC_REVISION:
        raise ValueError(
            f"OpenVTC checkout must be pinned to {OPENVTC_REVISION}; observed {head.stdout.strip()}"
        )
    status = run("git", "status", "--porcelain", cwd=checkout)
    if status.stdout.strip():
        raise ValueError("OpenVTC checkout must be clean before Track B task observation")


def restore_known_build_lock_refreshes(checkout: Path) -> None:
    status = run("git", "status", "--porcelain", "--untracked-files=no", cwd=checkout)
    lines = [line for line in status.stdout.splitlines() if line.strip()]
    changed = {line[3:] for line in lines}
    if not changed:
        return
    if changed.issubset(MECHANICAL_LOCKFILES):
        restored = run("git", "checkout", "--", *sorted(changed), cwd=checkout)
        if restored.returncode != 0:
            raise RuntimeError(restored.stderr.strip() or "could not restore build lockfiles")
        return
    raise RuntimeError(f"target test changed unexpected tracked files: {lines}")


def observe(checkout: Path, context: str) -> dict[str, object]:
    verify_checkout(checkout)
    path = checkout / TARGET_TEST
    original = path.read_text(encoding="utf-8")
    if original.count(NEEDLE) != 1:
        raise ValueError("target relationships test shape changed; refusing ambiguous instrumentation")
    instrumented = original.replace(NEEDLE, INJECTION, 1)
    path.write_text(instrumented, encoding="utf-8")
    try:
        completed = run(
            "cargo",
            "test",
            "-p",
            "vtc-service",
            "--test",
            "relationships",
            "pairwise::publishes_under_a_relationship_did",
            "--",
            "--exact",
            "--nocapture",
            cwd=checkout,
        )
    finally:
        path.write_text(original, encoding="utf-8")
    restore_known_build_lock_refreshes(checkout)

    if completed.returncode != 0:
        detail = "\n".join(x for x in (completed.stdout.strip(), completed.stderr.strip()) if x)
        raise RuntimeError(f"OpenVTC relationship Trust Task test failed:\n{detail[-12000:]}")
    marker_lines = [line for line in completed.stdout.splitlines() if MARKER in line]
    if len(marker_lines) != 1:
        raise RuntimeError(f"expected exactly one {MARKER} marker, observed {len(marker_lines)}")
    observation = json.loads(marker_lines[0].split(MARKER, 1)[1].strip())
    required = (
        "task_identifier",
        "thread_identifier",
        "retained_relationship_evidence",
        "retained_outcome_evidence",
    )
    if any(not isinstance(observation.get(k), str) or not observation[k] for k in required):
        raise RuntimeError(f"target observation missing required generated value: {observation}")

    return {
        "run_id": f"current-openvtc-track-b-task-{context.lower()}-{uuid.uuid4()}",
        "implementation_repository": OPENVTC_REPOSITORY,
        "implementation_revision": OPENVTC_REVISION,
        "executed_surfaces": list(required),
        "observations": observation,
        "producer_component": OPENVTC_REPOSITORY,
        "assurance_boundary": (
            "The target's existing pairwise relationship publish integration path executed. "
            "Values are target-generated Trust Task response, persisted relationship and audit "
            "identifiers exposed only through temporary test instrumentation. Only known "
            "Cargo/npm lockfile rewrites caused by the newer CI toolchain are restored before "
            "evidence return."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        type=Path,
        default=Path(os.environ.get("OPENVTC_CHECKOUT", "build/current-openvtc")),
    )
    parser.add_argument("--context", choices=["A", "B"], required=True)
    args = parser.parse_args()
    print(json.dumps(observe(args.checkout.resolve(), args.context), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
