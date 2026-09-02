#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = ROOT / "cases" / "dtg-vdc-vac-composition" / "scenario.yaml"
RESULT = ROOT / "results" / "dtg-vdc-vac-composition" / "run-results.json"


def load_scenario() -> dict:
    return yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))


def evaluate(vector: dict) -> dict:
    action = vector["requested_action"]
    delegation_scope_ok = action in vector["delegation_actions"]
    principal_scope_ok = action in vector["principal_authority_actions"]
    eligibility_ok = (
        not vector["delegate_eligibility_required"] or vector["delegate_eligible"]
    )
    checks = {
        "delegation_current": bool(vector["delegation_valid"]),
        "delegation_scope": delegation_scope_ok,
        "principal_authority_current": bool(vector["principal_authority_current"]),
        "principal_authority_scope": principal_scope_ok,
        "delegate_eligibility": eligibility_ok,
        "invocation_binding": bool(vector["invocation_binding_valid"]),
    }
    decision = "allow" if all(checks.values()) else "deny"
    return {
        "id": vector["id"],
        "class": vector["class"],
        "description": vector["description"],
        "requested_action": action,
        "checks": checks,
        "decision": decision,
        "expected": vector["expected"],
        "matches_expected": decision == vector["expected"],
    }


def build_result() -> dict:
    scenario = load_scenario()
    vectors = [evaluate(v) for v in scenario["vectors"]]
    return {
        "case": scenario["case"],
        "status": scenario["status"],
        "evaluator_version": "0.1",
        "source_pins": scenario["source_pins"],
        "propositions": scenario["propositions"],
        "semantic_rule": scenario["rule"],
        "vectors": vectors,
        "all_expected_outcomes_matched": all(v["matches_expected"] for v in vectors),
        "claim_boundary": "semantic composition evidence only; proposed upstream VDC/VAC semantics are not represented as adopted DTG behavior",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    result = build_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
    if args.check:
        if not RESULT.exists() or RESULT.read_text(encoding="utf-8") != text:
            print("VDC/VAC composition result fixture is stale", file=sys.stderr)
            return 1
    if not args.write and not args.check:
        print(text, end="")
    return 0 if result["all_expected_outcomes_matched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
