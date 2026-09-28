#!/usr/bin/env python3
import argparse, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
MATRIX=ROOT/"cases/ara-minimum-executable-relationship/decision-resolution-vectors.json"

def evaluate(v):
    event=v["event"]
    non_resolution={"unauthorized_peer","repeated_peer_assertions","out_of_scope_delegate","workflow_progression_only"}
    if event in non_resolution:
        return {"condition":"unresolved","basis":"none","authority_changed":False}
    if event=="in_scope_delegate":
        return {"condition":"resolved","basis":"authority_change","authority_changed":True}
    if event=="authoritative_evidence_changes_predicate":
        return {"condition":"resolved","basis":"evidence_change","authority_changed":False}
    if event=="legitimate_policy_change":
        return {"condition":"resolved","basis":"policy_change","authority_changed":False}
    if event=="authority_revoked_before_commitment":
        return {"condition":"unresolved","basis":"lifecycle_change","authority_changed":True}
    if event=="evidence_stale_before_commitment":
        return {"condition":"unresolved","basis":"lifecycle_change","authority_changed":False}
    raise ValueError(event)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--check",action="store_true"); ap.add_argument("--output")
    args=ap.parse_args()
    doc=json.loads(MATRIX.read_text())
    assert doc["case_id"]=="IC-ARA-REL-001"
    assert any("SIMULATION_01_RUNBOOK.md" in s for s in doc["research_provenance"])
    results=[]
    for v in doc["scenarios"]:
        got=evaluate(v)
        expected={"condition":v["expected_condition"],"basis":v["resolution_basis"],"authority_changed":v["authority_changed"]}
        ok=got==expected
        results.append({"id":v["id"],"pass":ok,"expected":expected,"observed":got})
        if not ok: raise AssertionError(f"{v['id']}: {got} != {expected}")
    out={"case_id":doc["case_id"],"status":"pass","passed":len(results),"failed":0,"results":results,
         "limitations":["Deterministic semantic pressure evidence; not external certification or production authorization evidence."]}
    if args.output: Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(f"ARA decision resolution: PASS ({len(results)} vectors)")

if __name__=="__main__": main()
