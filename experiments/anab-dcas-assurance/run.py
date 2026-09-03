#!/usr/bin/env python3
"""Deterministic evaluator for IC-ANAB-DCAS-001.

This is an Interop Lab experiment implementation, not the authoritative DCAS
reference implementation and not an ANAB requirements source. Canonical
normalized inputs remain in the scenario file; generated results bind to them
by evaluation ID and SHA-256 digest.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ROOT / "cases" / "anab-dcas-assurance" / "scenarios" / "scenarios.json"
RESULTS = ROOT / "results" / "anab-dcas-assurance" / "run-results.json"


def normalized_digest(value: dict) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def evaluate(vector: dict) -> dict:
    source_input = vector["input"]
    policy = source_input["policy"]
    claim = source_input["claim"]
    statuses = {item["id"]: item["status"] for item in source_input["evidence"]}

    rejected = [eid for eid, status in statuses.items() if status in {"stale", "revoked", "unverifiable"}]
    missing = [eid for eid, status in statuses.items() if status == "missing"]
    consumed = [eid for eid, status in statuses.items() if status == "available"]

    if "revoked" in statuses.values():
        decision = policy["revoked_evidence"]
        reason = "revoked evidence contradicts current reliance"
    elif "stale" in statuses.values():
        decision = policy["stale_evidence"]
        reason = "stale evidence cannot establish current reliance"
    elif claim.get("assurance_overclaim"):
        decision = policy["assurance_overclaim"]
        reason = "claimed assurance exceeds evidence demonstrated by the fixture"
    elif claim.get("requires_action_authority") and statuses.get("action-authority") != "available":
        decision = policy["authority_absent"]
        reason = "identity assurance is present but action-specific authority is not established"
    elif any(status in {"missing", "unverifiable"} for status in statuses.values()):
        decision = policy["missing_evidence"]
        reason = "required evidence is missing or unverifiable"
    else:
        decision = "PASS"
        reason = "declared evidence is current and available for this bounded fixture"

    finding_result = decision if decision in {"PASS", "FAIL", "INDETERMINATE"} else "INDETERMINATE"
    result = {
        "contract_version": source_input["contract_version"],
        "evaluation_id": source_input["evaluation_id"],
        "decision": decision,
        "evaluator": {"name": "interop-lab-anab-dcas-evaluator", "version": "0.1.0"},
        "findings": [
            {
                "requirement": requirement,
                "result": finding_result,
                "reason": reason,
                "evidence_ids": sorted(statuses),
            }
            for requirement in vector["requirements"]
        ],
        "evidence_summary": {
            "consumed": sorted(consumed),
            "missing": sorted(missing),
            "rejected": sorted(rejected),
        },
        "receipt_material": {
            "input_digest": normalized_digest(source_input),
            "result_digest_algorithm": "sha256",
        },
    }
    return {
        "vector": vector["id"],
        "fixture_id": vector["fixture_id"],
        "expected": vector["expected"],
        "observed": decision,
        "matches_expected": decision == vector["expected"],
        "result": result,
    }


def main() -> int:
    scenario_set = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    executions = [evaluate(vector) for vector in scenario_set["vectors"]]
    output = {
        "case_id": scenario_set["case_id"],
        "evaluator": "interop-lab-anab-dcas-evaluator@0.1.0",
        "scenario_source": "cases/anab-dcas-assurance/scenarios/scenarios.json",
        "executions": executions,
        "summary": {
            "total": len(executions),
            "matched": sum(1 for item in executions if item["matches_expected"]),
            "mismatched": sum(1 for item in executions if not item["matches_expected"]),
        },
    }
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output["summary"], sort_keys=True))
    return 0 if output["summary"]["mismatched"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
