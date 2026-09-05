"""PDC -> DTG Trust Task document binding.

This module binds application-owned PDC semantics into the outer Trust Task
shape observed in the pinned DTG/OpenVTC baselines. It does not implement a VTC,
prove generic Trust Tasks conformance, or treat relationship identity as action
authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


PDC_TASK_TYPE = "https://trustoverip.org/dtg/pdc/care-exception-response/0.1"
FRAMEWORK_MEMBERS = {
    "id",
    "threadId",
    "parentThreadId",
    "type",
    "issuer",
    "recipient",
    "issuedAt",
    "expiresAt",
    "payload",
    "proof",
}


@dataclass(frozen=True)
class PdcActionBinding:
    task_id: str
    issuer: str
    recipient: str
    principal: str
    requester: str
    relationship_ref: str
    delegation_ref: str | None
    action: str
    resource: str
    context: str
    policy_version: str
    authority_evidence_state: str
    issued_at: str
    expires_at: str


def build_trust_task_document(binding: PdcActionBinding, *, proof: Any | None = None) -> dict[str, Any]:
    """Build the bounded Trust Task-shaped document for one PDC action request."""
    if binding.action != "care.exception.respond":
        raise ValueError("PDC Trust Task profile only permits care.exception.respond")
    if not binding.resource.startswith("reminder:"):
        raise ValueError("PDC exception response must bind an exact reminder resource")
    if binding.authority_evidence_state not in {"present", "missing", "revoked", "stale"}:
        raise ValueError("unsupported authorityEvidenceState")

    payload = {
        "principal": binding.principal,
        "requester": binding.requester,
        "relationshipRef": binding.relationship_ref,
        "delegationRef": binding.delegation_ref,
        "action": binding.action,
        "resource": binding.resource,
        "context": binding.context,
        "policyVersion": binding.policy_version,
        "authorityEvidenceState": binding.authority_evidence_state,
    }
    doc: dict[str, Any] = {
        "id": binding.task_id,
        "type": PDC_TASK_TYPE,
        "issuer": binding.issuer,
        "recipient": binding.recipient,
        "issuedAt": binding.issued_at,
        "expiresAt": binding.expires_at,
        "payload": payload,
    }
    if proof is not None:
        doc["proof"] = proof
    return doc


def validate_profile_document(doc: dict[str, Any]) -> list[str]:
    """Return deterministic profile violations without claiming framework validation."""
    violations: list[str] = []
    unknown_outer = sorted(set(doc) - FRAMEWORK_MEMBERS)
    if unknown_outer:
        violations.append(f"unknown framework-level members: {unknown_outer}")

    for member in ("id", "type", "issuer", "recipient", "issuedAt", "expiresAt", "payload"):
        if member not in doc:
            violations.append(f"missing required profile member: {member}")

    payload = doc.get("payload")
    if not isinstance(payload, dict):
        violations.append("payload must be an object")
        return violations

    required_payload = {
        "principal",
        "requester",
        "relationshipRef",
        "delegationRef",
        "action",
        "resource",
        "context",
        "policyVersion",
        "authorityEvidenceState",
    }
    missing = sorted(required_payload - set(payload))
    if missing:
        violations.append(f"missing PDC payload members: {missing}")

    if payload.get("action") != "care.exception.respond":
        violations.append("action is outside PDC profile")
    resource = payload.get("resource")
    if not isinstance(resource, str) or not resource.startswith("reminder:"):
        violations.append("resource is not an exact reminder reference")
    if payload.get("relationshipRef") == payload.get("delegationRef"):
        violations.append("relationshipRef and delegationRef must not collapse")
    if payload.get("authorityEvidenceState") == "missing" and payload.get("delegationRef") is not None:
        violations.append("missing authority evidence must not carry a delegationRef")

    try:
        issued = datetime.fromisoformat(str(doc["issuedAt"]).replace("Z", "+00:00"))
        expires = datetime.fromisoformat(str(doc["expiresAt"]).replace("Z", "+00:00"))
        if issued.tzinfo is None or expires.tzinfo is None:
            violations.append("issuedAt/expiresAt must be timezone-aware")
        elif expires <= issued:
            violations.append("expiresAt must be after issuedAt")
    except (KeyError, ValueError):
        violations.append("issuedAt/expiresAt must be ISO-8601 timestamps")

    return violations


def classify_proof_transport_boundary(doc: dict[str, Any], transport: str) -> dict[str, str]:
    """Preserve the currently observed proof-vs-transport-auth distinction."""
    has_proof = "proof" in doc
    if has_proof:
        return {
            "document_proof": "present",
            "transport": transport,
            "claim": "profile-bound document; generic framework conformance not asserted",
        }
    if transport in {"didcomm-authcrypt", "tsp-authenticated"}:
        return {
            "document_proof": "absent",
            "transport": transport,
            "claim": "openvtc-transport-bound candidate only; generic Trust Tasks conformance not asserted",
        }
    return {
        "document_proof": "absent",
        "transport": transport,
        "claim": "insufficient authentication evidence",
    }


def canonical_binding(*, authority_state: str = "present") -> PdcActionBinding:
    delegation_ref = None if authority_state == "missing" else "delegation:caregiver-001"
    return PdcActionBinding(
        task_id="urn:uuid:00000000-0000-4000-8000-000000000132",
        issuer="did:example:caregiver",
        recipient="did:example:vtc",
        principal="did:example:care-recipient",
        requester="did:example:caregiver",
        relationship_ref="relctx:care-001",
        delegation_ref=delegation_ref,
        action="care.exception.respond",
        resource="reminder:rm001",
        context="protected-delegated-care",
        policy_version="pdc-policy-v1",
        authority_evidence_state=authority_state,
        issued_at="2026-09-05T09:00:00+00:00",
        expires_at="2026-09-05T09:05:00+00:00",
    )
