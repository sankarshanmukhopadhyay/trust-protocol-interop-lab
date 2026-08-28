#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path

from engine import RoleRecordStore


def run_vectors() -> dict:
    with tempfile.TemporaryDirectory(prefix="ara-role-record-") as temp:
        path = Path(temp) / "role-record.json"
        role_id = "urn:ara:agent-role:data-owner:001"
        relationship_id = "urn:ara:relationship:research:001"
        actor = "controller:data-owner"
        bootstrap = "wf.relationship-bootstrap/1.0"
        state_wf = "wf.relationship-state/1.0"
        store = RoleRecordStore(path, role_id)
        results = []

        def expect(vector_id: str, receipt: dict, expected: str) -> None:
            observed = receipt["code"]
            passed = observed == expected
            results.append({
                "vector_id": vector_id,
                "expected": expected,
                "observed": observed,
                "pass": passed,
                "receipt": receipt,
            })
            if not passed:
                raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")

        create = store.apply(
            transition_id="tr-001",
            relationship_id=relationship_id,
            actor_id=actor,
            workflow_id=bootstrap,
            transition_class="relationship.create",
            previous_head=None,
            visibility="private",
            payload={"set": {"purpose": "synthetic-research-query", "continuity_token": "ct-001"}},
        )
        expect("RR-P01-create", create, "accepted")
        head1 = create["resulting_head"]

        advance = store.apply(
            transition_id="tr-002",
            relationship_id=relationship_id,
            actor_id=actor,
            workflow_id=state_wf,
            transition_class="relationship.evidence",
            previous_head=head1,
            visibility="shared",
            payload={"set": {"dataset_ref": "sha256:synthetic-dataset"}},
        )
        expect("RR-P02-advance", advance, "accepted")
        head2 = advance["resulting_head"]

        # Destroy the in-memory engine and reconstruct only from persisted state.
        replacement = RoleRecordStore(path, role_id)
        continuation = replacement.apply(
            transition_id="tr-003",
            relationship_id=relationship_id,
            actor_id="controller:data-owner:replacement-session",
            workflow_id=state_wf,
            transition_class="relationship.continue",
            previous_head=head2,
            visibility="private",
            payload={
                "requires_persisted": ["continuity_token", "dataset_ref"],
                "set": {"replacement_live_agent_continued": True},
            },
        )
        expect("RR-P03-replacement-from-persisted-state", continuation, "accepted")
        head3 = continuation["resulting_head"]

        expect(
            "RR-N01-unauthorized-updater",
            replacement.apply(
                transition_id="tr-004",
                relationship_id=relationship_id,
                actor_id="live-agent:direct",
                workflow_id="live-agent-direct/0",
                transition_class="relationship.note",
                previous_head=head3,
                visibility="private",
                payload={"set": {"unsafe": True}},
            ),
            "unauthorized_updater",
        )

        expect(
            "RR-N02-missing-previous-head",
            replacement.apply(
                transition_id="tr-005",
                relationship_id=relationship_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=None,
                visibility="private",
                payload={"set": {"note": "missing head"}},
            ),
            "missing_previous_head",
        )

        expect(
            "RR-N03-stale-head",
            replacement.apply(
                transition_id="tr-006",
                relationship_id=relationship_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=head1,
                visibility="private",
                payload={"set": {"note": "stale"}},
            ),
            "rollback_or_stale_head",
        )

        expect(
            "RR-N04-replay",
            replacement.apply(
                transition_id="tr-003",
                relationship_id=relationship_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.continue",
                previous_head=head3,
                visibility="private",
                payload={"set": {"replacement_live_agent_continued": True}},
            ),
            "replay_transition",
        )

        expect(
            "RR-N05-competing-successor",
            replacement.apply(
                transition_id="tr-007",
                relationship_id=relationship_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.note",
                previous_head=head2,
                visibility="pointer",
                payload={"fork_candidate": True, "set": {"alternate": "branch"}},
            ),
            "competing_successor_head",
        )

        expect(
            "RR-N06-hidden-session-context",
            replacement.apply(
                transition_id="tr-008",
                relationship_id=relationship_id,
                actor_id=actor,
                workflow_id=state_wf,
                transition_class="relationship.continue",
                previous_head=head3,
                visibility="private",
                payload={
                    "requires_persisted": ["conversation_secret"],
                    "set": {"unsafe_continuation": True},
                },
            ),
            "missing_persisted_context",
        )

        correction = replacement.apply(
            transition_id="tr-009",
            relationship_id=relationship_id,
            actor_id=actor,
            workflow_id=state_wf,
            transition_class="relationship.correction",
            previous_head=head3,
            visibility="commitment",
            payload={"set": {"correction_ref": "sha256:correction-001"}},
        )
        expect("RR-P04-correction-is-appended", correction, "accepted")

        validation = replacement.validate_history(relationship_id)
        if not validation["valid"]:
            raise AssertionError(f"untampered history invalid: {validation}")
        results.append({
            "vector_id": "RR-P05-history-reconstructs",
            "expected": "valid",
            "observed": validation["code"],
            "pass": True,
            "validation": validation,
        })

        tampered = RoleRecordStore(path, role_id)
        tampered.data["relationships"][relationship_id]["events"][1]["payload"]["set"]["dataset_ref"] = "sha256:mutated"
        tampered_validation = tampered.validate_history(relationship_id)
        if tampered_validation["code"] != "historical_event_hash_mismatch":
            raise AssertionError(f"historical mutation not detected: {tampered_validation}")
        results.append({
            "vector_id": "RR-N07-historical-mutation",
            "expected": "historical_event_hash_mismatch",
            "observed": tampered_validation["code"],
            "pass": True,
            "validation": tampered_validation,
        })

        deleted = RoleRecordStore(path, role_id)
        del deleted.data["relationships"][relationship_id]["events"][1]
        deleted_validation = deleted.validate_history(relationship_id)
        if deleted_validation["valid"]:
            raise AssertionError("historical deletion was not detected")
        results.append({
            "vector_id": "RR-N08-historical-deletion",
            "expected": "invalid-history",
            "observed": deleted_validation["code"],
            "pass": True,
            "validation": deleted_validation,
        })

        rollback = RoleRecordStore(path, role_id)
        rollback.data["relationships"][relationship_id]["current_head"] = head1
        rollback_validation = rollback.validate_history(relationship_id)
        if rollback_validation["code"] != "current_head_mismatch":
            raise AssertionError(f"persisted rollback not detected: {rollback_validation}")
        results.append({
            "vector_id": "RR-N09-persisted-current-head-rollback",
            "expected": "current_head_mismatch",
            "observed": rollback_validation["code"],
            "pass": True,
            "validation": rollback_validation,
        })

        final_store = RoleRecordStore(path, role_id)
        final_validation = final_store.validate_history(relationship_id)
        final_state = final_store.current_state(relationship_id)
        visibility_seen = sorted({
            event["visibility"]
            for event in final_store.data["relationships"][relationship_id]["events"]
        })
        if visibility_seen != ["commitment", "private", "shared"]:
            raise AssertionError(f"unexpected visibility classes: {visibility_seen}")

        return {
            "case_id": "IC-ARA-REL-001",
            "gate": "ARA-G3-ROLE-STATE-EXECUTABLE",
            "implementation": "lab-local-role-record-v0.1",
            "summary": {
                "vectors": len(results),
                "passed": sum(1 for item in results if item["pass"]),
                "failed": sum(1 for item in results if not item["pass"]),
                "final_head": final_store.current_head(relationship_id),
                "final_history_valid": final_validation["valid"],
                "persisted_state_keys": sorted(final_state),
                "visibility_classes_exercised": visibility_seen,
            },
            "claim_boundary": {
                "demonstrates": [
                    "persistent Agent Role identifier across engine/Live Agent replacement",
                    "hash-linked append-only relationship-local state",
                    "canonical current head and previous-head binding",
                    "authorized update classes",
                    "stale/rollback/replay/competing-successor refusal",
                    "private/shared/pointer/commitment classification support",
                    "continuation from persisted authorized state only",
                    "historical mutation/deletion detection",
                    "correction by appended event",
                    "deterministic transition receipts",
                ],
                "does_not_demonstrate": [
                    "KERI or BetterSign conformance",
                    "OpenVTC VTA conformance",
                    "transparency-log or distributed-consensus guarantees",
                    "hardware-backed anti-rollback",
                    "Byzantine fork resolution",
                    "production persistence security",
                ],
            },
            "results": results,
        }


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
