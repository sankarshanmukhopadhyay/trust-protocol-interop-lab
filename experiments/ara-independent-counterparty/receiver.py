#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
POLICY_DIR = ROOT / "experiments" / "ara-policy-spine"
sys.path.insert(0, str(POLICY_DIR))

from authorization import SUPPORTED_TASK, canonical_json, digest  # type: ignore  # noqa: E402

SHARED_LAB_KEY = b"lab-only-protected-key-material"


def decision(result: str, code: str, package: dict[str, Any], extra: dict[str, Any] | None = None) -> dict[str, Any]:
    material = {
        "result": result,
        "code": code,
        "wire_ref": package.get("wire_ref"),
        "task_ref": package.get("task", {}).get("task_ref"),
        "sender_role_id": package.get("sender_role_id"),
        "receiver_role_id": package.get("recipient_role_id"),
        **(extra or {}),
    }
    return {**material, "receiver_receipt_ref": digest(material)}


def signed_context_from(package: dict[str, Any]) -> dict[str, Any]:
    task = package["task"]
    authority = package["authority"]
    sender_decision = package["sender_decision_receipt"]
    admission = package["sender_admission_receipt"]
    crypto = package["cryptographic_use_receipt"]
    return {
        "agent_role_id": package["sender_role_id"],
        "role_record_head": package["sender_role_record_head"],
        "workflow_id": crypto["workflow_id"],
        "workflow_version": crypto["workflow_version"],
        "task_id": task["task_id"],
        "task_ref": task["task_ref"],
        "relationship_id": package["relationship_id"],
        "agreement_ref": task["agreement_ref"],
        "authority_ref": authority["authority_ref"],
        "decision_ref": sender_decision["decision_ref"],
        "capability_ref": task["capability_ref"],
        "admission_receipt_ref": admission["receipt_ref"],
        "recipient": task["recipient"],
        "purpose": task["purpose"],
        "payload_digest": task["payload_digest"],
        "nonce": task["nonce"],
        "expires_at": task["expires_at"],
        "signing_identity": crypto["signing_identity"],
    }


def verify(package: dict[str, Any], state: dict[str, Any], replay_db: Path, now: int) -> dict[str, Any]:
    required = [
        "wire_ref", "sender_role_id", "recipient_role_id", "relationship_id",
        "sender_role_record_head", "agreement", "authority", "task",
        "sender_decision_receipt", "sender_admission_receipt", "cryptographic_use_receipt",
    ]
    missing = [k for k in required if package.get(k) is None]
    if missing:
        return decision("indeterminate", "missing_required_wire_evidence", package, {"missing": missing})

    wire_without_ref = {k: v for k, v in package.items() if k != "wire_ref"}
    if package["wire_ref"] != digest(wire_without_ref):
        return decision("deny", "wire_integrity_mismatch", package)

    if package["recipient_role_id"] != state["receiver_role_id"]:
        return decision("deny", "recipient_context_substitution", package)
    if package["relationship_id"] != state["relationship_id"]:
        return decision("deny", "relationship_mismatch", package)
    if package["sender_role_id"] != state["expected_sender_role_id"]:
        return decision("deny", "sender_role_not_recognized", package)

    task = package["task"]
    authority = package["authority"]
    agreement = package["agreement"]
    crypto = package["cryptographic_use_receipt"]

    if task.get("task_id") != SUPPORTED_TASK:
        return decision("deny", "unsupported_task_version", package)
    if task.get("relationship_id") != state["relationship_id"]:
        return decision("deny", "task_relationship_mismatch", package)
    if task.get("recipient") != state["receiver_role_id"]:
        return decision("deny", "task_recipient_mismatch", package)
    if task.get("purpose") not in state["allowed_purposes"]:
        return decision("deny", "receiver_policy_denied_purpose", package)
    if task.get("resource") not in state["allowed_resources"]:
        return decision("deny", "receiver_policy_denied_resource", package)
    if task.get("action") not in state["allowed_actions"]:
        return decision("deny", "receiver_policy_denied_action", package)
    if state.get("instance_policy") == "deny":
        return decision("deny", "receiver_instance_policy_denied", package)

    if agreement.get("agreement_ref") != state["agreement_ref"]:
        return decision("deny", "receiver_agreement_mismatch", package)
    if agreement.get("status") != "active":
        return decision("deny", "agreement_not_active", package)
    if task.get("agreement_ref") != agreement.get("agreement_ref"):
        return decision("deny", "task_agreement_mismatch", package)

    if authority.get("authority_ref") != task.get("authority_ref"):
        return decision("deny", "authority_reference_mismatch", package)
    if authority.get("active") is not True:
        return decision("deny", "authority_inactive", package)
    if authority.get("subject_role_id") != package["sender_role_id"]:
        return decision("deny", "authority_wrong_subject", package)
    if authority.get("relationship_id") != package["relationship_id"]:
        return decision("deny", "authority_wrong_relationship", package)
    if now >= int(authority.get("expires_at", 0)):
        return decision("deny", "authority_expired", package)
    if task.get("purpose") not in authority.get("purposes", []):
        return decision("deny", "authority_purpose_out_of_scope", package)
    if task.get("resource") not in authority.get("resources", []):
        return decision("deny", "authority_resource_out_of_scope", package)
    if task.get("action") not in authority.get("actions", []):
        return decision("deny", "authority_action_out_of_scope", package)

    if package["sender_role_record_head"] != state["accepted_sender_head"]:
        return decision("indeterminate", "relationship_state_inconsistent", package)
    if task.get("role_record_head") != package["sender_role_record_head"]:
        return decision("deny", "task_sender_head_mismatch", package)

    if now >= int(task.get("expires_at", 0)):
        return decision("deny", "task_expired", package)

    if crypto.get("result") != "accepted":
        return decision("deny", "sender_cryptographic_use_not_accepted", package)
    context = signed_context_from(package)
    if crypto.get("signed_context_ref") != digest(context):
        return decision("deny", "signed_context_mismatch", package)
    expected_signature = "hmac-sha256:" + hmac.new(
        SHARED_LAB_KEY,
        canonical_json(context).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(str(crypto.get("signature")), expected_signature):
        return decision("deny", "signature_invalid", package)

    seen: set[str] = set()
    if replay_db.exists():
        seen = set(json.loads(replay_db.read_text(encoding="utf-8")))
    nonce = str(task.get("nonce"))
    if nonce in seen:
        return decision("deny", "receiver_replay_detected", package)
    seen.add(nonce)
    replay_db.write_text(json.dumps(sorted(seen)) + "\n", encoding="utf-8")

    sender_decision = package["sender_decision_receipt"]
    sender_admission = package["sender_admission_receipt"]
    correlation = {
        "sender_decision_ref": sender_decision.get("decision_ref"),
        "sender_admission_ref": sender_admission.get("receipt_ref"),
        "sender_cryptographic_use_ref": crypto.get("receipt_ref"),
        "task_ref": task.get("task_ref"),
        "wire_ref": package["wire_ref"],
    }
    return decision("accept", "receiver_independently_accepted", package, {"correlation": correlation})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--replay-db", type=Path, required=True)
    parser.add_argument("--now", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    package = json.loads(args.input.read_text(encoding="utf-8"))
    state = json.loads(args.state.read_text(encoding="utf-8"))
    result = verify(package, state, args.replay_db, args.now)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
