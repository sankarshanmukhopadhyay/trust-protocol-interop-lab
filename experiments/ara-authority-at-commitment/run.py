#!/usr/bin/env python3
"""Deterministic authority-at-material-commitment fixture runner."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VECTORS = ROOT / "cases/ara-minimum-executable-relationship/authority-at-commitment-vectors.json"

DENY_STATES = {"revoked", "expired", "suspended"}
UNKNOWN_STATES = {"unknown", "unavailable", "stale"}
CURRENT_EVIDENCE = "current"
MISSING_EVIDENCE = {"missing", "unknown", "unavailable", None}


def evaluate_collective_authority(data: dict, collective: dict) -> str:
    """Evaluate only the bounded collective-authority proposition.

    Participant identity/signature validity is not authority. A collective act
    requires a current membership set, a current threshold rule, exact-action
    binding, and enough distinct valid current members.
    """
    membership_evidence = collective.get("membership_evidence")
    rule_evidence = collective.get("rule_evidence")

    if membership_evidence in MISSING_EVIDENCE or rule_evidence in MISSING_EVIDENCE:
        return "indeterminate"
    if membership_evidence != CURRENT_EVIDENCE or rule_evidence != CURRENT_EVIDENCE:
        return "deny"

    threshold = collective.get("threshold_required")
    members = collective.get("current_members")
    approvals = collective.get("approvals")

    if not isinstance(threshold, int) or threshold < 1:
        return "indeterminate"
    if not isinstance(members, list) or not members:
        return "indeterminate"
    if threshold > len(set(members)):
        return "deny"
    if approvals is None:
        return "indeterminate"
    if not isinstance(approvals, list):
        return "indeterminate"

    qualifying_members: set[str] = set()
    current_members = set(members)
    for approval in approvals:
        if not isinstance(approval, dict):
            return "deny"
        member = approval.get("member")
        if member not in current_members:
            return "deny"
        if approval.get("action_digest") != data["action_digest"]:
            return "deny"
        if approval.get("valid") is not True:
            return "deny"
        if member:
            qualifying_members.add(member)

    return "permit" if len(qualifying_members) >= threshold else "deny"


def evaluate(data: dict) -> str:
    state = data.get("authority_state")
    if state in DENY_STATES:
        return "deny"
    if state in UNKNOWN_STATES or state != "active":
        return "indeterminate"
    if not data.get("action_digest"):
        return "indeterminate"
    if data.get("scope_satisfied") is not True:
        return "deny"
    if data.get("approval_required"):
        approval = data.get("approval")
        if not approval:
            return "indeterminate"
        if approval.get("action_digest") != data["action_digest"]:
            return "deny"
        if approval.get("valid") is not True:
            return "deny"

    collective = data.get("collective_authority")
    if collective is not None:
        if not isinstance(collective, dict):
            return "indeterminate"
        return evaluate_collective_authority(data, collective)

    return "permit"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail unless every vector matches")
    parser.add_argument("--output", help="optional JSON evidence output")
    args = parser.parse_args()

    payload = json.loads(VECTORS.read_text())
    results = []
    failures = []
    for vector in payload["vectors"]:
        actual = evaluate(vector["input"])
        result = {"id": vector["id"], "expected": vector["expected"], "actual": actual, "pass": actual == vector["expected"]}
        results.append(result)
        if not result["pass"]:
            failures.append(result)

    evidence = {
        "case_id": payload["case_id"],
        "tranche": payload["tranche"],
        "vector_count": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "results": results,
        "claim_boundary": "bounded deterministic authority-at-material-commitment semantics, including collective-threshold exercise; not legal effect, wire-protocol conformance, or production authorization assurance",
    }
    rendered = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered)
    else:
        print(rendered, end="")
    return 1 if failures and args.check else 0


if __name__ == "__main__":
    raise SystemExit(main())
