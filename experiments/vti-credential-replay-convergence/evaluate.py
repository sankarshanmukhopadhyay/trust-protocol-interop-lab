from __future__ import annotations

REQUIRED = (
    "issue_authority_keyed",
    "signed_idempotency_key",
    "actor_key_payload_binding",
    "conflict_fails_closed",
    "completed_response_replayed",
    "failed_outcome_releases_claim",
    "dispatcher_claims_before_dispatch",
    "dispatcher_records_after_dispatch",
)


def evaluate(observations: dict, revision: str) -> dict:
    missing = [k for k in REQUIRED if observations.get(k) is not True]
    if missing:
        raise ValueError(f"required replay observations absent: {', '.join(missing)}")
    if observations.get("target_package_tests") != "passed":
        raise ValueError("target package tests did not pass")
    if len(revision) != 40:
        raise ValueError("immutable 40-character revision required")
    return {
        "schema": "interop-composition-observation/v1",
        "case": "IC-VTI-CREDENTIAL-REPLAY-001",
        "target": {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": revision},
        "evidence_maturity": "SOURCE_PINNED_REPLAY_CONVERGENCE_EVIDENCE",
        "r002": "PARTIALLY_DISCHARGED",
        "observations": observations,
        "remaining_gap": "The source-pinned dispatcher proves keyed retry convergence for this issuance path, but does not prove deployment-wide production retry behavior or external side-effect identity beyond VTI.",
        "claim_boundary": "Idempotency prevents a same-logical-operation keyed retry from redispatching this credential issuance path. It does not establish current downstream authority, universal Trust Tasks replay closure, or production runtime observation.",
    }
