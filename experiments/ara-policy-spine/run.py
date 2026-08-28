#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ROLE_DIR = ROOT / "experiments" / "ara-role-record"
sys.path.insert(0, str(ROLE_DIR))
from engine import RoleRecordStore  # type: ignore  # noqa: E402

from authorization import (  # noqa: E402
    AgreementLedger,
    CapabilityService,
    ExecutionAdmitter,
    PolicyGate,
    SUPPORTED_TASK,
    TrustTaskBuilder,
    digest,
)


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def make_active_agreement() -> tuple[AgreementLedger, dict[str, Any]]:
    ledger = AgreementLedger()
    ledger.propose(
        agreement_id="agr-research-001",
        version=1,
        parties=["role:data-owner", "role:researcher"],
        terms={
            "purpose": "synthetic-research",
            "resources": ["dataset:synthetic-001"],
            "actions": ["query"],
            "recipients": ["role:researcher"],
            "prohibited": ["mutate", "export"],
            "evidence_requirements": ["decision", "execution-effect"],
        },
    )
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:data-owner")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:researcher")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="activated", actor="role:data-owner")
    return ledger, ledger.snapshot("agr-research-001", 1)


def make_role_state(temp: Path) -> tuple[RoleRecordStore, str, str]:
    rel_id = "urn:ara:relationship:research:001"
    store = RoleRecordStore(temp / "role-record.json", "urn:ara:agent-role:data-owner:001")
    receipt = store.apply(
        transition_id="phase4-tr-001",
        relationship_id=rel_id,
        actor_id="controller:data-owner",
        workflow_id="wf.relationship-bootstrap/1.0",
        transition_class="relationship.create",
        previous_head=None,
        visibility="private",
        payload={"set": {"purpose": "synthetic-research", "status": "active"}},
    )
    if receipt["result"] != "accepted":
        raise AssertionError(receipt)
    return store, rel_id, receipt["resulting_head"]


def base_authority(rel_id: str) -> dict[str, Any]:
    authority = {
        "authority_id": "auth-data-owner-001",
        "relationship_id": rel_id,
        "active": True,
        "purposes": ["synthetic-research"],
        "resources": ["dataset:synthetic-001"],
        "actions": ["query"],
        "delegation_depth": 0,
    }
    return {**authority, "authority_ref": digest(authority)}


def policy_inputs(rel_id: str, head: str, agreement: dict[str, Any], authority: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {"subject": "role:data-owner", "authenticated": True},
        "authority": authority,
        "agreement": agreement,
        "agreement_ref": agreement["agreement_ref"],
        "relationship": {"relationship_id": rel_id, "status": "active", "current_head": head},
        "role_record_head": head,
        "recipient": "role:researcher",
        "purpose": "synthetic-research",
        "resource": "dataset:synthetic-001",
        "action": "query",
        "task_id": SUPPORTED_TASK,
        "instance_policy": "allow",
    }


def build_task(
    builder: TrustTaskBuilder,
    rel_id: str,
    head: str,
    agreement_ref: str,
    authority_ref: str,
    decision_ref: str,
    capability_ref: str,
    nonce: str,
    *,
    task_id: str = SUPPORTED_TASK,
    expires_at: int = 20,
) -> dict[str, Any]:
    return builder.build(
        relationship_id=rel_id,
        agreement_ref=agreement_ref,
        role_record_head=head,
        authority_ref=authority_ref,
        decision_ref=decision_ref,
        capability_ref=capability_ref,
        recipient="role:researcher",
        purpose="synthetic-research",
        resource="dataset:synthetic-001",
        action="query",
        payload={"query": "count records"},
        nonce=nonce,
        issued_at=10,
        expires_at=expires_at,
        evidence_requirements=["decision", "execution-effect"],
        task_id=task_id,
    )


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="ara-policy-spine-") as d:
        temp = Path(d)
        store, rel_id, head = make_role_state(temp)
        ledger, agreement = make_active_agreement()
        authority = base_authority(rel_id)
        gate = PolicyGate()
        caps = CapabilityService()
        builder = TrustTaskBuilder()
        admitter = ExecutionAdmitter()

        snapshot = ledger.snapshot("agr-research-001", 1)
        snapshot["terms"]["actions"].append("mutate")
        fresh = ledger.snapshot("agr-research-001", 1)
        record(results, "P4-P01-agreement-immutable", "query-only", "query-only" if fresh["terms"]["actions"] == ["query"] else "mutated", fresh)

        inputs = policy_inputs(rel_id, head, agreement, authority)
        allow = gate.evaluate(inputs)
        record(results, "P4-P02-policy-allow", "all_required_conditions_satisfied", allow["code"], allow)

        cap = caps.issue(
            decision=allow,
            relationship_id=rel_id,
            agreement_ref=agreement["agreement_ref"],
            recipient="role:researcher",
            purpose="synthetic-research",
            resource="dataset:synthetic-001",
            action="query",
            expires_at=20,
        )
        record(results, "P4-P03-capability-after-allow", "active", cap.get("status", "missing"), cap)

        task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], cap["capability_ref"], "nonce-positive-001")
        admitted = admitter.admit(task=task, decision=allow, capability=cap, authority=authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-P04-execution-admitted", "admitted", admitted["code"], admitted)

        observed_effect = {
            "relationship_id": task["relationship_id"],
            "agreement_ref": task["agreement_ref"],
            "resource": task["resource"],
            "action": task["action"],
            "payload_digest": task["payload_digest"],
            "task_ref": task["task_ref"],
            "decision_ref": allow["decision_ref"],
            "capability_ref": cap["capability_ref"],
        }
        correlated = admitter.validate_effect_correlation(receipt=admitted, observed_effect=observed_effect)
        record(results, "P4-P05-effect-correlated", "effect_correlated", correlated["code"], correlated)

        no_auth = dict(authority)
        no_auth["active"] = False
        decision = gate.evaluate(policy_inputs(rel_id, head, agreement, no_auth))
        record(results, "P4-N01-identity-without-authority", "authority_inactive_or_missing", decision["code"], decision)

        narrow = dict(authority)
        narrow["purposes"] = ["audit-only"]
        decision = gate.evaluate(policy_inputs(rel_id, head, agreement, narrow))
        record(results, "P4-N02-authority-purpose-out-of-scope", "authority_purpose_out_of_scope", decision["code"], decision)

        inactive_ledger = AgreementLedger()
        inactive_ledger.propose(agreement_id="agr-inactive", version=1, parties=["role:data-owner", "role:researcher"], terms=agreement["terms"])
        inactive_ledger.append_event(agreement_id="agr-inactive", version=1, event="accepted", actor="role:data-owner")
        inactive_ledger.append_event(agreement_id="agr-inactive", version=1, event="accepted", actor="role:researcher")
        inactive = inactive_ledger.snapshot("agr-inactive", 1)
        decision = gate.evaluate(policy_inputs(rel_id, head, inactive, authority))
        record(results, "P4-N03-accepted-but-inactive-agreement", "agreement_not_active", decision["code"], decision)

        missing_cap_task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], "urn:missing-capability", "nonce-no-cap")
        refused = admitter.admit(task=missing_cap_task, decision=allow, capability=None, authority=authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-N04-active-agreement-no-capability", "capability_missing", refused["code"], refused)

        revoked_authority = dict(authority)
        revoked_authority["active"] = False
        revoked_task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], cap["capability_ref"], "nonce-revoked-authority")
        refused = admitter.admit(task=revoked_task, decision=allow, capability=cap, authority=revoked_authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-N05-capability-after-authority-revocation", "authority_revoked_or_inactive", refused["code"], refused)

        wrong_agr_task = build_task(builder, rel_id, head, "sha256:wrong-agreement", authority["authority_ref"], allow["decision_ref"], cap["capability_ref"], "nonce-wrong-agreement")
        refused = admitter.admit(task=wrong_agr_task, decision=allow, capability=cap, authority=authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-N06-capability-wrong-agreement", "capability_wrong_agreement", refused["code"], refused)

        wrong_task_inputs = policy_inputs(rel_id, head, agreement, authority)
        wrong_task_inputs["task_id"] = "ara/research-query/9.9"
        decision = gate.evaluate(wrong_task_inputs)
        record(results, "P4-N07-wrong-task-version", "unsupported_task_version", decision["code"], decision)

        denied_inputs = policy_inputs(rel_id, head, agreement, authority)
        denied_inputs["instance_policy"] = "deny"
        denied_decision = gate.evaluate(denied_inputs)
        record(results, "P4-N08-policy-denial-despite-authority", "instance_policy_denied", denied_decision["code"], denied_decision)

        missing_inputs = policy_inputs(rel_id, head, agreement, authority)
        missing_inputs["role_record_head"] = None
        indeterminate = gate.evaluate(missing_inputs)
        record(results, "P4-N09-missing-evidence-indeterminate", "missing_required_evidence", indeterminate["code"], indeterminate)
        record(results, "P4-N09b-indeterminate-not-pass", "indeterminate", indeterminate["decision"], indeterminate)

        forged_effect = dict(observed_effect)
        forged_effect["resource"] = "dataset:other"
        correlation = admitter.validate_effect_correlation(receipt=admitted, observed_effect=forged_effect)
        record(results, "P4-N10-uncorrelated-effect", "effect_not_correlated_to_admission", correlation["code"], correlation)

        denied_cap = caps.issue(decision=denied_decision, relationship_id=rel_id, agreement_ref=agreement["agreement_ref"], recipient="role:researcher", purpose="synthetic-research", resource="dataset:synthetic-001", action="query", expires_at=20)
        record(results, "P4-N11-assurance-not-retroactive-authority", "capability_requires_allow_decision", denied_cap["code"], {"assurance": {"result": "pass", "scope": "implementation"}, "original_decision": denied_decision, "capability_result": denied_cap})

        child = caps.attenuate(cap["capability_ref"], expires_at=15)
        record(results, "P4-P06-capability-attenuation", "15", str(child.get("expires_at")), child)
        expanded = caps.attenuate(cap["capability_ref"], expires_at=25)
        record(results, "P4-N12-attenuation-cannot-expand", "attenuation_cannot_expand_expiry", expanded["code"], expanded)

        suspended = caps.set_status(child["capability_ref"], "suspended")
        suspended_task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], suspended["capability_ref"], "nonce-suspended")
        refused = admitter.admit(task=suspended_task, decision=allow, capability=suspended, authority=authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-N13-suspended-capability", "capability_not_active", refused["code"], refused)

        expired_cap = caps.issue(decision=allow, relationship_id=rel_id, agreement_ref=agreement["agreement_ref"], recipient="role:researcher", purpose="synthetic-research", resource="dataset:synthetic-001", action="query", expires_at=12)
        expired_task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], expired_cap["capability_ref"], "nonce-expired-cap", expires_at=20)
        refused = admitter.admit(task=expired_task, decision=allow, capability=expired_cap, authority=authority, agreement=agreement, current_role_record_head=head, now=12)
        record(results, "P4-N14-expired-capability", "capability_expired", refused["code"], refused)

        revoked_cap = caps.issue(decision=allow, relationship_id=rel_id, agreement_ref=agreement["agreement_ref"], recipient="role:researcher", purpose="synthetic-research", resource="dataset:synthetic-001", action="query", expires_at=20)
        revoked_cap = caps.set_status(revoked_cap["capability_ref"], "revoked")
        revoked_cap_task = build_task(builder, rel_id, head, agreement["agreement_ref"], authority["authority_ref"], allow["decision_ref"], revoked_cap["capability_ref"], "nonce-revoked-cap")
        refused = admitter.admit(task=revoked_cap_task, decision=allow, capability=revoked_cap, authority=authority, agreement=agreement, current_role_record_head=head, now=11)
        record(results, "P4-N15-revoked-capability", "capability_not_active", refused["code"], refused)

        stale_inputs = policy_inputs(rel_id, head, agreement, authority)
        stale_inputs["role_record_head"] = "sha256:older-valid-head"
        decision = gate.evaluate(stale_inputs)
        record(results, "P4-N16-stale-role-record-head", "stale_role_record_head", decision["code"], decision)

        summary = {
            "case_id": "IC-ARA-REL-001",
            "phase": 4,
            "experiment": "ara-policy-spine",
            "vectors": len(results),
            "passed": sum(1 for r in results if r["pass"]),
            "failed": sum(1 for r in results if not r["pass"]),
            "role_record_head": store.current_head(rel_id),
            "agreement_ref": agreement["agreement_ref"],
            "claim_boundary": "Lab-local executable ARA authorization composition; not standards-native policy, capability, Trust Task profile, VTA, TSP, or production authorization conformance.",
        }
        return {"summary": summary, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit non-zero if a vector fails")
    parser.add_argument("--output", type=Path, help="optional JSON evidence output")
    args = parser.parse_args()
    report = run_vectors()
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.check and report["summary"]["failed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
