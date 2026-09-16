#!/usr/bin/env python3
import hashlib, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases={c['id']:c for c in json.loads((ROOT/'catalog/interoperability-cases.yaml').read_text())['cases']}
count=0
for p in ROOT.rglob('evidence-manifest.json'):
    d=json.loads(p.read_text()); count+=1
    for k in ('case_id','evidence_id','claim_scope','artifacts','result_summary'): assert k in d, f'{p}: missing {k}'
    assert d['case_id'] in cases, f'{p}: unknown case_id {d["case_id"]}'
    assert d['claim_scope'].strip(), f'{p}: empty claim_scope'
    case=cases[d['case_id']]
    if case.get('status')=='interoperability-tested':
        assert case.get('paths',{}).get('evidence')==str(p.relative_to(ROOT)), f'{p}: tested case evidence path mismatch'
        assert d.get('executed_at') and d.get('runner'), f'{p}: tested evidence requires executed_at and runner'
    for a in d['artifacts']:
        target=(p.parent/a['path']).resolve()
        assert target.exists(), f'{p}: missing artifact {a["path"]}'
        if a.get('sha256'):
            actual=hashlib.sha256(target.read_bytes()).hexdigest()
            assert actual==a['sha256'], f'{p}: sha256 mismatch for {a["path"]}'
    result_path=p.parent/'result.json'
    if result_path.exists():
        result=json.loads(result_path.read_text())
        assert result.get('case_id')==d['case_id'], f'{p}: result case mismatch'
        assert result.get('claim_scope')==d['claim_scope'], f'{p}: result/manifest claim scope mismatch'
        assert result.get('status')==d['result_summary'].get('status'), f'{p}: result status mismatch'
        if case.get('status')=='interoperability-tested':
            assert result.get('status')=='pass', f'{p}: tested case must have passing result'

# DPIP evidence obligations are acquisition requests, not interoperability findings.
# Validate the reference #191 register through the same evidence CI without creating
# a new workflow or pretending targetless obligations have been executed.
admit_path=ROOT/'experiments/dpip-evidence-obligation/admit.py'
spec=importlib.util.spec_from_file_location('dpip_evidence_admit', admit_path)
mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
obligations=json.loads((ROOT/'experiments/dpip-evidence-obligation/dpip-191-obligations.json').read_text())['obligations']
admissions=[mod.evaluate(x) for x in obligations]
assert len(admissions)==3, 'DPIP #191 must expose three bounded obligations'
assert all(x['admission']=='BLOCKED' and x['reason']=='NO_TARGET' for x in admissions), 'targetless DPIP #191 obligations must remain blocked'
assert all('privacy PASS/FAIL' in x['claim_boundary']['lab_may_not_claim'] for x in admissions), 'Lab privacy authority boundary missing'
print(f'evidence: PASS ({count} executed evidence manifests; hashes and claim scopes verified; {len(admissions)} DPIP obligations correctly bounded)')
