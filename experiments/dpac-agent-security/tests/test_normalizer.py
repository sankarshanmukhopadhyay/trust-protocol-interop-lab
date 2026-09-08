#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("dpac_ash_normalizer", ROOT / "normalizer.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
normalize_record = module.normalize_record


def record(*, verdict="PASS", serviced=True, expected=0, observed=0, mapping="executed", applicable=True, coverage_complete=True):
    return {
        "vector_id": "DPAC-ASH-001",
        "attack_class": "authority-bypass",
        "applicable": applicable,
        "mapping": {"status": mapping, "coverage_complete": coverage_complete},
        "expected": {"effect_delta": expected},
        "observed": {
            "target_serviced": serviced,
            "harness_verdict": verdict,
            "effect_delta": observed,
        },
        "harness": {
            "project": "msaleme/red-team-blue-team-agent-fabric",
            "version": "4.21.1",
            "release_commit": "455fa46d35c0c13539c835bd758baced04ca2aa9",
        },
        "target": {
            "case_id": "IC-DPAC-ACTUATION-001",
            "experiment": "dpac-enforced-boundary",
            "lab_revision": "selftest",
        },
        "evidence": {"lab_observation": "self-test"},
    }


def check(expected_result: str, **kwargs):
    actual = normalize_record(record(**kwargs))["result"]
    assert actual == expected_result, (kwargs, expected_result, actual)


def main() -> int:
    check("pass")
    check("fail", verdict="PASS", expected=0, observed=1)
    check("not-observable", verdict="PASS", serviced=False)
    check("not-observable", verdict="INCONCLUSIVE")
    check("harness-gap", mapping="candidate")
    check("harness-gap", mapping="unresolved")
    check("not-applicable", applicable=False)
    check("not-observable", verdict="FAIL", expected=0, observed=0)
    check("pass", verdict="PASS", expected=1, observed=1)
    check("fail", verdict="PASS", expected=1, observed=0)

    # Partial coverage cannot become a full Lab PASS, but an unexpected effect
    # must still dominate the coverage downgrade and fail the proposition.
    check("not-observable", verdict="PASS", coverage_complete=False)
    check("fail", verdict="PASS", coverage_complete=False, expected=0, observed=1)

    print("PASS dpac-agent-security normalizer self-test")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
