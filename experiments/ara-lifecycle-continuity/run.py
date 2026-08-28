#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ROLE_DIR = ROOT / "experiments" / "ara-role-record"
POLICY_DIR = ROOT / "experiments" / "ara-policy-spine"
VRR_DIR = ROOT / "experiments" / "ara-distributed-vrr"
sys.path[:0] = [str(ROLE_DIR), str(POLICY_DIR), str(VRR_DIR)]

from engine import RoleRecordStore  # type: ignore  # noqa: E402
from authorization import (  # type: ignore  # noqa: E402
    AgreementLedger,
    CapabilityService,
    ExecutionAdmitter,
    PolicyGate,
    SUPPORTED_TASK,
    TrustTaskBuilder,
    digest,
)
from vrr import DistributedVRR  # type: ignore  # noqa: E402
from lifecycle import LifecycleCoordinator  # noqa: E402

ROLE_A = "urn:ara:agent-role:data-owner:001"
ROLE_B = "urn:ara:agent-role:researcher:001"
REL = "urn:ara:relationship:research:001"


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def append(
    store: RoleRecordStore,
    *,
    transition_id: str,
    transition_class: str,
    payload: dict[str, Any],
    visibility: str = "shared",
) -> dict[str, Any]:
    return store.apply(
        transition_id=transition_id,
        relationship_id=REL,
        actor_id="controller:data-owner",
        workflow_id="wf.relationship-state/1.0",
        transition_class=transition_class,
        previous_head=store.current_head(REL),
        visibility=visibility,
        payload=payload,
    )


def active_agreement() -> tuple[AgreementLedger, dict[str, Any]]:
    ledger = AgreementLedger()
    ledger.propose(
        agreement_id="agr-research-001",
        version=1,
        parties=["role:data-owner", "role:researcher"],
        terms={
            "purpose": "synthetic-research",
            "resources": ["dataset:synthetic-001"],
            "actions": ["query"],
            "recipients": [ROLE_B],
            "evidence_requirements": ["decision", "execution-effect"],
        },
    )
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:data-owner")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:researcher")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="activated", actor="role:data-owner")
    return ledger, ledger.snapshot("agr-research-001", 1)


def make_action(store: RoleRecordStore, agreement: dict[str, Any], caps: CapabilityService) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    authority = {
        "authority_id": "auth-data-owner-001",
        "relationship_id": REL,
        "active": True,
        "purposes": ["synthetic-research"],
        "resources": ["dataset:synthetic-001"],
        "actions": ["query"],
    }
    authority = {**authority, "authority_ref": digest(authority)}
    inputs = {
        "identity": {"subject": ROLE_A, "authenticated": True},
        "authority": authority,
        "agreement": agreement,
        "agreement_ref": agreement["agreement_ref"],
        "relationship": {"relationship_id": REL, "status": "active", "current_head": store.current_head(REL)},
        "role_record_head": store.current_head(REL),
        "recipient": ROLE_B,
        "purpose": "synthetic-research",
        "resource": "dataset:synthetic-001",
        "action": "query",
        "task_id": SUPPORTED_TASK,
    }
    decision = PolicyGate().evaluate(inputs)
    capability = caps.issue(
        decision=decision,
        relationship_id=REL,
        agreement_ref=agreement["agreement_ref"],
        recipient=ROLE_B,
        purpose="synthetic-research",
        resource="dataset:synthetic-001",
        action="query",
        expires_at=100,
    )
    task = TrustTaskBuilder().build(
        relationship_id=REL,
        agreement_ref=agreement["agreement_ref"],
        role_record_head=str(store.current_head(REL)),
        authority_ref=authority["authority_ref"],
        decision_ref=decision["decision_ref"],
        capability_ref=capability["capability_ref"],
        recipient=ROLE_B,
        purpose="synthetic-research",
        resource="dataset:synthetic-001",
        action="query",
        payload={"query": "count synthetic rows"},
        nonce="phase8-action-001",
        issued_at=10,
        expires_at=90,
        evidence_requirements=["decision", "execution-effect"],
    )
    admission = ExecutionAdmitter().admit(
        task=task,
        decision=decision,
        capability=capability,
        authority=authority,
        agreement=agreement,
        current_role_record_head=str(store.current_head(REL)),
        now=11,
    )
    return authority, capability, task, admission


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        path = tmp / "role-a.json"
        ledger, agreement = active_agreement()
        store = RoleRecordStore(path, ROLE_A)
        create = store.apply(
            transition_id="phase8-create",
            relationship_id=REL,
            actor_id="controller:data-owner",
            workflow_id="wf.relationship-bootstrap/1.0",
            transition_class="relationship.create",
            previous_head=None,
            visibility="shared",
            payload={
                "set": {
                    "purpose": "synthetic-research",
                    "status": "active",
                    "agreement_ref": agreement["agreement_ref"],
                    "authority_ref": "auth-data-owner-001",
                    "live_agent_generation": 1,
                }
            },
        )
        if create["result"] != "accepted":
            raise AssertionError(create)

        caps = CapabilityService()
        authority, capability, task, action = make_action(store, agreement, caps)
        record(results, "P8-P01-consequential-action-before-replacement", "admitted", action["result"], action)

        # Original Live Agent disappears. Replacement gets only the persisted Role Record path.
        del store
        replacement_store = RoleRecordStore(path, ROLE_A)
        coordinator = LifecycleCoordinator()
        reconstructed = coordinator.reconstruct_for_replacement(role_store=replacement_store, relationship_id=REL)
        record(results, "P8-P02-replacement-without-transcript-reconstructs", "reconstructed", reconstructed["result"], reconstructed)

        # Missing persisted state cannot be replaced by model memory.
        empty_store = RoleRecordStore(tmp / "empty-role.json", ROLE_A)
        missing = coordinator.reconstruct_for_replacement(role_store=empty_store, relationship_id=REL)
        record(results, "P8-N01-no-persisted-state-fails-safe", "replacement_missing_persisted_context", missing["code"], missing)

        challenge = append(
            replacement_store,
            transition_id="phase8-challenge",
            transition_class="relationship.challenge",
            payload={"set": {"status": "challenged", "suspect_since": "action:phase8-action-001", "suspect_interval_reviewed": False}},
        )
        record(results, "P8-P03-challenge-appended", "accepted", challenge["result"], challenge)

        vrr = DistributedVRR(REL, 1, [ROLE_A, ROLE_B])
        contested = vrr.add_object(owner_role=ROLE_A, evidence_class="shared_object", content={"effect_ref": action["effect_ref"], "claim": "query effect"}, label="contested action")
        vrr.dispose(actor_role=ROLE_A, object_ref=contested["object_ref"], disposition="accepted")
        dispute = vrr.dispose(actor_role=ROLE_B, object_ref=contested["object_ref"], disposition="disputed", note="effect challenged")
        disputed_state = vrr.mutual_state(contested["object_ref"])
        record(results, "P8-P04-dispute-remains-visible", "disputed", disputed_state["status"], disputed_state)

        before_bytes = json.dumps(contested, sort_keys=True)
        correction = vrr.correct(actor_role=ROLE_A, target_ref=dispute["disposition_ref"], correction="effect label corrected; original evidence retained")
        after_bytes = json.dumps(contested, sort_keys=True)
        record(results, "P8-N02-correction-does-not-rewrite-object", "unchanged", "unchanged" if before_bytes == after_bytes else "mutated", correction)

        revoked = caps.set_status(capability["capability_ref"], "revoked")
        record(results, "P8-P05-capability-revoked", "revoked", revoked["status"], revoked)

        replay_after_revoke = ExecutionAdmitter().admit(
            task=task,
            decision={"decision": "allow", "decision_ref": task["decision_ref"]},
            capability=revoked,
            authority=authority,
            agreement=agreement,
            current_role_record_head=task["role_record_head"],
            now=12,
        )
        record(results, "P8-N03-revoked-capability-not-usable", "capability_not_active", replay_after_revoke["code"], replay_after_revoke)

        # Remediation may narrow, never restore the revoked capability. A fresh decision is required.
        remediation = append(
            replacement_store,
            transition_id="phase8-remediation",
            transition_class="relationship.remediation",
            payload={"set": {"status": "remediated", "suspect_interval_reviewed": True, "remediation": "challenge reviewed; prior capability revoked"}},
        )
        record(results, "P8-P06-remediation-appended", "accepted", remediation["result"], remediation)

        old_cap_still_revoked = caps.get(capability["capability_ref"])
        record(results, "P8-N04-remediation-does-not-broaden-old-capability", "revoked", old_cap_still_revoked["status"], old_cap_still_revoked)

        # Historical validity does not disappear because current authority/capability changed.
        historical = coordinator.historical_action_status(action_receipt=action, later_authority_active=False)
        record(results, "P8-P07-historical-action-remains-valid", "historical_validity_preserved", historical["code"], historical)

        # Suspect interval must be reviewed before continuation.
        suspect_store = RoleRecordStore(tmp / "suspect-role.json", ROLE_A)
        suspect_store.apply(
            transition_id="suspect-create",
            relationship_id=REL,
            actor_id="controller:data-owner",
            workflow_id="wf.relationship-bootstrap/1.0",
            transition_class="relationship.create",
            previous_head=None,
            visibility="shared",
            payload={"set": {"purpose": "synthetic-research", "status": "active", "agreement_ref": agreement["agreement_ref"], "authority_ref": "auth", "suspect_since": "t1", "suspect_interval_reviewed": False}},
        )
        suspect_resume = coordinator.resume_after_remediation(role_store=suspect_store, relationship_id=REL)
        record(results, "P8-N05-suspect-interval-cannot-be-ignored", "suspect_interval_unreviewed", suspect_resume["code"], suspect_resume)

        continuation = coordinator.resume_after_remediation(role_store=replacement_store, relationship_id=REL)
        record(results, "P8-P08-reviewed-relationship-can-continue", "continuation_context_valid", continuation["code"], continuation)

        continue_event = append(
            replacement_store,
            transition_id="phase8-continue",
            transition_class="relationship.continue",
            payload={"set": {"status": "active", "live_agent_generation": 2}},
        )
        record(results, "P8-P09-continuation-is-explicit", "accepted", continue_event["result"], continue_event)

        # Closing one agreement does not erase the larger relationship or unrelated obligation.
        closed_agreement = ledger.append_event(agreement_id="agr-research-001", version=1, event="closed", actor="role:data-owner")
        obligations = [
            {"id": "obl-query", "agreement_ref": agreement["agreement_ref"], "termination": "agreement_close"},
            {"id": "obl-audit-history", "agreement_ref": "relationship-level", "termination": "relationship_close"},
        ]
        obligation_state = coordinator.surviving_obligations(obligations=obligations, closed_agreement_ref=agreement["agreement_ref"])
        surviving_ids = [o["id"] for o in obligation_state["surviving"]]
        record(results, "P8-N06-agreement-close-not-whole-relationship-close", "obl-audit-history", surviving_ids[0] if surviving_ids else "none", obligation_state)

        close_event = append(
            replacement_store,
            transition_id="phase8-close",
            transition_class="relationship.close",
            payload={"set": {"status": "closed", "closure_basis": "explicit relationship authority", "closed_agreement_ref": closed_agreement["agreement_ref"]}},
        )
        record(results, "P8-P10-relationship-closure-explicit", "accepted", close_event["result"], close_event)

        closed_resume = coordinator.reconstruct_for_replacement(role_store=replacement_store, relationship_id=REL)
        record(results, "P8-N07-closed-relationship-not-resumed", "relationship_closed", closed_resume["code"], closed_resume)

        history = replacement_store.validate_history(REL)
        record(results, "P8-P11-history-remains-valid-after-lifecycle", "valid", history["code"], history)

        summary = {
            "case_id": "IC-ARA-REL-001",
            "phase": 8,
            "experiment": "ara-lifecycle-continuity",
            "vectors": len(results),
            "passed": sum(1 for r in results if r["pass"]),
            "failed": sum(1 for r in results if not r["pass"]),
            "claim_boundary": "Lab-local lifecycle composition over Role Record, Agreement, Capability and distributed-VRR evidence; not production recovery, durable storage, revocation network, or normative ARA lifecycle conformance.",
        }
        return {"summary": summary, "results": results}


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
