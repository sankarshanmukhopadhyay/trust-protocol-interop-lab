#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
count=0
for p in ROOT.rglob('evidence-manifest.json'):
    d=json.loads(p.read_text()); count+=1
    for k in ('case_id','evidence_id','claim_scope','artifacts','result_summary'): assert k in d, f'{p}: missing {k}'
    for a in d['artifacts']:
        target=(p.parent/a['path']).resolve()
        assert target.exists(), f'{p}: missing artifact {a["path"]}'
print(f'evidence: PASS ({count} executed evidence manifests; zero is valid before tested maturity)')
