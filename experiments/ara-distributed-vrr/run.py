#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from vrr import DistributedVRR, digest

A = "urn:ara:agent-role:data-owner:001"
B = "urn:ara:agent-role:researcher:001"
REL = "urn:ara:relationship:research:001"


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    vrr = DistributedVRR(REL, 1, [A, B])

    shared = vrr.add_object(owner_role=A, evidence_class="shared_object", content={"dataset": "synthetic-001", "terms": "v1"}, label="shared terms")
    pointer = vrr.add_object(owner_role=A, evidence_class="source_pointer", pointer="role-record://data-owner/evidence/42", label="private source pointer")
    opaque = vrr.add_object(owner_role=A, evidence_class="opaque_commitment", commitment=digest({"hidden": "future disclosure"}), label="sealed evidence")
    private = vrr.add_object(owner_role=A, evidence_class="private_role_evidence", content={"secret": "not relationship state"}, label="private note")

    delivered = vrr.receipt(actor_role=B, object_ref=shared["object_ref"], stage="delivered")
    record(results, "P7-P01-delivery-distinct", "delivered", delivered["stage"], delivered)

    inspected = vrr.receipt(actor_role=B, object_ref=shared["object_ref"], stage="inspected", observed_content_id=shared["content_id"])
    record(results, "P7-P02-exact-inspection", "inspected", inspected["stage"], inspected)

    a_accept = vrr.dispose(actor_role=A, object_ref=shared["object_ref"], disposition="accepted", note="sender accepts")
    b_accept = vrr.dispose(actor_role=B, object_ref=shared["object_ref"], disposition="accepted", basis_receipt_ref=inspected["receipt_ref"], note="receiver accepts")
    mutual = vrr.mutual_state(shared["object_ref"])
    record(results, "P7-P03-mutual-acceptance-reconstructed", "mutual", mutual["status"], mutual)

    bad_inspection = vrr.receipt(actor_role=B, object_ref=shared["object_ref"], stage="inspected", observed_content_id="sha256:different")
    record(results, "P7-N01-copied-not-falsely-inspected", "inspection_digest_mismatch", bad_inspection["code"], bad_inspection)

    copied_only = vrr.receipt(actor_role=B, object_ref=pointer["object_ref"], stage="delivered")
    record(results, "P7-N02-delivery-not-inspection", "delivered", copied_only["stage"], copied_only)

    decrypted = vrr.receipt(actor_role=B, object_ref=shared["object_ref"], stage="decrypted")
    record(results, "P7-N03-decryption-not-acceptance", "decrypted", decrypted["stage"], decrypted)

    annotation_vrr = DistributedVRR(REL, 1, [A, B])
    annotation = annotation_vrr.add_object(owner_role=A, evidence_class="shared_object", content={"claim": "A's annotation"}, label="annotation")
    annotation_vrr.dispose(actor_role=A, object_ref=annotation["object_ref"], disposition="accepted")
    unilateral = annotation_vrr.mutual_state(annotation["object_ref"])
    record(results, "P7-N04-unilateral-annotation-not-mutual", "not_mutual", unilateral["status"], unilateral)

    dispute_vrr = DistributedVRR(REL, 1, [A, B])
    disputed_obj = dispute_vrr.add_object(owner_role=A, evidence_class="shared_object", content={"claim": "contested"}, label="contested")
    dispute_vrr.dispose(actor_role=A, object_ref=disputed_obj["object_ref"], disposition="accepted")
    dispute = dispute_vrr.dispose(actor_role=B, object_ref=disputed_obj["object_ref"], disposition="disputed", note="receiver challenges")
    state = dispute_vrr.mutual_state(disputed_obj["object_ref"])
    record(results, "P7-N05-dispute-not-silent-acceptance", "disputed", state["status"], state)

    correction = dispute_vrr.correct(actor_role=B, target_ref=dispute["disposition_ref"], correction="clarified reason; original dispute remains")
    checkpoint_after_correction = dispute_vrr.checkpoint(role_record_heads={A: "head:a:2", B: "head:b:2"})
    preserved = dispute["disposition_ref"] in checkpoint_after_correction["disposition_refs"] and correction["correction_ref"] in checkpoint_after_correction["correction_refs"]
    record(results, "P7-N06-correction-preserves-dispute", "preserved", "preserved" if preserved else "erased", checkpoint_after_correction)

    private_export = vrr.export_selective(object_refs=[private["object_ref"]])
    record(results, "P7-N07-private-not-shared-export", "private_object_export_forbidden", private_export["code"], private_export)

    opaque_inspect = vrr.receipt(actor_role=B, object_ref=opaque["object_ref"], stage="inspected", observed_content_id=opaque["content_id"])
    record(results, "P7-N08-commitment-not-hidden-knowledge", "opaque_content_not_inspectable", opaque_inspect["code"], opaque_inspect)

    traversal = vrr.traverse(requester_role=B, object_ref=pointer["object_ref"])
    record(results, "P7-N09-link-not-traversal-authority", "link_not_traversal_authority", traversal["code"], traversal)

    incomplete_checkpoint = vrr.checkpoint(role_record_heads={A: "head:a:1"})
    record(results, "P7-N10-checkpoint-missing-party-visible", "checkpoint_missing_party_head", incomplete_checkpoint["code"], incomplete_checkpoint)

    checkpoint = vrr.checkpoint(role_record_heads={A: "head:a:1", B: "head:b:1"})
    private_absent = private["object_ref"] not in checkpoint["shared_object_refs"]
    record(results, "P7-P04-checkpoint-excludes-private", "private_excluded", "private_excluded" if private_absent else "private_leaked", checkpoint)

    selective = vrr.export_selective(object_refs=[shared["object_ref"], pointer["object_ref"], opaque["object_ref"]])
    classes = sorted(o["evidence_class"] for o in selective["objects"])
    expected_classes = sorted(["shared_object", "source_pointer", "opaque_commitment"])
    record(results, "P7-P05-selective-export-preserves-classes", json.dumps(expected_classes), json.dumps(classes), selective)

    summary = {
        "case_id": "IC-ARA-REL-001",
        "phase": 7,
        "experiment": "ara-distributed-vrr",
        "vectors": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "claim_boundary": "Lab-local distributed relationship evidence semantics with independent Role Record heads and cross-anchored checkpoints; not normative VRC/RCard/VRR conformance or distributed consensus.",
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
