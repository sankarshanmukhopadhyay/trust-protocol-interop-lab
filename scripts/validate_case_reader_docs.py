#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "cases"

REQUIRED_HEADINGS = (
    "## At a glance",
    "## Concrete scenario",
    "## Where it resolved",
    "## What remains unresolved",
)

errors: list[str] = []
case_dirs = sorted(path for path in CASES.iterdir() if path.is_dir())

for case_dir in case_dirs:
    readme = case_dir / "README.md"
    rel = readme.relative_to(ROOT)
    if not readme.exists():
        errors.append(f"{rel}: missing README.md")
        continue

    text = readme.read_text(encoding="utf-8")

    if len(text.strip()) < 1800:
        errors.append(f"{rel}: too terse for the reader-facing case contract (<1800 chars)")

    for heading in REQUIRED_HEADINGS:
        if heading not in text:
            errors.append(f"{rel}: missing required heading {heading!r}")

    if not re.search(r"^## Why this matters", text, flags=re.MULTILINE):
        errors.append(f"{rel}: missing a 'Why this matters' section")

    if "Status" not in text[:1800]:
        errors.append(f"{rel}: maturity/status is not visible near the top")

    if not re.search(r"[[^]]+]([^)]+)", text):
        errors.append(f"{rel}: no navigable Markdown link to evidence/context")

if errors:
    print("Case reader-documentation validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print(f"PASS {len(case_dirs)} case READMEs satisfy the newcomer-oriented documentation contract")
