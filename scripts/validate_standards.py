#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
standards = json.loads((ROOT / "standards/register.yaml").read_text())
sources = json.loads((ROOT / "standards/sources.yaml").read_text())
mapping = json.loads((ROOT / "standards/mappings/portfolio.yaml").read_text())

allowed_rel = set(mapping["relationship_types"])
source_ids = {s["id"] for s in sources["sources"]}
ids = set()
errors = []

for s in standards["standards"]:
    sid = s.get("id", "")
    if not sid.startswith("STD-"):
        errors.append(f"{sid or '<missing>'}: invalid id")
    if sid in ids:
        errors.append(f"{sid}: duplicate id")
    ids.add(sid)
    if not s.get("title") or not s.get("publisher"):
        errors.append(f"{sid}: title and publisher are required")
    uri = s.get("canonical_uri", "")
    parsed = urlparse(uri)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append(f"{sid}: canonical_uri must be absolute HTTP(S)")
    if not s.get("domains"):
        errors.append(f"{sid}: at least one domain is required")
    if not s.get("portfolio_relevance"):
        errors.append(f"{sid}: portfolio_relevance is required")
    unknown = set(s.get("relationships", [])) - allowed_rel
    if unknown:
        errors.append(f"{sid}: unknown relationships {sorted(unknown)}")
    if s.get("normative_dependency") and "depends-on" not in s.get("relationships", []):
        errors.append(f"{sid}: normative_dependency requires depends-on relationship")
    review = s.get("review", {})
    if review.get("state") not in {"candidate", "mapped", "analysed", "pressure-tested", "retired"}:
        errors.append(f"{sid}: invalid review state")
    for src in s.get("source_relationships", []):
        if src.get("source_id") not in source_ids:
            errors.append(f"{sid}: unknown source_id {src.get('source_id')}")

if errors:
    print("Standards validation failed:")
    for e in errors:
        print(f"- {e}")
    raise SystemExit(1)
print(f"Standards validation passed: {len(ids)} entries; {len(source_ids)} governed source(s).")
