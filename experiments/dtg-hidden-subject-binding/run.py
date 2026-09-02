#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
SCENARIO = ROOT / 'cases' / 'dtg-hidden-subject-binding' / 'scenario.yaml'
RESULT = ROOT / 'results' / 'dtg-hidden-subject-binding' / 'run-results.json'

def evaluate(v: dict) -> dict:
    binding_ok = (not v['binding_required']) or v['binding_proven']
    checks = {
        'component_credentials_valid': bool(v['component_credentials_valid']),
        'required_binding_proven': bool(binding_ok),
        'context_binding_valid': bool(v['context_binding_valid']),
        'no_durable_correlator_exported': not bool(v['durable_correlator_exported']),
    }
    decision = 'allow' if all(checks.values()) else 'deny'
    return {'id':v['id'],'class':v['class'],'relation':v['relation'],'checks':checks,'decision':decision,'expected':v['expected'],'matches_expected':decision==v['expected']}

def build_result() -> dict:
    s=yaml.safe_load(SCENARIO.read_text(encoding='utf-8'))
    vectors=[evaluate(v) for v in s['vectors']]
    return {'case':s['case'],'status':s['status'],'evaluator_version':'0.1','source_pins':s['source_pins'],'propositions':s['propositions'],'vectors':vectors,'all_expected_outcomes_matched':all(v['matches_expected'] for v in vectors),'claim_boundary':'semantic binding evidence only; production ZKP same-subject/common-control construction remains independently required'}

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--write',action='store_true'); p.add_argument('--check',action='store_true'); a=p.parse_args()
    r=build_result(); text=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.write:
        RESULT.parent.mkdir(parents=True,exist_ok=True); RESULT.write_text(text,encoding='utf-8')
    if a.check:
        if not RESULT.exists() or json.loads(RESULT.read_text(encoding='utf-8')) != r:
            print('hidden-subject binding result fixture is stale',file=sys.stderr); return 1
    if not a.write and not a.check: print(text,end='')
    return 0 if r['all_expected_outcomes_matched'] else 1

if __name__ == '__main__': raise SystemExit(main())
