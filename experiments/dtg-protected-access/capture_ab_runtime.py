#!/usr/bin/env python3
"""Run two relying contexts and emit a provenance-bound A/B capture document.

The harness is deliberately an evidence producer, not a privacy evaluator. It executes
one command per relying context, reads each command's JSON observation document,
classifies named surfaces across A/B, and writes the capture contract consumed by
export_dpip_evidence.py.

A command succeeds only when it emits JSON with an `observations` mapping. The harness
never converts absence of a correlator into privacy PASS; it records only observation
classifications. Synthetic/self-test execution is explicitly marked and cannot be
mistaken for upstream runtime evidence.
"""
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
        raise RuntimeError(
            f"context {name} command failed ({completed.returncode}): {completed.stderr.strip()}"
        )
    try:
        doc = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"context {name} did not emit JSON: {exc}") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("observations"), dict):
        raise ValueError(f"context {name} output must contain an observations mapping")
    return doc


def classify(a: Any, b: Any, derivation: str | None = None) -> str:
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
    if not repository:
        raise ValueError("implementation.repository is required")
    if not SHA40.fullmatch(revision):
        raise ValueError("implementation.revision must be an immutable 40-hex commit SHA")

    contexts = manifest.get("contexts")
    if not isinstance(contexts, dict) or not isinstance(contexts.get("A"), dict) or not isinstance(contexts.get("B"), dict):
        raise ValueError("contexts.A and contexts.B are required")
    if contexts["A"].get("verifier") == contexts["B"].get("verifier"):
        raise ValueError("contexts A/B must use distinct verifier identifiers")
    if contexts["A"].get("purpose") == contexts["B"].get("purpose"):
        raise ValueError("contexts A/B must use distinct purpose values")
    if contexts["A"].get("challenge") == contexts["B"].get("challenge"):
        raise ValueError("contexts A/B must use distinct challenge values")

    a_doc = run_context("A", contexts["A"])
    b_doc = run_context("B", contexts["B"])
    contract = load_yaml(CONTRACT)
    requirements: dict[str, Any] = {}
    derivations = manifest.get("derivations", {})
    if not isinstance(derivations, dict):
        derivations = {}

    for rid, requirement in contract["requirements"].items():
        surfaces: dict[str, Any] = {}
        for surface in requirement.get("surfaces", []):
            a_value = a_doc["observations"].get(surface)
            b_value = b_doc["observations"].get(surface)
            derivation = derivations.get(surface)
            entry: dict[str, Any] = {
                "classification": classify(a_value, b_value, str(derivation) if derivation else None)
            }
            if a_value is not None:
                entry["context_a"] = a_value
            if b_value is not None:
                entry["context_b"] = b_value
            if derivation:
                entry["derivation_basis"] = derivation
            surfaces[surface] = entry
        requirements[rid] = {
            "observation_summary": (
                f"A/B capture for {rid}; classifications describe observed join surfaces only "
                "and are not a DPIP privacy conclusion."
            ),
            "surfaces": surfaces,
        }

    run_id = str(manifest.get("run_id") or f"ab-{uuid.uuid4()}")
    observed_at = str(manifest.get("observed_at") or datetime.now(timezone.utc).isoformat())
    return {
        "evidence_class": evidence_class,
        "provenance": {
            "producer": "trust-protocol-interop-lab",
            "run_id": run_id,
            "observed_at": observed_at,
            "implementation_repository": repository,
            "implementation_revision": revision,
            "context_a_run": str(a_doc.get("run_id") or f"{run_id}-A"),
            "context_b_run": str(b_doc.get("run_id") or f"{run_id}-B"),
        },
        "context_descriptors": {
            "A": {k: contexts["A"].get(k) for k in ("verifier", "purpose", "challenge")},
            "B": {k: contexts["B"].get(k) for k in ("verifier", "purpose", "challenge")},
        },
        "requirements": requirements,
        "assurance_boundary": (
            "This capture records runtime observations. It does not establish privacy PASS, "
            "unlinkability, or DPIP evidence sufficiency."
        ),
    }


def self_test() -> int:
    fixture = ROOT / "cases" / "dtg-protected-access" / "runtime-ab-harness.selftest.yaml"
    capture = build_capture(load_yaml(fixture))
    assert capture["evidence_class"] == "synthetic-fixture-self-test"
    rel = capture["requirements"]["ER-REL-DID-AB"]["surfaces"]["relationship_did"]
    assert rel["classification"] == "identical"
    verifier = capture["requirements"]["ER-VERIFIER-AB"]["surfaces"]["challenge"]
    assert verifier["classification"] == "fresh"
    print("PASS protected-access two-context capture harness self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.manifest:
        parser.error("manifest is required unless --self-test is used")
    capture = build_capture(load_yaml(args.manifest))
    rendered = yaml.safe_dump(capture, sort_keys=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
