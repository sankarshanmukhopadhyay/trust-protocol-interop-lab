#!/usr/bin/env python3
"""Deterministic evaluator for IC-DPAC-ACTUATION-001.

This is a deliberately small semantic reference model. It tests the non-collapsibility
and concurrence invariants of Dual-Path Actuation Control; it is not a production
actuator, policy engine, authority service, or Workspace implementation.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CASE_ROOT = ROOT / "cases" / "dpac-actuation"
SCENARIOS = CASE_ROOT / "scenarios" / "scenarios.yaml"
INVARIANTS = CASE_ROOT / "invariants.yaml"


def load_json_yaml(path: Path) -> dict[str, Any]:
    """Load the repository's JSON-compatible YAML deterministically."""
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(inputs: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one bounded actuation request and return observable outcome evidence."""
    required = {
        "authority_present",
        "authority_current",
        "authority_replayed",
        "capability_allows",
        "capability_control_capture",
    }
    missing = required - inputs.keys()
    if missing:
        return {
            "actuated": False,
            "reason": "indeterminate_input",
            "concurrence_recorded": False,
            "missing": sorted(missing),
        }

    if inputs["capability_control_capture"] is True:
        return {
            "actuated": False,
            "reason": "capability_control_capture",
            "concurrence_recorded": False,
        }

    authority_valid = (
        inputs["authority_present"] is True
        and inputs["authority_current"] is True
        and inputs["authority_replayed"] is False
    )
    if not authority_valid:
        return {
            "actuated": False,
            "reason": "authority_invalid",
            "concurrence_recorded": False,
        }

    if inputs["capability_allows"] is not True:
        return {
            "actuated": False,
            "reason": "capability_denied",
            "concurrence_recorded": False,
        }

    return {
        "actuated": True,
        "reason": "concurrence",
        "concurrence_recorded": True,
    }


def validate() -> tuple[list[dict[str, Any]], list[str]]:
    scenario_doc = load_json_yaml(SCENARIOS)
    invariant_doc = load_json_yaml(INVARIANTS)

    failures: list[str] = []
    results: list[dict[str, Any]] = []
    invariant_ids = {item["id"] for item in invariant_doc.get("invariants", [])}

    scenarios = scenario_doc.get("scenarios", [])
    if len(scenarios) != 5:
        failures.append(f"expected 5 scenarios, found {len(scenarios)}")

    seen: set[str] = set()
    for scenario in scenarios:
        scenario_id = scenario.get("id", "<missing>")
        if scenario_id in seen:
            failures.append(f"{scenario_id}: duplicate scenario id")
        seen.add(scenario_id)

        unknown = set(scenario.get("invariants", [])) - invariant_ids
        if unknown:
            failures.append(f"{scenario_id}: unknown invariants {sorted(unknown)}")

        actual = evaluate(scenario.get("inputs", {}))
        expected = scenario.get("expected", {})
        mismatches = {
            key: {"expected": value, "actual": actual.get(key)}
            for key, value in expected.items()
            if actual.get(key) != value
        }
        if mismatches:
            failures.append(f"{scenario_id}: mismatches {mismatches}")

        results.append(
            {
                "scenario_id": scenario_id,
                "expected": expected,
                "actual": actual,
                "pass": not mismatches,
            }
        )

    required_ids = {f"DPAC-{n:03d}" for n in range(1, 6)}
    if seen != required_ids:
        failures.append(f"scenario set mismatch: expected {sorted(required_ids)}, got {sorted(seen)}")

    return results, failures


def main() -> int:
    results, failures = validate()
    output = {
        "case_id": "IC-DPAC-ACTUATION-001",
        "claim": "bounded semantic reference-model execution only",
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for item in results if item["pass"]),
            "failed": len(failures),
        },
        "failures": failures,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
