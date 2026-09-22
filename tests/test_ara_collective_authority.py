from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "experiments" / "ara-authority-at-commitment" / "run.py"
VECTORS = ROOT / "cases" / "ara-minimum-executable-relationship" / "authority-at-commitment-vectors.json"

spec = importlib.util.spec_from_file_location("ara_authority_at_commitment", RUNNER)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def vectors():
    payload = json.loads(VECTORS.read_text(encoding="utf-8"))
    return {item["id"]: item for item in payload["vectors"]}


def test_current_two_of_three_collective_authority_permits():
    item = vectors()["AAC-PERMIT-COLLECTIVE-2-OF-3"]
    assert mod.evaluate(item["input"]) == "permit"


def test_one_of_three_cannot_be_upgraded_to_collective_authority():
    item = vectors()["AAC-DENY-COLLECTIVE-1-OF-3"]
    assert mod.evaluate(item["input"]) == "deny"


def test_missing_composition_rule_remains_indeterminate():
    item = vectors()["AAC-INDETERMINATE-COLLECTIVE-RULE-MISSING"]
    assert mod.evaluate(item["input"]) == "indeterminate"


def test_stale_membership_denies_new_commitment():
    item = vectors()["AAC-DENY-COLLECTIVE-STALE-MEMBERSHIP"]
    assert mod.evaluate(item["input"]) == "deny"


def test_stale_threshold_rule_denies_new_commitment():
    item = vectors()["AAC-DENY-COLLECTIVE-STALE-RULE"]
    assert mod.evaluate(item["input"]) == "deny"


def test_duplicate_member_does_not_count_twice():
    item = vectors()["AAC-DENY-COLLECTIVE-DUPLICATE-MEMBER"]
    collective = item["input"]["collective_authority"]
    assert len(collective["approvals"]) == collective["threshold_required"]
    assert len({x["member"] for x in collective["approvals"]}) < collective["threshold_required"]
    assert mod.evaluate(item["input"]) == "deny"


def test_legacy_single_actor_vectors_remain_compatible():
    for vector_id in (
        "AAC-PERMIT-001",
        "AAC-DENY-REVOKED",
        "AAC-DENY-SCOPE",
        "AAC-INDETERMINATE-APPROVAL",
        "AAC-DENY-WRONG-APPROVAL",
        "AAC-DENY-STALE-APPROVAL",
        "AAC-INDETERMINATE-STATUS",
    ):
        item = vectors()[vector_id]
        assert mod.evaluate(item["input"]) == item["expected"]
