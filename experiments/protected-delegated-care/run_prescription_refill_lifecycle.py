#!/usr/bin/env python3
"""Executable synthetic prescription-to-refill lifecycle for issue #150."""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

EVALUATED_AT = "2026-09-06T08:00:00Z"
VERIFIER = "pharmacy:synthetic-A"
CHALLENGE = "challenge:fresh-001"


@dataclass
class MedicationOrder:
    order_ref: str = "order:rx001"
    status: str = "active"
    expires_at: str = "2026-10-01T00:00:00Z"
    refill_limit: int = 2
    refills_used: int = 1


@dataclass
class RefillRequest:
    request_ref: str = "refill:req001"
    order_ref: str = "order:rx001"
    verifier_context: str = VERIFIER
    challenge: str = CHALLENGE
    requested_scope: str = "one_refill"
    consumed: bool = False


class RefillBoundary:
    def __init__(self) -> None:
        self.order = MedicationOrder()
        self.request = RefillRequest()
        self.effects = 0
        self.evidence: list[dict[str, Any]] = []

    def snapshot(self) -> tuple[int, int, bool]:
        return self.order.refills_used, self.effects, self.request.consumed

    def evaluate(self, *, verifier: str = VERIFIER, challenge: str = CHALLENGE) -> dict[str, Any]:
        if self.request.consumed:
            return {"authorization": "idempotent", "reason": "REQUEST_ALREADY_CONSUMED"}
        if self.request.order_ref != self.order.order_ref:
            return {"authorization": "deny", "reason": "ORDER_BINDING_MISMATCH"}
        if self.order.status != "active":
            return {"authorization": "deny", "reason": f"ORDER_{self.order.status.upper()}"}
        if self.order.expires_at <= EVALUATED_AT:
            return {"authorization": "deny", "reason": "ORDER_EXPIRED"}
        if self.order.refills_used >= self.order.refill_limit:
            return {"authorization": "deny", "reason": "REFILL_ALLOWANCE_EXHAUSTED"}
        if verifier != self.request.verifier_context:
            return {"authorization": "deny", "reason": "VERIFIER_CONTEXT_MISMATCH"}
        if challenge != self.request.challenge:
            return {"authorization": "deny", "reason": "CHALLENGE_MISMATCH"}
        if self.request.requested_scope != "one_refill":
            return {"authorization": "deny", "reason": "REFILL_SCOPE_NOT_PERMITTED"}
        return {"authorization": "permit", "reason": "CURRENT_REFILL_ELIGIBILITY"}

    def execute(self, *, verifier: str = VERIFIER, challenge: str = CHALLENGE) -> dict[str, Any]:
        before = self.snapshot()
        decision = self.evaluate(verifier=verifier, challenge=challenge)
        if decision["authorization"] != "permit":
            return {**decision, "state_mutation": self.snapshot() != before}
        self.order.refills_used += 1
        self.effects += 1
        self.request.consumed = True
        self.evidence.append({
            "event": "refill_effect_recorded",
            "order_ref": self.order.order_ref,
            "request_ref": self.request.request_ref,
            "scope": self.request.requested_scope,
            "evaluated_at": EVALUATED_AT,
        })
        return {"authorization": "permit", "reason": decision["reason"], "state_mutation": True}


def fresh_boundary() -> RefillBoundary:
    return RefillBoundary()


def denied_case(mutator=None, *, verifier=VERIFIER, challenge=CHALLENGE) -> dict[str, Any]:
    boundary = fresh_boundary()
    if mutator:
        mutator(boundary)
    before = boundary.snapshot()
    result = boundary.execute(verifier=verifier, challenge=challenge)
    return {"result": result, "no_effect": boundary.effects == 0, "no_mutation": boundary.snapshot() == before}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    args = parser.parse_args()

    positive = fresh_boundary()
    first = positive.execute()
    replay = positive.execute()

    expired = denied_case(lambda b: setattr(b.order, "expires_at", "2026-09-01T00:00:00Z"))
    revoked = denied_case(lambda b: setattr(b.order, "status", "revoked"))
    superseded = denied_case(lambda b: setattr(b.order, "status", "superseded"))
    exhausted = denied_case(lambda b: setattr(b.order, "refills_used", b.order.refill_limit))
    wrong_context = denied_case(verifier="pharmacy:synthetic-B")
    stale_challenge = denied_case(challenge="challenge:stale")

    checks = {
        "current_order_permits_one_refill": first["authorization"] == "permit" and positive.effects == 1,
        "replay_has_no_second_effect": replay["authorization"] == "idempotent" and positive.effects == 1,
        "expired_denied_no_effect": expired["result"]["reason"] == "ORDER_EXPIRED" and expired["no_effect"] and expired["no_mutation"],
        "revoked_denied_no_effect": revoked["result"]["reason"] == "ORDER_REVOKED" and revoked["no_effect"] and revoked["no_mutation"],
        "superseded_denied_no_effect": superseded["result"]["reason"] == "ORDER_SUPERSEDED" and superseded["no_effect"] and superseded["no_mutation"],
        "exhausted_denied_no_effect": exhausted["result"]["reason"] == "REFILL_ALLOWANCE_EXHAUSTED" and exhausted["no_effect"] and exhausted["no_mutation"],
        "context_mismatch_denied": wrong_context["result"]["reason"] == "VERIFIER_CONTEXT_MISMATCH" and wrong_context["no_effect"],
        "challenge_mismatch_denied": stale_challenge["result"]["reason"] == "CHALLENGE_MISMATCH" and stale_challenge["no_effect"],
    }

    result = {
        "case_id": "IC-PDC-REFILL-001",
        "claim": "synthetic prescription-to-refill lifecycle evidence; not prescribing or production pharmacy interoperability",
        "positive": {"first": first, "replay": replay},
        "negative": {
            "expired": expired,
            "revoked": revoked,
            "superseded": superseded,
            "exhausted": exhausted,
            "wrong_context": wrong_context,
            "stale_challenge": stale_challenge,
        },
        "checks": checks,
        "semantic_separation": {
            "prescription_exists": "not dispensing authority",
            "holder_possesses": "not refill eligibility",
            "refill_eligible": "not legal dispensing authorization",
            "effect_recorded": "synthetic bounded effect only",
        },
    }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
