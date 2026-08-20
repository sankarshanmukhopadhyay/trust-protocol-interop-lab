#!/usr/bin/env python3
"""Execute the bounded ARPA-A2A-ANAB-Trust Tasks semantic composition."""
import hashlib, json, os
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CASE_ID="IC-ARPA-A2A-TT-001"
CASE_DIR=ROOT/"cases"/"arpa-a2a-trust-tasks"
OUT=ROOT/"evidence"/"arpa-a2a-anab"
OUT.mkdir(parents=True,exist_ok=True)

def evaluate(v):
    if v.get("authority_state", "active") != "active": return "deny-before-consequential-execution"
    if "anab_name" in v and v.get("card_name") != v.get("anab_name"): return "deny-name-mismatch"
    if v.get("anab_freshness") not in (None,"fresh"): return "deny-assurance-freshness"
    if v.get("anab_identity_status") in ("revoked","suspended"): return "deny-assurance-status"
    if v.get("anab_identity_status") == "verified" and (not v.get("anab_declaration_digest_match") or not v.get("anab_card_binding_valid")):
        return "deny-assurance-evidence"
    if v.get("advertised_capability") not in v.get("delegated_scope",[]): return "deny-scope-expansion"
    return "allow-policy-evaluation"

vectors=[]
for kind in ("valid","invalid"):
    for p in sorted((CASE_DIR/"vectors"/kind).glob("*.json")):
        v=json.loads(p.read_text()); observed=evaluate(v)
        vectors.append({"id":v["id"],"kind":kind,"expected":v["expected"],"observed":observed,"pass":observed==v["expected"],"source":str(p.relative_to(ROOT))})
passed=sum(item["pass"] for item in vectors)
now=os.environ.get("EXECUTED_AT","2026-08-20T12:00:00Z")
claim="executed semantic composition of ARPA v0.9.5, ANAB v0.10.0 assurance inputs, A2A v1.0 interaction metadata, and Trust Tasks; excludes live-network, cryptographic, upstream-conformance, and certification claims"
result={"case_id":CASE_ID,"result_id":CASE_ID+"-RESULT-20260820","status":"pass" if passed==len(vectors) else "fail","claim_scope":claim,"executed_at":now,"observations":[f"{passed}/{len(vectors)} vectors matched declared behavior","Identity and name assurance remained separate from delegated authority and effect admission."],"vectors":vectors}
(OUT/"result.json").write_text(json.dumps(result,indent=2)+"\n")
log={"case_id":CASE_ID,"executed_at":now,"runner":str(Path(__file__).relative_to(ROOT)),"python":"stdlib-only","vector_count":len(vectors),"passed":passed,"failed":len(vectors)-passed}
(OUT/"run-log.json").write_text(json.dumps(log,indent=2)+"\n")
artifacts=[]
for rel,role in [("result.json","executed-result"),("run-log.json","run-log")]:
    p=OUT/rel; artifacts.append({"path":rel,"role":role,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
for p in sorted((CASE_DIR/"vectors").rglob("*.json")):
    artifacts.append({"path":os.path.relpath(p,OUT),"role":"test-vector","sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
for p,role in [(CASE_DIR/"invariants.yaml","invariant-set"),(CASE_DIR/"ownership.yaml","semantic-ownership"),(CASE_DIR/"known-limitations.md","known-limitations"),(Path(__file__),"reference-evaluator")]:
    artifacts.append({"path":os.path.relpath(p,OUT),"role":role,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()})
manifest={"case_id":CASE_ID,"evidence_id":CASE_ID+"-EVIDENCE-20260820","claim_scope":claim,"executed_at":now,"runner":str(Path(__file__).relative_to(ROOT)),"artifacts":artifacts,"result_summary":{"status":result["status"],"vectors":len(vectors),"passed":passed,"failed":len(vectors)-passed}}
(OUT/"evidence-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
print(f"{CASE_ID}: {result['status'].upper()} ({passed}/{len(vectors)} vectors)")
raise SystemExit(0 if result["status"]=="pass" else 1)
