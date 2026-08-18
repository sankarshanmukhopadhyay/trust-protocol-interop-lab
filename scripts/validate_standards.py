#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
load = lambda p: json.loads((ROOT / p).read_text())
standards = load('standards/register.yaml')
sources = load('standards/sources.yaml')
portfolio = load('standards/mappings/portfolio.yaml')
tsmm = load('standards/mappings/tsmm.yaml')
gaam = load('standards/mappings/gaam.yaml')
rahp = load('standards/assurance/rahp-candidates.yaml')
cross = load('standards/cross-spec/candidates.yaml')
cases = load('catalog/interoperability-cases.yaml')['cases']
case_by_id = {c['id']: c for c in cases}

allowed_rel = set(portfolio['relationship_types'])
source_ids = {s['id'] for s in sources['sources']}
project_ids = set(portfolio['projects'])
ids = set()
errors = []


def valid_http(uri):
    try:
        p = urlparse(uri)
        return p.scheme in {'http', 'https'} and bool(p.netloc)
    except Exception:
        return False

for s in standards['standards']:
    sid = s.get('id', '')
    if not sid.startswith('STD-'):
        errors.append(f"{sid or '<missing>'}: invalid id")
    if sid in ids:
        errors.append(f'{sid}: duplicate id')
    ids.add(sid)
    if not s.get('title') or not s.get('publisher'):
        errors.append(f'{sid}: title and publisher are required')
    if not valid_http(s.get('canonical_uri', '')):
        errors.append(f'{sid}: canonical_uri must be absolute HTTP(S)')
    if not s.get('domains'):
        errors.append(f'{sid}: at least one domain is required')
    if not s.get('portfolio_relevance'):
        errors.append(f'{sid}: portfolio_relevance is required')
    unknown_projects = set(s.get('portfolio_relevance', {})) - project_ids
    if unknown_projects:
        errors.append(f'{sid}: unknown portfolio project(s) {sorted(unknown_projects)}')
    unknown = set(s.get('relationships', [])) - allowed_rel
    if unknown:
        errors.append(f'{sid}: unknown relationships {sorted(unknown)}')
    if s.get('normative_dependency') and 'depends-on' not in s.get('relationships', []):
        errors.append(f'{sid}: normative_dependency requires depends-on relationship')
    review = s.get('review', {})
    if review.get('state') not in {'candidate', 'mapped', 'analysed', 'pressure-tested', 'retired'}:
        errors.append(f'{sid}: invalid review state')
    for src in s.get('source_relationships', []):
        if src.get('source_id') not in source_ids:
            errors.append(f"{sid}: unknown source_id {src.get('source_id')}")
    verification = s.get('verification', {})
    if verification.get('state') != 'canonical-verified':
        errors.append(f'{sid}: Commit 2 requires canonical-verified verification state')
    if not verification.get('version') or not verification.get('publisher_status') or not verification.get('verified_on'):
        errors.append(f'{sid}: incomplete canonical verification metadata')
    if not valid_http(verification.get('baseline_uri', '')):
        errors.append(f'{sid}: verification baseline_uri must be absolute HTTP(S)')
    evidence = verification.get('evidence_uris', [])
    if not evidence or any(not valid_http(u) for u in evidence):
        errors.append(f'{sid}: verification evidence_uris must contain absolute HTTP(S) sources')
    if not verification.get('lifecycle_note'):
        errors.append(f'{sid}: lifecycle_note is required')


def validate_matrix(name, matrix, gap_field):
    axes = set(matrix.get('axes', {}))
    legend = set(matrix.get('legend', {}))
    mapped = set()
    for row in matrix.get('mappings', []):
        sid = row.get('standard_id')
        if sid not in ids:
            errors.append(f'{name}: unknown standard {sid}')
            continue
        if sid in mapped:
            errors.append(f'{name}: duplicate mapping {sid}')
        mapped.add(sid)
        coverage = row.get('coverage', {})
        if set(coverage) != axes:
            errors.append(f'{name}/{sid}: coverage axes do not exactly match declared axes')
        bad = set(coverage.values()) - legend
        if bad:
            errors.append(f'{name}/{sid}: unknown coverage code(s) {sorted(bad)}')
        if not row.get(gap_field):
            errors.append(f'{name}/{sid}: {gap_field} is required')
    missing = ids - mapped
    if missing:
        errors.append(f'{name}: missing mappings for {sorted(missing)}')

validate_matrix('TSMM', tsmm, 'key_gap')
validate_matrix('GAAM', gaam, 'authority_gap')

for register_name, doc, prefix in [('RAHP candidates', rahp, 'RAHP-STD-'), ('Cross-spec candidates', cross, 'XSP-')]:
    seen = set()
    for c in doc.get('candidates', []):
        cid = c.get('id', '')
        if not cid.startswith(prefix):
            errors.append(f'{register_name}: invalid candidate id {cid}')
        if cid in seen:
            errors.append(f'{register_name}: duplicate candidate {cid}')
        seen.add(cid)
        if not c.get('standards'):
            errors.append(f'{cid}: at least one standard required')
        unknown = set(c.get('standards', [])) - ids
        if unknown:
            errors.append(f'{cid}: unknown standards {sorted(unknown)}')
        for p in c.get('projects', []):
            if p not in project_ids:
                errors.append(f'{cid}: unknown project {p}')
        if c.get('priority') not in {'critical', 'high', 'medium', 'low'}:
            errors.append(f'{cid}: invalid priority')
        promotion = c.get('promotion')
        if promotion:
            if register_name != 'Cross-spec candidates':
                errors.append(f'{cid}: promotion metadata is only defined for cross-spec candidates')
            elif promotion.get('state') != 'executed':
                errors.append(f'{cid}: unknown promotion state {promotion.get("state")}')
            else:
                ic = promotion.get('interop_case')
                if ic not in case_by_id:
                    errors.append(f'{cid}: promoted Interop Case {ic} not found')
                elif case_by_id[ic].get('status') != 'interoperability-tested':
                    errors.append(f'{cid}: promoted Interop Case {ic} is not interoperability-tested')
                ep = promotion.get('evidence')
                if not ep or not (ROOT / ep).exists():
                    errors.append(f'{cid}: promoted evidence path is missing')
                if not promotion.get('completed_on'):
                    errors.append(f'{cid}: completed_on is required for executed promotion')

if errors:
    print('Standards validation failed:')
    for e in errors:
        print(f'- {e}')
    raise SystemExit(1)
print(
    'Standards validation passed: '
    f"{len(ids)} verified entries; {len(source_ids)} governed source(s); "
    f"{len(tsmm['mappings'])} TSMM mappings; {len(gaam['mappings'])} GAAM mappings; "
    f"{len(rahp['candidates'])} RAHP candidates; {len(cross['candidates'])} cross-spec candidates."
)
