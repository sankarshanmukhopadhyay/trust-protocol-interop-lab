#!/usr/bin/env python3
"""Observe pinned Dogwood RC-1 execution without making a privacy judgment.

This adapter is intentionally target-specific. It validates that the caller is
running against the immutable Dogwood RC-1 revision and translates a real
upstream observation record into the JSON shape consumed by the Interop Lab
A/B capture harness.

The adapter never upgrades missing observations into evidence. Surfaces that
were not emitted by the upstream execution remain null and are therefore
classified downstream as not-evidenced.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any

DOGWOOD_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
DOGWOOD_REVISION = "cb01d0a758863fb3a02f9f4eef2c4f15f56c4c3b"
HEX40 = re.compile(r"^[0-9a-f]{40}$")

SURFACES = (
    "relationship_did",
    "edge_identifier",
    "status_handle",
    "status_endpoint",
    "policy_discovery_handle",
    "policy_endpoint",
    "task_identifier",
    "thread_identifier",
    "retained_relationship_evidence",
    "retained_outcome_evidence",
    "verifier_transcript",
    "challenge",
    "purpose",
    "transaction_context",
    "deliberate_join_attempt",
)


def load_json(path: str) -> dict[str, Any]:
    value = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("observation input must be a JSON object")
    return value


def adapt(payload: dict[str, Any], context: dict[str, str]) -> dict[str, Any]:
    provenance = payload.get("provenance") or {}
    if provenance.get("implementation_repository") != DOGWOOD_REPOSITORY:
        raise ValueError("observation is not attributable to the Dogwood repository")
    revision = str(provenance.get("implementation_revision") or "")
    if not HEX40.fullmatch(revision) or revision != DOGWOOD_REVISION:
        raise ValueError("observation is not pinned to immutable Dogwood RC-1 revision")

    upstream = payload.get("observations")
    if not isinstance(upstream, dict):
        raise ValueError("upstream execution did not emit an observations mapping")

    observations = {name: upstream.get(name) for name in SURFACES}

    # Context-defining values may be supplied by the runner only when they are
    # actual inputs to the observed execution. They are not inferred from test
    # success, fixture names, or specification intent.
    observations["challenge"] = observations.get("challenge") or context["challenge"]
    observations["purpose"] = observations.get("purpose") or context["purpose"]
    observations["transaction_context"] = observations.get("transaction_context") or context["verifier"]

    return {
        "observations": observations,
        "source": {
            "implementation_repository": DOGWOOD_REPOSITORY,
            "implementation_revision": DOGWOOD_REVISION,
            "upstream_run_id": provenance.get("run_id"),
            "upstream_observed_at": provenance.get("observed_at"),
            "adapter": "dogwood-rc1",
            "evidence_boundary": "runtime observation only; missing surfaces remain not-evidenced; no privacy conclusion",
        },
    }


def self_test() -> None:
    payload = {
        "provenance": {
            "implementation_repository": DOGWOOD_REPOSITORY,
            "implementation_revision": DOGWOOD_REVISION,
            "run_id": "dogwood-e2e-selftest",
            "observed_at": "2026-08-30T00:00:00Z",
        },
        "observations": {"relationship_did": "did:peer:2.example", "status_handle": None},
    }
    context = {"verifier": "verifier-a", "purpose": "protected-access-a", "challenge": "challenge-a"}
    result = adapt(payload, context)
    assert result["observations"]["relationship_did"] == "did:peer:2.example"
    assert result["observations"]["status_handle"] is None
    assert result["observations"]["challenge"] == "challenge-a"
    assert result["source"]["implementation_revision"] == DOGWOOD_REVISION
    bad = json.loads(json.dumps(payload))
    bad["provenance"]["implementation_revision"] = "main"
    try:
        adapt(bad, context)
    except ValueError:
        pass
    else:
        raise AssertionError("mutable target revision must be rejected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--observation-json")
    parser.add_argument("--verifier")
    parser.add_argument("--purpose")
    parser.add_argument("--challenge")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        print("PASS dogwood_rc1 adapter self-test")
        return 0
    if not all((args.observation_json, args.verifier, args.purpose, args.challenge)):
        parser.error("--observation-json, --verifier, --purpose and --challenge are required")
    result = adapt(
        load_json(args.observation_json),
        {"verifier": args.verifier, "purpose": args.purpose, "challenge": args.challenge},
    )
    json.dump(result, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
