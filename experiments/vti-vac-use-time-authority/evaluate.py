from __future__ import annotations

REQUIRED = (
    "presenter_from_request_proof",
    "exact_action_authorize_before_effect",
    "authorized_action_typestate",
    "credential_proof_verification",
    "room_root_and_scope_binding",
    "action_binding_and_non_widening",
    "validity_window_checked",
    "presenter_binding",
    "membership_authority_subject_coherence",
    "no_verifier_fails_closed",
    "private_without_zk_fails_closed",
)


def evaluate(observations: dict, revision: str) -> dict:
    missing = [k for k in REQUIRED if observations.get(k) is not True]
    if missing:
        raise ValueError(f"required observations absent: {', '.join(missing)}")
    if observations.get("vti_rooms_tests") != "passed":
        raise ValueError("vti-rooms target-native tests did not pass")
    if observations.get("vti_rooms_dtg_tests") != "passed":
        raise ValueError("vti-rooms-dtg target-native tests did not pass")
    if not revision or len(revision) != 40:
        raise ValueError("immutable target revision required")

    current_status_revocation = observations.get("current_status_revocation") is True
    live_policy_lookup = observations.get("live_policy_lookup") is True

    if current_status_revocation and live_policy_lookup:
        r001 = "SUBSTANTIALLY_DISCHARGED"
        remaining = (
            "This bounded room path has source-pinned use-time authority, current-status and live-policy evidence. "
            "Universal Trust Tasks authority and deployment behavior remain outside this case."
        )
    else:
        r001 = "PARTIALLY_DISCHARGED"
        gaps = []
        if not current_status_revocation:
            gaps.append("current credentialStatus/revocation is not established at this boundary")
        if not live_policy_lookup:
            gaps.append("no separate live policy/status decision is established for room operations")
        remaining = "; ".join(gaps) + "."

    return {
        "schema": "interop-use-time-authority-observation/v1",
        "case": "IC-VTI-VAC-USE-TIME-AUTHORITY-001",
        "target": {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": revision},
        "evidence_maturity": "SOURCE_PINNED_USE_TIME_AUTHORITY_EVIDENCE",
        "r001": r001,
        "observations": observations,
        "remaining_gap": remaining,
        "claim_boundary": (
            "The room authorization seam establishes proof-checked, room-rooted, action-specific, time-bounded, presenter-bound "
            "VAC use at request time. It does not manufacture credential revocation/status or a separate live governance policy "
            "lookup where the target does not expose one."
        ),
    }
