#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'catalog/interoperability-cases.yaml').read_text())['cases']
rows=[]
for c in cases:
    p=c['paths']; vectors=p.get('vectors'); pos=neg=0
    if vectors:
        v=ROOT/vectors; pos=len(list((v/'valid').glob('*.json'))) if (v/'valid').exists() else 0; neg=len(list((v/'invalid').glob('*.json'))) if (v/'invalid').exists() else 0
    rows.append((c['id'],c['status'],'yes' if Path(ROOT/c['ownership']).exists() else 'no','yes' if Path(ROOT/c['invariants']).exists() else 'no',pos,neg,'yes' if p.get('evidence') and (ROOT/p['evidence']).exists() else 'no'))
out=['---','layout: default','title: Interoperability Readiness','parent: Assessments','nav_order: 90','---','# Interoperability Readiness','','Generated from the machine-readable case catalog.','','| Case | Status | Ownership | Invariants | + vectors | − vectors | Executed evidence |','|---|---|---:|---:|---:|---:|---:|']
for r in rows: out.append('| '+' | '.join(map(str,r))+' |')
out += ['','A status is an evidence-bounded repository claim, not external certification.']
(ROOT/'docs/interoperability-readiness.md').write_text('\n'.join(out)+'\n')
print(f'readiness: generated {len(rows)} rows')
