#!/usr/bin/env python3
import hashlib, json
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
print(f'evidence: PASS ({count} executed evidence manifests; hashes and claim scopes verified)')
