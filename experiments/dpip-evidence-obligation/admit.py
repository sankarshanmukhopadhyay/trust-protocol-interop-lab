#!/usr/bin/env python3
"""Admit only DPIP evidence obligations the Interop Lab can legitimately observe.

This is an acquisition-boundary tool. It emits no privacy, discrimination, legitimacy,
or portfolio-assurance judgment.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "dpip-evidence-obligation/v1"
OUTPUT_SCHEMA = "interop-dpip-evidence-admission/v1"


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise ValueError(msg)


def evaluate(ob: dict[str, Any]) -> dict[str, Any]:
    require(ob.get("schema") == SCHEMA, f"schema must be {SCHEMA}")
    require(isinstance(ob.get("id"), str) and ob["id"].startswith("DPIP-EG-"), "obligation id is required")
    supplier = ob.get("supplier") or {}
    access = ob.get("access") or {}
    maturity = (ob.get("evidence_maturity") or {}).get("minimum_required")
    target = ob.get("target")
    source_class = supplier.get("evidence_source_class")
    blocker = access.get("blocker")

    status = "SUPPLIER_OR_AUTHORITY_REQUIRED"
    reason = "evidence-source-class-not-independent-lab-observable"
    if access.get("status") == "BLOCKED" or blocker not in {None, "NONE"}:
        status = "BLOCKED"
        reason = blocker or "UNSPECIFIED_BLOCKER"
    elif maturity in {"E3", "E4", "E5"} and not (isinstance(target, dict) and target.get("repository") and target.get("revision")):
        status = "BLOCKED"
        reason = "NO_BOUND_TARGET_REVISION"
    elif source_class in {"STATIC_IMPLEMENTATION", "BLACK_BOX_RUNTIME"}:
        status = "ADMISSIBLE"
        reason = "independently-observable"
    elif source_class == "WHITE_BOX_RUNTIME" and supplier.get("role") == "INTEROP_LAB":
        status = "ADMISSIBLE"
        reason = "explicit-lab-observer-access"

    return {
        "schema": OUTPUT_SCHEMA,
        "obligation_id": ob["id"],
        "admission": status,
        "reason": reason,
        "target": target,
        "observer": ob.get("observer"),
        "required_maturity": maturity,
        "required_observations": ob.get("required_observations", []),
        "claim_boundary": {
            "lab_may_claim": ["observation availability", "experiment provenance", "bounded observation result"],
            "lab_may_not_claim": ["privacy PASS/FAIL", "discrimination", "legitimacy", "harm", "portfolio assurance", "deployment behavior without target-bound runtime evidence"]
        }
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    doc = json.loads(args.input.read_text(encoding="utf-8"))
    items = doc if isinstance(doc, list) else doc.get("obligations", [doc])
    require(isinstance(items, list) and items, "input must contain obligation(s)")
    results = [evaluate(item) for item in items]
    bundle = {"schema": "interop-dpip-evidence-admission-bundle/v1", "results": results}
    text = json.dumps(bundle, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if args.check:
        require(all(r["admission"] in {"ADMISSIBLE", "BLOCKED", "SUPPLIER_OR_AUTHORITY_REQUIRED"} for r in results), "invalid admission")
        print(f"PASS: {len(results)} DPIP evidence obligation(s) classified without assurance overclaim")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
