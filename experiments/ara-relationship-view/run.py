#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from view import RelationshipViewBuilder, digest

REL = "urn:ara:relationship:research:001"
A = "urn:ara:agent-role:data-owner:001"
B = "urn:ara:agent-role:researcher:001"


def record(results: list[dict[str, Any]], vector_id: str, expected: str, observed: str, evidence: Any) -> None:
    passed = expected == observed
    results.append({"vector_id": vector_id, "expected": expected, "observed": observed, "pass": passed, "evidence": evidence})
    if not passed:
        raise AssertionError(f"{vector_id}: expected {expected}, observed {observed}")


def fixture() -> dict[str, Any]:
    agreement = {"agreement_ref": "sha256:agreement", "version": 1, "status": "active"}
    authority = {
        "authority_ref": "sha256:authority",
        "active": True,
        "purposes": ["synthetic-research"],
        "resources": ["dataset:synthetic-001"],
        "actions": ["query"],
    }
    decision = {
        "decision": "allow",
        "code": "all_required_conditions_satisfied",
        "decision_ref": "sha256:decision",
        "inputs_ref": "sha256:decision-inputs",
    }
    capability = {
        "capability_ref": "sha256:capability",
        "decision_ref": "sha256:decision",
        "status": "revoked",
        "expires_at": 100,
    }
    task = {
        "task_ref": "sha256:task",
        "task_id": "ara/research-query/0.1",
        "decision_ref": "sha256:decision",
        "recipient": B,
        "purpose": "synthetic-research",
        "payload_digest": "sha256:payload",
    }
    execution = {
        "result": "admitted",
        "code": "admitted",
        "receipt_ref": "sha256:execution",
        "effect_ref": "sha256:effect",
        "task_ref": "sha256:task",
    }
    return {
        "relationship": {
            "relationship_id": REL,
            "parties": [A, B],
            "purpose": "synthetic-research",
            "status": "remediated",
            "state_ref": "sha256:role-state-current",
        },
        "agreement": agreement,
        "authority": authority,
        "decision": decision,
        "capability": capability,
        "task": task,
        "execution": execution,
        "role_record_heads": {A: "sha256:head-a", B: "sha256:head-b"},
        "checkpoint_ref": "sha256:checkpoint",
        "dependencies": [
            {
                "kind": "source_pointer",
                "material": True,
                "pointer": "role-record://data-owner/evidence/42",
                "traversable": False,
                "restricted": True,
                "required_scope": "linked-context",
                "evidence_ref": "sha256:pointer",
            }
        ],
        "disputes": [
            {
                "status": "disputed",
                "target_ref": "sha256:effect",
                "disposition_ref": "sha256:dispute",
                "correction_ref": "sha256:correction",
                "remediation": "prior capability revoked; effect label corrected",
            }
        ],
        "evidence_gaps": [
            {
                "code": "counterparty_external_attestation_unresolved",
                "missing": ["external-attestation"],
                "impact": "cannot claim external corroboration",
                "evidence_refs": ["sha256:gap-register-row"],
            }
        ],
        "obligations": [
            {"id": "obl-audit-history", "status": "survives", "evidence_ref": "sha256:obligation"}
        ],
        "remedies": [
            {"action": "request-review", "evidence_ref": "sha256:remedy-review"},
            {"action": "submit-correction", "evidence_ref": "sha256:remedy-correction"},
        ],
        "private_evidence": [
            {"object_ref": "sha256:private", "secret": "must never appear"}
        ],
    }


def get_assertion(view: dict[str, Any], key: str) -> dict[str, Any]:
    return next(a for a in view["assertions"] if a["key"] == key)


def run_vectors() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    builder = RelationshipViewBuilder()
    f = fixture()

    principal = builder.build(
        viewer={"viewer_id": "principal:data-owner", "scopes": ["authority", "capability", "obligations", "linked-context"]},
        **f,
    )
    last_decision = get_assertion(principal, "policy.last_decision")
    action = get_assertion(principal, "action.execution")
    enough = last_decision["value"]["decision"] == "allow" and action["value"]["result"] == "admitted" and bool(last_decision["evidence_refs"]) and bool(action["evidence_refs"])
    record(results, "P9-P01-authorized-view-explains-last-action", "explained", "explained" if enough else "insufficient", principal)

    rendered = json.dumps(principal, sort_keys=True)
    record(results, "P9-N01-private-unrelated-evidence-absent", "absent", "absent" if "must never appear" not in rendered and "sha256:private" not in rendered else "leaked", principal)

    dependency = get_assertion(principal, "dependency.0")
    dep_visible = dependency["value"]["material"] is True and dependency["value"]["traversable"] is False
    record(results, "P9-P02-material-dependency-visible-without-traversal", "bounded-visible", "bounded-visible" if dep_visible else "concealed-or-traversable", dependency)

    restricted = builder.build(
        viewer={"viewer_id": "auditor:restricted", "scopes": []},
        **f,
    )
    restricted_dep = get_assertion(restricted, "dependency.0")
    material_not_concealed = restricted_dep["status"] == "restricted" and restricted_dep["note"].startswith("Dependency existence")
    record(results, "P9-N02-restricted-link-does-not-disappear", "restricted-visible", "restricted-visible" if material_not_concealed else "concealed", restricted_dep)

    principal_shared = builder.shared_fact_projection(principal)
    restricted_shared = builder.shared_fact_projection(restricted)
    record(results, "P9-P03-scope-different-views-share-history", digest(principal_shared), digest(restricted_shared), {"principal": principal_shared, "restricted": restricted_shared})

    # Redacting authority must not elevate it to verified.
    restricted_authority = get_assertion(restricted, "authority.current")
    record(results, "P9-N03-redaction-not-apparent-verification", "restricted", restricted_authority["status"], restricted_authority)

    uncertainty = get_assertion(principal, "uncertainty.0")
    record(results, "P9-P04-missing-evidence-visible-as-indeterminate", "indeterminate", uncertainty["status"], uncertainty)

    dispute = get_assertion(principal, "dispute.0")
    record(results, "P9-P05-dispute-and-remediation-visible", "disputed", dispute["status"], dispute)

    cap = get_assertion(principal, "capability.current")
    record(results, "P9-P06-revoked-capability-not-shown-active", "revoked", cap["value"]["status"], cap)

    no_cap = copy.deepcopy(f); no_cap["capability"] = None
    indeterminate_cap_view = builder.build(
        viewer={"viewer_id": "principal:data-owner", "scopes": ["authority", "capability", "obligations"]},
        **no_cap,
    )
    cap_gap = get_assertion(indeterminate_cap_view, "capability.current")
    record(results, "P9-N04-missing-capability-not-omitted-as-resolved", "indeterminate", cap_gap["status"], cap_gap)

    authority_assertion = get_assertion(principal, "authority.current")
    traceable = all(bool(a["evidence_refs"]) for a in principal["assertions"] if a["key"] not in {"privacy.unrelated_private_evidence"})
    record(results, "P9-P07-material-assertions-source-traceable", "traceable", "traceable" if traceable and authority_assertion["evidence_refs"] else "untraceable", principal)

    record(results, "P9-N05-view-is-not-authority", "none", principal["authority_effect"], principal)

    deterministic_again = builder.build(
        viewer={"viewer_id": "principal:data-owner", "scopes": ["authority", "capability", "obligations", "linked-context"]},
        **f,
    )
    record(results, "P9-P08-deterministic-generation", principal["view_ref"], deterministic_again["view_ref"], deterministic_again)

    summary = {
        "case_id": "IC-ARA-REL-001",
        "phase": 9,
        "experiment": "ara-relationship-view",
        "vectors": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "claim_boundary": "Lab-local deterministic authorized relationship explanation; not a normative ARA view schema, UX standard, legal disclosure, or new authority source.",
    }
    return {"summary": summary, "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = run_vectors()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if args.check and report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
