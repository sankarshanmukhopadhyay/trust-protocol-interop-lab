from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class LifecycleCoordinator:
    """Lab-local lifecycle guard over existing ARA components.

    It does not own Role Record, Agreement, Capability, or VRR state. It only
    enforces lifecycle preconditions that span those already-owned components.
    """

    def __init__(self, *, required_resume_keys: set[str] | None = None) -> None:
        self.required_resume_keys = required_resume_keys or {
            "purpose",
            "status",
            "agreement_ref",
            "authority_ref",
        }

    def reconstruct_for_replacement(self, *, role_store: Any, relationship_id: str) -> dict[str, Any]:
        state = role_store.current_state(relationship_id)
        missing = sorted(k for k in self.required_resume_keys if state.get(k) is None)
        if missing:
            return {
                "result": "refused",
                "code": "replacement_missing_persisted_context",
                "missing": missing,
                "relationship_id": relationship_id,
            }
        if state.get("status") == "closed":
            return {
                "result": "refused",
                "code": "relationship_closed",
                "relationship_id": relationship_id,
            }
        if state.get("suspect_since") and not state.get("suspect_interval_reviewed"):
            return {
                "result": "refused",
                "code": "suspect_interval_unreviewed",
                "relationship_id": relationship_id,
                "suspect_since": state.get("suspect_since"),
            }
        return {
            "result": "reconstructed",
            "code": "persisted_context_sufficient",
            "relationship_id": relationship_id,
            "state": json.loads(json.dumps(state, sort_keys=True)),
            "current_head": role_store.current_head(relationship_id),
        }

    def resume_after_remediation(self, *, role_store: Any, relationship_id: str) -> dict[str, Any]:
        state = role_store.current_state(relationship_id)
        if state.get("status") == "closed":
            return {"result": "refused", "code": "relationship_closed"}
        if state.get("suspect_since") and not state.get("suspect_interval_reviewed"):
            return {"result": "refused", "code": "suspect_interval_unreviewed"}
        if state.get("status") not in {"active", "remediated"}:
            return {"result": "refused", "code": "relationship_not_resumable"}
        return {
            "result": "allowed",
            "code": "continuation_context_valid",
            "current_head": role_store.current_head(relationship_id),
        }

    @staticmethod
    def historical_action_status(*, action_receipt: dict[str, Any], later_authority_active: bool) -> dict[str, Any]:
        if action_receipt.get("result") != "admitted":
            return {"historically_valid": False, "code": "original_action_not_admitted"}
        return {
            "historically_valid": True,
            "code": "historical_validity_preserved",
            "current_authority_active": later_authority_active,
            "action_receipt_ref": action_receipt.get("receipt_ref"),
        }

    @staticmethod
    def surviving_obligations(*, obligations: list[dict[str, Any]], closed_agreement_ref: str) -> dict[str, Any]:
        surviving = []
        terminated = []
        for obligation in obligations:
            if obligation.get("agreement_ref") == closed_agreement_ref and obligation.get("termination") == "agreement_close":
                terminated.append(obligation)
            else:
                surviving.append(obligation)
        return {"surviving": surviving, "terminated": terminated}
