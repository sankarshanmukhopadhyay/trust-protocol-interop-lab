#!/usr/bin/env python3
"""Execute and validate one characterized current OpenVTC A/B evidence-export member.

The runner deliberately supports only the two-artifact `evidence-export` boundary. A
member with deeper specialist integration (currently Track B policy) fails closed so
workflow consolidation cannot silently drop DPIP/RAHP semantics.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CHARACTERIZATION = ROOT / "evidence" / "workflow-characterization" / "current-openvtc-ab-family.yaml"
CAPTURE = ROOT / "experiments" / "dtg-protected-access" / "capture_ab_runtime.py"
EXPORT = ROOT / "experiments" / "dtg-protected-access" / "export_dpip_evidence.py"


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a mapping")
    return value


def member_contract(name: str) -> tuple[dict[str, Any], dict[str, Any]]:
    model = load_yaml(CHARACTERIZATION)
    member = (model.get("members") or {}).get(name)
    if not isinstance(member, dict):
        raise ValueError(f"unknown characterized member: {name}")
    if member.get("integration_depth") != "evidence-export":
        raise ValueError(
            f"member {name} has integration_depth={member.get('integration_depth')!r}; "
            "the reusable evidence-export runner must not discard deeper specialist semantics"
        )
    return model["shared"], member


def target_contract(shared: dict[str, Any], member: dict[str, Any]) -> tuple[str, str]:
    repository = str(member.get("implementation_repository") or shared["implementation_repository"])
    revision = str(member.get("implementation_revision") or shared["implementation_revision"])
    return repository, revision


def validate_capture(shared: dict[str, Any], member: dict[str, Any], doc: dict[str, Any]) -> None:
    expected_repository, expected_revision = target_contract(shared, member)
    provenance = doc.get("provenance") or {}
    if provenance.get("implementation_repository") != expected_repository:
        raise ValueError("capture implementation repository does not match characterization")
    if provenance.get("implementation_revision") != expected_revision:
        raise ValueError("capture implementation revision does not match characterization")
    experiment = doc.get("experiment") or {}
    if experiment.get("observed_join") != member["observed_join"]:
        raise ValueError(
            f"observed_join={experiment.get('observed_join')!r}; expected {member['observed_join']!r}"
        )

    requirements = doc.get("requirements") or {}
    for requirement_id, surface_expectations in (member.get("expectations") or {}).items():
        surfaces = ((requirements.get(requirement_id) or {}).get("surfaces") or {})
        if "*" in surface_expectations:
            expected = surface_expectations["*"]
            if not surfaces:
                raise ValueError(f"{requirement_id} has no surfaces to characterize")
            for surface_name, surface in surfaces.items():
                if surface.get("classification") != expected.get("classification"):
                    raise ValueError(
                        f"{requirement_id}.{surface_name}.classification={surface.get('classification')!r}; "
                        f"expected {expected.get('classification')!r}"
                    )
            continue

        for surface_name, expected in surface_expectations.items():
            surface = surfaces.get(surface_name)
            if not isinstance(surface, dict):
                raise ValueError(f"missing characterized surface {requirement_id}.{surface_name}")
            for key, expected_value in expected.items():
                if key == "context_a_execution":
                    actual = (surface.get("execution") or {}).get("context_a")
                elif key == "context_b_execution":
                    actual = (surface.get("execution") or {}).get("context_b")
                else:
                    actual = surface.get(key)
                if actual != expected_value:
                    raise ValueError(
                        f"{requirement_id}.{surface_name}.{key}={actual!r}; expected {expected_value!r}"
                    )


def run_checked(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")


def execute(member_name: str, output_dir: Path) -> tuple[Path, Path]:
    shared, member = member_contract(member_name)
    expected_repository, expected_revision = target_contract(shared, member)
    manifest = ROOT / member["manifest"]
    manifest_doc = load_yaml(manifest)
    implementation = manifest_doc.get("implementation") or {}
    experiment = manifest_doc.get("experiment") or {}
    if implementation.get("repository") != expected_repository:
        raise ValueError("manifest repository differs from member characterization")
    if implementation.get("revision") != expected_revision:
        raise ValueError("manifest revision differs from member characterization")
    if experiment.get("kind") != member["experiment_kind"]:
        raise ValueError("manifest experiment kind differs from member characterization")
    if experiment.get("expected_join") != member["expected_join"]:
        raise ValueError("manifest expected_join differs from member characterization")

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_names = member.get("expected_artifacts") or []
    if len(artifact_names) != 2:
        raise ValueError(f"member {member_name} must characterize exactly two evidence-export artifacts")
    capture_path = output_dir / artifact_names[0]
    export_path = output_dir / artifact_names[1]

    run_checked([sys.executable, str(CAPTURE.relative_to(ROOT)), str(manifest.relative_to(ROOT)), "--output", str(capture_path)])
    capture = load_yaml(capture_path)
    validate_capture(shared, member, capture)
    run_checked([sys.executable, str(EXPORT.relative_to(ROOT)), str(capture_path), "--output", str(export_path)])
    if not export_path.is_file() or not export_path.stat().st_size:
        raise RuntimeError("DPIP compatibility export was not produced")
    return capture_path, export_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--member", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--check-contract", action="store_true", help="validate member support without executing target commands")
    args = parser.parse_args()
    try:
        shared, member = member_contract(args.member)
        expected_repository, expected_revision = target_contract(shared, member)
        if args.check_contract:
            manifest = load_yaml(ROOT / member["manifest"])
            assert manifest["implementation"]["repository"] == expected_repository
            assert manifest["implementation"]["revision"] == expected_revision
            print(f"PASS characterized reusable member {args.member}: {expected_repository}@{expected_revision}")
            return 0
        capture, export = execute(args.member, args.output_dir)
        print(f"PASS {args.member}: {capture} {export}")
        return 0
    except (AssertionError, KeyError, ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
