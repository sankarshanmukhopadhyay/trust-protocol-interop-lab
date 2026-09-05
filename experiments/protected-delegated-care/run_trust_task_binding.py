#!/usr/bin/env python3
"""Executable evidence for the PDC Trust Task / OpenVTC binding tranche."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from trust_task_adapter import (
    build_trust_task_document,
    canonical_binding,
    classify_proof_transport_boundary,
    validate_profile_document,
)


TRUST_TASKS_SPEC = "trustoverip/dtgwg-trust-tasks-spec@7c6e1bd4e1585cbf1a6363bd3cbf9059e90a335c"
OPENVTC = "OpenVTC/openvtc@f93bc7e58f2766f3064e2b23ef877563069609ac"


def evaluate() -> dict:
    canonical = build_trust_task_document(canonical_binding())
    missing = build_trust_task_document(canonical_binding(authority_state="missing"))

    canonical_violations = validate_profile_document(canonical)
    missing_violations = validate_profile_document(missing)
    transport_boundary = classify_proof_transport_boundary(canonical, "didcomm-authcrypt")

    checks = {
        "canonical_profile_document_valid": not canonical_violations,
        "identity_not_authority": canonical["payload"]["relationshipRef"] != canonical["payload"]["delegationRef"],
        "action_resource_exactly_bound": canonical["payload"]["action"] == "care.exception.respond" and canonical["payload"]["resource"] == "reminder:rm001",
        "care_semantics_remain_in_payload": "action" not in {k for k in canonical if k != "payload"} and "resource" not in canonical,
        "missing_authority_remains_explicit": missing["payload"]["authorityEvidenceState"] == "missing" and missing["payload"]["delegationRef"] is None and not missing_violations,
        "unsigned_openvtc_transport_not_generic_conformance": transport_boundary["claim"].startswith("openvtc-transport-bound candidate only"),
    }

    result = {
        "case_id": "IC-PDC-MED-001",
        "claim": "evidence-backed PDC Trust Task document binding; not end-to-end DTG/VTC authorization",
        "baselines": {
            "trust_tasks_spec": TRUST_TASKS_SPEC,
            "openvtc": OPENVTC,
        },
        "observed_boundary": {
            "trust_tasks_framework": "current specification models a document proof member and examples verify it against issuer",
            "openvtc_transport": "observed DIDComm path can authenticate sender at transport and omit document-level proof",
            "classification": "unresolved-interoperability-boundary",
        },
        "documents": {
            "canonical": canonical,
            "missing_authority": missing,
        },
        "transport_boundary": transport_boundary,
        "checks": checks,
        "violations": {
            "canonical": canonical_violations,
            "missing_authority": missing_violations,
        },
        "summary": {
            "passed": sum(1 for value in checks.values() if value),
            "total": len(checks),
            "failed": [name for name, value in checks.items() if not value],
        },
        "next_seam": "exercise current-authority / revocation evaluation against an actual VTC/OpenVTC authorization surface",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    result = evaluate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")

    failed = result["summary"]["failed"]
    if failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
