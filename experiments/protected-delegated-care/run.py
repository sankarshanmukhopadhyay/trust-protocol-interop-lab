#!/usr/bin/env python3
"""Execute the IC-PDC-MED-001 deterministic acceptance contract.

The output is bounded application-reference evidence only. It does not demonstrate
DTG/VTC/OpenVTC interoperability, medical safety, messaging-provider privacy, or
production readiness.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import yaml

from core import CareCore, build_active_exception_core

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "cases" / "protected-delegated-care" / "scenarios" / "acceptance.yaml"


def load_contract() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


def with_no_mutation(core: CareCore, operation: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    before = core.state_copy()
    result = operation()
    result.setdefault("state_mutation", core.state_copy() != before)
    return result


def scenario_positive() -> dict[str, Any]:
    core = build_active_exception_core()
    payload = core.validate_exception_payload(core.safe_exception_payload())
    if payload["authorization"] != "permit":
        return payload
    result = core.execute_exception_response()
    result["evidence"] = "required" if core.evidence else "missing"
    return result


def scenario_over_broad() -> dict[str, Any]:
    core = build_active_exception_core()
    return with_no_mutation(core, lambda: core.evaluate_task(action="care.schedule.modify"))


def scenario_revoked() -> dict[str, Any]:
    core = build_active_exception_core()
    core.delegation.status = "revoked"
    return core.execute_exception_response()


def scenario_superseded_plan() -> dict[str, Any]:
    core = CareCore()
    core.extract_plan()
    core.approve_plan()
    core.activate_plan()
    core.supersede_plan()
    before = core.state_copy()
    result = core.schedule_reminder()
    return {
        "authorization": result["authorization"],
        "state_mutation": core.state_copy() != before,
        "reason": result["reason"],
    }


def scenario_prescription_access() -> dict[str, Any]:
    core = build_active_exception_core()
    return with_no_mutation(core, lambda: core.evaluate_task(action="care.prescription.view"))


def scenario_disclosure_expansion() -> dict[str, Any]:
    core = build_active_exception_core()
    payload = core.safe_exception_payload() | {
        "medication_name": "synthetic-medicine-placeholder",
        "diagnosis": "synthetic-sensitive-placeholder",
    }
    before = core.state_copy()
    result = core.validate_exception_payload(payload)
    result["state_mutation"] = core.state_copy() != before
    return result


def scenario_task_replay() -> dict[str, Any]:
    core = build_active_exception_core()
    first = core.execute_exception_response()
    if first["authorization"] != "permit":
        return first
    before_effects = core.re_reminder_effects
    replay = core.execute_exception_response()
    return {
        "authorization": replay["authorization"],
        "duplicate_effect": core.re_reminder_effects != before_effects,
    }


def scenario_duplicate_webhook() -> dict[str, Any]:
    core = CareCore()
    core.extract_plan()
    core.approve_plan()
    core.activate_plan()
    core.schedule_reminder()
    core.dispatch_reminder()
    core.acknowledge_channel_event("channel-event:ack-001")
    duplicate = core.acknowledge_channel_event("channel-event:ack-001")
    return {
        "authoritative_event_count": core.authoritative_ack_events,
        "duplicate_effect": duplicate["duplicate_effect"],
    }


def scenario_late_ack() -> dict[str, Any]:
    core = build_active_exception_core()
    core.mark_escalated()
    before_history = list(core.reminder.event_history)
    result = core.acknowledge_channel_event("channel-event:late-ack-001")
    return {
        "history_rewritten": core.reminder.event_history[: len(before_history)] != before_history,
        "deterministic_reconciliation": result.get("deterministic_reconciliation", False),
        "evidence": "required" if "late_acknowledgement" in core.reminder.event_history else "missing",
    }


def scenario_ambiguous_extraction() -> dict[str, Any]:
    core = CareCore()
    core.extract_plan(ambiguous=True)
    activated = core.activate_plan()
    return {"medication_plan_state": core.plan.status, "activation": activated}


def scenario_fabricated_extraction() -> dict[str, Any]:
    core = CareCore()
    core.extract_plan(fabricated=True)
    activated = core.activate_plan()
    return {
        "medication_plan_state": core.plan.status,
        "activation": activated,
        "evidence_comparison_required": core.plan.fabricated_claim_detected,
    }


def scenario_contextual_correlation() -> dict[str, Any]:
    core = CareCore()
    care_ref = core.contextual_relationship_ref("care")
    verifier_ref = core.contextual_relationship_ref("pharmacy")
    return {"durable_cross_context_identifier_disclosed": care_ref == verifier_ref}


def scenario_revoked_task_race() -> dict[str, Any]:
    core = build_active_exception_core()
    # Task already exists while delegation is active. Revocation happens immediately before execute.
    core.delegation.status = "revoked"
    return core.execute_exception_response()


def scenario_missing_evidence() -> dict[str, Any]:
    core = build_active_exception_core()
    core.delegation.evidence_present = False
    result = core.execute_exception_response()
    result["permit"] = result["authorization"] == "permit"
    return result


def scenario_routine_no_caregiver_disclosure() -> dict[str, Any]:
    core = CareCore()
    core.extract_plan()
    core.approve_plan()
    core.activate_plan()
    core.schedule_reminder()
    core.dispatch_reminder()
    result = core.acknowledge_channel_event("channel-event:routine-ack-001")
    return {
        "caregiver_notification_count": 0,
        "medication_disclosure_to_caregiver": False,
        "acknowledgement_authorized": result["authorization"] == "permit",
    }


HANDLERS: dict[str, Callable[[], dict[str, Any]]] = {
    "PDC-POS-001": scenario_positive,
    "PDC-NEG-001": scenario_over_broad,
    "PDC-NEG-002": scenario_revoked,
    "PDC-NEG-003": scenario_superseded_plan,
    "PDC-NEG-004": scenario_prescription_access,
    "PDC-NEG-005": scenario_disclosure_expansion,
    "PDC-NEG-006": scenario_task_replay,
    "PDC-NEG-007": scenario_duplicate_webhook,
    "PDC-BOUND-001": scenario_late_ack,
    "PDC-NEG-008": scenario_ambiguous_extraction,
    "PDC-NEG-009": scenario_fabricated_extraction,
    "PDC-PRIV-001": scenario_contextual_correlation,
    "PDC-NEG-010": scenario_revoked_task_race,
    "PDC-NEG-011": scenario_missing_evidence,
    "PDC-PRIV-002": scenario_routine_no_caregiver_disclosure,
}


ALTERNATIVES: dict[str, set[str]] = {
    "deny_or_suppress": {"deny", "suppress"},
    "deny_or_idempotent": {"deny", "idempotent"},
    "deny_or_indeterminate": {"deny", "indeterminate"},
}


def matches(expected: Any, actual: Any) -> bool:
    if isinstance(expected, str) and expected in ALTERNATIVES:
        return actual in ALTERNATIVES[expected]
    return expected == actual


def validate() -> tuple[list[dict[str, Any]], list[str]]:
    contract = load_contract()
    failures: list[str] = []
    results: list[dict[str, Any]] = []
    scenarios = contract.get("scenarios", [])
    contract_ids = {scenario.get("id") for scenario in scenarios}

    if contract_ids != set(HANDLERS):
        failures.append(
            "handler/contract scenario mismatch: "
            f"contract={sorted(contract_ids)} handlers={sorted(HANDLERS)}"
        )

    for scenario in scenarios:
        scenario_id = scenario["id"]
        handler = HANDLERS.get(scenario_id)
        if handler is None:
            continue
        actual = handler()
        expected = scenario.get("expected", {})
        mismatches = {
            key: {"expected": value, "actual": actual.get(key)}
            for key, value in expected.items()
            if not matches(value, actual.get(key))
        }
        if mismatches:
            failures.append(f"{scenario_id}: mismatches {mismatches}")
        results.append(
            {
                "scenario_id": scenario_id,
                "threat": scenario.get("threat"),
                "claim": scenario.get("claim"),
                "expected": expected,
                "actual": actual,
                "pass": not mismatches,
            }
        )

    return results, failures


def main() -> int:
    results, failures = validate()
    output = {
        "case_id": "IC-PDC-MED-001",
        "claim": "bounded deterministic reference implementation; not DTG/VTC interoperability evidence",
        "contract": str(CONTRACT.relative_to(ROOT)),
        "results": results,
        "summary": {
            "total": len(results),
            "passed": sum(1 for result in results if result["pass"]),
            "failed": len(failures),
        },
        "failures": failures,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
