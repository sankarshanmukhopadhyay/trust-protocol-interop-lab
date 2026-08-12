#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/'catalog/interoperability-cases.yaml').read_text())['cases']
rank={'exploratory':1,'experimental':2,'candidate':3,'interoperability-tested':4,'proposed-upstream':5,'upstreamed':6,'superseded':0}
for c in cases:
    r=rank[c['status']]
    inv=json.loads((ROOT/c['invariants']).read_text()).get('invariants',[])
    own=json.loads((ROOT/c['ownership']).read_text())
    assert own, f"{c['id']}: empty ownership"
    if r>=2:
        assert inv, f"{c['id']}: experimental requires invariants"
        sc=c['paths'].get('scenarios'); assert sc and (ROOT/sc).exists(), f"{c['id']}: experimental requires scenarios"
    if r>=3:
        vp=c['paths'].get('vectors'); assert vp, f"{c['id']}: candidate requires vectors"
        v=ROOT/vp
        assert any((v/'valid').glob('*.json')), f"{c['id']}: candidate requires positive vector"
        assert any((v/'invalid').glob('*.json')), f"{c['id']}: candidate requires negative vector"
        lp=c['paths'].get('limitations'); assert lp and (ROOT/lp).exists(), f"{c['id']}: candidate requires limitations"
    if r>=4:
        ev=c['paths'].get('evidence'); assert ev and (ROOT/ev).exists(), f"{c['id']}: tested requires evidence"
print(f'cases: PASS ({len(cases)} evidence-gated maturity claims)')
