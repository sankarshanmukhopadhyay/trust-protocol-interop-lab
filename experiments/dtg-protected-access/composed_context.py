#!/usr/bin/env python3
"""Executable composition producer for observer-bound DPIP A/B evidence.

This producer exercises Interop Lab composition surfaces. Its observations are evidence
about this executed composition; they are not attributed to a target implementation
unless that target actually produced the surface.
"""
from __future__ import annotations
import argparse
import hashlib
import json

SURFACES = [
    "relationship_did", "edge_identifier", "equivalent_relationship_binder",
    "status_handle", "status_endpoint", "policy_discovery_handle", "policy_endpoint",
    "task_identifier", "thread_identifier", "retained_relationship_evidence", "retained_outcome_evidence",
    "verifier_transcript", "challenge", "purpose", "transaction_context", "deliberate_join_attempt",
    "credential_identifier", "presentation_identifier", "proof_or_request_binding", "retained_evidence_reference",
]


def token(prefix: str, value: str) -> str:
    return f"{prefix}:{hashlib.sha256(value.encode()).hexdigest()[:20]}"


def build(context: str, mode: str, seeded: str | None) -> dict:
    if context not in {"A", "B"}:
        raise ValueError("context must be A or B")
    ctx = context.lower()
    if mode == "positive-control":
        binder = seeded or "relationship-control-001"
        credential_seed = seeded or "credential-control-001"
        status_seed = f"{binder}:status:{ctx}"
        task_seed = f"{binder}:task:{ctx}"
    elif mode == "unlinkability":
        binder = f"relationship-{ctx}-distinct"
        credential_seed = f"credential-{ctx}-distinct"
        status_seed = f"status-{ctx}-distinct"
        task_seed = f"task-{ctx}-distinct"
    elif mode == "status-falsification":
        binder = f"relationship-{ctx}-distinct"
        credential_seed = f"credential-{ctx}-distinct"
        status_seed = seeded or "deliberately-shared-status-handle"
        task_seed = f"task-{ctx}-distinct"
    else:
        raise ValueError("unsupported mode")

    observations = {
        "relationship_did": token("did", binder),
        "edge_identifier": token("edge", f"{binder}:{ctx}"),
        "equivalent_relationship_binder": token("binder", binder),
        "status_handle": token("status", status_seed),
        "status_endpoint": token("endpoint", f"status-service:{ctx}"),
        "policy_discovery_handle": token("policy", f"policy:{binder}:{ctx}"),
        "policy_endpoint": token("endpoint", f"policy-service:{ctx}"),
        "task_identifier": token("task", task_seed),
        "thread_identifier": token("thread", f"{task_seed}:thread"),
        "retained_relationship_evidence": token("retained-rel", f"{binder}:{ctx}:retained"),
        "retained_outcome_evidence": token("retained-outcome", f"{task_seed}:{ctx}:outcome"),
        "verifier_transcript": token("transcript", f"verifier-{ctx}:challenge-{ctx}:purpose-{ctx}"),
        "challenge": f"challenge-{ctx}",
        "purpose": f"purpose-{ctx}",
        "transaction_context": f"transaction-{ctx}",
        "deliberate_join_attempt": token("join-attempt", binder if mode == "positive-control" else f"{binder}:{ctx}"),
        "credential_identifier": token("credential", credential_seed),
        "presentation_identifier": token("presentation", credential_seed if mode == "positive-control" else f"{credential_seed}:{ctx}"),
        "proof_or_request_binding": token("proof-binding", credential_seed if mode == "positive-control" else f"{credential_seed}:request:{ctx}"),
        "retained_evidence_reference": token("retained-evidence", credential_seed if mode == "positive-control" else f"{credential_seed}:retained:{ctx}"),
    }
    return {
        "run_id": f"composed-{mode}-{ctx}",
        "producer_component": "trust-protocol-interop-lab/composed-unlinkability-v1",
        "executed_surfaces": SURFACES,
        "observations": observations,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--context", required=True, choices=["A", "B"])
    p.add_argument("--mode", required=True, choices=["positive-control", "unlinkability", "status-falsification"])
    p.add_argument("--seeded-correlator")
    args = p.parse_args()
    print(json.dumps(build(args.context, args.mode, args.seeded_correlator), sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
