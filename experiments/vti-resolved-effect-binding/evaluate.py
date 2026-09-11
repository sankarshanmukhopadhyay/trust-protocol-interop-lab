from __future__ import annotations

REQUIRED = (
    "vault_write_gate",
    "context_scope_gate",
    "version_gate",
    "force_hard_delete",
    "soft_delete_grace",
    "audit_declared",
)


def evaluate(observations: dict, revision: str) -> dict:
    missing = [k for k in REQUIRED if observations.get(k) is not True]
    if missing:
        raise ValueError(f"required resolved-effect observations absent: {', '.join(missing)}")
    if observations.get("target_package_tests") != "passed":
        raise ValueError("target package test gate did not pass")
    if not revision or len(revision) != 40:
        raise ValueError("immutable target revision required")

    runtime_branch_test = observations.get("runtime_branch_test") is True
    approval_surface = observations.get("approval_surface_observed") is True

    return {
        "schema": "interop-resolved-effect-observation/v1",
        "case": "IC-VTI-RESOLVED-EFFECT-001",
        "target": {
            "repository": "OpenVTC/verifiable-trust-infrastructure",
            "revision": revision,
            "task": "spec/vault/delete/0.1",
        },
        "evidence_maturity": (
            "TARGET_NATIVE_BEHAVIOR_EVIDENCE" if runtime_branch_test else "SOURCE_PINNED_EFFECT_BINDING_EVIDENCE"
        ),
        "resolved_effect": "ESTABLISHED_IN_SOURCE",
        "r001": "PARTIALLY_DISCHARGED",
        "r002": "PARTIALLY_DISCHARGED",
        "f004_retained_agency": "PARTIALLY_DISCHARGED" if approval_surface else "EVIDENCE_REQUIRED",
        "observations": observations,
        "remaining_gap": (
            "Source establishes distinct recoverable and irreversible request branches behind capability, context and version gates, "
            "but end-to-end runtime evidence must still prove the exact resolved branch through policy/approval, execution, replay and audit."
        ),
        "claim_boundary": (
            "Static task classification is not treated as proof of the concrete request effect. "
            "A source-visible force branch does not establish that a human approval surface presented that irreversible effect, "
            "nor that retries preserve effect identity. Missing runtime evidence remains non-PASS."
        ),
    }
