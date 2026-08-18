#!/usr/bin/env python3
import hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CASE_ID="IC-XSP-002"
CASE_DIR=ROOT/"cases"/"xsp-002"
OUT=ROOT/"evidence"/"xsp-002"
OUT.mkdir(parents=True,exist_ok=True)

def evaluate(v):
    if v.get("did_resolution") != "success": return "deny-resolution"
    if v.get("did_state") != "active": return "deny-did-state"
    if v.get("federation_chain") not in ("valid","not-required"): return "deny-federation"
    if v.get("authority_source") != "verified": return "deny-authority"
    if v.get("metadata_policy") == "attempts-to-widen": return "deny-policy-widening"
    if v.get("requested_action") not in v.get("authority_scope",[]): return "deny-scope"
    if not v.get("evidence_traversable",False): return "deny-untraceable-authority"
    if v.get("local_policy") != "allow": return "deny-policy"
    return "allow"

vectors=[]
for kind in ("valid","invalid"):
  for p in sorted((CASE_DIR/"vectors"/kind).glob("*.json")):
    v=json.loads(p.read_text()); observed=evaluate(v); expected=v["expected"]
    vectors.append({"id":v["id"],"kind":kind,"expected":expected,"observed":observed,"pass":observed==expected,"source":str(p.relative_to(ROOT))})
passed=sum(x["pass"] for x in vectors)
now=os.environ.get("EXECUTED_AT", "2026-08-18T01:10:48Z")
result={"case_id":CASE_ID,"result_id":CASE_ID+"-RESULT-20260818","status":"pass" if passed==len(vectors) else "fail","claim_scope":"executed semantic-composition interoperability only; excludes wire-protocol conformance and external certification","executed_at":now,"observations":[f"{passed}/{len(vectors)} vectors matched declared expected behavior","All decisions were produced by the repository-owned deterministic semantic reference evaluator."],"vectors":vectors}
(OUT/"result.json").write_text(json.dumps(result,indent=2)+"\n")
log={"case_id":CASE_ID,"executed_at":now,"runner":str(Path(__file__).relative_to(ROOT)),"python":"stdlib-only","vector_count":len(vectors),"passed":passed,"failed":len(vectors)-passed}
(OUT/"run-log.json").write_text(json.dumps(log,indent=2)+"\n")
arts=[]
for rel,role in [("result.json","executed-result"),("run-log.json","run-log")]:
    b=(OUT/rel).read_bytes(); arts.append({"path":rel,"role":role,"sha256":hashlib.sha256(b).hexdigest()})
for p in sorted((CASE_DIR/"vectors").rglob("*.json")):
    b=p.read_bytes(); arts.append({"path":os.path.relpath(p, OUT),"role":"test-vector","sha256":hashlib.sha256(b).hexdigest()})
for p,role in [(CASE_DIR/"invariants.yaml","invariant-set"),(CASE_DIR/"ownership.yaml","semantic-ownership"),(CASE_DIR/"known-limitations.md","known-limitations"),(CASE_DIR/"source-basis.md","source-basis"),(Path(__file__),"reference-evaluator")]:
    b=p.read_bytes(); arts.append({"path":os.path.relpath(p, OUT),"role":role,"sha256":hashlib.sha256(b).hexdigest()})
manifest={"case_id":CASE_ID,"evidence_id":CASE_ID+"-EVIDENCE-20260818","claim_scope":result["claim_scope"],"executed_at":now,"runner":str(Path(__file__).relative_to(ROOT)),"artifacts":arts,"result_summary":{"status":result["status"],"vectors":len(vectors),"passed":passed,"failed":len(vectors)-passed}}
(OUT/"evidence-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(f"{CASE_ID}: {result['status'].upper()} ({passed}/{len(vectors)} vectors)")
raise SystemExit(0 if result['status']=='pass' else 1)
