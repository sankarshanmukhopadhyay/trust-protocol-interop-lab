from __future__ import annotations

import hashlib
import hmac
import json
from typing import Any

from authorization import SUPPORTED_TASK, canonical_json, digest

RECEIPT_CLASS = "ara/cryptographic-use-receipt/0.1"


class ProtectedSigner:
    """Lab-local protected-signing adapter.

    The only public cryptographic-use operation accepts a fully bound signed-action
    request plus the already-admitted Phase 4 context. It deliberately exposes no
    raw sign(bytes) method.
    """

    REQUIRED_REQUEST_FIELDS = {
        "agent_role_id",
        "role_record_head",
        "workflow_id",
        "workflow_version",
        "task_id",
        "task_ref",
        "relationship_id",
        "agreement_ref",
        "authority_ref",
        "decision_ref",
        "capability_ref",
        "admission_receipt_ref",
        "recipient",
        "purpose",
        "payload_digest",
        "nonce",
        "expires_at",
        "signing_identity",
        "expected_receipt_class",
    }

    def __init__(
        self,
        *,
        secret: bytes,
        workflow_id: str,
        workflow_version: str,
        signing_identity: str,
    ) -> None:
        self._secret = secret
        self._workflow_id = workflow_id
        self._workflow_version = workflow_version
        self._signing_identity = signing_identity
        self._used_nonces: set[str] = set()

    def use(
        self,
        *,
        request: dict[str, Any],
        task: dict[str, Any],
        decision: dict[str, Any],
        capability: dict[str, Any] | None,
        authority: dict[str, Any],
        agreement: dict[str, Any],
        admission_receipt: dict[str, Any] | None,
        current_role_record_head: str,
        workflow_attestation: dict[str, Any],
        now: int,
    ) -> dict[str, Any]:
        """Attempt one attributable cryptographic use and always return a receipt."""

        base = {
            "receipt_class": RECEIPT_CLASS,
            "agent_role_id": request.get("agent_role_id"),
            "workflow_id": request.get("workflow_id"),
            "workflow_version": request.get("workflow_version"),
            "task_ref": request.get("task_ref"),
            "relationship_id": request.get("relationship_id"),
            "agreement_ref": request.get("agreement_ref"),
            "authority_ref": request.get("authority_ref"),
            "decision_ref": request.get("decision_ref"),
            "capability_ref": request.get("capability_ref"),
            "admission_receipt_ref": request.get("admission_receipt_ref"),
            "recipient": request.get("recipient"),
            "purpose": request.get("purpose"),
            "payload_digest": request.get("payload_digest"),
            "nonce": request.get("nonce"),
            "signing_identity": request.get("signing_identity"),
        }

        def refuse(code: str) -> dict[str, Any]:
            material = {**base, "result": "refused", "code": code}
            return {**material, "receipt_ref": digest(material)}

        missing = sorted(k for k in self.REQUIRED_REQUEST_FIELDS if request.get(k) is None)
        if missing:
            material = {**base, "result": "refused", "code": "missing_required_binding", "missing": missing}
            return {**material, "receipt_ref": digest(material)}

        if request.get("caller_class") == "live-agent":
            return refuse("direct_live_agent_call")
        if request.get("caller_class") != "workflow":
            return refuse("caller_not_authenticated_workflow")
        if "raw_bytes" in request:
            return refuse("arbitrary_byte_signing_not_permitted")

        if workflow_attestation.get("authenticated") is not True:
            return refuse("workflow_not_authenticated")
        if (
            workflow_attestation.get("workflow_id") != self._workflow_id
            or workflow_attestation.get("workflow_version") != self._workflow_version
        ):
            return refuse("workflow_identity_mismatch")
        if (
            request["workflow_id"] != self._workflow_id
            or request["workflow_version"] != self._workflow_version
        ):
            return refuse("workflow_request_mismatch")

        if task.get("task_id") != SUPPORTED_TASK or request["task_id"] != SUPPORTED_TASK:
            return refuse("unsupported_task_version")
        if request["task_ref"] != task.get("task_ref"):
            return refuse("task_instance_mismatch")

        if request["role_record_head"] != current_role_record_head:
            return refuse("stale_role_record_head")
        if request["role_record_head"] != task.get("role_record_head"):
            return refuse("task_role_record_mismatch")
        if request["relationship_id"] != task.get("relationship_id"):
            return refuse("relationship_mismatch")
        if request["agreement_ref"] != task.get("agreement_ref"):
            return refuse("agreement_mismatch")
        if request["recipient"] != task.get("recipient"):
            return refuse("recipient_substitution")
        if request["purpose"] != task.get("purpose"):
            return refuse("purpose_mismatch")
        if request["payload_digest"] != task.get("payload_digest"):
            return refuse("payload_substitution")
        if request["nonce"] != task.get("nonce"):
            return refuse("nonce_mismatch")
        if int(request["expires_at"]) != int(task.get("expires_at", 0)):
            return refuse("expiry_mismatch")

        if authority.get("active") is not True:
            return refuse("authority_revoked_or_inactive")
        if now >= int(authority.get("expires_at", 2**63 - 1)):
            return refuse("authority_expired")
        if request["authority_ref"] != authority.get("authority_ref"):
            return refuse("authority_reference_mismatch")
        if authority.get("relationship_id") != request["relationship_id"]:
            return refuse("authority_wrong_relationship")

        if agreement.get("status") != "active":
            return refuse("agreement_not_active")
        if request["agreement_ref"] != agreement.get("agreement_ref"):
            return refuse("agreement_reference_mismatch")

        if decision.get("decision") != "allow":
            return refuse("decision_not_allow")
        if request["decision_ref"] != decision.get("decision_ref"):
            return refuse("decision_reference_mismatch")
        if task.get("decision_ref") != decision.get("decision_ref"):
            return refuse("task_decision_mismatch")

        if capability is None:
            return refuse("capability_missing")
        if capability.get("status") != "active":
            return refuse("capability_not_active")
        if request["capability_ref"] != capability.get("capability_ref"):
            return refuse("capability_reference_mismatch")
        if task.get("capability_ref") != capability.get("capability_ref"):
            return refuse("task_capability_mismatch")
        if capability.get("relationship_id") != request["relationship_id"]:
            return refuse("capability_wrong_relationship")
        if capability.get("agreement_ref") != request["agreement_ref"]:
            return refuse("capability_wrong_agreement")
        if capability.get("recipient") != request["recipient"]:
            return refuse("capability_recipient_mismatch")
        if capability.get("purpose") != request["purpose"]:
            return refuse("capability_purpose_mismatch")
        if now >= int(capability.get("expires_at", 0)):
            return refuse("capability_expired")

        if admission_receipt is None:
            return refuse("admission_receipt_missing")
        if admission_receipt.get("result") != "admitted":
            return refuse("execution_not_admitted")
        if request["admission_receipt_ref"] != admission_receipt.get("receipt_ref"):
            return refuse("admission_receipt_mismatch")
        if admission_receipt.get("task_ref") != task.get("task_ref"):
            return refuse("admission_task_mismatch")
        if admission_receipt.get("decision_ref") != decision.get("decision_ref"):
            return refuse("admission_decision_mismatch")
        if admission_receipt.get("capability_ref") != capability.get("capability_ref"):
            return refuse("admission_capability_mismatch")

        if request["signing_identity"] != self._signing_identity:
            return refuse("signing_identity_mismatch")
        if request["expected_receipt_class"] != RECEIPT_CLASS:
            return refuse("receipt_class_mismatch")
        if now >= int(request["expires_at"]):
            return refuse("signing_request_expired")

        nonce = str(request["nonce"])
        if nonce in self._used_nonces:
            return refuse("signing_replay")

        signed_context = {
            "agent_role_id": request["agent_role_id"],
            "role_record_head": request["role_record_head"],
            "workflow_id": request["workflow_id"],
            "workflow_version": request["workflow_version"],
            "task_id": request["task_id"],
            "task_ref": request["task_ref"],
            "relationship_id": request["relationship_id"],
            "agreement_ref": request["agreement_ref"],
            "authority_ref": request["authority_ref"],
            "decision_ref": request["decision_ref"],
            "capability_ref": request["capability_ref"],
            "admission_receipt_ref": request["admission_receipt_ref"],
            "recipient": request["recipient"],
            "purpose": request["purpose"],
            "payload_digest": request["payload_digest"],
            "nonce": nonce,
            "expires_at": request["expires_at"],
            "signing_identity": request["signing_identity"],
        }
        signed_context_ref = digest(signed_context)
        signature = "hmac-sha256:" + hmac.new(
            self._secret,
            canonical_json(signed_context).encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        self._used_nonces.add(nonce)
        material = {
            **base,
            "result": "accepted",
            "code": "cryptographic_use_accepted",
            "signed_context_ref": signed_context_ref,
            "signature": signature,
        }
        return {**material, "receipt_ref": digest(material)}


def build_signed_action_request(
    *,
    agent_role_id: str,
    workflow_id: str,
    workflow_version: str,
    task: dict[str, Any],
    authority: dict[str, Any],
    decision: dict[str, Any],
    capability: dict[str, Any],
    admission_receipt: dict[str, Any],
    signing_identity: str,
) -> dict[str, Any]:
    """Derive the signer request from admitted context rather than caller bytes."""

    return {
        "caller_class": "workflow",
        "agent_role_id": agent_role_id,
        "role_record_head": task["role_record_head"],
        "workflow_id": workflow_id,
        "workflow_version": workflow_version,
        "task_id": task["task_id"],
        "task_ref": task["task_ref"],
        "relationship_id": task["relationship_id"],
        "agreement_ref": task["agreement_ref"],
        "authority_ref": authority["authority_ref"],
        "decision_ref": decision["decision_ref"],
        "capability_ref": capability["capability_ref"],
        "admission_receipt_ref": admission_receipt["receipt_ref"],
        "recipient": task["recipient"],
        "purpose": task["purpose"],
        "payload_digest": task["payload_digest"],
        "nonce": task["nonce"],
        "expires_at": task["expires_at"],
        "signing_identity": signing_identity,
        "expected_receipt_class": RECEIPT_CLASS,
    }
