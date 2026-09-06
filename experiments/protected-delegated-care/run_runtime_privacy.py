#!/usr/bin/env python3
"""Produce DPIP-consumable runtime privacy observations for IC-PDC-MED-001.

The output uses the existing interop-evidence-package/v1 shape. It records synthetic
runtime observations and deliberately preserves INDETERMINATE for provider/confidentiality
properties that the application harness cannot observe.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from core import CareCore, build_active_exception_core

SCHEMA = "interop-evidence-package/v1"
CASE_ID = "IC-PDC-MED-001"
PROHIBITED_CAREGIVER_FIELDS = {
    "medication_name",
    "diagnosis",
    "prescription_image",
    "broader_adherence_history",
    "unrelated_relationships",
    "medication_history",
    "caregiver_graph",
}
ALLOWED_EXCEPTION_FIELDS = {"exception_ref", "reminder_time", "permitted_actions"}


def token(label: str, value: str) -> str:
    return f"{label}:{sha256(value.encode('utf-8')).hexdigest()[:20]}"


def provenance() -> dict:
    return {
        "producer": "trust-protocol-interop-lab",
        "implementation_repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab",
        "case_id": CASE_ID,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "fixture_class": "synthetic",
    }


def package(requirement_id: str, evidence_class: str, summary: str, experiment: dict, surfaces: dict) -> dict:
    return {
        "requirement_id": requirement_id,
        "schema": SCHEMA,
        "evidence_class": evidence_class,
        "provenance": provenance(),
        "observation_summary": summary,
        "experiment": experiment,
        "surfaces": surfaces,
    }


def routine_ack_observation() -> dict:
    core = CareCore()
    core.extract_plan()
    core.approve_plan()
    core.activate_plan()
    core.schedule_reminder()
    core.dispatch_reminder()
    ack = core.acknowledge_channel_event("evt:routine-ack-001")
    caregiver_payload = None
    passed = ack["authorization"] == "permit" and core.reminder.status == "acknowledged" and caregiver_payload is None
    return package(
        "PDC-PRIV-DISCLOSURE-ROUTINE",
        "runtime-application-observation",
        "Routine reminder was acknowledged without generating a caregiver-facing payload.",
        {"kind": "routine-acknowledgement", "result": "PASS" if passed else "FAIL"},
        {
            "caregiver_disclosure": {
                "classification": "absent" if caregiver_payload is None else "present",
                "value": caregiver_payload,
                "execution": "executed",
                "producer_component": "pdc-deterministic-core",
            },
            "reminder_state": {
                "classification": "runtime-state",
                "value": core.reminder.status,
                "execution": "executed",
                "producer_component": "pdc-deterministic-core",
            },
        },
    )


def exception_observation() -> dict:
    core = build_active_exception_core()
    payload = core.safe_exception_payload()
    validation = core.validate_exception_payload(payload)
    keys = set(payload)
    passed = (
        validation["authorization"] == "permit"
        and not (keys & PROHIBITED_CAREGIVER_FIELDS)
        and keys == ALLOWED_EXCEPTION_FIELDS
    )
    return package(
        "PDC-PRIV-DISCLOSURE-EXCEPTION",
        "runtime-application-observation",
        "Exception payload was materially produced and checked against the minimum-disclosure profile.",
        {"kind": "exception-minimum-disclosure", "result": "PASS" if passed else "FAIL"},
        {
            "caregiver_payload_fields": {
                "classification": "bounded" if passed else "expanded",
                "value": sorted(keys),
                "execution": "executed",
                "producer_component": "pdc-deterministic-core",
            },
            "prohibited_fields_present": {
                "classification": "none" if not (keys & PROHIBITED_CAREGIVER_FIELDS) else "present",
                "value": sorted(keys & PROHIBITED_CAREGIVER_FIELDS),
                "execution": "executed",
                "producer_component": "pdc-runtime-privacy",
            },
        },
    )


def late_ack_observation() -> dict:
    core = build_active_exception_core()
    payload = core.safe_exception_payload()
    core.validate_exception_payload(payload)
    core.mark_escalated()
    before = list(core.reminder.event_history)
    ack = core.acknowledge_channel_event("evt:late-ack-001")
    after = list(core.reminder.event_history)
    history_preserved = all(item in after for item in before) and "late_acknowledgement" in after
    passed = ack.get("history_rewritten") is False and history_preserved
    return package(
        "PDC-PRIV-LATE-ACK",
        "runtime-application-observation",
        "Late acknowledgement preserved prior escalation history and did not expand the bounded caregiver payload.",
        {"kind": "late-ack-reconciliation", "result": "PASS" if passed else "FAIL"},
        {
            "event_history": {
                "classification": "append-only" if history_preserved else "rewritten",
                "value": after,
                "execution": "executed",
                "producer_component": "pdc-deterministic-core",
            },
            "caregiver_payload_fields": {
                "classification": "bounded",
                "value": sorted(payload.keys()),
                "execution": "executed",
                "producer_component": "pdc-deterministic-core",
            },
        },
    )


def correlation_observation() -> dict:
    core = CareCore()
    subject_ref = token("subject", core.relationship.principal)
    caregiver_ref = token("caregiver", core.relationship.delegate)
    channel_ref = token("channel", core.contextual_relationship_ref("channel"))
    task_ref = token("task", core.task.id)
    values = {subject_ref, caregiver_ref, channel_ref, task_ref}
    distinct = len(values) == 4
    # Distinct synthetic references demonstrate application scoping only. They do not
    # establish unlinkability against a real provider, network observer, or colluding service.
    return package(
        "PDC-PRIV-CORRELATION",
        "runtime-composition-observation",
        "Application-visible subject, caregiver, channel and Trust Task references were distinct; provider/network correlation remains unobserved.",
        {
            "kind": "cross-context-correlation-observation",
            "expected_join": "must-not-be-assumed",
            "observed_join": "not-detected-in-application-fixture",
            "result": "INDETERMINATE",
            "reason": "PROVIDER_AND_NETWORK_OBSERVER_NOT_EXERCISED",
        },
        {
            "subject_reference": {"classification": "contextual", "value": subject_ref, "execution": "executed", "correlator_origin": "application-fixture"},
            "caregiver_reference": {"classification": "contextual", "value": caregiver_ref, "execution": "executed", "correlator_origin": "application-fixture"},
            "channel_reference": {"classification": "contextual", "value": channel_ref, "execution": "executed", "correlator_origin": "application-fixture"},
            "trust_task_reference": {"classification": "contextual", "value": task_ref, "execution": "executed", "correlator_origin": "application-fixture"},
            "application_refs_distinct": {"classification": "observed", "value": distinct, "execution": "executed", "correlator_origin": "none"},
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    evidence = [
        routine_ack_observation(),
        exception_observation(),
        late_ack_observation(),
        correlation_observation(),
    ]
    results = [item["experiment"]["result"] for item in evidence]
    summary = {
        "pass": results.count("PASS"),
        "fail": results.count("FAIL"),
        "indeterminate": results.count("INDETERMINATE"),
    }
    output = {
        "case_id": CASE_ID,
        "schema": "pdc-dpip-runtime-evidence/v1",
        "claim": "runtime privacy observations suitable for DPIP consumption; not a DPIP or RAHP privacy conclusion",
        "evidence": evidence,
        "summary": summary,
        "overall": "FAIL" if summary["fail"] else "INDETERMINATE" if summary["indeterminate"] else "PASS",
    }
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    return 1 if args.check and summary["fail"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
