from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

SUPPORTED_TASK = "ara/research-query/0.1"
DECISIONS = {"allow", "deny", "escalate", "indeterminate"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Decision:
    decision: str
    code: str
    decision_ref: str
    inputs_ref: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class AgreementLedger:
    """Immutable agreement terms plus append-only lifecycle events."""

    def __init__(self) -> None:
        self._agreements: dict[str, dict[str, Any]] = {}

    def propose(self, *, agreement_id: str, version: int, parties: list[str], terms: dict[str, Any]) -> dict[str, Any]:
        key = f"{agreement_id}@{version}"
        if key in self._agreements:
            raise ValueError("agreement_version_exists")
        immutable = {
            "agreement_id": agreement_id,
            "version": version,
            "parties": list(parties),
            "terms": json.loads(canonical_json(terms)),
        }
        agreement_ref = digest(immutable)
        record = {
            **immutable,
            "agreement_ref": agreement_ref,
            "events": [
                {
                    "sequence": 1,
                    "event": "proposed",
                    "actor": parties[0],
                    "event_ref": digest({"agreement_ref": agreement_ref, "sequence": 1, "event": "proposed", "actor": parties[0]}),
                }
            ],
        }
        self._agreements[key] = record
        return self.snapshot(agreement_id, version)

    def _record(self, agreement_id: str, version: int) -> dict[str, Any]:
        key = f"{agreement_id}@{version}"
        if key not in self._agreements:
            raise KeyError("agreement_missing")
        return self._agreements[key]

    def append_event(self, *, agreement_id: str, version: int, event: str, actor: str) -> dict[str, Any]:
        if event not in {"accepted", "activated", "suspended", "closed"}:
            raise ValueError("unsupported_agreement_event")
        record = self._record(agreement_id, version)
        sequence = len(record["events"]) + 1
        event_obj = {
            "sequence": sequence,
            "event": event,
            "actor": actor,
            "event_ref": digest({
                "agreement_ref": record["agreement_ref"],
                "sequence": sequence,
                "event": event,
                "actor": actor,
            }),
        }
        record["events"].append(event_obj)
        return self.snapshot(agreement_id, version)

    def snapshot(self, agreement_id: str, version: int) -> dict[str, Any]:
        record = self._record(agreement_id, version)
        events = json.loads(canonical_json(record["events"]))
        status = "proposed"
        accepted_by = {e["actor"] for e in events if e["event"] == "accepted"}
        if accepted_by.issuperset(set(record["parties"])):
            status = "accepted"
        if any(e["event"] == "activated" for e in events):
            status = "active"
        if any(e["event"] == "suspended" for e in events):
            status = "suspended"
        if any(e["event"] == "closed" for e in events):
            status = "closed"
        return {
            "agreement_id": record["agreement_id"],
            "version": record["version"],
            "parties": list(record["parties"]),
            "terms": json.loads(canonical_json(record["terms"])),
            "agreement_ref": record["agreement_ref"],
            "events": events,
            "status": status,
        }


class PolicyGate:
    """Closed deterministic authorization decision over explicit evidence inputs."""

    REQUIRED_EVIDENCE = {
        "identity",
        "authority",
        "agreement",
        "relationship",
        "role_record_head",
        "recipient",
        "purpose",
        "resource",
        "action",
        "task_id",
    }

    def evaluate(self, inputs: dict[str, Any]) -> dict[str, Any]:
        missing = sorted(key for key in self.REQUIRED_EVIDENCE if inputs.get(key) is None)
        inputs_ref = digest(inputs)
        if missing:
            return self._decision("indeterminate", "missing_required_evidence", inputs_ref, {"missing": missing})

        identity = inputs["identity"]
        authority = inputs["authority"]
        agreement = inputs["agreement"]
        relationship = inputs["relationship"]

        if identity.get("authenticated") is not True:
            return self._decision("deny", "identity_not_authenticated", inputs_ref)
        if authority.get("active") is not True:
            return self._decision("deny", "authority_inactive_or_missing", inputs_ref)
        if authority.get("relationship_id") != relationship["relationship_id"]:
            return self._decision("deny", "authority_wrong_relationship", inputs_ref)
        if inputs["purpose"] not in authority.get("purposes", []):
            return self._decision("deny", "authority_purpose_out_of_scope", inputs_ref)
        if inputs["resource"] not in authority.get("resources", []):
            return self._decision("deny", "authority_resource_out_of_scope", inputs_ref)
        if inputs["action"] not in authority.get("actions", []):
            return self._decision("deny", "authority_action_out_of_scope", inputs_ref)
        if agreement.get("status") != "active":
            return self._decision("deny", "agreement_not_active", inputs_ref)
        if agreement["agreement_ref"] != inputs.get("agreement_ref"):
            return self._decision("deny", "agreement_reference_mismatch", inputs_ref)
        terms = agreement["terms"]
        if inputs["purpose"] != terms.get("purpose"):
            return self._decision("deny", "agreement_purpose_mismatch", inputs_ref)
        if inputs["resource"] not in terms.get("resources", []):
            return self._decision("deny", "agreement_resource_mismatch", inputs_ref)
        if inputs["action"] not in terms.get("actions", []):
            return self._decision("deny", "agreement_action_mismatch", inputs_ref)
        if inputs["recipient"] not in terms.get("recipients", []):
            return self._decision("deny", "agreement_recipient_mismatch", inputs_ref)
        if inputs["task_id"] != SUPPORTED_TASK:
            return self._decision("deny", "unsupported_task_version", inputs_ref)
        if relationship.get("status") != "active":
            return self._decision("deny", "relationship_not_active", inputs_ref)
        if inputs["role_record_head"] != relationship.get("current_head"):
            return self._decision("deny", "stale_role_record_head", inputs_ref)
        if inputs.get("instance_policy") == "deny":
            return self._decision("deny", "instance_policy_denied", inputs_ref)
        if inputs.get("instance_policy") == "escalate":
            return self._decision("escalate", "human_review_required", inputs_ref)
        return self._decision("allow", "all_required_conditions_satisfied", inputs_ref)

    def _decision(self, decision: str, code: str, inputs_ref: str, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        if decision not in DECISIONS:
            raise ValueError("invalid_decision")
        material = {"decision": decision, "code": code, "inputs_ref": inputs_ref, "extra": extra or {}}
        return Decision(decision, code, digest(material), inputs_ref).as_dict() | (extra or {})


class CapabilityService:
    """Least-privilege technical means derived only from an allow decision."""

    def __init__(self) -> None:
        self._caps: dict[str, dict[str, Any]] = {}

    def issue(
        self,
        *,
        decision: dict[str, Any],
        relationship_id: str,
        agreement_ref: str,
        recipient: str,
        purpose: str,
        resource: str,
        action: str,
        expires_at: int,
    ) -> dict[str, Any]:
        if decision.get("decision") != "allow":
            return {"result": "refused", "code": "capability_requires_allow_decision", "decision_ref": decision.get("decision_ref")}
        body = {
            "relationship_id": relationship_id,
            "agreement_ref": agreement_ref,
            "recipient": recipient,
            "purpose": purpose,
            "resource": resource,
            "action": action,
            "expires_at": expires_at,
            "decision_ref": decision["decision_ref"],
            "status": "active",
        }
        cap_ref = digest(body)
        cap = {**body, "capability_ref": cap_ref}
        self._caps[cap_ref] = cap
        return json.loads(canonical_json(cap))

    def get(self, capability_ref: str) -> dict[str, Any] | None:
        cap = self._caps.get(capability_ref)
        return None if cap is None else json.loads(canonical_json(cap))

    def set_status(self, capability_ref: str, status: str) -> dict[str, Any]:
        if status not in {"active", "suspended", "revoked"}:
            raise ValueError("invalid_capability_status")
        if capability_ref not in self._caps:
            raise KeyError("capability_missing")
        self._caps[capability_ref]["status"] = status
        return self.get(capability_ref) or {}

    def attenuate(self, capability_ref: str, *, expires_at: int) -> dict[str, Any]:
        parent = self._caps[capability_ref]
        if expires_at > parent["expires_at"]:
            return {"result": "refused", "code": "attenuation_cannot_expand_expiry"}
        body = {k: v for k, v in parent.items() if k != "capability_ref"}
        body["expires_at"] = expires_at
        body["parent_capability_ref"] = capability_ref
        cap_ref = digest(body)
        cap = {**body, "capability_ref": cap_ref}
        self._caps[cap_ref] = cap
        return json.loads(canonical_json(cap))


class TrustTaskBuilder:
    def build(
        self,
        *,
        relationship_id: str,
        agreement_ref: str,
        role_record_head: str,
        authority_ref: str,
        decision_ref: str,
        capability_ref: str,
        recipient: str,
        purpose: str,
        resource: str,
        action: str,
        payload: dict[str, Any],
        nonce: str,
        issued_at: int,
        expires_at: int,
        evidence_requirements: list[str],
        task_id: str = SUPPORTED_TASK,
    ) -> dict[str, Any]:
        task = {
            "task_id": task_id,
            "relationship_id": relationship_id,
            "agreement_ref": agreement_ref,
            "role_record_head": role_record_head,
            "authority_ref": authority_ref,
            "decision_ref": decision_ref,
            "capability_ref": capability_ref,
            "recipient": recipient,
            "purpose": purpose,
            "resource": resource,
            "action": action,
            "payload_digest": digest(payload),
            "nonce": nonce,
            "issued_at": issued_at,
            "expires_at": expires_at,
            "evidence_requirements": list(evidence_requirements),
        }
        return {**task, "task_ref": digest(task)}


class ExecutionAdmitter:
    """Final local admission boundary. Evidence and assurance are never authority inputs."""

    def __init__(self) -> None:
        self._used_nonces: set[str] = set()

    def admit(
        self,
        *,
        task: dict[str, Any],
        decision: dict[str, Any],
        capability: dict[str, Any] | None,
        authority: dict[str, Any],
        agreement: dict[str, Any],
        current_role_record_head: str,
        now: int,
    ) -> dict[str, Any]:
        base = {
            "task_ref": task.get("task_ref"),
            "decision_ref": decision.get("decision_ref"),
            "capability_ref": None if capability is None else capability.get("capability_ref"),
        }

        def refuse(code: str) -> dict[str, Any]:
            material = {**base, "result": "refused", "code": code}
            return {**material, "receipt_ref": digest(material)}

        if decision.get("decision") != "allow":
            return refuse("decision_not_allow")
        if task.get("decision_ref") != decision.get("decision_ref"):
            return refuse("task_decision_mismatch")
        if capability is None:
            return refuse("capability_missing")
        if capability.get("status") != "active":
            return refuse("capability_not_active")
        if authority.get("active") is not True:
            return refuse("authority_revoked_or_inactive")
        if agreement.get("status") != "active":
            return refuse("agreement_not_active")
        if task.get("task_id") != SUPPORTED_TASK:
            return refuse("unsupported_task_version")
        if task.get("role_record_head") != current_role_record_head:
            return refuse("stale_role_record_head")
        if task.get("relationship_id") != capability.get("relationship_id"):
            return refuse("capability_wrong_relationship")
        if task.get("agreement_ref") != capability.get("agreement_ref") or task.get("agreement_ref") != agreement.get("agreement_ref"):
            return refuse("capability_wrong_agreement")
        for key in ("recipient", "purpose", "resource", "action"):
            if task.get(key) != capability.get(key):
                return refuse(f"capability_{key}_mismatch")
        if now >= int(task.get("expires_at", 0)):
            return refuse("task_expired")
        if now >= int(capability.get("expires_at", 0)):
            return refuse("capability_expired")
        nonce = task.get("nonce")
        if nonce in self._used_nonces:
            return refuse("task_replay")
        self._used_nonces.add(str(nonce))
        effect = {
            "relationship_id": task["relationship_id"],
            "agreement_ref": task["agreement_ref"],
            "resource": task["resource"],
            "action": task["action"],
            "payload_digest": task["payload_digest"],
            "task_ref": task["task_ref"],
            "decision_ref": decision["decision_ref"],
            "capability_ref": capability["capability_ref"],
        }
        effect_ref = digest(effect)
        receipt = {**base, "result": "admitted", "code": "admitted", "effect_ref": effect_ref}
        return {**receipt, "receipt_ref": digest(receipt)}

    @staticmethod
    def validate_effect_correlation(*, receipt: dict[str, Any], observed_effect: dict[str, Any]) -> dict[str, Any]:
        expected = receipt.get("effect_ref")
        observed = digest(observed_effect)
        if expected != observed:
            return {"valid": False, "code": "effect_not_correlated_to_admission", "expected": expected, "observed": observed}
        return {"valid": True, "code": "effect_correlated", "effect_ref": observed}
