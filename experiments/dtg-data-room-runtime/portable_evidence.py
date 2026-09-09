from __future__ import annotations


def build_portable_result(
    legacy: dict,
    producer_revision: str,
    artifact_sha256: str,
    *,
    proposition_key: str,
    evidence_contract_key: str,
    execution_id: str,
    execution_timestamp: str,
) -> dict:
    target = legacy["target"]
    pin = {"repository": target["repository"], "revision": target["revision"], "role": "implementation"}
    case = legacy["case"]
    return {
        "schema": "rahp-evidence-producer-result/v1",
        "producer": {
            "id": "interop-lab:data-room-runtime",
            "implementation": "experiments/dtg-data-room-runtime/run_current_openvtc.py",
            "repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab",
            "revision": producer_revision,
        },
        "obligation": {
            "proposition_key": proposition_key,
            "evidence_contract_key": evidence_contract_key,
            "evidence_requirement_ids": sorted(legacy["propositions"].keys()),
        },
        "source": {"pins": [pin]},
        "execution": {
            "id": execution_id,
            "runner": "run_current_openvtc.py",
            "timestamp": execution_timestamp,
            "determinism": "environment-dependent",
            "status": "succeeded",
        },
        "evidence": {
            "status": "observed",
            "evidence_class": legacy["evidence_class"],
            "artifacts": [{
                "name": "current-openvtc-data-room-evidence.json",
                "media_type": "application/json",
                "sha256": artifact_sha256,
                "provenance": {"producer_id": "interop-lab:data-room-runtime"},
            }],
            "observations": [{"case": case, "propositions": legacy["propositions"]}],
        },
        "claim_boundary": {
            "supports": [f"bounded observations for {case}"],
            "does_not_support": ["terminal assurance PASS", "deployment-wide inference"],
            "limitations": [legacy["claim_boundary"]],
            "residual_uncertainty": legacy["claim_boundary"],
        },
        "freshness": {
            "valid_against": [pin],
            "invalidation_keys": [f"source:{target['repository']}@{target['revision']}"],
        },
    }
