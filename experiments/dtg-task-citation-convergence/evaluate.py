#!/usr/bin/env python3
"""Evaluate the DTG task-citation / completion-evidence convergence boundary.

Issue: #233
RAHP coordination: sankarshanmukhopadhyay/rahp-toolkit#690

The evaluator deliberately separates credential validity, citation identity,
exact initiating-document binding, Trust Task completion, action authorization,
and presentation correlation.

Only Trust Tasks PR #17 is treated as adopted source semantics. Credential PR
#56, VTI PR #33, and ZKP PR #11 are candidate semantics and must not be promoted
into target-runtime evidence merely because fixtures can model them.

The output is deterministic and JSON-serializable so RAHP and DPIP can consume
it without reinterpreting the experiment.
"""
from __future__ import annotations

from enum import Enum
from typing import Any


class Classification(str, Enum):
    SUPPORTED = "supported"
    DIVERGENT = "divergent"
    NOT_IMPLEMENTED = "not-implemented"
    NOT_OBSERVABLE = "not-observable"


class TriState(str, Enum):
    CONFIRMED = "confirmed"
    CONTRADICTED = "contradicted"
    UNRESOLVED = "unresolved"


AUTHORITY_STATE = {
    "trust_tasks_17": "merged",
    "credential_56": "open-proposal",
    "vti_33": "open-proposal",
    "zkp_11": "open-proposal",
}

def _bool(observations: dict[str, Any], key: str) -> bool | None:
    value = observations.get(key)
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be boolean when supplied")
    return value


def _require_vector_id(vector: dict[str, Any]) -> str:
    vector_id = str(vector.get("id") or "").strip()
    if not vector_id:
        raise ValueError("vector id is required")
    return vector_id


def evaluate_vector(vector: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one vector without converting missing observations into PASS."""

    vector_id = _require_vector_id(vector)
    surface = str(vector.get("surface") or "fixture")
    if surface not in {"fixture", "target-runtime"}:
        raise ValueError(f"{vector_id}: unsupported surface {surface!r}")

    runtime_available = _bool(vector, "runtime_available")
    observable = _bool(vector, "observable")
    if surface == "target-runtime":
        if runtime_available is False:
            return {
                "id": vector_id,
                "classification": Classification.NOT_IMPLEMENTED.value,
                "surface": surface,
                "credential_validity": TriState.UNRESOLVED.value,
                "citation_binding": TriState.UNRESOLVED.value,
                "completion": TriState.UNRESOLVED.value,
                "authorization": TriState.UNRESOLVED.value,
                "correlation": TriState.UNRESOLVED.value,
                "reason": "target runtime does not expose the required path",
            }
        if observable is False:
            return {
                "id": vector_id,
                "classification": Classification.NOT_OBSERVABLE.value,
                "surface": surface,
                "credential_validity": TriState.UNRESOLVED.value,
                "citation_binding": TriState.UNRESOLVED.value,
                "completion": TriState.UNRESOLVED.value,
                "authorization": TriState.UNRESOLVED.value,
                "correlation": TriState.UNRESOLVED.value,
                "reason": "target path exists but required observations are unavailable",
            }

    credential_valid = _bool(vector, "credential_valid")
    context_matches = _bool(vector, "task_context_matches")
    digest_matches = _bool(vector, "task_digest_matches")
    outcome_present = _bool(vector, "outcome_evidence_present")
    outcome_valid = _bool(vector, "outcome_evidence_valid")
    completion_required = _bool(vector, "completion_required")
    action_authorized = _bool(vector, "action_authorized")
    visible_citation = _bool(vector, "visible_citation")
    same_citation_across_contexts = _bool(vector, "same_citation_across_contexts")

    credential_state = (
        TriState.UNRESOLVED if credential_valid is None
        else TriState.CONFIRMED if credential_valid
        else TriState.CONTRADICTED
    )

    if context_matches is None or digest_matches is None:
        citation_state = TriState.UNRESOLVED
    elif context_matches and digest_matches:
        citation_state = TriState.CONFIRMED
    else:
        citation_state = TriState.CONTRADICTED

    if completion_required is False:
        completion_state = TriState.UNRESOLVED
    elif outcome_present is None or outcome_valid is None:
        completion_state = TriState.UNRESOLVED
    elif outcome_present and outcome_valid and citation_state == TriState.CONFIRMED:
        completion_state = TriState.CONFIRMED
    else:
        completion_state = TriState.CONTRADICTED

    if action_authorized is None:
        authorization_state = TriState.UNRESOLVED
    elif action_authorized:
        authorization_state = TriState.CONFIRMED
    else:
        authorization_state = TriState.CONTRADICTED

    if visible_citation is None or same_citation_across_contexts is None:
        correlation_state = TriState.UNRESOLVED
    elif visible_citation and same_citation_across_contexts:
        correlation_state = TriState.CONFIRMED
    else:
        correlation_state = TriState.CONTRADICTED

    observed = {
        "credential_validity": credential_state.value,
        "citation_binding": citation_state.value,
        "completion": completion_state.value,
        "authorization": authorization_state.value,
        "correlation": correlation_state.value,
    }

    expected = vector.get("expected")
    if expected is None:
        classification = Classification.SUPPORTED
    else:
        if not isinstance(expected, dict):
            raise ValueError(f"{vector_id}: expected must be a mapping")
        classification = (
            Classification.SUPPORTED
            if all(observed.get(key) == value for key, value in expected.items())
            else Classification.DIVERGENT
        )

    return {
        "id": vector_id,
        "classification": classification.value,
        "surface": surface,
        **observed,
        "reason": str(vector.get("reason") or ""),
    }


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    """Evaluate a complete case and return a bounded evidence package."""

    vectors = case.get("vectors")
    if not isinstance(vectors, list) or not vectors:
        raise ValueError("case must contain at least one vector")

    seen: set[str] = set()
    evaluated = []
    for vector in vectors:
        if not isinstance(vector, dict):
            raise ValueError("each vector must be a mapping")
        vector_id = _require_vector_id(vector)
        if vector_id in seen:
            raise ValueError(f"duplicate vector id: {vector_id}")
        seen.add(vector_id)
        evaluated.append(evaluate_vector(vector))

    counts = {
        state.value: sum(item["classification"] == state.value for item in evaluated)
        for state in Classification
    }

    return {
        "schema": "interop-task-citation-convergence-evidence/v1",
        "case": str(case.get("case") or "IC-DTG-TASK-CITATION-CONVERGENCE-001"),
        "issue": 233,
        "authority_state": {
            "trust_tasks_17": AUTHORITY_STATE["trust_tasks_17"],
            "credential_56": AUTHORITY_STATE["credential_56"],
            "vti_33": AUTHORITY_STATE["vti_33"],
            "zkp_11": AUTHORITY_STATE["zkp_11"],
        },
        "source_pins": {
            "trust_tasks_pr_17_merge": "2bdc08bc55e48fd3bd4e03cd665b26d266f75c11",
        },
        "candidate_sources": [
            "trustoverip/dtgwg-cred-spec#56",
            "trustoverip/dtgwg-vti-spec#33",
            "trustoverip/dtgwg-zkp-spec#11",
            "trustoverip/dtgwg-cred-spec#58",
        ],
        "vectors": evaluated,
        "summary": counts,
        "non_inference": [
            "valid credential != completed Trust Task",
            "matching taskContext != exact cited-document binding without digest verification",
            "matching citation != valid outcome evidence",
            "valid completion evidence != consequential action authority",
            "proof validity != presentation unlinkability",
            "fixture support != target-runtime conformance",
        ],
        "claim_boundary": (
            "The package records semantic fixture evidence and explicit target-runtime "
            "availability only. Open upstream proposals are not treated as adopted "
            "runtime semantics, and unavailable surfaces remain unresolved."
        ),
    }
