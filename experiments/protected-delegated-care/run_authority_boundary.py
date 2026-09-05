#!/usr/bin/env python3
"""Executable evidence for PDC execution-time current-authority integration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from authority_boundary import CurrentAuthorityGateway, OBSERVED_SURFACES, execute_through_gateway
from core import build_active_exception_core

VTI = "OpenVTC/verifiable-trust-infrastructure@1e50665c5313bbb75df80a96602f35a4355c8154"
OPENVTC = "OpenVTC/openvtc@f93bc7e58f2766f3064e2b23ef877563069609ac"


def evaluate() -> dict:
    gateway = CurrentAuthorityGateway()

    # Canonical integration attempt: the local application model would be able to
    # evaluate this task, but the integration boundary requires an actual upstream
    # delegated-action authority result before consequential actuation.
    canonical = build_active_exception_core()
    canonical_before = canonical.state_copy()
    canonical_result = execute_through_gateway(canonical, gateway)

    # Revoked-task race: create an actionable task, revoke local delegation after
    # task creation, then attempt execution through the same upstream boundary.
    revoked = build_active_exception_core()
    revoked.delegation.status = "revoked"
    revoked_before = revoked.state_copy()
    revoked_result = execute_through_gateway(revoked, gateway)

    # Comparison only: establish that the existing application-local controller
    # knows how to deny a revoked delegation, while keeping that fact distinct from
    # an upstream VTC authorization claim.
    local_control = build_active_exception_core()
    local_control.delegation.status = "revoked"
    local_control_result = local_control.execute_exception_response()

    checks = {
        "no_exact_upstream_delegated_action_surface_observed": not gateway.exact_surface_available,
        "canonical_integration_fails_closed": canonical_result["authorization"] == "indeterminate" and canonical_result["execution"] == "blocked",
        "canonical_block_has_no_state_mutation": canonical.state_copy() == canonical_before and canonical_result["state_mutation"] is False,
        "revoked_race_fails_closed": revoked_result["authorization"] == "indeterminate" and revoked_result["execution"] == "blocked",
        "revoked_race_has_no_state_mutation": revoked.state_copy() == revoked_before and revoked_result["state_mutation"] is False,
        "no_weaker_surface_substitution": canonical_result["substitution_used"] is False and revoked_result["substitution_used"] is False,
        "no_application_fallback_permit": canonical_result["application_fallback_invoked"] is False and revoked_result["application_fallback_invoked"] is False,
        "local_controller_comparison_denies_revoked_authority": local_control_result["authorization"] == "deny" and local_control_result["reason"] == "AUTHORITY_REVOKED",
    }

    return {
        "case_id": "IC-PDC-MED-001",
        "issue": 135,
        "claim": "evidence-backed actuation-boundary integration result; current upstream delegated-action authority surface not found",
        "baselines": {"vti": VTI, "openvtc": OPENVTC},
        "observed_surfaces": [
            {
                "id": surface.id,
                "semantics": surface.semantics,
                "delegated_action_authority": surface.delegated_action_authority,
            }
            for surface in OBSERVED_SURFACES
        ],
        "integration_classification": "INDETERMINATE/BLOCKED",
        "canonical_attempt": canonical_result,
        "revoked_task_race": revoked_result,
        "application_local_comparison": {
            "result": local_control_result,
            "claim": "local deterministic control only; not upstream VTC authorization evidence",
        },
        "checks": checks,
        "summary": {
            "passed": sum(1 for value in checks.values() if value),
            "total": len(checks),
            "failed": [name for name, value in checks.items() if not value],
        },
        "next_required_upstream_surface": "generic or profile-defined current delegated-action authority evaluation consumable immediately before PDC actuation",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    result = evaluate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 1 if result["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
