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
POLICY_DIR = ROOT / "experiments" / "ara-policy-spine"
ROLE_DIR = ROOT / "experiments" / "ara-role-record"
sys.path.insert(0, str(POLICY_DIR))
sys.path.insert(0, str(ROLE_DIR))

from authorization import (  # type: ignore  # noqa: E402
    AgreementLedger,
    CapabilityService,
    ExecutionAdmitter,
    PolicyGate,
    SUPPORTED_TASK,
    TrustTaskBuilder,
    digest,
)
from engine import RoleRecordStore  # type: ignore  # noqa: E402
from signer import ProtectedSigner, build_signed_action_request  # noqa: E402

WORKFLOW_ID = "wf.ara-protected-signing"
WORKFLOW_VERSION = "1.0"
SIGNING_IDENTITY = "vid:lab:data-owner:001"
AGENT_ROLE_ID = "urn:ara:agent-role:data-owner:001"


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def fixture(temp: Path) -> dict[str, Any]:
    relationship_id = "urn:ara:relationship:research:001"
    store = RoleRecordStore(temp / "role-record.json", AGENT_ROLE_ID)
    transition = store.apply(
        transition_id="phase5-tr-001",
        relationship_id=relationship_id,
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
            "recipients": ["role:researcher"],
            "evidence_requirements": ["decision", "execution-effect", "cryptographic-use"],
        },
    )
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:data-owner")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="accepted", actor="role:researcher")
    ledger.append_event(agreement_id="agr-research-001", version=1, event="activated", actor="role:data-owner")
    agreement = ledger.snapshot("agr-research-001", 1)

    authority = {
        "authority_id": "auth-data-owner-001",
        "relationship_id": relationship_id,
        "active": True,
        "expires_at": 100,
        "purposes": ["synthetic-research"],
        "resources": ["dataset:synthetic-001"],
        "actions": ["query"],
    }
    authority = {**authority, "authority_ref": digest(authority)}

    inputs = {
        "identity": {"subject": "role:data-owner", "authenticated": True},
        "authority": authority,
        "agreement": agreement,
        "agreement_ref": agreement["agreement_ref"],
        "relationship": {"relationship_id": relationship_id, "status": "active", "current_head": head},
        "role_record_head": head,
        "recipient": "role:researcher",
        "purpose": "synthetic-research",
        "resource": "dataset:synthetic-001",
        "action": "query",
        "task_id": SUPPORTED_TASK,
    }
    decision = PolicyGate().evaluate(inputs)
    if decision["decision"] != "allow":
        raise AssertionError(decision)

    capability = CapabilityService().issue(
        decision=decision,
        relationship_id=relationship_id,
        agreement_ref=agreement["agreement_ref"],
        recipient="role:researcher",
        purpose="synthetic-research",
        resource="dataset:synthetic-001",
        action="query",
        expires_at=50,
    )
    task = TrustTaskBuilder().build(
        relationship_id=relationship_id,
        agreement_ref=agreement["agreement_ref"],
        role_record_head=head,
        authority_ref=authority["authority_ref"],
        decision_ref=decision["decision_ref"],
        capability_ref=capability["capability_ref"],
        recipient="role:researcher",
        purpose="synthetic-research",
        resource="dataset:synthetic-001",
        action="query",
        payload={"query": "count synthetic rows"},
        nonce="nonce-phase5-001",
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
    if admission["result"] != "admitted":
        raise AssertionError(admission)

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
    workflow = {"authenticated": True, "workflow_id": WORKFLOW_ID, "workflow_version": WORKFLOW_VERSION}
    return {
        "store": store,
        "ledger": ledger,
        "head": head,
        "relationship_id": relationship_id,
        "agreement": agreement,
        "authority": authority,
        "decision": decision,
        "capability": capability,
        "task": task,
        "admission": admission,
        "request": request,
        "workflow": workflow,
    }


def signer() -> ProtectedSigner:
    return ProtectedSigner(
        secret=b"lab-only-protected-key-material",
        workflow_id=WORKFLOW_ID,
        workflow_version=WORKFLOW_VERSION,
        signing_identity=SIGNING_IDENTITY,
    )


def attempt(f: dict[str, Any], *, request=None, task=None, decision=None, capability="baseline", authority=None, agreement=None, admission="baseline", head=None, workflow=None, now=12, use_signer=None) -> dict[str, Any]:
    cap = f["capability"] if capability == "baseline" else capability
    adm = f["admission"] if admission == "baseline" else admission
    return (use_signer or signer()).use(
        request=copy.deepcopy(request if request is not None else f["request"]),
        task=copy.deepcopy(task if task is not None else f["task"]),
        decision=copy.deepcopy(decision if decision is not None else f["decision"]),
        capability=copy.deepcopy(cap),
        authority=copy.deepcopy(authority if authority is not None else f["authority"]),
        agreement=copy.deepcopy(agreement if agreement is not None else f["agreement"]),
        admission_receipt=copy.deepcopy(adm),
        current_role_record_head=head if head is not None else f["head"],
        workflow_attestation=copy.deepcopy(workflow if workflow is not None else f["workflow"]),
        now=now,
    )


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as tmp:
        f = fixture(Path(tmp))

        accepted = attempt(f)
        record(results, "P5-P01-admitted-context-signs", "cryptographic_use_accepted", accepted["code"], accepted)

        req = copy.deepcopy(f["request"]); req["caller_class"] = "live-agent"
        r = attempt(f, request=req)
        record(results, "P5-N01-direct-live-agent-call", "direct_live_agent_call", r["code"], r)

        req = copy.deepcopy(f["request"]); req["raw_bytes"] = "arbitrary"
        r = attempt(f, request=req)
        record(results, "P5-N02-arbitrary-byte-signing", "arbitrary_byte_signing_not_permitted", r["code"], r)

        wf = copy.deepcopy(f["workflow"]); wf["authenticated"] = False
        r = attempt(f, workflow=wf)
        record(results, "P5-N03-unauthenticated-workflow", "workflow_not_authenticated", r["code"], r)

        wf = copy.deepcopy(f["workflow"]); wf["workflow_version"] = "2.0"
        r = attempt(f, workflow=wf)
        record(results, "P5-N04-replaced-workflow", "workflow_identity_mismatch", r["code"], r)

        task = copy.deepcopy(f["task"]); task["task_id"] = "ara/research-query/0.0"
        req = copy.deepcopy(f["request"]); req["task_id"] = "ara/research-query/0.0"
        r = attempt(f, request=req, task=task)
        record(results, "P5-N05-unsupported-task-version", "unsupported_task_version", r["code"], r)

        req = copy.deepcopy(f["request"]); req["recipient"] = "role:attacker"
        r = attempt(f, request=req)
        record(results, "P5-N06-recipient-substitution", "recipient_substitution", r["code"], r)

        req = copy.deepcopy(f["request"]); req["payload_digest"] = digest({"query": "export everything"})
        r = attempt(f, request=req)
        record(results, "P5-N07-payload-substitution", "payload_substitution", r["code"], r)

        req = copy.deepcopy(f["request"]); req["relationship_id"] = "urn:ara:relationship:other"
        r = attempt(f, request=req)
        record(results, "P5-N08-wrong-relationship", "relationship_mismatch", r["code"], r)

        req = copy.deepcopy(f["request"]); req["agreement_ref"] = "sha256:other-agreement"
        r = attempt(f, request=req)
        record(results, "P5-N09-wrong-agreement", "agreement_mismatch", r["code"], r)

        r = attempt(f, head="sha256:new-current-head")
        record(results, "P5-N10-stale-role-record-head", "stale_role_record_head", r["code"], r)

        authority = copy.deepcopy(f["authority"]); authority["active"] = False
        r = attempt(f, authority=authority)
        record(results, "P5-N11-revoked-authority", "authority_revoked_or_inactive", r["code"], r)

        authority = copy.deepcopy(f["authority"]); authority["expires_at"] = 12
        r = attempt(f, authority=authority, now=12)
        record(results, "P5-N12-expired-authority", "authority_expired", r["code"], r)

        replay_signer = signer()
        first = attempt(f, use_signer=replay_signer)
        if first["result"] != "accepted":
            raise AssertionError(first)
        r = attempt(f, use_signer=replay_signer)
        record(results, "P5-N13-replayed-nonce-task", "signing_replay", r["code"], r)

        suspended = copy.deepcopy(f["agreement"]); suspended["status"] = "suspended"
        r = attempt(f, agreement=suspended)
        record(results, "P5-N14-signing-after-suspension", "agreement_not_active", r["code"], r)

        closed = copy.deepcopy(f["agreement"]); closed["status"] = "closed"
        r = attempt(f, agreement=closed)
        record(results, "P5-N15-signing-after-closure", "agreement_not_active", r["code"], r)

        req = copy.deepcopy(f["request"]); req["decision_ref"] = None
        r = attempt(f, request=req)
        record(results, "P5-N16-missing-decision-binding", "missing_required_binding", r["code"], r)

        req = copy.deepcopy(f["request"]); req["admission_receipt_ref"] = None
        r = attempt(f, request=req)
        record(results, "P5-N17-missing-admission-evidence", "missing_required_binding", r["code"], r)

        summary = {
            "case_id": "IC-ARA-REL-001",
            "phase": 5,
            "experiment": "ara-protected-signing",
            "vectors": len(results),
            "passed": sum(1 for item in results if item["pass"]),
            "failed": sum(1 for item in results if not item["pass"]),
            "claim_boundary": "Lab-local protected-signing adapter using HMAC as executable stand-in; not OpenVTC VTA, HSM, TEE, DID, TSP, VID, or production key-protection conformance.",
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
