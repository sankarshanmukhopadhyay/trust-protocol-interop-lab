#!/usr/bin/env python3
"""Execute the #237/#240 paired A/B composition cases and write DPIP-ready evidence."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
import yaml

ROOT = Path(__file__).resolve().parents[2]
CAPTURE = ROOT / "experiments" / "dtg-protected-access" / "capture_ab_runtime.py"
EXPORT = ROOT / "experiments" / "dtg-protected-access" / "export_dpip_evidence.py"
CONTEXT = ROOT / "experiments" / "dtg-protected-access" / "composed_context.py"


def context_command(context: str, mode: str) -> list[str]:
    return ["python", str(CONTEXT.relative_to(ROOT)), "--context", context, "--mode", mode]


def manifest(revision: str, kind: str, mode: str, origins: dict[str, str]) -> dict:
    return {
        "evidence_class": "runtime-upstream-observation",
        "implementation": {"repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab", "revision": revision},
        "experiment": {"kind": kind, "expected_join": "must-detect" if kind == "positive-control" else "must-not-emerge"},
        "contexts": {
            "A": {"verifier": "verifier-A", "purpose": "purpose-A", "challenge": "challenge-A", "command": context_command("A", mode)},
            "B": {"verifier": "verifier-B", "purpose": "purpose-B", "challenge": "challenge-B", "command": context_command("B", mode)},
        },
        "correlator_origins": origins,
        "surface_producers": {
            "status_handle": "interop-lab/status-policy-composition",
            "status_endpoint": "interop-lab/status-policy-composition",
            "policy_discovery_handle": "interop-lab/status-policy-composition",
            "policy_endpoint": "interop-lab/status-policy-composition",
            "task_identifier": "interop-lab/trust-task-composition",
            "thread_identifier": "interop-lab/trust-task-composition",
            "retained_relationship_evidence": "interop-lab/trust-task-retention",
            "retained_outcome_evidence": "interop-lab/trust-task-retention",
        },
    }


def execute_case(out: Path, revision: str, name: str, kind: str, mode: str, origins: dict[str, str]) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    m = manifest(revision, kind, mode, origins)
    manifest_path = out / f"{name}-manifest.yaml"
    capture_path = out / f"{name}-capture.yaml"
    export_path = out / f"{name}-provided-evidence.json"
    manifest_path.write_text(yaml.safe_dump(m, sort_keys=False), encoding="utf-8")
    subprocess.run(["python", str(CAPTURE.relative_to(ROOT)), str(manifest_path), "--output", str(capture_path)], cwd=ROOT, check=True)
    subprocess.run(["python", str(EXPORT.relative_to(ROOT)), str(capture_path), "--output", str(export_path)], cwd=ROOT, check=True)
    return yaml.safe_load(capture_path.read_text(encoding="utf-8"))


def assert_all_executed(capture: dict, rid: str) -> None:
    for surface, entry in capture["requirements"][rid]["surfaces"].items():
        assert entry["execution"] == {"context_a": "executed", "context_b": "executed"}, (rid, surface, entry)
        assert entry["classification"] != "not-evidenced", (rid, surface, entry)


def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("--output-dir", type=Path); p.add_argument("--revision", default=os.environ.get("GITHUB_SHA")); args = p.parse_args()
    revision = args.revision or "a" * 40
    if len(revision) != 40: raise SystemExit("--revision must be a 40-character commit SHA")
    output = args.output_dir or Path(tempfile.mkdtemp(prefix="composed-ab-"))

    positive = execute_case(output, revision, "positive-control", "positive-control", "positive-control", {
        "relationship_did": "fixture-supplied",
        "equivalent_relationship_binder": "fixture-supplied",
        "deliberate_join_attempt": "fixture-supplied",
    })
    assert positive["experiment"]["observed_join"] == "detected"
    assert "relationship_did" in positive["experiment"]["join_surfaces"]
    assert positive["requirements"]["ER-REL-DID-AB"]["surfaces"]["relationship_did"]["correlator_origin"] == "fixture-supplied"

    pressure = execute_case(output, revision, "unlinkability-pressure", "unlinkability-pressure-case", "unlinkability", {})
    for rid in ("ER-REL-DID-AB", "ER-STATUS-AB", "ER-TASK-AB", "ER-VERIFIER-AB"):
        assert_all_executed(pressure, rid)
        for entry in pressure["requirements"][rid]["surfaces"].values():
            assert entry["classification"] == "fresh", (rid, entry)

    falsification = execute_case(output, revision, "status-falsification", "unlinkability-pressure-case", "status-falsification", {"status_handle": "composition-derived"})
    status = falsification["requirements"]["ER-STATUS-AB"]["surfaces"]["status_handle"]
    assert status["classification"] == "identical"
    assert status["correlator_origin"] == "composition-derived"

    # Regression: an unexecuted surface must remain not-evidenced; executed+None may be absent.
    import importlib.util
    spec = importlib.util.spec_from_file_location("capture_ab_runtime", CAPTURE); module = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(module)
    assert module.classify(None, None, False, False) == "not-evidenced"
    assert module.classify(None, None, True, True) == "absent"
    assert module.classify("same", "same", True, True) == "identical"

    summary = {
        "positive_control": positive["experiment"],
        "unlinkability_pressure": pressure["experiment"],
        "falsification": falsification["experiment"],
        "evidence_boundary": "Status/policy and Trust Task observations are produced by the executable Interop Lab composition. They are composition evidence and are not attributed to any target implementation unless that target actually produced those surfaces.",
        "requirements_materially_exercised": [
            "ER-REL-DID-AB", "ER-STATUS-AB", "ER-TASK-AB", "ER-VERIFIER-AB"
        ],
    }
    (output / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASS paired A/B composition: all four privacy evidence requirements, positive control, distinct-context pressure case, falsification vector, and execution-state regression")
    print(json.dumps(summary, sort_keys=True))
    return 0

if __name__ == "__main__": raise SystemExit(main())
