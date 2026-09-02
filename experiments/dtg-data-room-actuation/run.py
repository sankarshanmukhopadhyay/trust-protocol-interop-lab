#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
SCENARIO=ROOT/'cases'/'dtg-data-room-actuation'/'scenario.yaml'
RESULT=ROOT/'results'/'dtg-data-room-actuation'/'run-results.json'

def evaluate(v):
    if not v['source_pins_current']:
        decision='stale'
        checks={'source_pins_current':False}
    else:
        membership_ok=(not v['membership_required']) or v['membership_valid']
        delegation_ok=(not v['delegation_required']) or v['delegation_valid']
        checks={
          'source_pins_current':True,
          'actor_relationship_valid':bool(v['actor_relationship_valid']),
          'membership_valid':bool(membership_ok),
          'delegation_valid':bool(delegation_ok),
          'authority_current':bool(v['authority_current']),
          'authority_action_valid':bool(v['authority_action_valid']),
          'subject_binding_valid':bool(v['subject_binding_valid']),
          'governance_policy_current':bool(v['governance_policy_current']),
          'task_binding_valid':bool(v['task_binding_valid']),
          'privacy_within_declared_scope':bool(v['privacy_within_declared_scope']),
          'one_effect_available':not bool(v['effect_already_recorded']),
        }
        decision='allow' if all(checks.values()) else 'deny'
    return {'id':v['id'],'class':v['class'],'operation':v['operation'],'checks':checks,'decision':decision,'expected':v['expected'],'matches_expected':decision==v['expected']}

def build():
    s=yaml.safe_load(SCENARIO.read_text()); vec=[evaluate(v) for v in s['vectors']]
    return {'case':s['case'],'status':s['status'],'informative_pressure_test':s['informative_pressure_test'],'source_pins':s['source_pins'],'propositions':s['propositions'],'vectors':vec,'all_expected_outcomes_matched':all(v['matches_expected'] for v in vec),'claim_boundary':'semantic umbrella composition only; unresolved runtime privacy, native proof and final upstream semantics remain independently bounded'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args();r=build();t=json.dumps(r,indent=2,sort_keys=True)+'\n'
    if a.write: RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(t)
    if a.check and (not RESULT.exists() or json.loads(RESULT.read_text())!=r): print('Data Room actuation result fixture is stale',file=sys.stderr);return 1
    if not a.write and not a.check: print(t,end='')
    return 0 if r['all_expected_outcomes_matched'] else 1
if __name__=='__main__': raise SystemExit(main())
