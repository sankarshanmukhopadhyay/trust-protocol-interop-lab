#!/usr/bin/env python3
"""Executable privacy comparison for IC-PDC-REFILL-001.

This is a synthetic disclosure/linkability experiment. It does not implement prescribing,
pharmacy dispensing, or a cryptographic ZKP primitive. A modeled ZKP candidate remains
INDETERMINATE until real proof generation/verification is exercised.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PROHIBITED = {
    "subject_id", "prescription_image", "diagnosis", "medication_history",
    "caregiver_identity", "caregiver_graph", "prescriber_identity",
    "unrelated_care_data", "durable_cross_context_identifier",
}
REQUIRED = {"eligible", "refill_scope", "medication_class_ref"}

CREDENTIAL = {
    "subject_id": "person:p001",
    "medication_order_ref": "order:rx001",
    "eligible": True,
    "refill_scope": "one_refill",
    "medication_class_ref": "class:synthetic-001",
    "prescriber_identity": "person:synthetic-prescriber",
    "diagnosis": "synthetic-diagnosis",
    "medication_history": ["synthetic-event"],
}


def contextual_ref(context: str) -> str:
    material = f"{context}|{CREDENTIAL['subject_id']}".encode()
    return "ctx:" + hashlib.sha256(material).hexdigest()[:16]


def ordinary(context: str) -> dict[str, Any]:
    return {
        "eligible": CREDENTIAL["eligible"],
        "refill_scope": CREDENTIAL["refill_scope"],
        "medication_class_ref": CREDENTIAL["medication_class_ref"],
        "contextual_subject_ref": contextual_ref(context),
    }


def selective() -> dict[str, Any]:
    return {key: CREDENTIAL[key] for key in sorted(REQUIRED)}


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    prohibited = sorted(PROHIBITED & payload.keys())
    missing = sorted(REQUIRED - payload.keys())
    return {
        "minimum_disclosure": "PASS" if not prohibited and not missing else "FAIL",
        "prohibited_fields": prohibited,
        "missing_required": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    ordinary_a, ordinary_b = ordinary("pharmacy:A"), ordinary("pharmacy:B")
    selective_a, selective_b = selective(), selective()
    negative = {**selective(), "diagnosis": CREDENTIAL["diagnosis"]}

    checks = {
        "ordinary_minimized_excludes_prohibited_data": evaluate(ordinary_a)["minimum_disclosure"] == "PASS",
        "ordinary_context_refs_are_distinct": ordinary_a["contextual_subject_ref"] != ordinary_b["contextual_subject_ref"],
        "selective_disclosure_excludes_subject_and_prohibited_data": evaluate(selective_a)["minimum_disclosure"] == "PASS",
        "selective_disclosure_reveals_only_required_claims": set(selective_a) == REQUIRED,
        "negative_overdisclosure_is_detected": evaluate(negative)["minimum_disclosure"] == "FAIL",
    }

    result = {
        "case_id": "IC-PDC-REFILL-001",
        "parent_case": "IC-PDC-MED-001",
        "claim": "synthetic refill disclosure comparison; not production pharmacy interoperability or cryptographic ZKP evidence",
        "proposition": "holder is eligible for one refill under a current synthetic medication-order reference",
        "constructions": {
            "ordinary_minimized": {
                "context_a": ordinary_a,
                "context_b": ordinary_b,
                "minimum_disclosure": "PASS",
                "cross_context_linkability": "NO_DIRECT_CORRELATOR_OBSERVED_IN_CAPTURED_APPLICATION_FIELDS",
                "limitation": "provider/network/status-resolution surfaces not observed",
            },
            "selective_disclosure": {
                "context_a": selective_a,
                "context_b": selective_b,
                "minimum_disclosure": "PASS",
                "attribute_minimization_gain": "contextual_subject_ref removed",
                "cross_context_linkability": "INDETERMINATE",
                "limitation": "equal proposition values may themselves be joinable; no universal unlinkability claim",
            },
            "unlinkable_zkp_candidate": {
                "status": "INDETERMINATE",
                "reason": "cryptographic proof generation and verification not exercised in this tranche",
            },
        },
        "negative_overdisclosure": {"payload": negative, "evaluation": evaluate(negative)},
        "checks": checks,
        "decision": {
            "preferred_current_construction": "selective_disclosure",
            "reason": "removes an application-visible contextual subject reference without requiring an unexercised ZKP claim",
            "zkp_required": False,
            "zkp_escalation_condition": "measured residual linkability remains unacceptable after selective disclosure",
        },
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if all(checks.values()) else 1

if __name__ == "__main__":
    raise SystemExit(main())
