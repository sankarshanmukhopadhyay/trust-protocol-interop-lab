#!/usr/bin/env python3
"""Evaluate Trust Tasks cryptosuite capability-set interoperability fixtures.

This is deliberately a capability/interoperability test, not a cryptographic
implementation. "verify-capable" means both sides support the declared suite
and the fixture marks the proof as valid; it does not independently establish
signature correctness.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "cases" / "trust-tasks-cryptosuite-interop" / "matrix.json"


def evaluate(case: dict, implementations: dict[str, dict]) -> str:
    producer = implementations[case["producer"]]
    consumer = implementations[case["consumer"]]
    suite = case["document_cryptosuite"]
    known_suites = {
        supported
        for implementation in implementations.values()
        for supported in implementation["supported_cryptosuites"]
    }

    if suite not in known_suites:
        return "unsupported-cryptosuite"
    if suite not in producer["supported_cryptosuites"]:
        return "producer-capability-mismatch"
    if suite not in consumer["supported_cryptosuites"]:
        return "unsupported-cryptosuite"
    if case.get("proof_state") != "valid":
        return "invalid-proof"
    return "verify-capable"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output")
    args = ap.parse_args()

    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    implementations = {x["id"]: x for x in payload["implementations"]}
    results = []
    failures = []
    for case in payload["cases"]:
        actual = evaluate(case, implementations)
        row = {
            "id": case["id"],
            "expected": case["expected"],
            "actual": actual,
            "pass": actual == case["expected"],
        }
        results.append(row)
        if not row["pass"]:
            failures.append(row)

    evidence = {
        "schema": "trust-tasks-cryptosuite-interop-result/v1",
        "status": "downstream-interoperability-evidence",
        "cases": len(results),
        "passed": len(results) - len(failures),
        "failed": len(failures),
        "results": results,
        "claim_boundary": payload["claim_boundary"],
    }
    rendered = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if args.check and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
