#!/usr/bin/env python3
"""Validate the reader-facing documentation contract for mature Interop Cases."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "interoperability-cases.yaml"

# Semantic markers deliberately allow richer domain-specific pages while still
# requiring the same reader journey. All matching is case-insensitive.
REQUIRED_SEMANTICS = {
    "question": ("## question", "## what was tested"),
    "composition boundary": (
        "## composition boundary",
        "## the bounded scenario",
        "## the most important architectural separations",
    ),
    "admitted claim": (
        "## admitted claim",
        "**admitted claim:**",
        "**evidence scope:**",
        "## final claim",
    ),
    "scenarios/vectors": (
        "scenarios",
        "vectors",
        "positive vectors",
        "negative vectors",
        "adversarial",
    ),
    "evidence": ("evidence manifest", "## evidence", "## executed assurance result"),
    "reproduction": (
        "## reproduce",
        "## run the experiment",
        "reproduction instructions",
        "evidence target",
    ),
    "limitations/non-claims": (
        "## limitations",
        "known limitations",
        "does **not** establish",
        "does not claim",
        "excludes",
    ),
    "upstream/next disposition": (
        "## upstream",
        "upstream",
        "follow-on",
        "next disposition",
    ),
}

# If the catalog declares one of these paths for an interoperability-tested
# case, promotion is invalid when the artifact is missing.
PATH_GROUPS = {
    "scenario/vector basis": ("scenarios", "vectors"),
    "evidence": ("evidence", "result"),
    "reproduction": ("experiment",),
    "limitations": ("limitations",),
}


def exists(path_value: str) -> bool:
    return (ROOT / path_value).exists()


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    failures: list[str] = []
    tested = [c for c in catalog["cases"] if c.get("status") == "interoperability-tested"]

    if not tested:
        failures.append("catalog contains no interoperability-tested cases")

    for case in tested:
        case_id = case.get("id", "<unknown>")
        paths = case.get("paths") or {}
        readme = paths.get("readme")
        if not readme:
            failures.append(f"{case_id}: no paths.readme declared")
            continue

        readme_path = ROOT / readme
        if not readme_path.is_file():
            failures.append(f"{case_id}: landing page missing: {readme}")
            continue

        text = readme_path.read_text(encoding="utf-8").lower()
        for semantic, markers in REQUIRED_SEMANTICS.items():
            if not any(marker.lower() in text for marker in markers):
                failures.append(f"{case_id}: landing page lacks {semantic}")

        for label, keys in PATH_GROUPS.items():
            declared = [paths[k] for k in keys if paths.get(k)]
            if not declared:
                failures.append(f"{case_id}: catalog declares no {label} path")
                continue
            missing = [p for p in declared if not exists(p)]
            if missing:
                failures.append(f"{case_id}: missing {label} artifact(s): {', '.join(missing)}")

    if failures:
        print("FAIL Interop Case documentation contract")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print(f"PASS Interop Case documentation contract: {len(tested)} tested case(s)")
    for case in tested:
        print(f" - {case['id']}: {case['paths']['readme']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
