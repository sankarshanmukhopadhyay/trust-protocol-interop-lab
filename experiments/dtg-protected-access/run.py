#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[2]
CASE_DIR = ROOT / "cases" / "dtg-protected-access"
VECTOR_DIR = CASE_DIR / "vectors"
PROFILE = CASE_DIR / "dpip" / "interaction-profile.yaml"
RESULT = ROOT / "results" / "dtg-protected-access" / "run-results.json"

VECTOR_IDS = ("PA-POS-001", "PA-NEG-001", "PA-ADV-001")
PROHIBITED = {
    "protected_provider_identity",
    "protected_provider_location",
    "protected_relationship_type",
    "case_identifier",
    "durable_subject_identifier",
    "durable_provider_identifier",
}
DPIP_BASELINE = "3e5d286853178bec9b6579ecbdccd1932c281fc7"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def status(value: bool) -> str:
    return "pass" if value else "fail"


def evaluate(vector_doc: dict) -> dict:
    v = vector_doc["vector"]
    setup = v["setup"]
    observations = setup.get("observations", {})

    authority = setup.get("authority_provenance", {})
    authority_ok = bool(authority.get("attributable")) and bool(authority.get("provider_class_authorised"))

    prohibited_present = set(v.get("prohibited_observations_present", []))
    prohibited_from_observation = PROHIBITED.intersection(observations.keys())
    minimum_ok = not prohibited_present and not prohibited_from_observation

    discovered = v.get("discoverable_protected_relationships", setup.get("discovered_relationships", []))
    non_discoverability_ok = not bool(discovered)

    stable = v.get("stable_cross_context_identifiers_present", [])
    replay_ids = setup.get("replay_artifact_identifiers", {})
    replay_stable = [value for value in replay_ids.values() if value]
    correlation_ok = not bool(stable or replay_stable)

    if "context" in setup:
        context_ok = bool(setup["context"].get("matches_presentation"))
    else:
        context_ok = bool(setup.get("context_matches_presentation"))

    checks = {
        "cryptographic_verification": setup.get("cryptographic_verification", "not-evaluated"),
        "authority_provenance": status(authority_ok),
        "minimum_disclosure": status(minimum_ok),
        "non_discoverability": status(non_discoverability_ok),
        "correlation_resistance": status(correlation_ok),
        "context_binding": status(context_ok),
    }
    checks["case_outcome"] = status(all(value == "pass" for key, value in checks.items() if key != "cryptographic_verification"))

    expected = v["expected"]
    comparable = {k: checks[k] for k in expected}
    matches_expected = comparable == expected

    dpip_claims = {
        "PA-PC-1": checks["minimum_disclosure"],
        "PA-PC-2": checks["minimum_disclosure"],
        "PA-PC-3": checks["non_discoverability"],
        "PA-PC-4": checks["correlation_resistance"],
        "PA-PC-5": checks["context_binding"],
    }

    return {
        "vector_id": v["id"],
        "vector_class": v["class"],
        "checks": checks,
        "expected": expected,
        "matches_expected": matches_expected,
        "verifier_observations": observations,
        "privacy_observations": {
            "prohibited_fields": sorted(prohibited_present | prohibited_from_observation),
            "stable_cross_context_identifiers": stable + replay_stable,
            "discoverable_protected_relationships": discovered,
        },
        "dpip_claim_results": dpip_claims,
    }


def build_result() -> dict:
    profile = load_yaml(PROFILE)
    assert profile["provenance"]["dpip_baseline"] == DPIP_BASELINE
    vectors = [evaluate(load_yaml(VECTOR_DIR / f"{vector_id}.yaml")) for vector_id in VECTOR_IDS]
    return {
        "case": "IC-DTG-PROTECTED-ACCESS-001",
        "evaluator_version": "0.1",
        "dpip_binding": {
            "baseline": DPIP_BASELINE,
            "interaction_profile": str(PROFILE.relative_to(ROOT)),
            "target_profile": profile["interaction"]["target_profile"],
            "claim_scope": "repository-owned semantic execution bound to DPIP interaction/profile semantics; not external certification",
        },
        "vectors": vectors,
        "all_expected_outcomes_matched": all(v["matches_expected"] for v in vectors),
        "admission_recommendation": "eligible-for-admission-review" if all(v["matches_expected"] for v in vectors) else "not-ready",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write deterministic result fixture")
    parser.add_argument("--check", action="store_true", help="compare computed result with committed fixture")
    args = parser.parse_args()

    result = build_result()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"

    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(text, encoding="utf-8")
    if args.check:
        if not RESULT.exists() or RESULT.read_text(encoding="utf-8") != text:
            print("protected-access result fixture is stale", file=sys.stderr)
            return 1
    if not args.write and not args.check:
        print(text, end="")
    if not result["all_expected_outcomes_matched"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
