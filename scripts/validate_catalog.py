#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text())
components=load('catalog/components.yaml')['components']; cases=load('catalog/interoperability-cases.yaml')['cases']
ids=[c['id'] for c in components]
assert len(ids)==len(set(ids)), 'duplicate component ids'
case_ids=[c['id'] for c in cases]
assert len(case_ids)==len(set(case_ids)), 'duplicate case ids'
known=set(ids)
for c in cases:
    assert set(c['components']) <= known, f"{c['id']}: unknown component"
    assert len(c['components'])>=2, f"{c['id']}: needs 2+ components"
    assert len(c['baselines'])>=2, f"{c['id']}: needs baselines"
    for k,p in c['paths'].items():
        assert (ROOT/p).exists(), f"{c['id']}: missing {k}: {p}"
    assert (ROOT/c['ownership']).exists(), f"{c['id']}: missing ownership"
    assert (ROOT/c['invariants']).exists(), f"{c['id']}: missing invariants"
print(f'catalog: PASS ({len(components)} components, {len(cases)} cases)')
