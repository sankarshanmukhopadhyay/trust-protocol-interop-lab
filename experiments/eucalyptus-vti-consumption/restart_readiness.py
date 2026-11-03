#!/usr/bin/env python3
"""Source-pinned admission gate for an actual Eucalyptus restart/commit-point experiment.

This is a *feasibility* record, NOT a process-restart test or a native PASS.
It refuses to translate in-process fixture success into crash-consistency evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

TARGET = "49f5f1beb61adc34bdf7cf0bd3eb10f594415b80"
REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
SOURCES = {
    "fixture": "vta-service/src/test_support.rs",
    "consumer": "vta-service/tests/it/idempotency_trust_task.rs",
    "dispatch": "vta-service/src/trust_tasks/mod.rs",
    "policy": "vta-service/src/trust_tasks/idempotency.rs",
    "store": "vti-common/src/idempotency/store.rs",
    "restart": "tests/e2e/tests/common/restart.rs",
}
ANCHORS = {
    "fixture": ("pub async fn build_test_app_with", "let dir = tempfile::tempdir()", "open_with_keyspaces(dir.path()"),
    "consumer": ("async fn a_retry_under_the_same_key_converges_to_one_effect", "let (router, token) = app().await", "key_count(&router, &token).await"),
    "dispatch": ("idempotency::claim(&state.idempotency_ks", "dispatch_typed(state, auth, doc)", "idempotency::record_outcome(&state.idempotency_ks"),
    "policy": ("IN_FLIGHT_GRACE_MINS: i64 = 10", "idempotency claim failed; dispatching unguarded", "failed to record an idempotent outcome; a retry may re-run this task"),
    "store": ("if now - existing.created_at > in_flight_grace", "return Ok(ClaimOutcome::Claimed)", "ClaimOutcome::Completed"),
    "restart": ("pub fn simulate_restart(data_dir: &Path) -> Store", "Re-open the store at", "snapshot_survives_simulated_restart"),
}


def repo_head(target: Path) -> str:
    return subprocess.check_output(["git", "-C", str(target), "rev-parse", "HEAD"], text=True).strip()


def check(target: Path) -> dict:
    if repo_head(target) != TARGET:
        raise ValueError("immutable Eucalyptus target revision mismatch")
    # Ignore untracked Cargo outputs, reject altered tracked implementation.
    dirty = subprocess.check_output(["git", "-C", str(target), "diff", "HEAD", "--"], text=True)
    if dirty:
        raise ValueError("target has modified tracked source")
    pins = []
    for role, relative in SOURCES.items():
        path = target / relative
        raw = path.read_bytes()
        source = raw.decode("utf-8")
        matches = []
        for marker in ANCHORS[role]:
            if source.count(marker) != 1:
                raise ValueError(f"{role}: missing/ambiguous frozen source anchor: {marker}")
            matches.append({"text": marker, "line": source[:source.index(marker)].count("\n") + 1})
        pins.append({"role": role, "path": relative,
                     "sha256": hashlib.sha256(raw).hexdigest(), "anchors": matches})
    fixture = (target / SOURCES["fixture"]).read_text()
    assert fixture.index("let dir = tempfile::tempdir()", fixture.index("pub async fn build_test_app_with")) > 0
    dispatcher = (target / SOURCES["dispatch"]).read_text()
    if not (dispatcher.index("idempotency::claim(&state.idempotency_ks") <
            dispatcher.index("dispatch_typed(state, auth, doc)") <
            dispatcher.index("idempotency::record_outcome(&state.idempotency_ks")):
        raise ValueError("unexpected idempotency dispatcher ordering")

    return {
        "schema": "eucalyptus-restart-feasibility/v1",
        "target": {"repository": REPOSITORY, "revision": TARGET},
        "source_inventory": pins,
        "consumer_post_restart_observation": "NOT_EXECUTED",
        "reason": "The existing service integration-test app allocates a fresh owned temporary store; its retry suite does not reconstruct a service against the original retained database.",
        "source_supported_hypothesis": "An interruption after effect commit but before idempotency completion may leave an in-flight claim; after grace-based reclaim, a duplicate effect may be possible. No such effect is observed or claimed here.",
        "existing_evidence": "Four previously executed in-process consuming vectors remain valid at their original source pin; they are not restarted-service evidence.",
        "restart_store_helper_scope": "An e2e test helper reopens persistent fjall state for service-management snapshots, not the keyed Trust Task consumer/router and consequential effect.",
        "required_test_seam": [
            "Reconstruct an actual VTA router/service against the SAME retained keyspaces and persistent database after teardown.",
            "Exercise the same signed keyed operation before restart; inspect its concrete stored effect and retained idempotency record.",
            "Reopen from disk with no old router or keyspace handles and retry a fresh envelope under the same logical key; inspect effect count and identity.",
            "Exercise same-key changed-payload refusal after restart and verify no added effect.",
            "Separately inject interruption between effect commit and idempotency completion to determine whether stale-claim recovery is safe or duplicates.",
            "Retain exact target and test-harness revisions, commands, logs, clock/state and SHA-256 evidence; never infer deployed composition PASS.",
        ],
        "assurance_state": "INDETERMINATE",
        "composition_pass": 0,
        "closed_propositions": [],
        "disposition": "BLOCKED_MISSING_CONSUMER_RESTART_FIXTURE",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    try:
        record = check(args.target.resolve())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(record["disposition"])
        return 0  # successfully *observed an unavailable assurance boundary*
    except (OSError, subprocess.SubprocessError, UnicodeError, ValueError, AssertionError) as e:
        print(f"RESTART_FEASIBILITY_ERROR: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
