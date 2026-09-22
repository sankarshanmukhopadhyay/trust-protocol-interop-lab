from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "experiments" / "trust-tasks-cryptosuite-interop" / "run.py"
MATRIX = ROOT / "cases" / "trust-tasks-cryptosuite-interop" / "matrix.json"

spec = importlib.util.spec_from_file_location("trust_tasks_cryptosuite_interop", RUNNER)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def payload():
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    return data, {x["id"]: x for x in data["implementations"]}, {x["id"]: x for x in data["cases"]}


def test_shared_jcs_suite_is_verify_capable():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-001"], impls) == "verify-capable"


def test_disjoint_suite_sets_do_not_interoperate():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-002"], impls) == "unsupported-cryptosuite"
    assert mod.evaluate(cases["CSI-003"], impls) == "unsupported-cryptosuite"


def test_shared_rdfc_suite_is_verify_capable():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-004"], impls) == "verify-capable"


def test_invalid_proof_is_not_conflated_with_unsupported_suite():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-005"], impls) == "invalid-proof"


def test_unknown_suite_is_explicitly_unsupported():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-006"], impls) == "unsupported-cryptosuite"


def test_producer_cannot_claim_suite_it_does_not_support():
    _, impls, cases = payload()
    assert mod.evaluate(cases["CSI-007"], impls) == "producer-capability-mismatch"


def test_no_silent_suite_fallback_is_present():
    source = RUNNER.read_text(encoding="utf-8")
    assert "fallback" not in source.lower()
    _, impls, cases = payload()
    case = dict(cases["CSI-002"])
    assert mod.evaluate(case, impls) == "unsupported-cryptosuite"
