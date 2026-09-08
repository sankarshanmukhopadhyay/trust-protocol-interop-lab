#!/usr/bin/env python3
"""Capture target-generated OpenVTC policy-discovery handles/endpoints."""
from __future__ import annotations
import argparse, json, os, subprocess, sys, uuid
from pathlib import Path

REPO="OpenVTC/verifiable-trust-infrastructure"
REV="72bf5794071971da506eb7a5af8e4765c35c137c"
MARKER="RAHP_TRACK_B_POLICY="
TARGET=Path("vtc-service/tests/policies.rs")
NEEDLE='    assert_eq!(body["id"], id);\n'
INJECT=r'''    assert_eq!(body["id"], id);
    println!("RAHP_TRACK_B_POLICY={}", json!({
        "policy_discovery_handle": id,
        "policy_endpoint": format!("https://vtc.example.com/v1/policies/{id}"),
    }));
'''

def run(*args,cwd): return subprocess.run(list(args),cwd=cwd,text=True,capture_output=True,check=False)

def restore_known_cargo_lock_refresh(checkout:Path):
    cp=run("git","status","--porcelain","--untracked-files=no",cwd=checkout)
    lines=[x for x in cp.stdout.splitlines() if x.strip()]
    if not lines: return
    if len(lines)==1 and lines[0][3:]=="Cargo.lock":
        restored=run("git","checkout","--","Cargo.lock",cwd=checkout)
        if restored.returncode: raise RuntimeError(restored.stderr.strip() or "could not restore Cargo.lock")
        return
    raise RuntimeError(f"target test changed unexpected tracked files: {lines}")

def observe(checkout:Path,context:str):
    head=run("git","rev-parse","HEAD",cwd=checkout)
    if head.returncode or head.stdout.strip()!=REV: raise ValueError("OpenVTC checkout pin mismatch")
    if run("git","status","--porcelain",cwd=checkout).stdout.strip(): raise ValueError("OpenVTC checkout not clean")
    path=checkout/TARGET; original=path.read_text(encoding="utf-8")
    marker='async fn show_returns_full_row() {'
    start=original.index(marker); tail=original[start:]
    pos=tail.index(NEEDLE)+start
    instrumented=original[:pos]+original[pos:].replace(NEEDLE,INJECT,1)
    path.write_text(instrumented,encoding="utf-8")
    try:
        cp=run("cargo","test","-p","vtc-service","--test","policies","show_returns_full_row","--","--exact","--nocapture",cwd=checkout)
    finally: path.write_text(original,encoding="utf-8")
    restore_known_cargo_lock_refresh(checkout)
    if cp.returncode: raise RuntimeError((cp.stdout+"\n"+cp.stderr)[-12000:])
    lines=[x for x in cp.stdout.splitlines() if MARKER in x]
    if len(lines)!=1: raise RuntimeError(f"expected one marker, got {len(lines)}")
    obs=json.loads(lines[0].split(MARKER,1)[1].strip())
    if not all(isinstance(obs.get(k),str) and obs[k] for k in ("policy_discovery_handle","policy_endpoint")):
        raise RuntimeError(f"invalid target observation: {obs}")
    return {"run_id":f"current-openvtc-track-b-policy-{context.lower()}-{uuid.uuid4()}","implementation_repository":REPO,"implementation_revision":REV,"executed_surfaces":["policy_discovery_handle","policy_endpoint"],"observations":obs,"producer_component":REPO,"assurance_boundary":"Target policy upload/show integration executed; generated policy id and GET endpoint are observed. Cargo.lock may be mechanically refreshed by CI Cargo and is restored before evidence return. Status and task surfaces are not claimed by this slice."}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--checkout",type=Path,default=Path(os.environ.get("OPENVTC_CHECKOUT","build/current-openvtc"))); p.add_argument("--context",choices=["A","B"],required=True); a=p.parse_args(); print(json.dumps(observe(a.checkout.resolve(),a.context),sort_keys=True)); return 0
if __name__=="__main__":
    try: raise SystemExit(main())
    except (ValueError,RuntimeError,json.JSONDecodeError) as e: print(f"ERROR: {e}",file=sys.stderr); raise SystemExit(2)
