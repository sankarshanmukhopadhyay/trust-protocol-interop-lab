from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


BASELINES = {
    "trust-tasks": {
        "repository": "trustoverip/dtgwg-trust-tasks-spec",
        "commit": "6425a74136c1d2dfa7115889abe0b3521700e887",
        "kind": "normative-specification",
        "capability": "framework for versioned transport-agnostic JSON Trust Tasks",
    },
    "tsp": {
        "repository": "trustoverip/tswg-tsp-specification",
        "commit": "ea01152425d281da944f40e8da799d7fa7a79f51",
        "kind": "normative-specification",
        "capability": "transport/endpoint semantics",
    },
    "dtg-credentials": {
        "repository": "trustoverip/dtgwg-cred-spec",
        "commit": "344a66af868c192f15b511e7116ccab2039221de",
        "kind": "normative-specification",
        "capability": "RCard/VRC credential semantics",
    },
    "openvtc-vti": {
        "repository": "OpenVTC/verifiable-trust-infrastructure",
        "commit": "a71a1ca5766810ccd040f9b5f76f6c97dc41e168",
        "kind": "implementation",
        "capability": "VTA/VTC, key custody, ACL/policy, TSP and versioned Trust Task machinery",
    },
}


class StandardsBoundaryReview:
    """Evidence-bounded substitution review.

    A substitution is only 'executed' when an independently governed implementation
    has actually replaced the Lab adapter in the tested path. Pinned specifications
    can constrain semantics but do not count as implementation substitution.
    """

    def __init__(self) -> None:
        self.components = {
            "TrustTaskCodec": {
                "baseline": "trust-tasks",
                "status": "normative-semantic-binding",
                "reason": "Framework semantics are pinned and preserved; ARA research-query remains a Lab-local task profile and is not claimed as registered Trust Task conformance.",
            },
            "RelationshipTransport": {
                "baseline": "tsp",
                "implementation_candidate": "openvtc-vti",
                "status": "residual-adapter",
                "reason": "TSP semantics and an OpenVTC TSP implementation are evidenced, but no pinned in-Lab endpoint instance has replaced the Phase 6 file/subprocess transport.",
            },
            "ProtectedSigner": {
                "baseline": "openvtc-vti",
                "status": "residual-adapter",
                "reason": "OpenVTC VTA is a real protected trust implementation, but an exact ARA signed-action request/API mapping has not been executed; substitution would require unproven glue.",
            },
            "ParticipantCardProvider": {
                "baseline": "dtg-credentials",
                "status": "normative-semantic-binding",
                "reason": "RCard semantics are pinned, but no independently executed RCard provider is in the ARA path.",
            },
            "RelationshipEdgeProvider": {
                "baseline": "dtg-credentials",
                "status": "normative-semantic-binding",
                "reason": "VRC semantics are pinned; no runtime VRC implementation has replaced the local relationship-recognition fixture.",
            },
        }

    def report(self) -> dict[str, Any]:
        material = {
            "baselines": BASELINES,
            "components": self.components,
            "executed_substitutions": [
                name for name, item in self.components.items() if item["status"] == "implementation-substituted"
            ],
            "residual_adapters": [
                name for name, item in self.components.items() if item["status"] == "residual-adapter"
            ],
            "semantic_bindings": [
                name for name, item in self.components.items() if item["status"] == "normative-semantic-binding"
            ],
        }
        return {**material, "review_ref": digest(material)}

    @staticmethod
    def classify_transport(*, authenticated_channel: bool, relationship_authority: bool) -> dict[str, Any]:
        return {
            "channel_authenticated": authenticated_channel,
            "relationship_authority": relationship_authority,
            "code": "transport_not_relationship_authority" if authenticated_channel and not relationship_authority else "unchanged",
        }

    @staticmethod
    def classify_vta_use(*, protected_key_use: bool, workflow_authorized: bool) -> dict[str, Any]:
        return {
            "protected_key_use": protected_key_use,
            "workflow_authorized": workflow_authorized,
            "authorization": "deny" if protected_key_use and not workflow_authorized else "unchanged",
            "code": "protected_key_use_not_policy_authorization" if protected_key_use and not workflow_authorized else "unchanged",
        }

    @staticmethod
    def classify_rcard(*, self_asserted_standing: bool, verified_standing: bool) -> dict[str, Any]:
        return {
            "standing": "reported" if self_asserted_standing and not verified_standing else "verified" if verified_standing else "unknown",
            "code": "self_assertion_not_verified_standing" if self_asserted_standing and not verified_standing else "unchanged",
        }

    @staticmethod
    def classify_vrc(*, relationship_recognized: bool, delegation: bool, agreement: bool, capability: bool) -> dict[str, Any]:
        if relationship_recognized and not (delegation or agreement or capability):
            return {"authorization": "none", "code": "relationship_recognition_not_authority"}
        return {"authorization": "unchanged", "code": "unchanged"}

    @staticmethod
    def classify_registry(*, lookup_success: bool, permission_to_act: bool) -> dict[str, Any]:
        if lookup_success and not permission_to_act:
            return {"authorization": "none", "code": "registry_lookup_not_permission"}
        return {"authorization": "unchanged", "code": "unchanged"}

    @staticmethod
    def classify_current_control(*, current_key_control: bool, historical_authority_proved: bool) -> dict[str, Any]:
        if current_key_control and not historical_authority_proved:
            return {"historical_authority": False, "code": "current_control_not_historical_authority"}
        return {"historical_authority": historical_authority_proved, "code": "unchanged"}

    @staticmethod
    def classify_community_assurance(*, community_assured: bool, universal_authorization: bool) -> dict[str, Any]:
        if community_assured and not universal_authorization:
            return {"authorization": "bounded", "code": "community_assurance_not_universal_authorization"}
        return {"authorization": "unchanged", "code": "unchanged"}
