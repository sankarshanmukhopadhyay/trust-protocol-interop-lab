#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

TARGET_REVISION = "56cd6e5b7116777f1d9734e76c9a7b0569870e19"


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> dict:
    cp = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, env=env, check=False)
    return {
        "command": " ".join(cmd),
        "returncode": cp.returncode,
        "stdout_tail": cp.stdout[-4000:],
        "stderr_tail": cp.stderr[-4000:],
    }


def require(text: str, needle: str, label: str) -> dict:
    return {"label": label, "needle": needle, "present": needle in text}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    target = Path(args.target).resolve()
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=target, text=True).strip()
    if head != TARGET_REVISION:
        raise SystemExit(f"target pin mismatch: {head} != {TARGET_REVISION}")

    lifecycle = run(["cargo", "test", "-p", "vti-rooms", "-p", "vti-rooms-dtg", "-p", "room-host"], target)
    vtc_rooms = run(["cargo", "test", "-p", "vtc-service", "rooms::", "--lib"], target)

    design = (target / "docs/05-design-notes/data-rooms.md").read_text(encoding="utf-8")
    anchoring = (target / "docs/05-design-notes/data-rooms-epoch-anchoring.md").read_text(encoding="utf-8")
    handlers = (target / "vtc-service/src/rooms/handlers.rs").read_text(encoding="utf-8")

    source_checks = [
        require(handlers, "authorized by the chain the room issued and nothing else", "room authority is independent of host-local ACL/session state"),
        require(design, "removal stays forward-only", "removed member cannot read future epochs"),
        require(design, "one write-primary", "host topology has a defined single write-primary"),
        require(design, "Host-neutral by construction", "record identity does not name the host"),
        require(anchoring, "not implemented", "witnessed epoch anchoring is explicitly not implemented"),
        require(design, "Untrusted in the human direction too", "human rendering threat is specified"),
        require(design, "data, never", "agent-memory instruction-isolation requirement is specified"),
    ]

    target_native_pass = lifecycle["returncode"] == 0 and vtc_rooms["returncode"] == 0
    all_source_checks = all(x["present"] for x in source_checks)

    propositions = {
        "P-ROOM-005": {
            "state": "SATISFIED_WITH_BOUNDARY" if target_native_pass else "EVIDENCE_REQUIRED",
            "basis": "target-native room lifecycle/authorization tests plus source-pinned room-chain authorization semantics",
            "boundary": "current OpenVTC implementation at the pinned revision; not deployment-wide current-authority assurance",
        },
        "P-ROOM-012": {
            "state": "SATISFIED_WITH_BOUNDARY" if target_native_pass else "EVIDENCE_REQUIRED",
            "basis": "target-native succession/room tests and forward-only removal semantics",
            "boundary": "does not establish governance/operator independence outside the implementation",
        },
        "P-ROOM-013": {
            "state": "PARTIALLY_SATISFIED",
            "basis": "host-neutral room/record identity and owner-transfer/write-primary semantics are implemented",
            "remaining": "stale endpoint, in-flight write, and complete host-migration continuity are not separately exercised",
        },
        "P-ROOM-009": {
            "state": "EVIDENCE_REQUIRED",
            "basis": "the design defines witnessed fork detection but the pinned implementation still describes witnessed epoch anchoring as not implemented",
        },
        "P-ROOM-010": {
            "state": "EVIDENCE_REQUIRED",
            "basis": "client watermarks exist architecturally, but fresh-client witnessed version-floor/rollback anchoring is not implemented",
        },
        "P-ROOM-014": {
            "state": "EVIDENCE_REQUIRED",
            "basis": "the design requires recalled room content to remain data rather than instruction, but no target-native composed agent execution is evidenced here",
        },
        "P-ROOM-015": {
            "state": "EVIDENCE_REQUIRED",
            "basis": "record authorship semantics are specified, but downstream recall provenance through an agent runtime is not exercised",
        },
        "P-ROOM-016": {
            "state": "EVIDENCE_REQUIRED",
            "basis": "inert human rendering is a specified security requirement, but no target-native human renderer is exercised",
        },
    }

    result = {
        "schema": "interop-evidence-package/v1",
        "case": "IC-DTG-DATA-ROOM-RUNTIME-001",
        "source_issue": 185,
        "target": {
            "repository": "OpenVTC/verifiable-trust-infrastructure",
            "revision": TARGET_REVISION,
        },
        "evidence_class": "runtime-upstream-observation",
        "target_native_tests": {
            "rooms_and_host": lifecycle,
            "vtc_service_rooms": vtc_rooms,
            "all_passed": target_native_pass,
        },
        "source_checks": source_checks,
        "all_source_checks_present": all_source_checks,
        "propositions": propositions,
        "claim_boundary": "This evidence advances only proposition-specific implementation maturity. Missing private-room ZK, witnessed anchoring, operator-control evidence, host-migration edge cases, and composed agent/human runtimes remain explicit residuals rather than PASS.",
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if target_native_pass and all_source_checks else 1


if __name__ == "__main__":
    raise SystemExit(main())
