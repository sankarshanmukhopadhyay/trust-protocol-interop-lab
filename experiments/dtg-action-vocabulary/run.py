#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
SCENARIO=ROOT/'cases'/'dtg-action-vocabulary'/'scenario.yaml'
RESULT=ROOT/'results'/'dtg-action-vocabulary'/'run-results.json'

def evaluate(v):
    same_domain=bool(v['same_governance'])
    mapped=bool(v['explicit_mapping'])
    hierarchy=bool(v['hierarchy_declared'])
    lexical_direct=(v['issuer_action']==v['verifier_operation'])
    # Local semantics still need either a direct declared operation match or an explicit hierarchy/mapping.
    semantic_mapping = mapped or hierarchy or (same_domain and lexical_direct)
    decision='allow' if semantic_mapping else 'deny'
    return {'id':v['id'],'class':v['class'],'issuer_action':v['issuer_action'],'verifier_operation':v['verifier_operation'],'semantic_mapping_established':semantic_mapping,'decision':decision,'expected':v['expected'],'matches_expected':decision==v['expected']}

def build():
    s=yaml.safe_load(SCENARIO.read_text()); vec=[evaluate(v) for v in s['vectors']]
    return {'case':s['case'],'status':s['status'],'source_pin':s['source_pin'],'propositions':s['propositions'],'vectors':vec,'all_expected_outcomes_matched':all(v['matches_expected'] for v in vec),'claim_boundary':'semantic governance-mapping evidence only; no normative federation mechanism selected'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();r=build();t=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.write: RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(t)
    if a.check and (not RESULT.exists() or json.loads(RESULT.read_text())!=r): print('action vocabulary result fixture is stale',file=sys.stderr);return 1
    if not a.write and not a.check: print(t,end='')
    return 0 if r['all_expected_outcomes_matched'] else 1
if __name__=='__main__': raise SystemExit(main())
