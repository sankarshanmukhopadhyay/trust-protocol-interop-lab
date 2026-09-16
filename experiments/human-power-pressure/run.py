#!/usr/bin/env python3
"""Deterministic human-power pressure evidence runner.

The runner records observable execution facts only. It deliberately does not
produce harm, privacy, legitimacy, discrimination, or assurance judgments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any

FIXTURE_SCHEMA = "interop-human-power-fixture/v1"
EVIDENCE_SCHEMA = "interop-human-power-observation-evidence/v1"
ALLOWED_FAMILIES = {"disclosure", "correlation", "refusal", "decision-feature"}

FAMILY_REQUIRED = {
    "disclosure": {
        "disclosure": {
            "available_minimal",
            "requested",
            "disclosed",
            "purpose_bound",
        }
    },
    "correlation": {
        "correlation": {
            "declared_scope",
            "requested_scope",
            "presented_scope",
            "retained_scope",
            "effective_scope",
            "observer_evidence",
        }
    },
    "refusal": {
        "refusal": {"available", "consequence", "continuation_path"},
        "interaction": {
            "bundled_authorization",
            "default_state",
            "prompt_count_after_refusal",
            "reversible",
            "purpose_specific",
        },
    },
    "decision-feature": {
        "decision": {
            "declared_features",
            "evaluated_features",
            "outcome",
        }
    },
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def fixture_digest(fixture: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(fixture).encode("utf-8")).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_fixture(fixture: dict[str, Any]) -> list[str]:
    """Validate structure and return observation paths still requiring evidence."""
    _require(isinstance(fixture, dict), "fixture must be an object")
    _require(fixture.get("schema") == FIXTURE_SCHEMA, f"schema must be {FIXTURE_SCHEMA}")
    _require(isinstance(fixture.get("id"), str) and fixture["id"], "id is required")
    family = fixture.get("family")
    _require(family in ALLOWED_FAMILIES, f"family must be one of {sorted(ALLOWED_FAMILIES)}")

    task = fixture.get("task")
    _require(isinstance(task, dict), "task must be an object")
    _require(isinstance(task.get("id"), str) and task["id"], "task.id is required")
    _require(isinstance(task.get("semantics"), str) and task["semantics"], "task.semantics is required")

    source = fixture.get("source")
    _require(isinstance(source, dict), "source must be an object")
    _require(isinstance(source.get("kind"), str) and source["kind"], "source.kind is required")
    _require(isinstance(source.get("revision"), str) and source["revision"], "source.revision is required")

    observations = fixture.get("observations")
    _require(isinstance(observations, dict), "observations must be an object")

    missing: list[str] = []
    for section, keys in FAMILY_REQUIRED[family].items():
        value = observations.get(section)
        if not isinstance(value, dict):
            missing.append(f"observations.{section}")
            continue
        for key in sorted(keys):
            if key not in value or value[key] is None:
                missing.append(f"observations.{section}.{key}")

    authorization = observations.get("authorization")
    if not isinstance(authorization, dict):
        missing.append("observations.authorization")
    else:
        for key in ("presented", "validity_observed"):
            if key not in authorization or authorization[key] is None:
                missing.append(f"observations.authorization.{key}")
    return missing


def derive_signals(fixture: dict[str, Any]) -> dict[str, Any]:
    """Derive neutral, reproducible differences from observations."""
    family = fixture["family"]
    obs = fixture["observations"]
    signals: dict[str, Any] = {}

    if family == "disclosure" and isinstance(obs.get("disclosure"), dict):
        d = obs["disclosure"]
        requested = list(d.get("requested") or [])
        minimal = list(d.get("available_minimal") or [])
        disclosed = list(d.get("disclosed") or [])
        signals["requested_beyond_available_minimal"] = sorted(set(requested) - set(minimal))
        signals["disclosed_beyond_available_minimal"] = sorted(set(disclosed) - set(minimal))
    elif family == "correlation" and isinstance(obs.get("correlation"), dict):
        c = obs["correlation"]
        signals["declared_scope"] = c.get("declared_scope")
        signals["requested_scope"] = c.get("requested_scope")
        signals["effective_scope"] = c.get("effective_scope")
        signals["scope_changed_from_declared"] = (
            c.get("effective_scope") is not None
            and c.get("declared_scope") is not None
            and c.get("effective_scope") != c.get("declared_scope")
        )
    elif family == "refusal":
        r = obs.get("refusal") or {}
        i = obs.get("interaction") or {}
        signals.update({
            "refusal_available": r.get("available"),
            "refusal_consequence": r.get("consequence"),
            "continuation_path": r.get("continuation_path"),
            "bundled_authorization": i.get("bundled_authorization"),
            "default_state": i.get("default_state"),
            "prompt_count_after_refusal": i.get("prompt_count_after_refusal"),
            "reversible": i.get("reversible"),
            "purpose_specific": i.get("purpose_specific"),
        })
    elif family == "decision-feature" and isinstance(obs.get("decision"), dict):
        d = obs["decision"]
        declared = set(d.get("declared_features") or [])
        evaluated = set((d.get("evaluated_features") or {}).keys())
        signals["undeclared_evaluated_features"] = sorted(evaluated - declared)
        signals["declared_but_not_evaluated_features"] = sorted(declared - evaluated)
        signals["outcome"] = d.get("outcome")
    return signals


def build_result(fixture: dict[str, Any], producer_revision: str | None = None) -> dict[str, Any]:
    missing = validate_fixture(fixture)
    revision = producer_revision or os.getenv("GITHUB_SHA") or "workspace"
    return {
        "schema": EVIDENCE_SCHEMA,
        "producer": {
            "repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab",
            "component": "experiments/human-power-pressure/run.py",
            "revision": revision,
        },
        "case": {
            "id": fixture["id"], "family": fixture["family"],
            "comparison_group": fixture.get("comparison_group"),
            "variant": fixture.get("variant"), "task": fixture["task"],
        },
        "source": fixture["source"],
        "evidence_state": "COMPLETE" if not missing else "EVIDENCE_REQUIRED",
        "missing_observations": missing,
        "observations": fixture["observations"],
        "derived_signals": derive_signals(fixture),
        "provenance": {"fixture_sha256": fixture_digest(fixture)},
        "claim_boundary": {
            "supports": [
                "reproduction of declared fixture observations",
                "comparison of bounded variants where comparison invariants hold",
                "downstream RAHP/DPIP assessment using explicit observations",
            ],
            "does_not_support": [
                "a harm or discrimination judgment",
                "a privacy PASS or FAIL judgment",
                "a legitimacy or consent judgment",
                "an assurance PASS",
                "production deployment claims from synthetic fixtures",
            ],
        },
    }


def validate_comparison_groups(fixtures: list[dict[str, Any]]) -> None:
    groups: dict[str, list[dict[str, Any]]] = {}
    for fixture in fixtures:
        group = fixture.get("comparison_group")
        if group:
            groups.setdefault(group, []).append(fixture)
    for name, members in groups.items():
        if len(members) < 2:
            continue
        task_pairs = {(m["task"]["id"], m["task"]["semantics"]) for m in members}
        families = {m["family"] for m in members}
        _require(len(task_pairs) == 1, f"comparison group {name} changes task identity or semantics")
        _require(len(families) == 1, f"comparison group {name} mixes pressure families")


def load_fixtures(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    values = value if isinstance(value, list) else [value]
    if not all(isinstance(item, dict) for item in values):
        raise ValueError(f"{path}: fixture root must be an object or array of objects")
    return values


def default_fixture_paths() -> list[Path]:
    return [Path(__file__).parent / "fixtures.json"]


def run(paths: list[Path], producer_revision: str | None = None) -> dict[str, Any]:
    fixtures = [fixture for path in paths for fixture in load_fixtures(path)]
    for fixture in fixtures:
        validate_fixture(fixture)
    validate_comparison_groups(fixtures)
    results = [build_result(fixture, producer_revision=producer_revision) for fixture in fixtures]
    return {
        "schema": "interop-human-power-evidence-package/v1",
        "producer_revision": producer_revision or os.getenv("GITHUB_SHA") or "workspace",
        "case_count": len(results),
        "evidence_required_count": sum(r["evidence_state"] == "EVIDENCE_REQUIRED" for r in results),
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", nargs="*", type=Path, help="fixture JSON files; defaults to bundled fixtures")
    parser.add_argument("--output", type=Path, help="write deterministic evidence package")
    parser.add_argument("--check", action="store_true", help="fail if any bundled fixture requires evidence")
    args = parser.parse_args()
    paths = args.fixtures or default_fixture_paths()
    package = run(paths)
    text = json.dumps(package, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.check and package["evidence_required_count"]:
        print(f"FAIL: {package['evidence_required_count']} case(s) require evidence")
        return 1
    if args.check:
        print(f"PASS: {package['case_count']} human-power pressure case(s) complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
