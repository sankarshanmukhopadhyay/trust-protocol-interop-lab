"""Evidence-backed PDC current-authority integration boundary.

This module does not emulate OpenVTC authorization. It records the currently observed
upstream authority-related surfaces and refuses to substitute weaker or domain-specific
surfaces for a generic delegated-action evaluator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuthoritySurface:
    id: str
    semantics: str
    delegated_action_authority: bool


OBSERVED_SURFACES = (
    AuthoritySurface(
        "vtc_trust_task_dispatch",
        "framework validation, holder resolution per verb/transport, and type dispatch",
        False,
    ),
    AuthoritySurface(
        "vrc_publish_current_membership",
        "live membership plus separate authorization to publish a VRC relationship edge",
        False,
    ),
    AuthoritySurface(
        "vrc_relationship_revoke",
        "retraction of a published VRC relationship edge",
        False,
    ),
    AuthoritySurface(
        "room_authority_chain",
        "room-specific authority-chain evaluation",
        False,
    ),
)


class CurrentAuthorityGateway:
    """Fail-closed bridge between PDC actuation and observed upstream authority surfaces."""

    def __init__(self, surfaces: tuple[AuthoritySurface, ...] = OBSERVED_SURFACES) -> None:
        self.surfaces = surfaces

    @property
    def exact_surface_available(self) -> bool:
        return any(surface.delegated_action_authority for surface in self.surfaces)

    def evaluate(self, *, task: dict[str, Any]) -> dict[str, Any]:
        """Return only what the current upstream evidence supports.

        Until an exact delegated-action authority evaluator is observed, the integration
        result is INDETERMINATE/BLOCKED. Identity, relationship state, membership state,
        VRC lifecycle, and room authority are intentionally non-substitutable.
        """
        if not self.exact_surface_available:
            return {
                "authorization": "indeterminate",
                "execution": "blocked",
                "reason": "NO_UPSTREAM_DELEGATED_ACTION_AUTHORITY_SURFACE",
                "task_id": task.get("id"),
                "action": task.get("action"),
                "resource": task.get("resource"),
                "substitution_used": False,
            }
        raise NotImplementedError("an exact upstream delegated-action surface must be integrated explicitly")


def execute_through_gateway(core: Any, gateway: CurrentAuthorityGateway) -> dict[str, Any]:
    """Evaluate upstream authority immediately before actuation and mutate nothing on block."""
    before = core.state_copy()
    decision = gateway.evaluate(task={
        "id": core.task.id,
        "action": core.task.action,
        "resource": core.task.resource,
        "requester": core.task.requester,
        "principal": core.task.principal,
        "relationship": core.task.relationship,
        "delegation": core.task.delegation,
    })
    if decision["authorization"] != "permit":
        return {
            **decision,
            "state_mutation": core.state_copy() != before,
            "application_fallback_invoked": False,
        }
    # This path is deliberately unreachable with the pinned upstream observations.
    result = core.execute_exception_response()
    return {**result, "application_fallback_invoked": False}
