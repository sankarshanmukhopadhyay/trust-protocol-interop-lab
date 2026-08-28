#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments" / "ara-independent-counterparty"
POLICY_DIR = ROOT / "experiments" / "ara-policy-spine"
sys.path.insert(0, str(POLICY_DIR))
from authorization import digest  # type: ignore  # noqa: E402


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rewire(package: dict[str, Any]) -> dict[str, Any]:
    body = {k: v for k, v in package.items() if k != "wire_ref"}
    package["wire_ref"] = digest(body)
    return package


def receive(tmp: Path, package: dict[str, Any], state: dict[str, Any], vector: str, *, replay_db: Path | None = None) -> dict[str, Any]:
    inp = tmp / f"{vector}-wire.json"
    st = tmp / f"{vector}-state.json"
    out = tmp / f"{vector}-receiver.json"
    replay = replay_db or (tmp / f"{vector}-replay.json")
    write_json(inp, package)
    write_json(st, state)
    subprocess.run(
        [sys.executable, str(EXP / "receiver.py"), "--input", str(inp), "--state", str(st), "--replay-db", str(replay), "--output", str(out)],
        check=True,
    )
    return json.loads(out.read_text(encoding="utf-8"))


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        baseline_path = tmp / "sender-wire.json"
        subprocess.run([sys.executable, str(EXP / "sender.py"), "--output", str(baseline_path)], check=True)
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))

        state = {
            "receiver_role_id": baseline["recipient_role_id"],
            "expected_sender_role_id": baseline["sender_role_id"],
            "relationship_id": baseline["relationship_id"],
            "accepted_sender_head": baseline["sender_role_record_head"],
            "agreement_ref": baseline["agreement"]["agreement_ref"],
            "allowed_purposes": ["synthetic-research"],
            "allowed_resources": ["dataset:synthetic-001"],
            "allowed_actions": ["query"],
            "instance_policy": "allow",
        }

        r = receive(tmp, copy.deepcopy(baseline), copy.deepcopy(state), "P6-P01")
        record(results, "P6-P01-independent-receiver-accepts", "receiver_independently_accepted", r["code"], r)

        deny_state = copy.deepcopy(state); deny_state["instance_policy"] = "deny"
        r = receive(tmp, copy.deepcopy(baseline), deny_state, "P6-N01")
        record(results, "P6-N01-sender-allow-receiver-deny", "receiver_instance_policy_denied", r["code"], r)

        p = copy.deepcopy(baseline); p["authority"]["active"] = False; rewire(p)
        r = receive(tmp, p, copy.deepcopy(state), "P6-N02")
        record(results, "P6-N02-valid-looking-signature-invalid-authority", "authority_inactive", r["code"], r)

        stale_state = copy.deepcopy(state); stale_state["accepted_sender_head"] = "sha256:newer-receiver-known-head"
        r = receive(tmp, copy.deepcopy(baseline), stale_state, "P6-N03")
        record(results, "P6-N03-stale-sender-state", "relationship_state_inconsistent", r["code"], r)

        p = copy.deepcopy(baseline); p["recipient_role_id"] = "urn:ara:agent-role:attacker:001"; rewire(p)
        r = receive(tmp, p, copy.deepcopy(state), "P6-N04")
        record(results, "P6-N04-recipient-context-substitution", "recipient_context_substitution", r["code"], r)

        replay_db = tmp / "shared-replay.json"
        first = receive(tmp, copy.deepcopy(baseline), copy.deepcopy(state), "P6-N05-first", replay_db=replay_db)
        if first["result"] != "accept":
            raise AssertionError(first)
        r = receive(tmp, copy.deepcopy(baseline), copy.deepcopy(state), "P6-N05-second", replay_db=replay_db)
        record(results, "P6-N05-replayed-serialized-request", "receiver_replay_detected", r["code"], r)

        p = copy.deepcopy(baseline); p.pop("authority"); rewire(p)
        r = receive(tmp, p, copy.deepcopy(state), "P6-N06")
        record(results, "P6-N06-unresolvable-required-evidence", "missing_required_wire_evidence", r["code"], r)

        inconsistent = copy.deepcopy(state); inconsistent["agreement_ref"] = "sha256:receiver-different-agreement"
        r = receive(tmp, copy.deepcopy(baseline), inconsistent, "P6-N07")
        record(results, "P6-N07-materially-inconsistent-relationship-state", "receiver_agreement_mismatch", r["code"], r)

        p = copy.deepcopy(baseline); p["task"]["purpose"] = "forbidden-export"; rewire(p)
        r = receive(tmp, p, copy.deepcopy(state), "P6-N08")
        record(results, "P6-N08-transport-success-not-task-acceptance", "receiver_policy_denied_purpose", r["code"], r)

        p = copy.deepcopy(baseline); p["cryptographic_use_receipt"]["signature"] = "hmac-sha256:" + "00" * 32; rewire(p)
        r = receive(tmp, p, copy.deepcopy(state), "P6-N09")
        record(results, "P6-N09-invalid-signature", "signature_invalid", r["code"], r)

        summary = {
            "case_id": "IC-ARA-REL-001",
            "phase": 6,
            "experiment": "ara-independent-counterparty",
            "vectors": len(results),
            "passed": sum(1 for x in results if x["pass"]),
            "failed": sum(1 for x in results if not x["pass"]),
            "process_boundary": "sender.py and receiver.py execute as separate subprocesses and exchange serialized JSON files only",
            "claim_boundary": "Lab-local subprocess/file transport with shared HMAC verification stand-in; not TSP, public-key identity, remote attestation, or production transport/security conformance.",
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
