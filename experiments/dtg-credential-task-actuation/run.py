#!/usr/bin/env python3
"""Produce bounded machine-readable evidence for issue #163.

This adapter composes already-established repository evidence without promoting it into
an end-to-end claim. Vectors lacking a target-native integrated evaluator are explicitly
classified not-implemented or not-observable.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = ROOT / "cases/dtg-credential-task-actuation/scenario.yaml"


def run_json(path: str) -> dict:
    cp = subprocess.run([sys.executable, path], cwd=ROOT, text=True, capture_output=True, check=False)
    if cp.returncode != 0:
        raise RuntimeError(cp.stderr.strip() or cp.stdout.strip())
    return json.loads(cp.stdout)


def main() -> int:
    # Reuse the existing action-time evidence producer; do not duplicate its authority logic.
    action = run_json("experiments/dtg-vdc-vac-composition/run_action_time.py")
    by_id = {v["id"]: v for v in action["vectors"]}
    vectors = [
        {"id":"CTA-POS-001","classification":"not-implemented","observed":"integrated current-authority evaluator absent","effect_count":"not-observable"},
        {"id":"CTA-NEG-001","classification":"supported","observed":by_id["AT-NEG-001"]["expected"],"effect_count":0},
        {"id":"CTA-NEG-002","classification":"supported","observed":by_id["AT-NEG-002"]["expected"],"effect_count":0},
        {"id":"CTA-NEG-003","classification":"supported","observed":by_id["AT-NEG-004"]["expected"],"effect_count":0},
        {"id":"CTA-NEG-004","classification":"not-observable","observed":"no integrated presenter/subject/relationship actuation evaluator evidenced","effect_count":"not-observable"},
        {"id":"CTA-NEG-005","classification":"supported","observed":by_id["AT-NEG-003"]["expected"],"effect_count":0},
        {"id":"CTA-NEG-006","classification":"not-observable","observed":"no consequential side-effect surface available for one-effect replay measurement","effect_count":"not-observable"},
        {"id":"CTA-NEG-007","classification":"supported","observed":by_id["AT-NEG-005"]["expected"],"effect_count":0},
        {"id":"CTA-NEG-008","classification":"not-implemented","observed":"independently administered capability envelope not exposed at integrated actuation boundary","effect_count":"not-observable"},
    ]
    result = {
        "schema":"interop-actuation-evidence/v1",
        "case":"IC-DTG-CREDENTIAL-TASK-ACTUATION-001",
        "issue":163,
        "source_epoch":{
            "credential_spec":"37074bdcd861c51f3e5b7868ce700832b17b73ce",
            "trust_tasks":"84a4329a5f797dec9d240c83ab5d564c120dde8f",
            "openvtc":"3f21929ae5ce870f7c17726120d4aa1c1acbf13c",
            "dtg_credentials":"5cb04fab2d9272ee891b352a4886343ccc86b52b",
        },
        "supporting_evidence":{"action_time_case":action["case"],"runtime_maturity":action.get("runtime_maturity")},
        "vectors":vectors,
        "summary":{
            "supported":sum(v["classification"]=="supported" for v in vectors),
            "divergent":sum(v["classification"]=="divergent" for v in vectors),
            "not_implemented":sum(v["classification"]=="not-implemented" for v in vectors),
            "not_observable":sum(v["classification"]=="not-observable" for v in vectors),
        },
        "rahp_propositions":["P03","P04","P05","P08","P09"],
        "claim_boundary":"No integrated PASS is asserted. Existing semantic and Lab evidence is reused only within its attributable boundary; unavailable target-native surfaces remain explicitly unresolved."
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if result["summary"]["divergent"] else 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, KeyError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
