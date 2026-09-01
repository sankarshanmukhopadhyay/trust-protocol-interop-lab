#!/usr/bin/env python3
"""Deterministic evaluator for IC-GOVOPS-EXEC-TRUST-001 scenario contracts.

The evaluator tests governance-boundary claims, not a particular policy engine.
It deliberately treats missing observability as indeterminate rather than success.
Candidate vectors are required to remain mechanically equivalent to the scenario contracts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CASE_ROOT = ROOT / "cases" / "govops-executable-trust"
SCENARIOS = CASE_ROOT / "scenarios" / "scenarios.yaml"
INVARIANTS = CASE_ROOT / "invariants.yaml"
VECTORS = CASE_ROOT / "vectors"


def load_json_yaml(path: Path) -> dict[str, Any]:
    """Load repository JSON-compatible YAML/JSON deterministically."""
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(inputs: dict[str, Any]) -> dict[str, Any]:
    """Evaluate only observable governance state implied by scenario inputs."""
    result: dict[str, Any] = {}

    decision = inputs.get("policy_decision") or inputs.get("historical_policy_decision")
    enforced = inputs.get("decision_enforced")

    if enforced is True:
        result["enforcement_state"] = "enforced"
    elif enforced is False and decision == "allow":
        result["enforcement_state"] = "not_established"

    if decision in {"deny", "challenge"}:
        result["execution_state"] = "blocked"
        result["effect_state"] = "absent"
    elif decision == "allow" and enforced is False:
        result["execution_state"] = "not_established"
        result["effect_state"] = "absent"
        result["assurance_state"] = "indeterminate"
    elif decision == "allow" and enforced is True:
        result["execution_state"] = "admitted"

    decision_match = inputs.get("effect_decision_match")
    capability_match = inputs.get("effect_capability_match")
    request_match = inputs.get("decision_request_match")
    decision_capability_match = inputs.get("decision_capability_match")

    correlation_invalid = any(value is False for value in (
        decision_match,
        capability_match,
        request_match,
        decision_capability_match,
    ))

    if correlation_invalid:
        result["correlation_state"] = "invalid"
        result["effect_state"] = "mismatched"
        result["evidence_state"] = "inconsistent"
        result["assurance_state"] = "fail"
    elif decision == "allow" and enforced is True and (
        decision_match is True or capability_match is True
    ):
        result["correlation_state"] = "valid"
        result["effect_state"] = "observed"
        result["evidence_state"] = "complete"

    if inputs.get("effect_observed") is False:
        result["effect_state"] = "absent"

    if "policy_store_id" in inputs and inputs.get("policy_store_version") is None:
        result["policy_provenance_state"] = "indeterminate"
        result["evidence_state"] = "incomplete"
        result["assurance_state"] = "indeterminate"

    if inputs.get("authority_revoked_after_effect") is True:
        result["historical_evidence_preserved"] = True
        result["current_authority_valid"] = False

    if inputs.get("historical_policy_decision") == "deny":
        result["historical_authorization_changed"] = False
        result["authority_conferred_by_evidence"] = False
        result["execution_state"] = "blocked"

    if "evidence_state" not in result and inputs.get("policy_decision") in {"deny", "challenge"}:
        result["evidence_state"] = "complete"

    if "assurance_state" not in result and decision == "allow" and enforced is True:
        result["assurance_state"] = "not_evaluated"

    return result


def validate_contracts() -> list[str]:
    scenario_doc = load_json_yaml(SCENARIOS)
    invariant_doc = load_json_yaml(INVARIANTS)

    invariant_ids = {item["id"] for item in invariant_doc["invariants"]}
    failures: list[str] = []

    if len(invariant_ids) != 12:
        failures.append(f"expected 12 unique invariants, found {len(invariant_ids)}")

    scenarios = scenario_doc.get("scenarios", [])
    if len(scenarios) != 10:
        failures.append(f"expected 10 scenarios, found {len(scenarios)}")

    scenario_by_id: dict[str, dict[str, Any]] = {}
    for scenario in scenarios:
        scenario_id = scenario.get("id", "<missing>")
        if scenario_id in scenario_by_id:
            failures.append(f"{scenario_id}: duplicate scenario id")
        scenario_by_id[scenario_id] = scenario

        unknown = set(scenario.get("invariants", [])) - invariant_ids
        if unknown:
            failures.append(f"{scenario_id}: unknown invariants {sorted(unknown)}")

        actual = evaluate(scenario.get("inputs", {}))
        expected = scenario.get("expected", {})
        for key, expected_value in expected.items():
            if key not in actual:
                failures.append(f"{scenario_id}: evaluator did not establish expected field {key}")
            elif actual[key] != expected_value:
                failures.append(
                    f"{scenario_id}: {key} expected {expected_value!r}, got {actual[key]!r}"
                )

    required_negative_ids = {"GOVOPS-SC-008", "GOVOPS-SC-009", "GOVOPS-SC-010"}
    if not required_negative_ids.issubset(scenario_by_id):
        failures.append("missing one or more upstream-clarification negative scenarios")

    vector_paths = sorted((VECTORS / "valid").glob("*.json")) + sorted((VECTORS / "invalid").glob("*.json"))
    if len(vector_paths) != 10:
        failures.append(f"expected 10 candidate vectors, found {len(vector_paths)}")

    seen_vector_ids: set[str] = set()
    covered_scenarios: set[str] = set()
    for path in vector_paths:
        vector = load_json_yaml(path)
        vector_id = vector.get("id")
        scenario_id = vector.get("scenario_id")
        if not vector_id or vector_id in seen_vector_ids:
            failures.append(f"{path}: missing or duplicate vector id")
        else:
            seen_vector_ids.add(vector_id)
        if scenario_id not in scenario_by_id:
            failures.append(f"{path}: unknown scenario_id {scenario_id!r}")
            continue
        if scenario_id in covered_scenarios:
            failures.append(f"{path}: duplicate scenario coverage {scenario_id}")
        covered_scenarios.add(scenario_id)

        scenario = scenario_by_id[scenario_id]
        if vector.get("inputs") != scenario.get("inputs"):
            failures.append(f"{path}: inputs drift from {scenario_id}")
        if vector.get("expected") != scenario.get("expected"):
            failures.append(f"{path}: expected behavior drifts from {scenario_id}")

        actual = evaluate(vector.get("inputs", {}))
        for key, expected_value in vector.get("expected", {}).items():
            if actual.get(key) != expected_value:
                failures.append(
                    f"{path}: {key} expected {expected_value!r}, got {actual.get(key)!r}"
                )

    if covered_scenarios != set(scenario_by_id):
        missing = sorted(set(scenario_by_id) - covered_scenarios)
        failures.append(f"candidate vector estate does not cover scenarios {missing}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if any contract proposition is violated")
    args = parser.parse_args()

    failures = validate_contracts()
    if failures:
        print("FAIL IC-GOVOPS-EXEC-TRUST-001")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS IC-GOVOPS-EXEC-TRUST-001: 10 scenarios / 12 invariants / 10 vectors")
    print("PASS policy-engine neutrality, enforcement observability, correlation, policy provenance")
    print("PASS candidate vectors remain equivalent to scenario contracts")
    if not args.check:
        print(json.dumps({"case_id": "IC-GOVOPS-EXEC-TRUST-001", "result": "pass"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
