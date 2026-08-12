#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
cases = json.loads((ROOT / 'catalog/interoperability-cases.yaml').read_text())['cases']
rank = {
    'exploratory': 1,
    'experimental': 2,
    'candidate': 3,
    'interoperability-tested': 4,
    'proposed-upstream': 5,
    'upstreamed': 6,
    'superseded': 0,
}

case_ids = set()
vector_ids = set()
invariant_ids = set()

for c in cases:
    assert c['id'] not in case_ids, f"duplicate case id: {c['id']}"
    case_ids.add(c['id'])
    r = rank[c['status']]

    # Every declared component must have a stated baseline so experiments are
    # reproducible against an explicit, bounded input set.
    missing_baselines = set(c['components']) - set(c['baselines'])
    assert not missing_baselines, f"{c['id']}: missing baselines for {sorted(missing_baselines)}"

    inv_doc = json.loads((ROOT / c['invariants']).read_text())
    inv = inv_doc.get('invariants', [])
    own = json.loads((ROOT / c['ownership']).read_text())
    assert own, f"{c['id']}: empty ownership"

    for item in inv:
        assert item.get('id') and item.get('statement'), f"{c['id']}: invariant missing id/statement"
        assert item['id'] not in invariant_ids, f"duplicate invariant id: {item['id']}"
        invariant_ids.add(item['id'])

    if r >= 2:
        assert inv, f"{c['id']}: experimental requires invariants"
        sc = c['paths'].get('scenarios')
        assert sc and (ROOT / sc).exists(), f"{c['id']}: experimental requires scenarios"

    if r >= 3:
        vp = c['paths'].get('vectors')
        assert vp, f"{c['id']}: candidate requires vectors"
        v = ROOT / vp
        positive = sorted((v / 'valid').glob('*.json'))
        negative = sorted((v / 'invalid').glob('*.json'))
        assert positive, f"{c['id']}: candidate requires positive vector"
        assert negative, f"{c['id']}: candidate requires negative vector"
        for path in positive + negative:
            vector = json.loads(path.read_text())
            assert vector.get('id'), f"{c['id']}: {path} missing vector id"
            assert vector['id'] not in vector_ids, f"duplicate vector id: {vector['id']}"
            vector_ids.add(vector['id'])
            assert ('expected' in vector or 'expect' in vector), f"{c['id']}: {path} missing expected behavior"
        lp = c['paths'].get('limitations')
        assert lp and (ROOT / lp).exists(), f"{c['id']}: candidate requires limitations"

    if r >= 4:
        ev = c['paths'].get('evidence')
        assert ev and (ROOT / ev).exists(), f"{c['id']}: tested requires evidence"

print(
    f"cases: PASS ({len(cases)} evidence-gated maturity claims; "
    f"{len(invariant_ids)} invariants; {len(vector_ids)} candidate vectors)"
)
