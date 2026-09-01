#!/usr/bin/env python3
from __future__ import annotations
import json
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> int:
    registry = yaml.safe_load((ROOT / "catalog" / "evidence-producers.yaml").read_text(encoding="utf-8"))
    producers = registry.get("producers", [])
    if not producers:
        raise SystemExit("no evidence producers registered")
    producer = next((x for x in producers if x.get("id") == "composed-unlinkability-v1"), None)
    if not producer or producer.get("mode") != "registered-executable":
        raise SystemExit("composed-unlinkability-v1 must be registered-executable")
    required = {"ER-REL-DID-AB", "ER-STATUS-AB", "ER-TASK-AB", "ER-VERIFIER-AB", "ER-CREDENTIAL-ID-AB", "ER-DEVICE-METADATA-AB"}
    if not required.issubset(set(producer.get("requirement_ids", []))):
        raise SystemExit("producer requirement coverage incomplete")
    if not producer.get("observer_model_required") or not producer.get("source_pins_required"):
        raise SystemExit("observer/source pin discipline not required")

    executable_coverage: set[str] = set()
    for name, entry in (producer.get("entrypoints") or {}).items():
        if entry.get("capability_status") != "executable":
            raise SystemExit(f"{name}: registered producer entrypoint is not executable")
        path = ROOT / str(entry.get("path") or "")
        if not path.is_file():
            raise SystemExit(f"{name}: executable path does not exist: {path}")
        executable_coverage.update(str(v) for v in entry.get("satisfies", []) or [])
    if not required.issubset(executable_coverage):
        raise SystemExit(f"requirements lack executable adapter: {sorted(required - executable_coverage)}")

    schema = json.loads((ROOT / "schemas" / "interop-evidence-package-v1.schema.json").read_text(encoding="utf-8"))
    for key in ("schema", "observer", "source_pins", "requirement_id", "experiment", "surfaces"):
        if key not in schema["required"]:
            raise SystemExit(f"evidence schema missing required {key}")
    print("PASS evidence producer registry: all declared requirements have real executable entrypoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
