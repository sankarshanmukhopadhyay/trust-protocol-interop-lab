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
from assurance import AssuranceBoundary, digest

PHASE_RUNNERS = [
    "ara-role-record/run.py",
    "ara-policy-spine/run.py",
    "ara-protected-signing/run.py",
    "ara-independent-counterparty/run.py",
    "ara-distributed-vrr/run.py",
    "ara-lifecycle-continuity/run.py",
    "ara-relationship-view/run.py",
]


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any, boundary: str) -> None:
    passed = expected == observed
    results.append({
        "vector_id": vector_id,
        "expected": expected,
        "observed": observed,
        "pass": passed,
        "boundary": boundary,
        "evidence": evidence,
    })
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def phase_evidence() -> list[dict[str, Any]]:
    records = []
    for runner in PHASE_RUNNERS:
        proc = subprocess.run(
            [sys.executable, str(EXP / runner), "--check"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        payload = json.loads(proc.stdout)
        records.append({
            "runner": runner,
            "summary": payload["summary"],
            "output_ref": digest(payload),
        })
    return records


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    boundary = AssuranceBoundary()

    # Explicit assurance-boundary pressure.
    missing = boundary.decide_from_evidence(
        required=["identity", "authority", "agreement", "decision", "capability", "task", "execution"],
        present={"identity": True, "authority": True, "agreement": True, "decision": True, "capability": True, "task": True},
    )
    record(results, "P10-N01-missing-evidence-is-indeterminate", "INDETERMINATE", missing["assurance"], missing, "evidence-sufficiency")

    supported = boundary.decide_from_evidence(
        required=["identity", "authority", "agreement", "decision", "capability", "task", "execution"],
        present={"identity": True, "authority": True, "agreement": True, "decision": True, "capability": True, "task": True, "execution": True},
    )
    no_authority = boundary.assurance_is_not_authority(assurance=supported, authority_active=False)
    record(results, "P10-N02-assurance-not-authority", "assurance_cannot_create_authority", no_authority["code"], no_authority, "authority")

    retro = boundary.historical_authorization(original_result="refused", later_assurance="SUPPORTED")
    record(results, "P10-N03-assurance-not-retroactive", "later_assurance_not_retroactive", retro["code"], retro, "historical-authority")

    correlated = [
        {"attestation_ref": "att:1", "issuer_lineage": "operator:A"},
        {"attestation_ref": "att:2", "issuer_lineage": "operator:A"},
        {"attestation_ref": "att:3", "issuer_lineage": "operator:A"},
        {"attestation_ref": "att:4", "issuer_lineage": "operator:B"},
    ]
    grouped = boundary.independent_support(correlated)
    record(results, "P10-N04-false-independence-by-issuer-lineage", "2", str(grouped["independent_groups"]), grouped, "false-independence")

    sockpuppets = [
        {"attestation_ref": "witness:alpha", "control_lineage": "controller:one"},
        {"attestation_ref": "witness:beta", "control_lineage": "controller:one"},
        {"attestation_ref": "witness:gamma", "control_lineage": "controller:one"},
    ]
    sock_grouped = boundary.independent_support(sockpuppets)
    record(results, "P10-N05-sockpuppet-multiplicity-not-independent", "1", str(sock_grouped["independent_groups"]), sock_grouped, "false-independence")

    collective = boundary.collective_state(
        party_dispositions={"role:A": "accepted"},
        required_parties=["role:A", "role:B"],
    )
    record(results, "P10-N06-unilateral-not-collective", "not_collective", collective["status"], collective, "shared-state")

    disputed = boundary.collective_state(
        party_dispositions={"role:A": "accepted", "role:B": "disputed"},
        required_parties=["role:A", "role:B"],
    )
    record(results, "P10-N07-disagreement-not-suppressed", "disputed", disputed["status"], disputed, "shared-state")

    recovery = boundary.recovery_checkpoint(
        requested_head="sha256:later-unreviewed-head",
        last_defensible_head="sha256:last-defensible-head",
    )
    record(results, "P10-N08-recovery-beyond-checkpoint-refused", "recovery_beyond_last_defensible_checkpoint", recovery["code"], recovery, "recovery")

    phase_records = phase_evidence()
    all_phase_green = all(p["summary"]["failed"] == 0 for p in phase_records)
    record(results, "P10-P01-all-executable-ara-phases-rerun-green", "green", "green" if all_phase_green else "failure", phase_records, "regression")

    # Gate dispositions are evidence-bounded; standards-native gate deliberately remains partial until #43.
    gates = {
        "ARA-G1-SEMANTIC-OWNERSHIP": "satisfied",
        "ARA-G2-BASELINES-PINNED": "satisfied",
        "ARA-G3-ROLE-STATE-EXECUTABLE": "satisfied",
        "ARA-G4-POLICY-TASK-CAPABILITY": "satisfied",
        "ARA-G5-PROTECTED-SIGNING": "satisfied",
        "ARA-G6-INDEPENDENT-COUNTERPARTY": "satisfied",
        "ARA-G7-DISTRIBUTED-RELATIONSHIP-STATE": "satisfied",
        "ARA-G8-CONTINUITY-REMEDIATION": "satisfied",
        "ARA-G9-RELATIONSHIP-VIEW": "satisfied",
        "ARA-G10-ADVERSARIAL-EVIDENCE": "satisfied",
        "ARA-G11-STANDARDS-NATIVE-BOUNDARY": "partially-satisfied",
        "ARA-G12-CLAIM-BOUNDARY-REVIEW": "partially-satisfied",
    }

    manifest_material = {
        "case_id": "IC-ARA-REL-001",
        "phase": 10,
        "phase_runs": phase_records,
        "adversarial_vectors": [
            {
                "vector_id": r["vector_id"],
                "pass": r["pass"],
                "boundary": r["boundary"],
                "evidence_ref": digest(r["evidence"]),
            }
            for r in results
        ],
        "gates": gates,
        "run_contract": {
            "command": "python experiments/ara-adversarial-assurance/run.py --check",
            "deterministic": True,
        },
    }
    manifest = {**manifest_material, "manifest_ref": digest(manifest_material)}

    summary = {
        "case_id": "IC-ARA-REL-001",
        "phase": 10,
        "experiment": "ara-adversarial-assurance",
        "vectors": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "maturity_recommendation": "adapter-backed executable relationship with adversarial evidence; standards-native integration not yet complete",
        "claim_boundary": "Semantic/executable assurance only. Green CI is not production security certification, standards conformance, or external certification.",
    }
    return {"summary": summary, "gates": gates, "manifest": manifest, "results": results}


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
