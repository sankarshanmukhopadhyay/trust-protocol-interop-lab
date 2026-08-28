from __future__ import annotations

import hashlib
import json
from typing import Any

EVIDENCE_CLASSES = {"shared_object", "source_pointer", "opaque_commitment", "private_role_evidence"}
RECEIPT_STAGES = {"sent", "delivered", "resolved", "decrypted", "inspected", "acknowledged"}
DISPOSITIONS = {"accepted", "disputed", "rejected", "accepted_as_evidence_only"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class DistributedVRR:
    """Lab-local distributed relationship evidence model with no shared mutable master record."""

    def __init__(self, relationship_id: str, party_set_epoch: int, parties: list[str]) -> None:
        self.relationship_id = relationship_id
        self.party_set_epoch = party_set_epoch
        self.parties = tuple(sorted(parties))
        self._objects: dict[str, dict[str, Any]] = {}
        self._receipts: list[dict[str, Any]] = []
        self._dispositions: list[dict[str, Any]] = []
        self._corrections: list[dict[str, Any]] = []

    def add_object(
        self,
        *,
        owner_role: str,
        evidence_class: str,
        content: Any | None = None,
        pointer: str | None = None,
        commitment: str | None = None,
        label: str,
    ) -> dict[str, Any]:
        if owner_role not in self.parties:
            raise ValueError("owner_not_in_party_set")
        if evidence_class not in EVIDENCE_CLASSES:
            raise ValueError("unsupported_evidence_class")
        if evidence_class == "shared_object" and content is None:
            raise ValueError("shared_object_requires_content")
        if evidence_class == "source_pointer" and pointer is None:
            raise ValueError("source_pointer_requires_pointer")
        if evidence_class == "opaque_commitment" and commitment is None:
            raise ValueError("opaque_commitment_requires_commitment")
        if evidence_class == "private_role_evidence" and content is None:
            raise ValueError("private_evidence_requires_content")

        content_id = digest(content) if content is not None else commitment or digest({"pointer": pointer})
        obj = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "owner_role": owner_role,
            "evidence_class": evidence_class,
            "label": label,
            "content_id": content_id,
            "pointer": pointer,
            "commitment": commitment,
        }
        if evidence_class in {"shared_object", "private_role_evidence"}:
            obj["content"] = json.loads(canonical_json(content))
        object_ref = digest(obj)
        stored = {**obj, "object_ref": object_ref}
        self._objects[object_ref] = stored
        return json.loads(canonical_json(stored))

    def receipt(self, *, actor_role: str, object_ref: str, stage: str, observed_content_id: str | None = None) -> dict[str, Any]:
        if actor_role not in self.parties:
            raise ValueError("actor_not_in_party_set")
        if object_ref not in self._objects:
            raise KeyError("object_missing")
        if stage not in RECEIPT_STAGES:
            raise ValueError("unsupported_receipt_stage")
        obj = self._objects[object_ref]
        if stage == "inspected":
            if observed_content_id is None:
                raise ValueError("inspection_requires_digest")
            if observed_content_id != obj["content_id"]:
                return self._refusal(actor_role, object_ref, "inspection_digest_mismatch")
            if obj["evidence_class"] == "opaque_commitment":
                return self._refusal(actor_role, object_ref, "opaque_content_not_inspectable")
            if obj["evidence_class"] == "private_role_evidence":
                return self._refusal(actor_role, object_ref, "private_object_not_shared")
        material = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "actor_role": actor_role,
            "object_ref": object_ref,
            "stage": stage,
            "observed_content_id": observed_content_id,
            "sequence": len(self._receipts) + 1,
        }
        record = {**material, "receipt_ref": digest(material)}
        self._receipts.append(record)
        return json.loads(canonical_json(record))

    def dispose(self, *, actor_role: str, object_ref: str, disposition: str, basis_receipt_ref: str | None = None, note: str | None = None) -> dict[str, Any]:
        if actor_role not in self.parties:
            raise ValueError("actor_not_in_party_set")
        if object_ref not in self._objects:
            raise KeyError("object_missing")
        if disposition not in DISPOSITIONS:
            raise ValueError("unsupported_disposition")
        if basis_receipt_ref is not None and not any(r["receipt_ref"] == basis_receipt_ref for r in self._receipts):
            return self._refusal(actor_role, object_ref, "basis_receipt_missing")
        material = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "actor_role": actor_role,
            "object_ref": object_ref,
            "disposition": disposition,
            "basis_receipt_ref": basis_receipt_ref,
            "note": note,
            "sequence": len(self._dispositions) + 1,
        }
        record = {**material, "disposition_ref": digest(material)}
        self._dispositions.append(record)
        return json.loads(canonical_json(record))

    def correct(self, *, actor_role: str, target_ref: str, correction: str) -> dict[str, Any]:
        if actor_role not in self.parties:
            raise ValueError("actor_not_in_party_set")
        known = {d["disposition_ref"] for d in self._dispositions} | {r["receipt_ref"] for r in self._receipts}
        if target_ref not in known:
            return {"result": "refused", "code": "correction_target_missing"}
        material = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "actor_role": actor_role,
            "target_ref": target_ref,
            "correction": correction,
            "sequence": len(self._corrections) + 1,
        }
        record = {**material, "correction_ref": digest(material)}
        self._corrections.append(record)
        return json.loads(canonical_json(record))

    def checkpoint(self, *, role_record_heads: dict[str, str]) -> dict[str, Any]:
        if set(role_record_heads) != set(self.parties):
            return {"result": "refused", "code": "checkpoint_missing_party_head"}
        shared_objects = [
            o for o in self._objects.values()
            if o["evidence_class"] != "private_role_evidence"
        ]
        material = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "parties": list(self.parties),
            "role_record_heads": dict(sorted(role_record_heads.items())),
            "shared_object_refs": sorted(o["object_ref"] for o in shared_objects),
            "receipt_refs": sorted(r["receipt_ref"] for r in self._receipts),
            "disposition_refs": sorted(d["disposition_ref"] for d in self._dispositions),
            "correction_refs": sorted(c["correction_ref"] for c in self._corrections),
        }
        return {**material, "checkpoint_ref": digest(material)}

    def export_selective(self, *, object_refs: list[str]) -> dict[str, Any]:
        exported = []
        for ref in object_refs:
            obj = self._objects.get(ref)
            if obj is None:
                raise KeyError("object_missing")
            if obj["evidence_class"] == "private_role_evidence":
                return {"result": "refused", "code": "private_object_export_forbidden", "object_ref": ref}
            exported.append(json.loads(canonical_json(obj)))
        relevant_receipts = [r for r in self._receipts if r["object_ref"] in object_refs]
        relevant_dispositions = [d for d in self._dispositions if d["object_ref"] in object_refs]
        return {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "objects": exported,
            "receipts": json.loads(canonical_json(relevant_receipts)),
            "dispositions": json.loads(canonical_json(relevant_dispositions)),
        }

    def mutual_state(self, object_ref: str) -> dict[str, Any]:
        dispositions = [d for d in self._dispositions if d["object_ref"] == object_ref]
        by_actor: dict[str, str] = {}
        for d in dispositions:
            by_actor[d["actor_role"]] = d["disposition"]
        if set(by_actor) != set(self.parties):
            return {"status": "not_mutual", "code": "missing_party_disposition", "by_actor": by_actor}
        if len(set(by_actor.values())) != 1:
            return {"status": "disputed", "code": "party_dispositions_differ", "by_actor": by_actor}
        disposition = next(iter(by_actor.values()))
        return {"status": "mutual", "disposition": disposition, "by_actor": by_actor}

    def traverse(self, *, requester_role: str, object_ref: str) -> dict[str, Any]:
        obj = self._objects.get(object_ref)
        if obj is None:
            return {"result": "refused", "code": "object_missing"}
        if obj["evidence_class"] == "source_pointer":
            return {"result": "refused", "code": "link_not_traversal_authority", "pointer": obj["pointer"]}
        return {"result": "refused", "code": "no_automatic_traversal"}

    def _refusal(self, actor_role: str, object_ref: str, code: str) -> dict[str, Any]:
        material = {
            "relationship_id": self.relationship_id,
            "party_set_epoch": self.party_set_epoch,
            "actor_role": actor_role,
            "object_ref": object_ref,
            "result": "refused",
            "code": code,
        }
        return {**material, "receipt_ref": digest(material)}
