#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments"
from standards import StandardsBoundaryReview, digest

AFFECTED_RUNNERS = [
    "ara-policy-spine/run.py",
    "ara-protected-signing/run.py",
    "ara-independent-counterparty/run.py",
    "ara-distributed-vrr/run.py",
    "ara-adversarial-assurance/run.py",
]


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def rerun_affected() -> list[dict[str, Any]]:
    records = []
    for runner in AFFECTED_RUNNERS:
        proc = subprocess.run(
            [sys.executable, str(EXP / runner), "--check"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        payload = json.loads(proc.stdout)
        records.append({"runner": runner, "summary": payload["summary"], "output_ref": digest(payload)})
    return records


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    review = StandardsBoundaryReview()
    report = review.report()

    record(results, "P11-P01-pinned-standards-boundary-report", "present", "present" if report["review_ref"] else "missing", report)

    transport = review.classify_transport(authenticated_channel=True, relationship_authority=False)
    record(results, "P11-N01-tsp-authenticity-not-authority", "transport_not_relationship_authority", transport["code"], transport)

    vta = review.classify_vta_use(protected_key_use=True, workflow_authorized=False)
    record(results, "P11-N02-vta-key-use-not-policy-authorization", "protected_key_use_not_policy_authorization", vta["code"], vta)

    rcard = review.classify_rcard(self_asserted_standing=True, verified_standing=False)
    record(results, "P11-N03-rcard-self-assertion-not-standing", "self_assertion_not_verified_standing", rcard["code"], rcard)

    vrc = review.classify_vrc(relationship_recognized=True, delegation=False, agreement=False, capability=False)
    record(results, "P11-N04-vrc-not-delegation-agreement-capability", "relationship_recognition_not_authority", vrc["code"], vrc)

    registry = review.classify_registry(lookup_success=True, permission_to_act=False)
    record(results, "P11-N05-registry-lookup-not-permission", "registry_lookup_not_permission", registry["code"], registry)

    history = review.classify_current_control(current_key_control=True, historical_authority_proved=False)
    record(results, "P11-N06-current-key-not-historical-authority", "current_control_not_historical_authority", history["code"], history)

    community = review.classify_community_assurance(community_assured=True, universal_authorization=False)
    record(results, "P11-N07-community-assurance-bounded", "community_assurance_not_universal_authorization", community["code"], community)

    no_false_substitution = len(report["executed_substitutions"]) == 0
    record(
        results,
        "P11-P02-no-unproven-implementation-substitution",
        "none",
        "none" if no_false_substitution else ",".join(report["executed_substitutions"]),
        report,
    )

    expected_residuals = {"RelationshipTransport", "ProtectedSigner"}
    record(
        results,
        "P11-P03-residual-adapters-explicit",
        json.dumps(sorted(expected_residuals)),
        json.dumps(sorted(set(report["residual_adapters"]) & expected_residuals)),
        report,
    )

    affected = rerun_affected()
    all_green = all(x["summary"]["failed"] == 0 for x in affected)
    record(results, "P11-P04-ara-invariants-survive-standards-boundary-review", "green", "green" if all_green else "failed", affected)

    summary = {
        "case_id": "IC-ARA-REL-001",
        "phase": 11,
        "experiment": "ara-standards-boundary",
        "vectors": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "standards_native_maturity": {
            "TrustTaskCodec": "normative-semantic-binding",
            "RelationshipTransport": "residual-adapter",
            "ProtectedSigner": "residual-adapter",
            "ParticipantCardProvider": "normative-semantic-binding",
            "RelationshipEdgeProvider": "normative-semantic-binding",
        },
        "graduation_recommendation": "no repository extraction; no observed downstream reuse or independently stable lifecycle yet",
        "claim_boundary": "Standards-native boundary is evaluated and pinned per component; no implementation substitution is claimed where an independently executed replacement has not occurred.",
    }
    return {"summary": summary, "review": report, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_vectors()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if args.check and report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
