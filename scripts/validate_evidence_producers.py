#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, yaml

ROOT=pathlib.Path(__file__).resolve().parents[1]

def main():
    registry=yaml.safe_load((ROOT/"catalog"/"evidence-producers.yaml").read_text())
    producers=registry.get("producers",[])
    if not producers:
        raise SystemExit("no evidence producers registered")
    p=next((x for x in producers if x.get("id")=="composed-unlinkability-v1"),None)
    if not p:
        raise SystemExit("composed-unlinkability-v1 missing")
    required={"ER-REL-DID-AB","ER-STATUS-AB","ER-TASK-AB","ER-VERIFIER-AB","ER-CREDENTIAL-ID-AB","ER-DEVICE-METADATA-AB"}
    if not required.issubset(set(p.get("requirement_ids",[]))):
        raise SystemExit("producer requirement coverage incomplete")
    if not p.get("observer_model_required") or not p.get("source_pins_required"):
        raise SystemExit("observer/source pin discipline not required")
    schema=json.loads((ROOT/"schemas"/"interop-evidence-package-v1.schema.json").read_text())
    for key in ("observer","source_pins","requirement_id"):
        if key not in schema["required"]:
            raise SystemExit(f"evidence schema missing required {key}")
    print("PASS evidence producer registry")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
