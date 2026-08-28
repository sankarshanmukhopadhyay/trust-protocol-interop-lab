from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

VISIBILITY_CLASSES = {"private", "shared", "pointer", "commitment"}
AUTHORIZED_WORKFLOWS = {
    "wf.relationship-bootstrap/1.0": {"relationship.create"},
    "wf.relationship-state/1.0": {
        "relationship.note",
        "relationship.evidence",
        "relationship.correction",
        "relationship.continue",
    },
}
FIXED_TIME_BASE = "2026-08-28T06:30:"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def timestamp_for(sequence: int) -> str:
    return f"{FIXED_TIME_BASE}{sequence:02d}Z"


@dataclass(frozen=True)
class Receipt:
    transition_id: str
    agent_role_id: str
    relationship_id: str
    actor_id: str
    workflow_id: str
    transition_class: str
    prior_head: str | None
    resulting_head: str | None
    sequence: int
    timestamp: str
    result: str
    code: str

    def as_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


class RoleRecordStore:
    """Lab-local append-only state chain for one persistent Agent Role."""

    def __init__(self, path: Path, agent_role_id: str):
        self.path = path
        self.agent_role_id = agent_role_id
        if path.exists():
            self.data = json.loads(path.read_text(encoding="utf-8"))
            if self.data.get("agent_role_id") != agent_role_id:
                raise ValueError("agent_role_id mismatch")
        else:
            self.data = {"version": 1, "agent_role_id": agent_role_id, "relationships": {}, "receipts": []}
            self._persist()

    def _persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(canonical_json(self.data) + "\n", encoding="utf-8")

    def _branch(self, relationship_id: str) -> dict[str, Any] | None:
        return self.data["relationships"].get(relationship_id)

    def current_head(self, relationship_id: str) -> str | None:
        branch = self._branch(relationship_id)
        return None if branch is None else branch["current_head"]

    def current_state(self, relationship_id: str) -> dict[str, Any]:
        branch = self._branch(relationship_id)
        if branch is None:
            return {}
        state: dict[str, Any] = {}
        for event in branch["events"]:
            payload = event.get("payload", {})
            state.update(payload.get("set", {}))
            for key in payload.get("delete", []):
                state.pop(key, None)
        return state

    def _receipt(self, **kwargs: Any) -> dict[str, Any]:
        receipt = Receipt(**kwargs).as_dict()
        self.data["receipts"].append(receipt)
        self._persist()
        return receipt

    def _refuse(
        self,
        *,
        transition_id: str,
        relationship_id: str,
        actor_id: str,
        workflow_id: str,
        transition_class: str,
        previous_head: str | None,
        current_head: str | None,
        sequence: int,
        code: str,
    ) -> dict[str, Any]:
        return self._receipt(
            transition_id=transition_id,
            agent_role_id=self.agent_role_id,
            relationship_id=relationship_id,
            actor_id=actor_id,
            workflow_id=workflow_id,
            transition_class=transition_class,
            prior_head=previous_head,
            resulting_head=current_head,
            sequence=sequence,
            timestamp=timestamp_for(sequence),
            result="refused",
            code=code,
        )

    def apply(
        self,
        *,
        transition_id: str,
        relationship_id: str,
        actor_id: str,
        workflow_id: str,
        transition_class: str,
        previous_head: str | None,
        visibility: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        branch = self._branch(relationship_id)
        sequence = 1 if branch is None else len(branch["events"]) + 1
        current_head = None if branch is None else branch["current_head"]

        common = dict(
            transition_id=transition_id,
            relationship_id=relationship_id,
            actor_id=actor_id,
            workflow_id=workflow_id,
            transition_class=transition_class,
            previous_head=previous_head,
            current_head=current_head,
            sequence=sequence,
        )

        if visibility not in VISIBILITY_CLASSES:
            return self._refuse(**common, code="invalid_visibility_class")
        if transition_class not in AUTHORIZED_WORKFLOWS.get(workflow_id, set()):
            return self._refuse(**common, code="unauthorized_updater")

        accepted_ids = {
            event["transition_id"]
            for rel in self.data["relationships"].values()
            for event in rel["events"]
        }
        if transition_id in accepted_ids:
            return self._refuse(**common, code="replay_transition")

        if transition_class == "relationship.create":
            if branch is not None:
                return self._refuse(**common, code="relationship_already_exists")
            if previous_head is not None:
                return self._refuse(**common, code="genesis_previous_head_must_be_null")
        else:
            if branch is None:
                return self._refuse(**common, code="relationship_missing")
            if previous_head is None:
                return self._refuse(**common, code="missing_previous_head")
            if previous_head != current_head:
                known_heads = [event["head"] for event in branch["events"]]
                if previous_head in known_heads:
                    code = "competing_successor_head" if payload.get("fork_candidate") else "rollback_or_stale_head"
                else:
                    code = "unknown_previous_head"
                return self._refuse(**common, code=code)

        persisted_state = {} if branch is None else self.current_state(relationship_id)
        missing = [key for key in payload.get("requires_persisted", []) if key not in persisted_state]
        if missing:
            return self._refuse(**common, code="missing_persisted_context")

        if payload.get("delete") and transition_class != "relationship.correction":
            return self._refuse(**common, code="destructive_update_class_forbidden")

        event_without_hash = {
            "sequence": sequence,
            "timestamp": timestamp_for(sequence),
            "transition_id": transition_id,
            "agent_role_id": self.agent_role_id,
            "relationship_id": relationship_id,
            "actor_id": actor_id,
            "workflow_id": workflow_id,
            "transition_class": transition_class,
            "previous_head": previous_head,
            "visibility": visibility,
            "payload": payload,
        }
        head = digest(event_without_hash)
        event = {**event_without_hash, "head": head}

        if branch is None:
            self.data["relationships"][relationship_id] = {
                "relationship_id": relationship_id,
                "current_head": head,
                "events": [event],
            }
        else:
            branch["events"].append(event)
            branch["current_head"] = head
        self._persist()

        return self._receipt(
            transition_id=transition_id,
            agent_role_id=self.agent_role_id,
            relationship_id=relationship_id,
            actor_id=actor_id,
            workflow_id=workflow_id,
            transition_class=transition_class,
            prior_head=previous_head,
            resulting_head=head,
            sequence=sequence,
            timestamp=timestamp_for(sequence),
            result="accepted",
            code="accepted",
        )

    def validate_history(self, relationship_id: str) -> dict[str, Any]:
        branch = self._branch(relationship_id)
        if branch is None:
            return {"valid": False, "code": "relationship_missing"}
        prior = None
        for index, event in enumerate(branch["events"], start=1):
            candidate = {key: value for key, value in event.items() if key != "head"}
            if digest(candidate) != event["head"]:
                return {"valid": False, "code": "historical_event_hash_mismatch", "sequence": index}
            if event["previous_head"] != prior:
                return {"valid": False, "code": "historical_previous_head_mismatch", "sequence": index}
            prior = event["head"]
        if branch["current_head"] != prior:
            return {"valid": False, "code": "current_head_mismatch"}
        return {"valid": True, "code": "valid", "events": len(branch["events"]), "head": prior}
