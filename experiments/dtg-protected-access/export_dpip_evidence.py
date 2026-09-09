#!/usr/bin/env python3
"""Validate and export protected-access A/B runtime observations for DPIP."""
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
EVIDENCE_CLASSES = {"runtime-upstream-observation", "synthetic-fixture-self-test", "derived-analysis-artifact"}
KINDS = {"positive-control", "unlinkability-pressure-case"}
JOIN_CLASSES = {"identical", "derivably-related"}


def load_contract() -> dict[str, Any]:
    doc = yaml.safe_load(CONTRACT.read_text(encoding="utf-8")) or {}
    if not isinstance(doc.get("requirements"), dict):
        raise ValueError("runtime evidence contract has no requirements mapping")
    return doc


def validate_capture(capture: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if str(capture.get("evidence_class") or "") not in EVIDENCE_CLASSES:
        errors.append("invalid evidence_class")
    experiment = capture.get("experiment")
    if experiment is not None:
        if not isinstance(experiment, dict) or experiment.get("kind") not in KINDS:
            errors.append("invalid experiment.kind")
        elif experiment["kind"] == "positive-control" and experiment.get("expected_join") != "must-detect":
            errors.append("positive-control must expect join detection")
        elif experiment["kind"] == "unlinkability-pressure-case" and experiment.get("expected_join") != "must-not-emerge":
            errors.append("unlinkability pressure case must not expect a seeded join")
    provenance = capture.get("provenance")
    if not isinstance(provenance, dict):
        return errors + ["provenance must be a mapping"]
    for key in contract.get("required_provenance", []):
        if not str(provenance.get(key, "")).strip():
            errors.append(f"missing provenance.{key}")
    revision = str(provenance.get("implementation_revision") or "")
    if revision and not SHA40.fullmatch(revision):
        errors.append("provenance.implementation_revision must be an immutable 40-hex commit SHA")
    observations = capture.get("requirements")
    if not isinstance(observations, dict):
        return errors + ["requirements must be a mapping"]
    allowed = set(contract.get("classification_values", [])); origins = set(contract.get("correlator_origins", []))
    for rid, requirement in contract["requirements"].items():
        supplied = observations.get(rid)
        if not isinstance(supplied, dict):
            errors.append(f"missing runtime observation package for {rid}"); continue
        surfaces = supplied.get("surfaces")
        if not isinstance(surfaces, dict):
            errors.append(f"{rid}.surfaces must be a mapping"); continue
        for surface in requirement.get("surfaces", []):
            observation = surfaces.get(surface)
            if not isinstance(observation, dict):
                errors.append(f"{rid} missing surface {surface}"); continue
            classification = str(observation.get("classification") or "")
            if classification not in allowed:
                errors.append(f"{rid}.{surface} invalid classification")
            if classification not in {"absent", "not-evidenced"} and ("context_a" not in observation or "context_b" not in observation):
                errors.append(f"{rid}.{surface} requires A/B values")
            execution = observation.get("execution")
            if not isinstance(execution, dict) or execution.get("context_a") not in {"executed", "not-executed"} or execution.get("context_b") not in {"executed", "not-executed"}:
                errors.append(f"{rid}.{surface} invalid execution state")
            if origins and observation.get("correlator_origin") not in origins:
                errors.append(f"{rid}.{surface} invalid correlator_origin")
        if not str(supplied.get("observation_summary") or "").strip():
            errors.append(f"{rid}.observation_summary is required")
    return errors


def export_bindings(capture: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    errors = validate_capture(capture, contract)
    if errors:
        raise ValueError("; ".join(errors))
    provenance, evidence_class = capture["provenance"], capture["evidence_class"]
    descriptors = capture.get("context_descriptors") or {}
    observer = {"model": "distinct-verifier-contexts", "contexts": [
        {"id": "A", **(descriptors.get("A") or {})},
        {"id": "B", **(descriptors.get("B") or {})},
    ]}
    source_pins = [{"repository": provenance["implementation_repository"], "revision": provenance["implementation_revision"]}]
    bindings = []
    for rid, requirement in contract["requirements"].items():
        observed = capture["requirements"][rid]
        bindings.append({
            "schema": "interop-evidence-package/v1",
            "requirement_id": rid,
            "title": requirement.get("title"),
            "summary": requirement.get("summary"),
            "evidence_class": evidence_class,
            "experiment": capture.get("experiment"),
            "observer": observer,
            "provenance": {k: provenance[k] for k in contract.get("required_provenance", [])},
            "source_pins": source_pins,
            "observation_summary": observed["observation_summary"],
            "surfaces": observed["surfaces"],
        })
    return {"schema": "interop-evidence-bundle/v1", "experiment": capture.get("experiment"), "provided_evidence": bindings, "human_summary": {"title": "Protected-access A/B runtime evidence package", "explanation": "Bindings preserve observer context, experiment kind, execution state, correlator origin and immutable runtime provenance.", "boundary": "Export validity proves package structure and attribution, not privacy PASS or universal unlinkability. Positive-control joins are expected detector evidence."}}


def export_privacy_observability_result(
    capture: dict[str, Any],
    *,
    requirement_id: str,
    surface_names: list[str],
    experiment_id: str,
) -> dict[str, Any]:
    """Project selected A/B observations into DPIP's reusable privacy semantics.

    Generic producer identity, source pins and artifact provenance remain outside this
    DPIP result and belong to the RAHP producer envelope. This function owns only the
    bounded privacy observation and interpretation inputs.
    """
    if not surface_names:
        raise ValueError("privacy observability export requires at least one surface")
    requirements = capture.get("requirements")
    if not isinstance(requirements, dict) or not isinstance(requirements.get(requirement_id), dict):
        raise ValueError(f"missing runtime observation package for {requirement_id}")
    surfaces = requirements[requirement_id].get("surfaces")
    if not isinstance(surfaces, dict):
        raise ValueError(f"{requirement_id}.surfaces must be a mapping")
    selected: list[tuple[str, dict[str, Any]]] = []
    for name in surface_names:
        observation = surfaces.get(name)
        if not isinstance(observation, dict):
            raise ValueError(f"{requirement_id} missing selected privacy surface {name}")
        selected.append((name, observation))

    all_executed = all(
        isinstance(obs.get("execution"), dict)
        and obs["execution"].get("context_a") == "executed"
        and obs["execution"].get("context_b") == "executed"
        for _, obs in selected
    )
    join_surfaces = sorted(name for name, obs in selected if obs.get("classification") in JOIN_CLASSES)
    if not all_executed:
        result, signal, effective_join = "evidence-incomplete", "not-tested", False
    elif join_surfaces:
        result, signal, effective_join = "not-supported", "found", True
    else:
        result, signal, effective_join = "supported", "not-found", False

    experiment = capture.get("experiment") if isinstance(capture.get("experiment"), dict) else {}
    if experiment.get("kind") != "unlinkability-pressure-case":
        raise ValueError("DPIP privacy observability result requires an unlinkability-pressure-case, not a positive control")

    evidence_class = str(capture.get("evidence_class") or "")
    return {
        "schema": "dpip-privacy-observability-result/v1",
        "experiment": {
            "id": experiment_id,
            "privacy_proposition": "Across independently configured verifier contexts, the selected observed surfaces should not expose a stable join within this bounded A/B experiment.",
            "comparison": {"kind": "A/B", "scenarios": ["A", "B"]},
            "required_observer_planes": ["verifier"],
            "minimum_evidence_class": evidence_class,
            "reproducibility": "source-pinned",
        },
        "observer_planes": [{
            "id": "verifier",
            "direct_observables": surface_names,
            "derived_or_joinable": join_surfaces,
            "privilege": "ordinary",
            "threat_model": "in-scope",
            "composition_notes": [f"Selected from {requirement_id}; other observer planes are not measured by this result."],
        }],
        "correlation": {
            "signal": signal,
            "effective_join": effective_join,
            "composition": join_surfaces,
        },
        "result": result,
        "executed": all_executed,
        "unsupported_inference": [
            "deployment-wide unlinkability",
            "host, network, device, audit, or privileged-observer unlinkability",
            "terminal assurance PASS",
        ],
        "residual_uncertainty": [
            "The result is limited to the selected surfaces and declared verifier observer plane.",
            "Other implementations, revisions, deployments and observer planes require independent evidence.",
        ],
    }


def self_test() -> int:
    contract = load_contract()
    capture: dict[str, Any] = {"evidence_class": "synthetic-fixture-self-test", "experiment": {"kind": "unlinkability-pressure-case", "expected_join": "must-not-emerge", "observed_join": "not-detected", "join_surfaces": []}, "context_descriptors": {"A": {"verifier": "v-a", "purpose": "p-a", "challenge": "c-a"}, "B": {"verifier": "v-b", "purpose": "p-b", "challenge": "c-b"}}, "provenance": {"producer": "trust-protocol-interop-lab", "run_id": "test-run-001", "observed_at": "2026-08-30T00:00:00Z", "implementation_repository": "example/runtime", "implementation_revision": "a" * 40, "context_a_run": "context-a-001", "context_b_run": "context-b-001"}, "requirements": {}}
    for rid, req in contract["requirements"].items():
        capture["requirements"][rid] = {"observation_summary": f"Self-test {rid}", "surfaces": {s: {"classification": "not-evidenced", "execution": {"context_a": "not-executed", "context_b": "not-executed"}, "correlator_origin": "none", "producer_component": "self-test"} for s in req.get("surfaces", [])}}
    assert validate_capture(capture, contract) == []
    result = export_bindings(capture, contract)
    assert len(result["provided_evidence"]) == len(contract["requirements"])
    credential = next(x for x in result["provided_evidence"] if x["requirement_id"] == "ER-CREDENTIAL-ID-AB")
    assert credential["schema"] == "interop-evidence-package/v1"
    assert len(credential["observer"]["contexts"]) == 2
    assert credential["source_pins"][0]["revision"] == "a" * 40
    privacy = export_privacy_observability_result(
        capture,
        requirement_id="ER-STATUS-AB",
        surface_names=["policy_discovery_handle", "policy_endpoint"],
        experiment_id="self-test-policy-discovery-ab",
    )
    assert privacy["schema"] == "dpip-privacy-observability-result/v1"
    assert privacy["result"] == "evidence-incomplete"
    print("PASS observer-bound DPIP runtime evidence exporter self-test")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("capture", type=Path, nargs="?")
    p.add_argument("--output", type=Path)
    p.add_argument("--privacy-output", type=Path)
    p.add_argument("--privacy-requirement")
    p.add_argument("--privacy-surfaces")
    p.add_argument("--privacy-experiment-id")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        return self_test()
    if not args.capture:
        p.error("capture is required unless --self-test is used")
    text = args.capture.read_text(encoding="utf-8")
    capture = json.loads(text) if args.capture.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(capture, dict):
        raise SystemExit("capture must be a mapping")
    rendered = json.dumps(export_bindings(capture, load_contract()), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    elif not args.privacy_output:
        print(rendered, end="")

    if args.privacy_output:
        if not args.privacy_requirement or not args.privacy_surfaces or not args.privacy_experiment_id:
            p.error("--privacy-output requires --privacy-requirement, --privacy-surfaces and --privacy-experiment-id")
        privacy = export_privacy_observability_result(
            capture,
            requirement_id=args.privacy_requirement,
            surface_names=[x.strip() for x in args.privacy_surfaces.split(",") if x.strip()],
            experiment_id=args.privacy_experiment_id,
        )
        args.privacy_output.parent.mkdir(parents=True, exist_ok=True)
        args.privacy_output.write_text(json.dumps(privacy, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
