from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


class AssuranceBoundary:
    """Lab-local meta-assurance rules for ARA evidence interpretation."""

    @staticmethod
    def decide_from_evidence(*, required: list[str], present: dict[str, Any]) -> dict[str, Any]:
        missing = sorted(k for k in required if present.get(k) in (None, False, [], {}))
        if missing:
            material = {
                "assurance": "INDETERMINATE",
                "code": "missing_required_evidence",
                "missing": missing,
            }
            return {**material, "assurance_ref": digest(material)}
        material = {"assurance": "SUPPORTED", "code": "required_evidence_present"}
        return {**material, "assurance_ref": digest(material)}

    @staticmethod
    def independent_support(attestations: list[dict[str, Any]]) -> dict[str, Any]:
        """Count evidence groups by control/source lineage, not artifact count."""
        if not attestations:
            return {"independent_groups": 0, "code": "no_attestations", "groups": {}}
        groups: dict[str, list[str]] = {}
        for att in attestations:
            lineage = att.get("control_lineage") or att.get("issuer_lineage") or att.get("source_lineage")
            if not lineage:
                lineage = f"unknown:{att.get('attestation_ref','missing')}"
            groups.setdefault(str(lineage), []).append(str(att.get("attestation_ref")))
        return {
            "independent_groups": len(groups),
            "artifact_count": len(attestations),
            "code": "lineage_grouped",
            "groups": groups,
        }

    @staticmethod
    def assurance_is_not_authority(*, assurance: dict[str, Any], authority_active: bool) -> dict[str, Any]:
        if assurance.get("assurance") == "SUPPORTED" and not authority_active:
            return {
                "authorization": "deny",
                "code": "assurance_cannot_create_authority",
                "assurance_ref": assurance.get("assurance_ref"),
            }
        return {
            "authorization": "unchanged",
            "code": "assurance_has_no_authority_effect",
            "assurance_ref": assurance.get("assurance_ref"),
        }

    @staticmethod
    def historical_authorization(*, original_result: str, later_assurance: str) -> dict[str, Any]:
        if original_result != "admitted":
            return {
                "historical_authorization": False,
                "code": "later_assurance_not_retroactive",
                "later_assurance": later_assurance,
            }
        return {
            "historical_authorization": True,
            "code": "original_admission_controls_historical_status",
            "later_assurance": later_assurance,
        }

    @staticmethod
    def recovery_checkpoint(*, requested_head: str, last_defensible_head: str) -> dict[str, Any]:
        if requested_head != last_defensible_head:
            return {
                "result": "refused",
                "code": "recovery_beyond_last_defensible_checkpoint",
                "requested_head": requested_head,
                "last_defensible_head": last_defensible_head,
            }
        return {
            "result": "allowed",
            "code": "recovery_at_defensible_checkpoint",
            "requested_head": requested_head,
        }

    @staticmethod
    def collective_state(*, party_dispositions: dict[str, str], required_parties: list[str]) -> dict[str, Any]:
        missing = sorted(set(required_parties) - set(party_dispositions))
        if missing:
            return {
                "status": "not_collective",
                "code": "missing_party_disposition",
                "missing": missing,
            }
        values = set(party_dispositions.values())
        if len(values) != 1:
            return {
                "status": "disputed",
                "code": "party_dispositions_differ",
                "by_party": party_dispositions,
            }
        return {
            "status": "collective",
            "code": "all_parties_match",
            "disposition": next(iter(values)),
        }
