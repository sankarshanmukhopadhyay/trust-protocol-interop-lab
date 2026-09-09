from __future__ import annotations


REQUIRED_SOURCE_OBSERVATIONS = (
    "trust_task_type",
    "credential_write_gate",
    "independent_signing_context",
    "vac_constructor",
    "empty_actions_fail_closed",
    "credential_response",
)


def evaluate(observations: dict, revision: str) -> dict:
    missing = [key for key in REQUIRED_SOURCE_OBSERVATIONS if observations.get(key) is not True]
    if missing:
        raise ValueError(f"required integration observations absent: {', '.join(missing)}")
    if observations.get("target_package_tests") != "passed":
        raise ValueError("target package test gate did not pass")
    if not revision or len(revision) != 40:
        raise ValueError("immutable target revision required")

    behavior_test_present = observations.get("behavior_test_present") is True
    if behavior_test_present:
        maturity = "TARGET_NATIVE_BEHAVIOR_EVIDENCE"
        remaining = (
            "A single VTI Room authority issuance path does not establish universal Trust Tasks × Credential Spec composition; "
            "status/revocation, later VAC use and deployment policy remain independently bounded."
        )
    else:
        maturity = "SOURCE_PINNED_INTEGRATION_EVIDENCE"
        remaining = (
            "The owning VTI package compiles/tests and the source-pinned integration boundary is explicit, but no dedicated "
            "behavioral target-native test was found for allowed/denied issue-authority execution, credential effect identity, "
            "or replay behavior; those propositions remain EVIDENCE_REQUIRED."
        )

    return {
        "schema": "interop-composition-observation/v1",
        "case": "IC-VTI-TRUST-TASK-CREDENTIAL-AUTHORITY-001",
        "target": {
            "repository": "OpenVTC/verifiable-trust-infrastructure",
            "revision": revision,
        },
        "evidence_maturity": maturity,
        "r001": "PARTIALLY_DISCHARGED",
        "r002": "PARTIALLY_DISCHARGED",
        "observations": observations,
        "remaining_gap": remaining,
        "claim_boundary": (
            "This evidence supports a bounded integration claim for one Trust Task credential-issuance path. "
            "Task admission, credential issuance or credential validity do not establish future consequential authority, "
            "current status/policy, or deployment-wide composition assurance."
        ),
    }
