#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / "cases" / "ara-minimum-executable-relationship"
MAP = CASE / "architecture-to-code.yaml"
README = CASE / "README.md"

REQUIRED_CONCEPTS = {
    "persistent-agent-role",
    "role-record",
    "agreement-object",
    "authority-and-policy",
    "scoped-capability",
    "exact-trust-task",
    "protected-signing",
    "independent-counterparty",
    "distributed-vrr",
    "lifecycle-continuity",
    "relationship-view",
    "adversarial-assurance",
    "standards-boundary",
    "programme-admission",
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    mapping = yaml.safe_load(MAP.read_text(encoding="utf-8"))
    concepts = mapping.get("concepts", [])
    ids = [row.get("id") for row in concepts]

    missing_concepts = sorted(REQUIRED_CONCEPTS - set(ids))
    extra_duplicates = sorted({x for x in ids if ids.count(x) > 1})
    if missing_concepts:
        fail(errors, f"missing architecture concepts: {missing_concepts}")
    if extra_duplicates:
        fail(errors, f"duplicate architecture concepts: {extra_duplicates}")

    for row in concepts:
        cid = row.get("id", "<missing-id>")
        for key in ("architecture_concept", "claim", "runner", "status", "boundary"):
            if not row.get(key):
                fail(errors, f"{cid}: missing {key}")
        impl = row.get("implementation", [])
        evidence = row.get("evidence", [])
        if not impl:
            fail(errors, f"{cid}: no implementation paths")
        if not evidence:
            fail(errors, f"{cid}: no evidence paths")
        for path in [*impl, *evidence, row.get("runner")]:
            if not path:
                continue
            target = ROOT / path
            if not target.exists():
                fail(errors, f"{cid}: missing mapped path {path}")

    readme = README.read_text(encoding="utf-8")
    required_readme_phrases = [
        "Current status: Interoperability Tested",
        "bounded executable semantic composition",
        "architecture-to-code.yaml",
        "FOLLOW-ALONG.md",
        "experiments/ara-program-admission/run.py --check",
        "The source architecture document itself is not stored in this repository",
    ]
    for phrase in required_readme_phrases:
        if phrase not in readme:
            fail(errors, f"README missing required phrase: {phrase}")

    stale_markers = [
        "Status: pre-admission construction",
        "Until then, `IC-ARA-REL-001` is a pre-admission experimental construction.",
    ]
    for marker in stale_markers:
        if marker in readme:
            fail(errors, f"README contains stale present-tense marker: {marker}")

    required_docs = [
        CASE / "FOLLOW-ALONG.md",
        CASE / "final-claim-boundary.md",
        CASE / "promotion-gates.yaml",
        ROOT / "experiments" / "ara-program-admission" / "README.md",
        ROOT / "evidence" / "ara-minimum-executable-relationship" / "evidence-manifest.json",
    ]
    for path in required_docs:
        if not path.exists():
            fail(errors, f"missing follow-along foundation file: {path.relative_to(ROOT)}")

    report = {
        "case_id": "IC-ARA-REL-001",
        "result": "documentation_foundation_valid" if not errors else "documentation_foundation_invalid",
        "mapped_concepts": len(concepts),
        "required_concepts": len(REQUIRED_CONCEPTS),
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if args.check and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
