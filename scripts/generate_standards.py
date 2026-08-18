#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "standards/register.yaml").read_text())
standards = sorted(data["standards"], key=lambda x: x["id"])
out = ROOT / "standards/generated"
out.mkdir(parents=True, exist_ok=True)

rows = []
for s in standards:
    projects = ", ".join(f"`{k}` ({v})" for k, v in sorted(s["portfolio_relevance"].items()))
    rows.append(f"| `{s['id']}` | [{s['title']}]({s['canonical_uri']}) | {s['publisher']} | {', '.join(s['domains'])} | {s['review']['state']} | {'yes' if s['normative_dependency'] else 'no'} | {projects} |")

register = """---
layout: default
title: Standards Register
nav_order: 9
---
# Portfolio Standards Register

> **Source acknowledgement:** Initial standards discovery is informed by the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC). GSMI is a discovery source, not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply GSMI/GBBC endorsement.

This page is generated from `standards/register.yaml`. Do not hand-edit it.

| ID | Standard | Publisher | Domains | Review state | Normative dependency | Portfolio relevance |
|---|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"
(out / "standards-register.md").write_text(register)

projects = sorted({p for s in standards for p in s["portfolio_relevance"]})
header = "| Standard | " + " | ".join(f"`{p}`" for p in projects) + " |\n"
sep = "|---|" + "---|" * len(projects) + "\n"
body = []
for s in standards:
    cells = [s["portfolio_relevance"].get(p, "—") for p in projects]
    body.append(f"| `{s['id']}` | " + " | ".join(cells) + " |")
matrix = """---
layout: default
title: Standards × Portfolio Matrix
nav_order: 10
---
# Standards × Portfolio Matrix

Generated applicability view. Values indicate local analytical relevance, **not conformance or endorsement**.

""" + header + sep + "\n".join(body) + "\n"
(out / "portfolio-matrix.md").write_text(matrix)

counts = Counter(s["review"]["state"] for s in standards)
summary = {"version": 1, "total": len(standards), "states": dict(sorted(counts.items())), "normative_dependencies": sum(bool(s["normative_dependency"]) for s in standards)}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(f"Generated standards views for {len(standards)} entries.")
