#!/usr/bin/env python3
"""Compose WD02 VDC/VAC semantics with the real Lab actuation boundary.

This is deliberately a cross-evidence evaluator. It does not pretend the current
OpenVTC implementation exposes the entire adopted VDC/VAC contract. Instead it
requires the semantic non-substitution layer to pass and verifies that the closest
real consequential-action boundary fails closed, with no effect, when exact current
authority cannot be resolved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "results" / "dtg-vdc-vac-composition" / "action-time-results.json"


def run_json(path: str) -> dict:
    cp = subprocess.run([sys.executable, path], cwd=ROOT, text=True, capture_output=True, check=False)
    if cp.returncode != 0:
        raise RuntimeError(f"{path} failed: {cp.stderr.strip() or cp.stdout.strip()}")
    return json.loads(cp.stdout)


def vector_by_id(result: dict, vector_id: str) -> dict:
    return next(v for v in result["vectors"] if v["id"] == vector_id)


def build_result() -> dict:
    semantic = run_json("experiments/dtg-vdc-vac-composition/run.py")
    authority = run_json("experiments/protected-delegated-care/run_authority_boundary.py")

    positive = vector_by_id(semantic, "VDV-POS-001")
    no_authority = vector_by_id(semantic, "VDV-NEG-001")
    no_delegation = vector_by_id(semantic, "VDV-NEG-002")
    narrower = vector_by_id(semantic, "VDV-NEG-003")
    authority_withdrawn = vector_by_id(semantic, "VDV-NEG-004")
    delegation_revoked = vector_by_id(semantic, "VDV-NEG-005")
    invocation_mismatch = vector_by_id(semantic, "VDV-NEG-007")

    vectors = [
        {
            "id": "AT-POS-001",
            "proposition": "valid VDC and VAC remain necessary but are not sufficient without an exact current-authority actuation result",
            "semantic_decision": positive["decision"],
            "runtime_decision": authority["canonical_attempt"]["authorization"],
            "execution": authority["canonical_attempt"]["execution"],
            "state_mutation": authority["canonical_attempt"]["state_mutation"],
            "expected": "indeterminate-blocked-no-effect",
            "matches_expected": positive["decision"] == "allow"
            and authority["canonical_attempt"]["authorization"] == "indeterminate"
            and authority["canonical_attempt"]["execution"] == "blocked"
            and authority["canonical_attempt"]["state_mutation"] is False,
        },
        {
            "id": "AT-NEG-001",
            "proposition": "VDC cannot authorize after principal authority is withdrawn",
            "semantic_decision": authority_withdrawn["decision"],
            "runtime_local_control": authority["application_local_comparison"]["result"]["authorization"],
            "runtime_gateway": authority["revoked_task_race"]["execution"],
            "state_mutation": authority["revoked_task_race"]["state_mutation"],
            "expected": "deny-or-block-no-effect",
            "matches_expected": authority_withdrawn["decision"] == "deny"
            and authority["application_local_comparison"]["result"]["authorization"] == "deny"
            and authority["revoked_task_race"]["execution"] == "blocked"
            and authority["revoked_task_race"]["state_mutation"] is False,
        },
        {
            "id": "AT-NEG-002",
            "proposition": "VAC without valid VDC cannot establish represented action",
            "semantic_decision": no_delegation["decision"],
            "expected": "deny",
            "matches_expected": no_delegation["decision"] == "deny",
        },
        {
            "id": "AT-NEG-003",
            "proposition": "valid standing credentials cannot survive invocation mismatch",
            "semantic_decision": invocation_mismatch["decision"],
            "expected": "deny",
            "matches_expected": invocation_mismatch["decision"] == "deny",
        },
        {
            "id": "AT-NEG-004",
            "proposition": "narrower delegation and revoked delegation fail closed at the semantic boundary",
            "semantic_decisions": [narrower["decision"], delegation_revoked["decision"]],
            "expected": "deny",
            "matches_expected": narrower["decision"] == delegation_revoked["decision"] == "deny",
        },
        {
            "id": "AT-NEG-005",
            "proposition": "missing principal authority is not replaced by task validity or retained evidence",
            "semantic_decision": no_authority["decision"],
            "no_application_fallback_permit": authority["checks"]["no_application_fallback_permit"],
            "no_weaker_surface_substitution": authority["checks"]["no_weaker_surface_substitution"],
            "expected": "deny-without-substitution",
            "matches_expected": no_authority["decision"] == "deny"
            and authority["checks"]["no_application_fallback_permit"]
            and authority["checks"]["no_weaker_surface_substitution"],
        },
        {
            "id": "AT-NEG-006",
            "proposition": "unavailable or stale current policy/authority view is distinguishable from current authority",
            "exact_surface_available": not authority["checks"]["no_exact_upstream_delegated_action_surface_observed"],
            "classification": authority["integration_classification"],
            "execution": authority["canonical_attempt"]["execution"],
            "expected": "indeterminate-blocked",
            "matches_expected": authority["integration_classification"] == "INDETERMINATE/BLOCKED"
            and authority["canonical_attempt"]["execution"] == "blocked",
        },
    ]

    return {
        "case": "IC-DTG-VDC-VAC-COMPOSITION-EXP/action-time",
        "issue": 174,
        "status": "terminal-bounded-composition-evidence",
        "source_pins": {
            "credential_spec_wd02": "67149716032318f7f29770e5d3e6f0d35e52b8c3",
            "semantic_fixture": semantic["source_pins"],
            "actuation_boundary": authority["baselines"],
        },
        "propositions": ["RAHP-428-F-001", "RAHP-428-F-002", "RAHP-474-H1", "RAHP-474-H2"],
        "vectors": vectors,
        "all_expected_outcomes_matched": all(v["matches_expected"] for v in vectors),
        "runtime_conclusion": "INDETERMINATE/BLOCKED where the exact external current-authority evaluator is unavailable; fail-closed and no-effect behavior is evidenced",
        "claim_boundary": "Composition evidence at the Lab application/actuation boundary plus adopted WD02 semantic evidence. This does not claim current OpenVTC implements the complete adopted VDC/VAC runtime contract, production deployment assurance, or successful external side effects merely from credential/task validity.",
        "remaining_gap": "No exact current OpenVTC delegated-action evaluator implementing the complete adopted VDC/VAC action-time contract was evidenced; absence is terminally represented as INDETERMINATE/BLOCKED rather than PASS.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = build_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
    if args.check:
        if not RESULT.exists() or json.loads(RESULT.read_text(encoding="utf-8")) != result:
            print("action-time composition result fixture is stale", file=sys.stderr)
            return 1
    if not args.write and not args.check:
        print(text, end="")
    return 0 if result["all_expected_outcomes_matched"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, json.JSONDecodeError, StopIteration) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
