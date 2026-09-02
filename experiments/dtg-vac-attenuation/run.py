#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = ROOT / "cases" / "dtg-vac-attenuation" / "scenario.yaml"
RESULT = ROOT / "results" / "dtg-vac-attenuation" / "run-results.json"


def evaluate(parent: dict, vector: dict) -> dict:
    child = vector["child"]
    checks = {
        "actions_narrowed": set(child["actions"]).issubset(set(parent["actions"])),
        "scope_not_widened": child["scope"] == parent["scope"],
        "expiry_not_later": child["expires_at"] <= parent["expires_at"],
        "audience_binding": child.get("audience") in (None, vector["presenter"]),
        "chain_complete": bool(vector["chain_complete"]),
        "depth_within_limit": child["chain_depth"] <= parent["max_depth"],
        "root_current": bool(vector["root_current"]),
        "intermediate_current": bool(vector["intermediate_current"]),
        "current_state_fresh": bool(vector["current_state_fresh"]),
    }
    decision = "allow" if all(checks.values()) else "deny"
    return {
        "id": vector["id"],
        "class": vector["class"],
        "checks": checks,
        "decision": decision,
        "expected": vector["expected"],
        "matches_expected": decision == vector["expected"],
    }


def build_result() -> dict:
    scenario = yaml.safe_load(SCENARIO.read_text(encoding="utf-8"))
    vectors = [evaluate(scenario["parent"], v) for v in scenario["vectors"]]
    return {
        "case": scenario["case"],
        "status": scenario["status"],
        "evaluator_version": "0.1",
        "source_pin": scenario["source_pin"],
        "propositions": scenario["propositions"],
        "vectors": vectors,
        "all_expected_outcomes_matched": all(v["matches_expected"] for v in vectors),
        "claim_boundary": "semantic attenuation evidence only; proposed VAC semantics are not represented as adopted DTG behavior",
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
            print("VAC attenuation result fixture is stale", file=sys.stderr)
            return 1
    if not args.write and not args.check:
        print(text, end="")
    return 0 if result["all_expected_outcomes_matched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
