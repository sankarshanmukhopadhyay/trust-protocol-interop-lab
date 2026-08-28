#!/usr/bin/env python3
"""Executable evidence for IC-ARA-REL-001 Phase 3 Role Record semantics.

This is deliberately a Lab-local state mechanism. It proves bounded ARA state semantics:
append-only transition hashing, current-head binding, stale/rollback/fork detection,
authorized updater classes, explicit evidence visibility classes, deterministic receipts,
and Live Agent replacement from persisted state only.

It does NOT claim KERI, BetterSign, VTA, transparency-log, HSM, TEE, or production
anti-rollback conformance.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ZERO_HEAD = None
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
        return {
            "transition_id": self.transition_id,
            "agent_role_id": self.agent_role_id,
            "relationship_id": self.relationship_id,
            "actor_id": self.actor_id,
            "workflow_id": self.workflow_id,
            "transition_class": self.transition_class,
            "prior_head": self.prior_head,
            "resulting_head": self.resulting_head,
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "result": self.result,
            "code": self.code,
        }


class RoleRecordStore:
    def __init__(self, path: Path, agent_role_id: str):
        self.path = path
        self.agent_role_id = agent_role_id
        if self.path.exists():
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
            if self.data["agent_role_id"] != agent_role_id:
                raise ValueError("agent role mismatch")
        else:
            self.data = {
                "version": 1,
                "agent_role_id": agent_role_id,
                "relationships": {},
                "receipts": [],
            }
            self._persist()

    def _persist(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(canonical_json(self.data) + "\n", encoding="utf-8")

    def _branch(self, relationship_id: str) -> dict[str, Any] | None:
        return self.data["relationships"].get(relationship_id)

    def _next_sequence(self, branch: dict[str, Any] | None) -> int:
        return 1 if branch is None else len(branch["events"]) + 1

    def _receipt(
        self,
        *,
        transition_id: str,
        relationship_id: str,
        actor_id: str,
        workflow_id: str,
        transition_class: str,
        prior_head: str | None,
        resulting_head: str | None,
        sequence: int,
        result: str,
        code: str,
    ) -> dict[str, Any]:
        receipt = Receipt(
            transition_id=transition_id,
            agent_role_id=self.agent_role_id,
            relationship_id=relationship_id,
            actor_id=actor_id,
            workflow_id=workflow_id,
            transition_class=transition_class,
            prior_head=prior_head,
            resulting_head=resulting_head,
            sequence=sequence,
            timestamp=timestamp_for(sequence),
            result=result,
            code=code,
        ).as_dict()
        self.data["receipts"].append(receipt)
        self._persist()
        return receipt

    def _authorized(self, workflow_id: str, transition_class: str) -> bool:
        return transition_class in AUTHORIZED_WORKFLOWS.get(workflow_id, set())

    def _event_hash(self, event_without_hash: dict[str, Any]) -> str:
        return digest(event_without_hash)

    def _state_from_events(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        state: dict[str, Any] = {}
        for event in events:
            payload = event.get("payload", {})
            for key, value in payload.get("set", {}).items():
                state[key] = value
            for key in payload.get("delete", []):
                state.pop(key, None)
        return state

    def current_head(self, relationship_id: str) -> str | None:
        branch = self._branch(relationship_id)
        return None if branch is None else branch["current_head"]

    def current_state(self, relationship_id: str) -> dict[str, Any]:
        branch = self._branch(relationship_id)
        if branch is None:
            return {}
        return self._state_from_events(branch["events"])

    def history(self, relationship_id: str) -> list[dict[str, Any]]:
        branch = self._branch(relationship_id)
        return [] if branch is None else copy.deepcopy(branch["events"])

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
        sequence = self._next_sequence(branch)
        current_head = None if branch is None else branch["current_head"]

        if visibility not in VISIBILITY_CLASSES:
            return self._receipt(
                transition_id=transition_id,
                relationship_id=relationship_id,
                actor_id=actor_id,
                workflow_id=workflow_id,
                transition_class=transition_class,
                prior_head=previous_head,
                resulting_head=current_head,
                sequence=sequence,
                result="refused",
                code="invalid_visibility_class",
            )

        if not self._authorized(workflow_id, transition_class):
            return self._receipt(
                transition_id=transition_id,
                relationship_id=relationship_id,
                actor_id=actor_id,
                workflow_id=workflow_id,
                transition_class=transition_class,
                prior_head=previous_head,
                resulting_head=current_head,
                sequence=sequence,
                result="refused",
                code="unauthorized_updater",
            )

        accepted_ids = {
            event["transition_id"]
            for rel in self.data["relationships"].values()
            for event in rel["events"]
        }
        if transition_id in accepted_ids:
            return self._receipt(
                transition_id=transition_id,
                relationship_id=relationship_id,
                actor_id=actor_id,
                workflow_id=workflow_id,
                transition_class=transition_class,
                prior_head=previous_head,
                resulting_head=current_head,
                sequence=sequence,
                result="refused",
                code="replay_transition",
            )

        if transition_class == "relationship.create":
            if branch is not None:
                return self._receipt(
                    transition_id=transition_id,
                    relationship_id=relationship_id,
                    actor_id=actor_id,
                    workflow_id=workflow_id,
                    transition_class=transition_class,
                    prior_head=previous_head,
                    resulting_head=current_head,
                    sequence=sequence,
                    result="refused",
                    code="relationship_already_exists",
                )
            if previous_head is not None:
                return self._receipt(
                    transition_id=transition_id,
                    relationship_id=relationship_id,
                    actor_id=actor_id,
                    workflow_id=workflow_id,
                    transition_class=transition_class,
                    prior_head=previous_head,
                    resulting_head=current_head,
                    sequence=sequence,
                    result="refused",
                    code="genesis_previous_head_must_be_null",
                )
        else:
            if branch is None:
                return self._receipt(
                    transition_id=transition_id,
                    relationship_id=relationship_id,
                    actor_id=actor_id,
                    workflow_id=workflow_id,
                    transition_class=transition_class,
                    prior_head=previous_head,
                    resulting_head=None,
                    sequence=sequence,
                    result="refused",
                    code="relationship_missing",
                )
            if previous_head is None:
                return self._receipt(
                    transition_id=transition_id,
                    relationship_id=relationship_id,
                    actor_id=actor_id,
                    workflow_id=workflow_id,
                    transition_class=transition_class,
                    prior_head=None,
                    resulting_head=current_head,
                    sequence=sequence,
                    result="refused",
                    code="missing_previous_head",
                )
            if previous_head != current_head:
                known_heads = [event["head"] for event in branch["events"]]
                if previous_head in branch.get("accepted_successor_by_head", {}):
                    code = "competing_successor_head"
                elif previous_head in known_heads:
                    code = "rollback_or_stale_head"
                else:
                    code = "unknown_previous_head"
                return self._receipt(
                    transition_id=transition_id,
                    relationship_id=relationship_id,
                    actor_id=actor_id,
                    workflow_id=workflow_id,
                    transition_class=transition_class,
                    prior_head=previous_head,
                    resulting_head=current_head,
                    sequence=sequence,
                    result="refused",
                    code=code,
                )

        persisted_state = {} if branch is None else self._state_from_events(branch["events"])
        required_state = payload.get("requires_persisted", [])
        missing = [key for key in required_state if key not in persisted_state]
        if missing:
            return self._receipt(
                transition_id=transition_id,
                relationship_id=relationship_id,
                actor_id=actor_id,
                workflow_id=workflow_id,
                transition_class=transition_class,
                prior_head=previous_head,
                resulting_head=current_head,
                sequence=sequence,
                result="refused",
                code="missing_persisted_context",
            )

        if payload.get("delete") and transition_class != "relationship.correction":
            return self._receipt(
                transition_id=transition_id,
                relationship_id=relationship_id,
                actor_id=actor_id,
                workflow_id=workflow_id,
                transition_class=transition_class,
                prior_head=previous_head,
                resulting_head=current_head,
                sequence=sequence,
                result="refused",
                code="destructive_update_class_forbidden",
            )

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
        head = self._event_hash(event_without_hash)
        event = {**event_without_hash, "head": head}

        if branch is None:
            branch = {
                "relationship_id": relationship_id,
                "current_head": head,
                "events": [event],
                "accepted_successor_by_head": {},
            }
            self.data["relationships"][relationship_id] = branch
        else:
            branch["accepted_successor_by_head"][previous_head] = head
            branch["events"].append(event)
            branch["current_head"] = head

        self._persist()
        return self._receipt(
            transition_id=transition_id,
            relationship_id=relationship_id,
            actor_id=actor_id,
            workflow_id=workflow_id,
            transition_class=transition_class,
            prior_head=previous_head,
            resulting_head=head,
            sequence=sequence,
            result="accepted",
            code="accepted",
        )

    def validate_history(self, relationship_id: str) -> dict[str, Any]:
        branch = self._branch(relationship_id)
        if branch is None:
            return {"valid": False, "code": "relationship_missing"}
        prior = None
        observed_successors: dict[str, str] = {}
        for index, event in enumerate(branch["events"], start=1):
            candidate = {key: value for key, value in event.items() if key != "head"}
            if event["head"] != self._event_hash(candidate):
                return {"valid": False, "code": "historical_event_hash_mismatch", "sequence": index}
            if event["previous_head"] != prior:
                return {"valid": False, "code": "historical_previous_head_mismatch", "sequence": index}
            if prior is not None:
                existing = observed_successors.get(prior)
                if existing is not None and existing != event["head"]:
                    return {"valid": False, "code": "historical_equivocation", "sequence": index}
                observed_successors[prior] = event["head"]
            prior = event["head"]
        if branch["current_head"] != prior:
            return {"valid": False, "code": "current_head_mismatch"}
        return {"valid": True, "code": "valid", "head": prior, "events": len(branch["events"])}


def accepted(receipt: dict[str, Any]) -> bool:
    return receipt["result"] == "accepted"


def run_vectors() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="ara-role-record-") as temp:
        path = Path(temp) / "role-record.json"
        role_id = "urn:ara:agent-role:data-owner:001"
        rel_id = "urn:ara:relationship:research:001"
        actor = "controller:data-owner"
        bootstrap = "wf.relationship-bootstrap/1.0"
        state_wf = "wf.relationship-state/1.0"

        store = RoleRecordStore(path, role_id)
        results: list[dict[str, Any]] = []

        def record(vector_id: str, expected: str, receipt: dict[str, Any]) -> None:
            outcome = receipt["code"]
            ok = outcome == expected
            results.append({
                "vector_id": vector_id,
                "expected": expected,
                "observed": outcome,
                "pass": ok,
                "receipt": receipt,
            })
            if not ok:
                raise AssertionError(f"{vector_id}: expected {expected}, observed {outcome}")

        r1 = store.apply(
            transition_id="tr-001",
            relationship_id=rel_id,
            actor_id=actor,
            workflow_id=bootstrap,
            transition_class="relationship.create",
            previous_head=None,
            visibility="private",
            payload={"set": {"purpose": "synthetic-research-query", "continuity_token": "ct-001"}},
        )
        record("RR-P01-create", "accepted", r1)
        head1 = r1["resulting_head"]

        r2 = store.apply(
            transition_id="tr-002",
            relationship_id=rel_id,
            actor_id=actor,
            workflow_id=state_wf,
            transition_class="relationship.evidence",
            previous_head=head1,
            visibility="shared",
            payload={"set": {"dataset_ref": "sha256:synthetic-dataset"}},
        )
        record("RR-P02-advance", "accepted", r2)
        head2 = r2["resulting_head"]

        # Replacement Live Agent: construct a new engine from disk with no conversation/session state.
        replacement = RoleRecordStore(path, role_id)
        r3 = replacement.apply(
            transition_id="tr-003",
            relationship_id=rel_id,
            actor_id="controller:data-owner:replacement-live-agent-session",
            workflow_id=state_wf,
            transition_class="relationship.continue",
            previous_head=head2,
            visibility="private",
            payload={"requires_persisted": ["continuity_token", "dataset_ref"], "set": {"continued": True}},
        )
        record("RR-P03-live-agent-replacement", "accepted", r3)
        head3 = r3["resulting_head"]

        record(
            "RR-N01-unauthorized-updater",
            "unauthorized_updater",
            replacement.apply(
                transition_id="tr-004",
                relationship_id=rel_id,
                actor_id="live-agent:untrusted",
                workflow_id="live-agent-direct/0",
                transition_class="relationship.note",
                previous_head=head3,
                visibility="private",
                payload={"set": {"unsafe": True}},
            ),
        )

        record(
            "RR-N02-missing-previous-head",
            "missing_previous_head",
            replacement.apply(
                transition_id="tr-005",
                relationship_id=rel_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=None,
                visibility="private",
                payload={"set": {"note": "missing head"}},
            ),
        )

        record(
            "RR-N03-stale-or-rollback",
            "rollback_or_stale_head",
            replacement.apply(
                transition_id="tr-006",
                relationship_id=rel_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=head1,
                visibility="private",
                payload={"set": {"note": "rollback"}},
            ),
        )

        record(
            "RR-N04-replay",
            "replay_transition",
            replacement.apply(
                transition_id="tr-003",
                relationship_id=rel_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.continue",
                previous_head=head3,
                visibility="private",
                payload={"set": {"continued": True}},
            ),
        )

        record(
            "RR-N05-competing-successor",
            "competing_successor_head",
            replacement.apply(
                transition_id="tr-007",
                relationship_id=rel_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=head2,
                visibility="pointer",
                payload={"set": {"alternate": "branch"}},
            ),
        )

        record(
            "RR-N06-hidden-session-context",
            "missing_persisted_context",
            replacement.apply(
                transition_id="tr-008",
                relationship_id=rel_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.continue",
                previous_head=head3,
                visibility="private",
                payload={"requires_persisted": ["conversation_secret"], "set": {"continued": "unsafe"}},
            ),
        )

        correction = replacement.apply(
            transition_id="tr-009",
            relationship_id=rel_id,
            actor_id=actor,
            workflow_id=state_wf,
            transition_class="relationship.correction",
            previous_head=head3,
            visibility="commitment",
            payload={"set": {"correction_ref": "sha256:correction-001"}},
        )
        record("RR-P04-correction-appended", "accepted", correction)

        validation = replacement.validate_history(rel_id)
        if not validation["valid"]:
            raise AssertionError(f"history should validate: {validation}")
        results.append({"vector_id": "RR-P05-history-validation", "expected": "valid", "observed": validation["code"], "pass": True, "validation": validation})

        # Tamper with accepted history in memory only; validation must detect it.
        tampered = RoleRecordStore(path, role_id)
        tampered.data["relationships"][rel_id]["events"][1]["payload"]["set"]["dataset_ref"] = "sha256:mutated"
        tamper_validation = tampered.validate_history(rel_id)
        if tamper_validation["code"] != "historical_event_hash_mismatch":
            raise AssertionError(f"tamper not detected: {tamper_validation}")
        results.append({
            "vector_id": "RR-N07-history-mutation",
            "expected": "historical_event_hash_mismatch",
            "observed": tamper_validation["code"],
            "pass": True,
            "validation": tamper_validation,
        })

        # Deletion of an accepted event also breaks predecessor binding/current-head reconstruction.
        deleted = RoleRecordStore(path, role_id)
        del deleted.data["relationships"][rel_id]["events"][1]
        deletion_validation = deleted.validate_history(rel_id)
        if deletion_validation["valid"]:
            raise AssertionError("historical deletion was not detected")
        results.append({
            "vector_id": "RR-N08-history-deletion",
            "expected": "invalid-history",
            "observed": deletion_validation["code"],
            "pass": True,
            "validation": deletion_validation,
        })

        final_store = RoleRecordStore(path, role_id)
        final_validation = final_store.validate_history(rel_id)
        if not final_validation["valid"]:
            raise AssertionError("persisted untampered history invalid")

        return {
            "case_id": "IC-ARA-REL-001",
            "phase": "ARA-G3-ROLE-STATE-EXECUTABLE",
            "implementation": "lab-local-role-record-v0.1",
            "claim_boundary": {
                "demonstrates": [
                    "persistent Agent Role identifier independent of Live Agent process instance",
                    "append-only hash-linked local relationship transitions",
                    "canonical current head and previous-head binding",
                    "authorized transition classes",
                    "stale/rollback/replay/competing-successor refusal",
                    "private/shared/pointer/commitment classification",
                    "replacement continuation from persisted state only",
                    "history mutation/deletion detection",
                    "correction by append rather than overwrite",
                    "deterministic machine-readable transition receipts",
                ],
                "does_not_demonstrate": [
                    "KERI or BetterSign conformance",
                    "VTA protected-state conformance",
                    "transparency log guarantees",
                    "hardware-backed anti-rollback",
                    "distributed consensus or Byzantine fork resolution",
                    "production persistence security",
                ],
            },
            "summary": {
                "vectors": len(results),
                "passed": sum(1 for item in results if item["pass"]),
                "failed": sum(1 for item in results if not item["pass"]),
                "final_head": final_store.current_head(rel_id),
                "final_history_valid": final_validation["valid"],
            },
            "results": results,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail unless every required vector passes")
    parser.add_argument("--output", type=Path, help="optional file for deterministic JSON evidence")
    args = parser.parse_args()

    report = run_vectors()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")

    if args.check and report["summary"]["failed"] != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
