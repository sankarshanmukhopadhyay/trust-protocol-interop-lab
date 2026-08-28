from __future__ import annotations

import hashlib
import json
from typing import Any

STATUSES = {"verified", "historical", "disputed", "restricted", "indeterminate", "reported"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class RelationshipViewBuilder:
    """Deterministic, source-traceable, authorization-scoped relationship explanation."""

    def build(
        self,
        *,
        viewer: dict[str, Any],
        relationship: dict[str, Any],
        agreement: dict[str, Any],
        authority: dict[str, Any],
        decision: dict[str, Any],
        capability: dict[str, Any] | None,
        task: dict[str, Any] | None,
        execution: dict[str, Any] | None,
        role_record_heads: dict[str, str],
        checkpoint_ref: str,
        dependencies: list[dict[str, Any]],
        disputes: list[dict[str, Any]],
        evidence_gaps: list[dict[str, Any]],
        obligations: list[dict[str, Any]],
        remedies: list[dict[str, Any]],
        private_evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        allowed = set(viewer.get("scopes", []))
        assertions: list[dict[str, Any]] = []

        def add(
            key: str,
            value: Any,
            *,
            status: str,
            evidence_refs: list[str],
            required_scope: str | None = None,
            note: str | None = None,
        ) -> None:
            if status not in STATUSES:
                raise ValueError("invalid_assertion_status")
            visible = required_scope is None or required_scope in allowed
            assertion = {
                "key": key,
                "status": status if visible else "restricted",
                "evidence_refs": sorted(set(evidence_refs)),
                "value": value if visible else None,
            }
            if note is not None:
                assertion["note"] = note
            if not visible:
                assertion["restriction"] = f"requires:{required_scope}"
            assertions.append(assertion)

        add("relationship.id", relationship["relationship_id"], status="verified", evidence_refs=[checkpoint_ref])
        add("relationship.parties", relationship["parties"], status="verified", evidence_refs=[checkpoint_ref])
        add("relationship.purpose", relationship["purpose"], status="verified", evidence_refs=[relationship["state_ref"]])
        add("relationship.current_status", relationship["status"], status="verified", evidence_refs=[relationship["state_ref"]])
        add(
            "agreement.current",
            {
                "agreement_ref": agreement["agreement_ref"],
                "version": agreement["version"],
                "status": agreement["status"],
            },
            status="verified",
            evidence_refs=[agreement["agreement_ref"]],
        )
        add(
            "authority.current",
            {
                "authority_ref": authority.get("authority_ref"),
                "active": authority.get("active"),
                "purposes": authority.get("purposes", []),
                "resources": authority.get("resources", []),
                "actions": authority.get("actions", []),
            },
            status="verified",
            evidence_refs=[authority.get("authority_ref")],
            required_scope="authority",
        )
        add(
            "policy.last_decision",
            {"decision": decision.get("decision"), "code": decision.get("code")},
            status="verified",
            evidence_refs=[decision.get("decision_ref"), decision.get("inputs_ref")],
        )
        if capability is None:
            add(
                "capability.current",
                None,
                status="indeterminate",
                evidence_refs=[decision.get("decision_ref")],
                note="No capability evidence is available in this view.",
            )
        else:
            cap_status = "verified" if capability.get("status") == "active" else "historical"
            add(
                "capability.current",
                {
                    "capability_ref": capability.get("capability_ref"),
                    "status": capability.get("status"),
                    "expires_at": capability.get("expires_at"),
                },
                status=cap_status,
                evidence_refs=[capability.get("capability_ref"), capability.get("decision_ref")],
                required_scope="capability",
            )
        if task is not None:
            add(
                "action.last_task",
                {
                    "task_ref": task.get("task_ref"),
                    "task_id": task.get("task_id"),
                    "recipient": task.get("recipient"),
                    "purpose": task.get("purpose"),
                    "payload_digest": task.get("payload_digest"),
                },
                status="historical",
                evidence_refs=[task.get("task_ref"), task.get("decision_ref")],
            )
        if execution is not None:
            add(
                "action.execution",
                {
                    "result": execution.get("result"),
                    "code": execution.get("code"),
                    "receipt_ref": execution.get("receipt_ref"),
                    "effect_ref": execution.get("effect_ref"),
                },
                status="historical",
                evidence_refs=[execution.get("receipt_ref"), execution.get("task_ref")],
            )

        add(
            "relationship.role_record_heads",
            role_record_heads,
            status="verified",
            evidence_refs=[checkpoint_ref, *role_record_heads.values()],
        )

        for index, dep in enumerate(dependencies):
            add(
                f"dependency.{index}",
                {
                    "kind": dep.get("kind"),
                    "material": dep.get("material"),
                    "pointer": dep.get("pointer") if dep.get("traversable") else None,
                    "traversable": False,
                },
                status="restricted" if dep.get("restricted") else "reported",
                evidence_refs=[dep["evidence_ref"]],
                required_scope=dep.get("required_scope") if dep.get("restricted") else None,
                note="Dependency existence is disclosed without granting traversal.",
            )

        for index, dispute in enumerate(disputes):
            add(
                f"dispute.{index}",
                {
                    "status": dispute.get("status"),
                    "target_ref": dispute.get("target_ref"),
                    "correction_ref": dispute.get("correction_ref"),
                    "remediation": dispute.get("remediation"),
                },
                status="disputed" if dispute.get("status") == "disputed" else "historical",
                evidence_refs=[r for r in [dispute.get("disposition_ref"), dispute.get("correction_ref"), dispute.get("target_ref")] if r],
            )

        for index, gap in enumerate(evidence_gaps):
            add(
                f"uncertainty.{index}",
                {"code": gap.get("code"), "missing": gap.get("missing"), "impact": gap.get("impact")},
                status="indeterminate",
                evidence_refs=[r for r in gap.get("evidence_refs", []) if r],
            )

        add(
            "obligations.surviving",
            obligations,
            status="verified",
            evidence_refs=sorted({o["evidence_ref"] for o in obligations}),
            required_scope="obligations",
        )
        add(
            "remedies.available",
            remedies,
            status="reported",
            evidence_refs=sorted({r["evidence_ref"] for r in remedies}),
        )

        # Private evidence is never rendered; only a non-revealing omission statement may appear.
        if private_evidence:
            add(
                "privacy.unrelated_private_evidence",
                {"count": len(private_evidence), "included": False},
                status="restricted",
                evidence_refs=[],
                note="Unrelated private Role Record material is excluded by construction.",
            )

        # Redaction safety: no assertion with no evidence may appear verified.
        for assertion in assertions:
            if assertion["status"] == "verified" and not assertion["evidence_refs"]:
                raise ValueError("verified_assertion_requires_evidence")

        material = {
            "view_version": "ara/authorized-relationship-view/0.1",
            "viewer_id": viewer["viewer_id"],
            "viewer_scopes": sorted(allowed),
            "relationship_id": relationship["relationship_id"],
            "checkpoint_ref": checkpoint_ref,
            "assertions": sorted(assertions, key=lambda a: a["key"]),
            "authority_effect": "none",
        }
        return {**material, "view_ref": digest(material)}

    @staticmethod
    def shared_fact_projection(view: dict[str, Any]) -> dict[str, Any]:
        shared = {}
        for assertion in view["assertions"]:
            if assertion["key"] in {
                "relationship.id",
                "relationship.parties",
                "relationship.purpose",
                "relationship.current_status",
                "agreement.current",
                "policy.last_decision",
                "action.last_task",
                "action.execution",
                "relationship.role_record_heads",
            }:
                shared[assertion["key"]] = {
                    "status": assertion["status"],
                    "value": assertion["value"],
                    "evidence_refs": assertion["evidence_refs"],
                }
        return shared
