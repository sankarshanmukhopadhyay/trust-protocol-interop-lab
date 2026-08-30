#!/usr/bin/env python3
"""Run two contexts and emit provenance-bound A/B evidence without making a privacy judgment."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import uuid
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "cases" / "dtg-protected-access" / "dpip-runtime-evidence-contract.yaml"
ALLOWED_CLASSES = {"runtime-upstream-observation", "synthetic-fixture-self-test"}
EXPERIMENT_KINDS = {"positive-control", "unlinkability-pressure-case"}
ORIGINS = {"fixture-supplied", "target-derived", "composition-derived", "retained", "observer-derived", "none", "unknown"}
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)


def load_yaml(path: Path) -> dict[str, Any]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(doc, dict):
        raise ValueError(f"{path} must contain a mapping")
    return doc


def run_context(name: str, config: dict[str, Any]) -> dict[str, Any]:
    command = config.get("command")
    if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
        raise ValueError(f"context {name}.command must be a non-empty string array")
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"context {name} command failed ({completed.returncode}): {completed.stderr.strip()}")
    try:
        doc = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context {name} did not emit JSON: {exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("observations"), dict):
        raise ValueError(f"context {name} output must contain an observations mapping")
    executed = doc.get("executed_surfaces", [])
    if executed is not None and (not isinstance(executed, list) or not all(isinstance(x, str) for x in executed)):
        raise ValueError(f"context {name}.executed_surfaces must be a string array")
    return doc


def surface_executed(doc: dict[str, Any], surface: str) -> bool:
    explicit = doc.get("executed_surfaces")
    if isinstance(explicit, list):
        return surface in explicit
    return surface in doc.get("observations", {})


def classify(a: Any, b: Any, a_executed: bool, b_executed: bool, derivation: str | None = None) -> str:
    if not a_executed or not b_executed:
        return "not-evidenced"
    if a is None and b is None:
        return "absent"
    if a is None or b is None:
        return "not-evidenced"
    if a == b:
        return "identical"
    if derivation:
        return "derivably-related"
    return "fresh"


def build_capture(manifest: dict[str, Any]) -> dict[str, Any]:
    evidence_class = str(manifest.get("evidence_class") or "")
    if evidence_class not in ALLOWED_CLASSES:
        raise ValueError(f"evidence_class must be one of {sorted(ALLOWED_CLASSES)}")
    implementation = manifest.get("implementation")
    if not isinstance(implementation, dict):
        raise ValueError("implementation must be a mapping")
    repository = str(implementation.get("repository") or "").strip()
    revision = str(implementation.get("revision") or "").strip()
    if not repository or not SHA40.fullmatch(revision):
        raise ValueError("implementation requires repository and immutable 40-hex revision")

    experiment = manifest.get("experiment")
    if not isinstance(experiment, dict):
        raise ValueError("experiment is required and must explicitly declare kind and expected_join")
    if experiment.get("kind") not in EXPERIMENT_KINDS:
        raise ValueError(f"experiment.kind must be one of {sorted(EXPERIMENT_KINDS)}")
    expected = "must-detect" if experiment["kind"] == "positive-control" else "must-not-emerge"
    if experiment.get("expected_join", expected) != expected:
        raise ValueError(f"{experiment['kind']} requires expected_join={expected}")

    contexts = manifest.get("contexts")
    if not isinstance(contexts, dict) or not isinstance(contexts.get("A"), dict) or not isinstance(contexts.get("B"), dict):
        raise ValueError("contexts.A and contexts.B are required")
    for key in ("verifier", "purpose", "challenge"):
        if contexts["A"].get(key) == contexts["B"].get(key):
            raise ValueError(f"contexts A/B must use distinct {key} values")

    a_doc, b_doc = run_context("A", contexts["A"]), run_context("B", contexts["B"])
    contract = load_yaml(CONTRACT)
    requirements: dict[str, Any] = {}
    derivations = manifest.get("derivations", {}) if isinstance(manifest.get("derivations", {}), dict) else {}
    origins = manifest.get("correlator_origins", {}) if isinstance(manifest.get("correlator_origins", {}), dict) else {}
    producers = manifest.get("surface_producers", {}) if isinstance(manifest.get("surface_producers", {}), dict) else {}
    join_surfaces: list[str] = []

    for rid, requirement in contract["requirements"].items():
        surfaces: dict[str, Any] = {}
        for surface in requirement.get("surfaces", []):
            a_value, b_value = a_doc["observations"].get(surface), b_doc["observations"].get(surface)
            a_exec, b_exec = surface_executed(a_doc, surface), surface_executed(b_doc, surface)
            derivation = derivations.get(surface)
            classification = classify(a_value, b_value, a_exec, b_exec, str(derivation) if derivation else None)
            origin = str(origins.get(surface, "unknown" if classification in {"identical", "derivably-related"} else "none"))
            if experiment["kind"] == "positive-control" and classification in {"identical", "derivably-related"} and origin == "unknown":
                raise ValueError(f"positive-control join surface {surface} requires explicit correlator origin")
            if origin not in ORIGINS:
                raise ValueError(f"invalid correlator origin for {surface}: {origin}")
            entry: dict[str, Any] = {
                "classification": classification,
                "execution": {"context_a": "executed" if a_exec else "not-executed", "context_b": "executed" if b_exec else "not-executed"},
                "correlator_origin": origin,
                "producer_component": str(producers.get(surface, a_doc.get("producer_component") or b_doc.get("producer_component") or repository)),
            }
            if a_value is not None: entry["context_a"] = a_value
            if b_value is not None: entry["context_b"] = b_value
            if derivation: entry["derivation_basis"] = derivation
            if classification in {"identical", "derivably-related"}: join_surfaces.append(surface)
            surfaces[surface] = entry
        requirements[rid] = {"observation_summary": f"A/B capture for {rid}; execution and correlator attribution are evidence, not a privacy conclusion.", "surfaces": surfaces}

    run_id = str(manifest.get("run_id") or f"ab-{uuid.uuid4()}")
    observed_at = str(manifest.get("observed_at") or datetime.now(timezone.utc).isoformat())
    return {
        "evidence_class": evidence_class,
        "experiment": {"kind": experiment["kind"], "expected_join": expected, "observed_join": "detected" if join_surfaces else "not-detected", "join_surfaces": sorted(set(join_surfaces))},
        "provenance": {"producer": "trust-protocol-interop-lab", "run_id": run_id, "observed_at": observed_at, "implementation_repository": repository, "implementation_revision": revision, "context_a_run": str(a_doc.get("run_id") or f"{run_id}-A"), "context_b_run": str(b_doc.get("run_id") or f"{run_id}-B")},
        "context_descriptors": {"A": {k: contexts["A"].get(k) for k in ("verifier", "purpose", "challenge")}, "B": {k: contexts["B"].get(k) for k in ("verifier", "purpose", "challenge")}},
        "requirements": requirements,
        "assurance_boundary": "This capture records runtime observations and attribution. Positive-control joins are expected. It does not establish privacy PASS, unlinkability, or target-level fault.",
    }


def self_test() -> int:
    fixture = ROOT / "cases" / "dtg-protected-access" / "runtime-ab-harness.selftest.yaml"
    capture = build_capture(load_yaml(fixture))
    assert capture["evidence_class"] == "synthetic-fixture-self-test"
    assert capture["requirements"]["ER-REL-DID-AB"]["surfaces"]["relationship_did"]["classification"] == "identical"
    assert capture["requirements"]["ER-VERIFIER-AB"]["surfaces"]["challenge"]["classification"] == "fresh"
    assert capture["experiment"]["kind"] == "positive-control"
    assert capture["experiment"]["expected_join"] == "must-detect"
    assert capture["experiment"]["observed_join"] == "detected"
    print("PASS protected-access two-context capture harness self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test: return self_test()
    if not args.manifest: parser.error("manifest is required unless --self-test is used")
    rendered = yaml.safe_dump(build_capture(load_yaml(args.manifest)), sort_keys=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(rendered, encoding="utf-8")
    else: print(rendered, end="")
    return 0

if __name__ == "__main__":
    try: raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); raise SystemExit(2)
