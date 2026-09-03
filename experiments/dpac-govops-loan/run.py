#!/usr/bin/env python3
"""DPAC × GovOps delegated-loan pressure test.

This experiment composes the existing GovOps loan semantics with the DPAC actuation
invariant. The authority/policy path and Workspace capability path remain separate
state surfaces and are re-evaluated at actuation time. This is a deterministic
reference model, not a production isolation mechanism.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = Path(__file__).with_name("scenarios.yaml")

REQUIRED = {
    "action",
    "loan_id",
    "amount_inr",
    "authority_limit_inr",
    "authority_current_at_actuation",
    "authority_bound_loan_id",
    "authority_bound_amount_inr",
    "policy_decision",
    "decision_enforced",
    "capability_action",
    "capability_max_amount_inr",
    "capability_revision_at_authorization",
    "capability_revision_at_actuation",
    "capability_controller_separate",
    "actuation_authorization_consumed",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def outcome(reason: str, *, actuated: bool = False) -> dict[str, Any]:
    return {
        "actuated": actuated,
        "reason": reason,
        "effect_count": 1 if actuated else 0,
        "evidence_state": "complete",
    }


def evaluate(inputs: dict[str, Any]) -> dict[str, Any]:
    missing = sorted(REQUIRED - inputs.keys())
    if missing:
        return {
            "actuated": False,
            "reason": "indeterminate_input",
            "effect_count": 0,
            "evidence_state": "indeterminate",
            "missing": missing,
        }

    # Non-collapsibility: the Workflow/authorization path must not administer its
    # own technical capability boundary.
    if inputs["capability_controller_separate"] is not True:
        return outcome("capability_control_capture")

    # GovOps authorization remains distinct from authority and from actuation.
    if inputs["policy_decision"] != "allow":
        return outcome("policy_not_allowed")
    if inputs["decision_enforced"] is not True:
        return outcome("authorization_not_enforced")

    # Authority is rechecked at the actuation boundary rather than trusting a
    # previously observed authorization state.
    if inputs["authority_current_at_actuation"] is not True:
        return outcome("authority_not_current")
    if inputs["amount_inr"] > inputs["authority_limit_inr"]:
        return outcome("authority_scope_exceeded")
    if (
        inputs["loan_id"] != inputs["authority_bound_loan_id"]
        or inputs["amount_inr"] != inputs["authority_bound_amount_inr"]
    ):
        return outcome("authority_binding_mismatch")

    # Capability is independently rechecked and must be the same administered
    # state that the prior authorization assumed. A changed revision requires a
    # fresh concurrence decision rather than silently using stale capability state.
    if inputs["capability_revision_at_authorization"] != inputs["capability_revision_at_actuation"]:
        return outcome("capability_state_changed")
    if inputs["action"] != inputs["capability_action"]:
        return outcome("capability_scope_exceeded")
    if inputs["amount_inr"] > inputs["capability_max_amount_inr"]:
        return outcome("capability_scope_exceeded")

    # The actuation authorization is single-use in this bounded model so retries
    # cannot turn one concurrence decision into multiple consequential effects.
    if inputs["actuation_authorization_consumed"] is True:
        return outcome("duplicate_actuation")

    return outcome("concurrence", actuated=True)


def validate() -> tuple[list[dict[str, Any]], list[str]]:
    document = load(SCENARIOS)
    scenarios = document.get("scenarios", [])
    failures: list[str] = []
    results: list[dict[str, Any]] = []

    if len(scenarios) != 8:
        failures.append(f"expected 8 pressure scenarios, found {len(scenarios)}")

    seen: set[str] = set()
    for scenario in scenarios:
        sid = scenario.get("id", "<missing>")
        if sid in seen:
            failures.append(f"{sid}: duplicate scenario id")
        seen.add(sid)
        actual = evaluate(scenario.get("inputs", {}))
        expected = scenario.get("expected", {})
        mismatches = {
            key: {"expected": value, "actual": actual.get(key)}
            for key, value in expected.items()
            if actual.get(key) != value
        }
        if mismatches:
            failures.append(f"{sid}: mismatches {mismatches}")
        results.append({"scenario_id": sid, "expected": expected, "actual": actual, "pass": not mismatches})

    required = {f"DPAC-GOVOPS-{n:03d}" for n in range(1, 9)}
    if seen != required:
        failures.append(f"scenario set mismatch: expected {sorted(required)}, got {sorted(seen)}")

    return results, failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit non-zero on any contract mismatch")
    parser.add_argument("--output", type=Path, help="write deterministic result JSON")
    args = parser.parse_args()

    results, failures = validate()
    payload = {
        "case_id": "IC-DPAC-ACTUATION-001",
        "composition": "IC-GOVOPS-EXEC-TRUST-001 delegated-loan pressure test",
        "claim": "bounded deterministic composition evidence; no production isolation claim",
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for item in results if item["pass"]),
            "failed": len(failures),
        },
        "failures": failures,
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if args.check and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
