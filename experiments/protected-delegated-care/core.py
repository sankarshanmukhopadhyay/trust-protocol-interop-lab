"""Deterministic application-owned reference core for IC-PDC-MED-001.

This module deliberately models only the PDC application control boundary. It is not a
DTG/VTC/OpenVTC implementation, medical device, clinical rules engine, or messaging
provider integration. External/probabilistic systems may propose inputs; this core owns
only deterministic validation, lifecycle transitions, bounded authorization, disclosure
checks, idempotency, and minimized evidence for the experiment.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any

POLICY_VERSION = "pdc-policy-v1"
EVALUATED_AT = "2026-09-05T08:00:00Z"


@dataclass
class Relationship:
    id: str = "relationship:r001"
    principal: str = "person:p001"
    delegate: str = "person:c001"
    status: str = "active"


@dataclass
class Delegation:
    id: str = "delegation:d001"
    relationship: str = "relationship:r001"
    capabilities: set[str] = field(
        default_factory=lambda: {"care.exception.receive", "care.exception.respond"}
    )
    status: str = "active"
    evidence_present: bool = True


@dataclass
class MedicationPlan:
    id: str = "medication-plan:mp001"
    subject: str = "person:p001"
    version: int = 1
    status: str = "review_required"
    extraction_ambiguous: bool = False
    fabricated_claim_detected: bool = False
    human_approved: bool = False


@dataclass
class Reminder:
    id: str = "reminder:rm001"
    plan: str = "medication-plan:mp001"
    scheduled_at: str = "2026-09-05T08:00:00Z"
    status: str = "scheduled"
    dispatch_count: int = 0
    late_acknowledged: bool = False
    event_history: list[str] = field(default_factory=list)


@dataclass
class Task:
    id: str = "task:t001"
    action: str = "care.exception.respond"
    requester: str = "person:c001"
    principal: str = "person:p001"
    relationship: str = "relationship:r001"
    delegation: str = "delegation:d001"
    resource: str = "reminder:rm001"
    state: str = "proposed"
    consumed: bool = False


class CareCore:
    """Small deterministic state machine for the first PDC vertical slice."""

    def __init__(self) -> None:
        self.relationship = Relationship()
        self.delegation = Delegation()
        self.plan = MedicationPlan()
        self.reminder = Reminder()
        self.task = Task()
        self.evidence: list[dict[str, Any]] = []
        self.channel_event_ids: set[str] = set()
        self.authoritative_ack_events = 0
        self.re_reminder_effects = 0

    def snapshot(self) -> dict[str, Any]:
        """Return deterministic authoritative state, excluding append-only evidence."""
        delegation = asdict(self.delegation)
        delegation["capabilities"] = sorted(self.delegation.capabilities)
        return {
            "relationship": asdict(self.relationship),
            "delegation": delegation,
            "plan": asdict(self.plan),
            "reminder": asdict(self.reminder),
            "task": asdict(self.task),
            "authoritative_ack_events": self.authoritative_ack_events,
            "re_reminder_effects": self.re_reminder_effects,
        }

    def state_copy(self) -> dict[str, Any]:
        return deepcopy(self.snapshot())

    def record_decision(
        self,
        *,
        action: str,
        decision: str,
        reason: str,
        resource: str | None = None,
        actor: str = "person:c001",
    ) -> dict[str, Any]:
        record = {
            "event": "authorization_decision",
            "actor": actor,
            "action": action,
            "resource": resource or self.task.resource,
            "relationship": self.relationship.id,
            "delegation": self.delegation.id,
            "decision": decision,
            "reason": reason,
            "policy_version": POLICY_VERSION,
            "evaluated_at": EVALUATED_AT,
        }
        self.evidence.append(record)
        return record

    # Medication plan lifecycle -------------------------------------------------

    def extract_plan(self, *, ambiguous: bool = False, fabricated: bool = False) -> str:
        """Represent extraction as advisory input; it can never approve or activate."""
        self.plan.status = "review_required"
        self.plan.extraction_ambiguous = ambiguous
        self.plan.fabricated_claim_detected = fabricated
        self.plan.human_approved = False
        return self.plan.status

    def approve_plan(self) -> str:
        if self.plan.extraction_ambiguous or self.plan.fabricated_claim_detected:
            return "review_required"
        self.plan.human_approved = True
        self.plan.status = "approved"
        return self.plan.status

    def activate_plan(self) -> bool:
        if self.plan.status != "approved" or not self.plan.human_approved:
            return False
        self.plan.status = "active"
        return True

    def supersede_plan(self) -> None:
        if self.plan.status == "active":
            self.plan.status = "superseded"

    # Reminder lifecycle --------------------------------------------------------

    def schedule_reminder(self) -> dict[str, Any]:
        if self.plan.status != "active":
            return {"authorization": "suppress", "reason": "PLAN_NOT_ACTIVE", "created": False}
        self.reminder.plan = self.plan.id
        self.reminder.status = "scheduled"
        self.reminder.event_history.append("scheduled")
        return {"authorization": "permit", "created": True}

    def dispatch_reminder(self) -> bool:
        if self.plan.status != "active" or self.reminder.status not in {"scheduled", "escalation_pending"}:
            return False
        self.reminder.status = "dispatched"
        self.reminder.dispatch_count += 1
        self.reminder.event_history.append("dispatched")
        return True

    def timeout_reminder(self) -> bool:
        if self.reminder.status != "dispatched":
            return False
        self.reminder.status = "unacknowledged"
        self.reminder.event_history.append("unacknowledged")
        self.reminder.status = "escalation_pending"
        self.reminder.event_history.append("escalation_pending")
        return True

    def mark_escalated(self) -> None:
        if self.reminder.status == "escalation_pending":
            self.reminder.status = "escalated"
            self.reminder.event_history.append("escalated")

    def acknowledge_channel_event(self, event_id: str) -> dict[str, Any]:
        """Apply one acknowledgement at most once, preserving late-event history."""
        if event_id in self.channel_event_ids:
            return {"authorization": "idempotent", "duplicate_effect": False}
        self.channel_event_ids.add(event_id)

        if self.reminder.status == "escalated":
            self.reminder.late_acknowledged = True
            self.reminder.event_history.append("late_acknowledgement")
            self.authoritative_ack_events += 1
            return {
                "authorization": "permit",
                "deterministic_reconciliation": True,
                "history_rewritten": False,
            }

        if self.reminder.status != "dispatched":
            return {"authorization": "deny", "reason": "REMINDER_NOT_ACKNOWLEDGEABLE"}

        self.reminder.status = "acknowledged"
        self.reminder.event_history.append("acknowledged")
        self.authoritative_ack_events += 1
        return {"authorization": "permit", "duplicate_effect": False}

    # Disclosure ---------------------------------------------------------------

    @staticmethod
    def validate_exception_payload(payload: dict[str, Any]) -> dict[str, Any]:
        prohibited = {
            "medication_name",
            "diagnosis",
            "prescription_image",
            "medication_history",
            "caregiver_graph",
        }
        present = sorted(prohibited & payload.keys())
        if present:
            return {
                "authorization": "policy_failure",
                "reason": "MESSAGE_EXCEEDS_DISCLOSURE_SCOPE",
                "prohibited_fields": present,
            }
        required = {"exception_ref", "reminder_time", "permitted_actions"}
        missing = sorted(required - payload.keys())
        if missing:
            return {
                "authorization": "policy_failure",
                "reason": "MESSAGE_MISSING_REQUIRED_FIELDS",
                "missing": missing,
            }
        return {"authorization": "permit", "caregiver_disclosure": "minimum"}

    def safe_exception_payload(self) -> dict[str, Any]:
        return {
            "exception_ref": "exception:x001",
            "reminder_time": "08:00",
            "permitted_actions": ["check_in", "remind_again"],
        }

    # Authorization and execution ---------------------------------------------

    def evaluate_task(self, *, action: str | None = None) -> dict[str, Any]:
        requested_action = action or self.task.action
        if not self.delegation.evidence_present:
            record = self.record_decision(
                action=requested_action,
                decision="indeterminate",
                reason="MISSING_AUTHORITY_EVIDENCE",
            )
            return {"authorization": "indeterminate", "reason": record["reason"]}
        if self.relationship.status != "active":
            record = self.record_decision(
                action=requested_action, decision="deny", reason="RELATIONSHIP_NOT_ACTIVE"
            )
            return {"authorization": "deny", "reason": record["reason"]}
        if self.delegation.status != "active":
            reason = "AUTHORITY_REVOKED" if self.delegation.status == "revoked" else "AUTHORITY_NOT_ACTIVE"
            record = self.record_decision(action=requested_action, decision="deny", reason=reason)
            return {"authorization": "deny", "reason": record["reason"]}
        if requested_action not in self.delegation.capabilities:
            record = self.record_decision(
                action=requested_action, decision="deny", reason="ACTION_OUTSIDE_DELEGATION"
            )
            return {"authorization": "deny", "reason": record["reason"]}
        if self.task.resource != self.reminder.id:
            record = self.record_decision(
                action=requested_action, decision="deny", reason="RESOURCE_BINDING_MISMATCH"
            )
            return {"authorization": "deny", "reason": record["reason"]}
        record = self.record_decision(action=requested_action, decision="permit", reason="CURRENT_AUTHORITY")
        return {"authorization": "permit", "reason": record["reason"]}

    def execute_exception_response(self) -> dict[str, Any]:
        """Re-evaluate current authority immediately before the bounded effect."""
        if self.task.consumed:
            return {"authorization": "idempotent", "duplicate_effect": False}

        before = self.state_copy()
        decision = self.evaluate_task()
        if decision["authorization"] != "permit":
            # Evidence is append-only and excluded from authoritative-state mutation comparison.
            return {
                **decision,
                "state_mutation": self.state_copy() != before,
            }

        if self.reminder.status not in {"escalation_pending", "escalated"}:
            self.record_decision(
                action=self.task.action,
                decision="deny",
                reason="REMINDER_NOT_EXCEPTION_ACTIONABLE",
            )
            return {"authorization": "deny", "reason": "REMINDER_NOT_EXCEPTION_ACTIONABLE", "state_mutation": False}

        self.task.state = "executed"
        self.task.consumed = True
        self.re_reminder_effects += 1
        self.reminder.status = "scheduled"
        self.reminder.event_history.append("re_reminder_scheduled")
        self.evidence.append(
            {
                "event": "effect_recorded",
                "action": self.task.action,
                "resource": self.task.resource,
                "effect": "re_reminder_scheduled",
                "policy_version": POLICY_VERSION,
                "observed_at": EVALUATED_AT,
            }
        )
        return {
            "authorization": "permit",
            "state_mutation": True,
            "caregiver_disclosure": "minimum",
            "evidence": "required",
        }

    # Contextual correlation ---------------------------------------------------

    def contextual_relationship_ref(self, context: str) -> str:
        material = f"{context}|{self.relationship.id}".encode("utf-8")
        return f"ctx:{context}:{sha256(material).hexdigest()[:16]}"


def build_active_exception_core() -> CareCore:
    """Construct the canonical synthetic state just before caregiver exception action."""
    core = CareCore()
    core.extract_plan()
    if core.approve_plan() != "approved":
        raise AssertionError("canonical fixture plan was not approvable")
    if not core.activate_plan():
        raise AssertionError("canonical fixture plan did not activate")
    if not core.schedule_reminder()["created"]:
        raise AssertionError("canonical reminder was not scheduled")
    if not core.dispatch_reminder():
        raise AssertionError("canonical reminder was not dispatched")
    if not core.timeout_reminder():
        raise AssertionError("canonical reminder did not reach escalation_pending")
    return core
