#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY_DIR = ROOT / "experiments" / "ara-policy-spine"
ROLE_DIR = ROOT / "experiments" / "ara-role-record"
SIGN_DIR = ROOT / "experiments" / "ara-protected-signing"
sys.path[:0] = [str(POLICY_DIR), str(ROLE_DIR), str(SIGN_DIR)]

from authorization import AgreementLedger, CapabilityService, ExecutionAdmitter, PolicyGate, SUPPORTED_TASK, TrustTaskBuilder, digest  # type: ignore  # noqa: E402
from engine import RoleRecordStore  # type: ignore  # noqa: E402
from signer import ProtectedSigner, build_signed_action_request  # type: ignore  # noqa: E402

AGENT_ROLE_ID = "urn:ara:agent-role:data-owner:001"
RECIPIENT_ROLE_ID = "urn:ara:agent-role:researcher:001"
RELATIONSHIP_ID = "urn:ara:relationship:research:001"
WORKFLOW_ID = "wf.ara-protected-signing"
WORKFLOW_VERSION = "1.0"
SIGNING_IDENTITY = "vid:lab:data-owner:001"
SHARED_LAB_KEY = b"lab-only-protected-key-material"


def build_package() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        store = RoleRecordStore(Path(tmp) / "sender-role-record.json", AGENT_ROLE_ID)
        transition = store.apply(
            transition_id="phase6-sender-001",
            relationship_id=RELATIONSHIP_ID,
            actor_id="controller:data-owner",
            workflow_id="wf.relationship-bootstrap/1.0",
            transition_class="relationship.create",
            previous_head=None,
            visibility="private",
            payload={"set": {"purpose": "synthetic-research", "status": "active"}},
        )
        head = transition["resulting_head"]

        ledger = AgreementLedger()
        ledger.propose(
            agreement_id="agr-research-001",
            version=1,
            parties=["role:data-owner", "role:researcher"],
            terms={
                "purpose": "synthetic-research",
                "resources": ["dataset:synthetic-001"],
                "actions": ["query"],
                "recipients": [RECIPIENT_ROLE_ID],
                "evidence_requirements": ["decision", "execution-effect", "cryptographic-use"],
            },
        )
        ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:data-owner")
        ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:researcher")
        ledger.append_event(agreement_id="agr-research-001", version=1, event="activated", actor="role:data-owner")
        agreement = ledger.snapshot("agr-research-001", 1)

        authority = {
            "authority_id": "auth-data-owner-001",
            "subject_role_id": AGENT_ROLE_ID,
            "relationship_id": RELATIONSHIP_ID,
            "active": True,
            "expires_at": 100,
            "purposes": ["synthetic-research"],
            "resources": ["dataset:synthetic-001"],
            "actions": ["query"],
        }
        authority = {**authority, "authority_ref": digest(authority)}

        policy_inputs = {
            "identity": {"subject": "role:data-owner", "authenticated": True},
            "authority": authority,
            "agreement": agreement,
            "agreement_ref": agreement["agreement_ref"],
            "relationship": {"relationship_id": RELATIONSHIP_ID, "status": "active", "current_head": head},
            "role_record_head": head,
            "recipient": RECIPIENT_ROLE_ID,
            "purpose": "synthetic-research",
            "resource": "dataset:synthetic-001",
            "action": "query",
            "task_id": SUPPORTED_TASK,
        }
        decision = PolicyGate().evaluate(policy_inputs)
        if decision["decision"] != "allow":
            raise RuntimeError(decision)

        capability = CapabilityService().issue(
            decision=decision,
            relationship_id=RELATIONSHIP_ID,
            agreement_ref=agreement["agreement_ref"],
            recipient=RECIPIENT_ROLE_ID,
            purpose="synthetic-research",
            resource="dataset:synthetic-001",
            action="query",
            expires_at=50,
        )
        task = TrustTaskBuilder().build(
            relationship_id=RELATIONSHIP_ID,
            agreement_ref=agreement["agreement_ref"],
            role_record_head=head,
            authority_ref=authority["authority_ref"],
            decision_ref=decision["decision_ref"],
            capability_ref=capability["capability_ref"],
            recipient=RECIPIENT_ROLE_ID,
            purpose="synthetic-research",
            resource="dataset:synthetic-001",
            action="query",
            payload={"query": "count synthetic rows"},
            nonce="phase6-wire-nonce-001",
            issued_at=10,
            expires_at=40,
            evidence_requirements=["decision", "execution-effect", "cryptographic-use"],
        )
        admission = ExecutionAdmitter().admit(
            task=task,
            decision=decision,
            capability=capability,
            authority=authority,
            agreement=agreement,
            current_role_record_head=head,
            now=11,
        )
        request = build_signed_action_request(
            agent_role_id=AGENT_ROLE_ID,
            workflow_id=WORKFLOW_ID,
            workflow_version=WORKFLOW_VERSION,
            task=task,
            authority=authority,
            decision=decision,
            capability=capability,
            admission_receipt=admission,
            signing_identity=SIGNING_IDENTITY,
        )
        cryptographic_use = ProtectedSigner(
            secret=SHARED_LAB_KEY,
            workflow_id=WORKFLOW_ID,
            workflow_version=WORKFLOW_VERSION,
            signing_identity=SIGNING_IDENTITY,
        ).use(
            request=request,
            task=task,
            decision=decision,
            capability=capability,
            authority=authority,
            agreement=agreement,
            admission_receipt=admission,
            current_role_record_head=head,
            workflow_attestation={"authenticated": True, "workflow_id": WORKFLOW_ID, "workflow_version": WORKFLOW_VERSION},
            now=12,
        )
        if cryptographic_use["result"] != "accepted":
            raise RuntimeError(cryptographic_use)

        wire = {
            "wire_version": "ara/relationship-action/0.1",
            "sender_role_id": AGENT_ROLE_ID,
            "recipient_role_id": RECIPIENT_ROLE_ID,
            "relationship_id": RELATIONSHIP_ID,
            "sender_role_record_head": head,
            "agreement": agreement,
            "authority": authority,
            "task": task,
            "sender_decision_receipt": decision,
            "sender_admission_receipt": admission,
            "cryptographic_use_receipt": cryptographic_use,
        }
        return {**wire, "wire_ref": digest(wire)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = build_package()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(package, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
