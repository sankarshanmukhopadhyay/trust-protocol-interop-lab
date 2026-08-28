#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def run(path: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / path), "--check"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return json.loads(proc.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    phase10 = run("experiments/ara-adversarial-assurance/run.py")
    phase11 = run("experiments/ara-standards-boundary/run.py")

    gates = yaml.safe_load((ROOT / "cases/ara-minimum-executable-relationship/promotion-gates.yaml").read_text())
    gate_rows = gates["gates"]
    all_gates = len(gate_rows) == 12 and all(g["status"] == "satisfied" for g in gate_rows)

    catalog = yaml.safe_load((ROOT / "catalog/interoperability-cases.yaml").read_text())
    entry = next((c for c in catalog["cases"] if c["id"] == "IC-ARA-REL-001"), None)
    catalog_ok = entry is not None and entry.get("status") == "interoperability-tested"

    checks = {
        "phase10_green": phase10["summary"]["failed"] == 0,
        "phase11_green": phase11["summary"]["failed"] == 0,
        "all_12_gates_satisfied": all_gates,
        "promotion_ready": gates.get("promotion_ready") is True,
        "gate_status": gates.get("status") == "interoperability-tested",
        "catalog_admitted": catalog_ok,
        "final_claim_boundary_present": (ROOT / "cases/ara-minimum-executable-relationship/final-claim-boundary.md").exists(),
        "evidence_manifest_present": (ROOT / "evidence/ara-minimum-executable-relationship/evidence-manifest.json").exists(),
    }
    passed = all(checks.values())
    report = {
        "case_id": "IC-ARA-REL-001",
        "result": "admission_evidence_satisfied" if passed else "admission_evidence_incomplete",
        "checks": checks,
        "claim": "bounded executable semantic composition only",
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if (passed or not args.check) else 1


if __name__ == "__main__":
    raise SystemExit(main())
