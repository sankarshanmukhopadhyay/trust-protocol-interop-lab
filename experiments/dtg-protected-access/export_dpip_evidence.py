#!/usr/bin/env python3
"""Validate and export protected-access A/B runtime observations for DPIP.

This exporter does not manufacture runtime evidence. It accepts an externally captured
A/B observation document, verifies that each declared DPIP evidence requirement has
attributable provenance and explicit surface classifications, and emits typed
`provided_evidence` bindings suitable for a comparable RAHP→DPIP examination.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "cases" / "dtg-protected-access" / "dpip-runtime-evidence-contract.yaml"
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)


def load_contract() -> dict[str, Any]:
    doc = yaml.safe_load(CONTRACT.read_text(encoding="utf-8")) or {}
    if not isinstance(doc.get("requirements"), dict):
        raise ValueError("runtime evidence contract has no requirements mapping")
    return doc


def validate_capture(capture: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    provenance = capture.get("provenance")
    if not isinstance(provenance, dict):
        return ["provenance must be a mapping"]
    for key in contract.get("required_provenance", []):
        if not str(provenance.get(key, "")).strip():
            errors.append(f"missing provenance.{key}")
    revision = str(provenance.get("implementation_revision") or "")
    if revision and not SHA40.fullmatch(revision):
        errors.append("provenance.implementation_revision must be an immutable 40-hex commit SHA")

    observations = capture.get("requirements")
    if not isinstance(observations, dict):
        return errors + ["requirements must be a mapping"]
    allowed = set(contract.get("classification_values", []))
    for rid, requirement in contract["requirements"].items():
        supplied = observations.get(rid)
        if not isinstance(supplied, dict):
            errors.append(f"missing runtime observation package for {rid}")
            continue
        surfaces = supplied.get("surfaces")
        if not isinstance(surfaces, dict):
            errors.append(f"{rid}.surfaces must be a mapping")
            continue
        for surface in requirement.get("surfaces", []):
            observation = surfaces.get(surface)
            if not isinstance(observation, dict):
                errors.append(f"{rid} missing surface {surface}")
                continue
            classification = str(observation.get("classification") or "")
            if classification not in allowed:
                errors.append(f"{rid}.{surface} has invalid classification: {classification or '<missing>'}")
            if classification not in {"absent", "not-evidenced"}:
                if "context_a" not in observation or "context_b" not in observation:
                    errors.append(f"{rid}.{surface} requires context_a and context_b values")
        if not str(supplied.get("observation_summary") or "").strip():
            errors.append(f"{rid}.observation_summary is required")
    return errors


def export_bindings(capture: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    errors = validate_capture(capture, contract)
    if errors:
        raise ValueError("; ".join(errors))
    provenance = capture["provenance"]
    bindings = []
    for rid, requirement in contract["requirements"].items():
        observed = capture["requirements"][rid]
        bindings.append({
            "requirement_id": rid,
            "title": requirement.get("title"),
            "summary": requirement.get("summary"),
            "provenance": {
                "producer": provenance["producer"],
                "run_id": provenance["run_id"],
                "observed_at": provenance["observed_at"],
                "implementation_repository": provenance["implementation_repository"],
                "implementation_revision": provenance["implementation_revision"],
                "context_a_run": provenance["context_a_run"],
                "context_b_run": provenance["context_b_run"],
            },
            "observation_summary": observed["observation_summary"],
            "surfaces": observed["surfaces"],
        })
    return {
        "provided_evidence": bindings,
        "human_summary": {
            "title": "Protected-access A/B runtime evidence package",
            "explanation": "Each binding below corresponds to one named DPIP evidence requirement and carries immutable implementation provenance plus explicit observations from relying contexts A and B.",
            "boundary": "Export validity proves evidence-package structure and provenance, not a privacy PASS or universal unlinkability claim.",
        },
    }


def self_test() -> int:
    contract = load_contract()
    classifications = contract["classification_values"]
    assert "not-evidenced" in classifications
    capture: dict[str, Any] = {
        "provenance": {
            "producer": "trust-protocol-interop-lab",
            "run_id": "test-run-001",
            "observed_at": "2026-08-30T00:00:00Z",
            "implementation_repository": "example/runtime",
            "implementation_revision": "a" * 40,
            "context_a_run": "context-a-001",
            "context_b_run": "context-b-001",
        },
        "requirements": {},
    }
    for rid, req in contract["requirements"].items():
        capture["requirements"][rid] = {
            "observation_summary": f"Self-test observation package for {rid}",
            "surfaces": {surface: {"classification": "not-evidenced"} for surface in req.get("surfaces", [])},
        }
    assert validate_capture(capture, contract) == []
    result = export_bindings(capture, contract)
    assert len(result["provided_evidence"]) == len(contract["requirements"])
    assert result["provided_evidence"][0]["title"]
    bad = json.loads(json.dumps(capture))
    del bad["provenance"]["context_b_run"]
    assert any("context_b_run" in e for e in validate_capture(bad, contract))
    print("PASS protected-access DPIP runtime evidence exporter self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path, nargs="?", help="JSON or YAML A/B runtime capture")
    parser.add_argument("--output", type=Path, help="write exported JSON evidence bindings")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.capture:
        parser.error("capture is required unless --self-test is used")
    text = args.capture.read_text(encoding="utf-8")
    capture = json.loads(text) if args.capture.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(capture, dict):
        raise SystemExit("capture must be a mapping")
    result = export_bindings(capture, load_contract())
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
