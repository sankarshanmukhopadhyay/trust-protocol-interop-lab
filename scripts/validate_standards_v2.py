#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]


def load_json_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def fail(message):
    raise SystemExit(f"standards-v2 validation failed: {message}")


sources = load_json_yaml(ROOT / "standards" / "sources.yaml")
source_ids = {item["id"] for item in sources.get("sources", [])}
bodies = load_json_yaml(ROOT / "standards" / "bodies.yaml")
body_ids = {item["id"] for item in bodies.get("bodies", [])}

for body in bodies.get("bodies", []):
    required = {"id", "name", "class", "authority_level", "jurisdiction", "standards_process", "publication_authority", "canonical_uri"}
    missing = required - body.keys()
    if missing:
        fail(f"{body.get('id', '<body>')} missing {sorted(missing)}")
    if body.get("parent_body_id") and body["parent_body_id"] not in body_ids:
        fail(f"{body['id']} references unknown parent body {body['parent_body_id']}")

core = load_json_yaml(ROOT / "standards" / "register.yaml")
entries = [(ROOT / "standards" / "register.yaml", e) for e in core.get("standards", [])]
for shard in sorted((ROOT / "standards" / "corpus").glob("*.yaml")):
    data = load_json_yaml(shard)
    entries.extend((shard, e) for e in data.get("standards", []))

seen = set()
for path, entry in entries:
    sid = entry.get("id")
    if not sid or not sid.startswith("STD-"):
        fail(f"{path}: invalid or missing standard id")
    if sid in seen:
        fail(f"duplicate standard id {sid}")
    seen.add(sid)

    for key in ("title", "publisher", "canonical_uri", "domains", "portfolio_relevance", "relationships", "normative_dependency", "review", "verification"):
        if key not in entry:
            fail(f"{sid} missing {key}")

    uri = entry["canonical_uri"]
    parsed = urlparse(uri)
    if parsed.scheme != "https" or not parsed.netloc:
        fail(f"{sid} canonical_uri must be HTTPS")

    for rel in entry.get("source_relationships", []):
        if rel.get("source_id") not in source_ids:
            fail(f"{sid} references unknown source {rel.get('source_id')}")

    for key in ("publisher_id", "technical_committee_id"):
        if entry.get(key) and entry[key] not in body_ids:
            fail(f"{sid} references unknown body {entry[key]}")

    verification = entry["verification"]
    for key in ("state", "verified_on", "version", "publisher_status", "baseline_uri", "evidence_uris", "lifecycle_note"):
        if key not in verification:
            fail(f"{sid} verification missing {key}")

    if path.parent.name == "corpus":
        for key in ("artifact_type", "monitoring"):
            if key not in entry:
                fail(f"{sid} corpus entry missing {key}")
        if entry["monitoring"].get("baseline_pinned") is not True:
            fail(f"{sid} corpus baseline must be pinned")

print(f"standards-v2 validation passed: {len(seen)} total standards across core register and corpus shards; {len(body_ids)} standards bodies; {len(source_ids)} sources")
