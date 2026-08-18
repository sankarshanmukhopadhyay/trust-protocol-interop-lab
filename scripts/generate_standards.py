#!/usr/bin/env python3
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
load = lambda p: json.loads((ROOT / p).read_text())
data = load('standards/register.yaml')
tsmm = load('standards/mappings/tsmm.yaml')
gaam = load('standards/mappings/gaam.yaml')
rahp = load('standards/assurance/rahp-candidates.yaml')
cross = load('standards/cross-spec/candidates.yaml')
standards = sorted(data['standards'], key=lambda x: x['id'])
byid = {s['id']: s for s in standards}
out = ROOT / 'standards/generated'
out.mkdir(parents=True, exist_ok=True)

ACK = '> **Source acknowledgement:** Initial standards discovery is informed by the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC). GSMI is a discovery source, not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply GSMI/GBBC endorsement.\n\n'

def front(title, order):
    return f'---\nlayout: default\ntitle: {title}\nnav_order: {order}\n---\n'

rows = []
for s in standards:
    projects = ', '.join(f"`{k}` ({v})" for k, v in sorted(s['portfolio_relevance'].items()))
    v = s['verification']
    rows.append(f"| `{s['id']}` | [{s['title']}]({s['canonical_uri']}) | {s['publisher']} | {v['version']} | {v['publisher_status']} | {s['review']['state']} | {'yes' if s['normative_dependency'] else 'no'} | {projects} |")
register = front('Standards Register', 9) + '# Portfolio Standards Register\n\n' + ACK + 'Generated from `standards/register.yaml`. Canonical verification confirms publisher baseline/status only; it is **not** a conformance, compatibility, authority-sufficiency, or endorsement claim.\n\n| ID | Standard | Publisher | Verified baseline | Publisher status | Review state | Normative dependency | Portfolio relevance |\n|---|---|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n'
(out/'standards-register.md').write_text(register)

projects = sorted({p for s in standards for p in s['portfolio_relevance']})
header = '| Standard | ' + ' | '.join(f'`{p}`' for p in projects) + ' |\n'
sep = '|---|' + '---|' * len(projects) + '\n'
body=[]
for s in standards:
    body.append(f"| `{s['id']}` | " + ' | '.join(s['portfolio_relevance'].get(p, '—') for p in projects) + ' |')
matrix = front('Standards × Portfolio Matrix', 10) + '# Standards × Portfolio Matrix\n\n' + ACK + 'Values indicate local analytical relevance, **not conformance, dependency, compatibility or endorsement**.\n\n' + header + sep + '\n'.join(body) + '\n'
(out/'portfolio-matrix.md').write_text(matrix)

verification_rows=[]
for s in standards:
    v=s['verification']; date=v.get('publication_date') or 'not recorded'
    verification_rows.append(f"| `{s['id']}` | `{v['version']}` | {v['publisher_status']} | {date} | {v['verified_on']} | {v['lifecycle_note']} |")
verification = front('Canonical Verification', 11) + '# Canonical Source Verification\n\n' + ACK + 'Every entry is verified against publisher-controlled sources and pinned to a deliberate baseline. A newer draft does not automatically move the portfolio baseline.\n\n| Standard | Baseline | Publisher status | Publication | Verified | Lifecycle note |\n|---|---|---|---|---|---|\n' + '\n'.join(verification_rows) + '\n'
(out/'verification-report.md').write_text(verification)


def semantic_matrix(doc, title, order, gap_field):
    axes=list(doc['axes'])
    rows=[]
    for m in sorted(doc['mappings'], key=lambda x:x['standard_id']):
        cells=[m['coverage'][a] for a in axes]
        rows.append('| `'+m['standard_id']+'` | '+' | '.join(cells)+' | '+m[gap_field]+' |')
    legends='; '.join(f'`{k}` = {v}' for k,v in doc['legend'].items())
    hdr='| Standard | '+' | '.join(doc['axes'][a] for a in axes)+' | Key boundary |\n'
    sep='|---|'+'---|'*len(axes)+'---|\n'
    return front(title, order)+f'# {title}\n\n{ACK}Baseline: `{doc["model_baseline"]["version"]}`. {doc["model_baseline"]["authority_note"]}\n\n{legends}. These values are analytical coverage classifications, not claims of conformance.\n\n'+hdr+sep+'\n'.join(rows)+'\n'

(out/'tsmm-semantic-matrix.md').write_text(semantic_matrix(tsmm,'Standards × TSMM Semantic Matrix',12,'key_gap'))
(out/'gaam-authority-matrix.md').write_text(semantic_matrix(gaam,'Standards × GAAM Authority Matrix',13,'authority_gap'))

rrows=[]
for c in rahp['candidates']:
    std=', '.join(f'`{x}`' for x in c['standards'])
    projects=', '.join(f'`{x}`' for x in c.get('projects',[]))
    rrows.append(f"| `{c['id']}` | **{c['priority']}** | {c['title']} | {std} | {projects} | {c['risk_hypothesis']} |")
rpage=front('RAHP Assessment Candidates',14)+'# RAHP Assessment Candidate Register\n\n'+ACK+rahp['governance']+'\n\n| ID | Priority | Candidate | Standards | Portfolio targets | Risk hypothesis |\n|---|---|---|---|---|---|\n'+'\n'.join(rrows)+'\n'
(out/'rahp-candidates.md').write_text(rpage)

xrows=[]
for c in cross['candidates']:
    std=', '.join(f'`{x}`' for x in c['standards'])
    owner=f"`{c['recommended_owner']}`"
    xrows.append(f"| `{c['id']}` | **{c['priority']}** | {c['title']} | {std} | {owner} | {c['question']} |")
xpage=front('Cross-Spec Test Candidates',15)+'# Cross-Specification Pressure-Test Candidates\n\n'+ACK+cross['governance']+'\n\n| ID | Priority | Composition | Standards | Suggested owner | Pressure-test question |\n|---|---|---|---|---|---|\n'+'\n'.join(xrows)+'\n'
(out/'cross-spec-candidates.md').write_text(xpage)

counts=Counter(s['review']['state'] for s in standards)
summary={
 'version':2,
 'total':len(standards),
 'states':dict(sorted(counts.items())),
 'canonical_verified':sum(s.get('verification',{}).get('state')=='canonical-verified' for s in standards),
 'normative_dependencies':sum(bool(s['normative_dependency']) for s in standards),
 'tsmm_mappings':len(tsmm['mappings']),
 'gaam_mappings':len(gaam['mappings']),
 'rahp_candidates':len(rahp['candidates']),
 'cross_spec_candidates':len(cross['candidates']),
 'critical_rahp_candidates':sum(c['priority']=='critical' for c in rahp['candidates']),
 'critical_cross_spec_candidates':sum(c['priority']=='critical' for c in cross['candidates']),
}
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(f"Generated standards intelligence views for {len(standards)} verified entries.")
