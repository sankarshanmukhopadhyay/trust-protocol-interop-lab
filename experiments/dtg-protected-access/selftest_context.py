#!/usr/bin/env python3
"""Synthetic context emitter used only to falsify/test capture mechanics.

This is not upstream runtime evidence and is deliberately labelled by the calling
manifest as synthetic-fixture-self-test.
"""
from __future__ import annotations

import argparse
import json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("context", choices=["A", "B"])
    args = parser.parse_args()
    common = {
        "relationship_did": "did:example:durable-correlator",
        "edge_identifier": "edge-durable-001",
        "equivalent_relationship_binder": None,
        "status_handle": None,
        "status_endpoint": "https://status.example.invalid/check",
        "policy_discovery_handle": None,
        "policy_endpoint": "https://policy.example.invalid/v1",
        "task_identifier": None,
        "thread_identifier": None,
        "retained_relationship_evidence": None,
        "retained_outcome_evidence": None,
        "verifier_transcript": f"synthetic-transcript-{args.context}",
        "challenge": f"challenge-{args.context}",
        "purpose": f"purpose-{args.context}",
        "transaction_context": f"transaction-{args.context}",
        "deliberate_join_attempt": "joined-on-relationship_did",
    }
    print(json.dumps({"run_id": f"selftest-context-{args.context}", "observations": common}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
