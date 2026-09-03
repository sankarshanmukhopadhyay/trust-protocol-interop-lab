#!/usr/bin/env python3
import json
import re
import shlex
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
cases = yaml.safe_load((ROOT / 'catalog/interoperability-cases.yaml').read_text())['cases']
rank = {
    'exploratory': 1,
    'experimental': 2,
    'candidate': 3,
    'interoperability-tested': 4,
    'proposed-upstream': 5,
    'upstreamed': 6,
    'superseded': 0,
}
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')
GIT_SHA_RE = re.compile(r'^[0-9a-f]{40}$')

case_ids = set()
vector_ids = set()
invariant_ids = set()


def validate_tested_evidence(case, evidence_path):
    """Validate the minimum machine-verifiable contract for a Tested claim.

    This is repository evidence discipline, not external certification.  It
    verifies that a Tested claim is bound to an executable command, a passing
    result, a bounded claim scope, existing evidence artifacts and at least one
    integrity reference.  Existing packages may use SHA-256 content hashes or
    Git blob SHAs; future packages can use either without weakening the gate.
    """
    manifest_path = ROOT / evidence_path
    assert manifest_path.is_file(), f"{case['id']}: tested evidence must be a manifest file"

    manifest = json.loads(manifest_path.read_text())
    assert manifest.get('case_id') == case['id'], (
        f"{case['id']}: evidence manifest case_id mismatch"
    )

    claim_scope = manifest.get('claim_scope')
    assert isinstance(claim_scope, str) and claim_scope.strip(), (
        f"{case['id']}: tested evidence requires bounded claim_scope"
    )

    runner = manifest.get('runner')
    assert isinstance(runner, str) and runner.strip(), (
        f"{case['id']}: tested evidence requires reproduction runner"
    )
    runner_parts = shlex.split(runner)
    assert runner_parts, f"{case['id']}: tested evidence runner is empty"
    runner_path = ROOT / runner_parts[0]
    assert runner_path.is_file(), (
        f"{case['id']}: evidence runner does not exist: {runner_parts[0]}"
    )

    result = manifest.get('result_summary')
    assert isinstance(result, dict), f"{case['id']}: tested evidence requires result_summary"
    assert result.get('status') == 'pass', (
        f"{case['id']}: tested evidence result_summary must be pass"
    )

    artifacts = manifest.get('artifacts')
    assert isinstance(artifacts, list) and artifacts, (
        f"{case['id']}: tested evidence requires artifacts"
    )

    integrity_bound = 0
    manifest_dir = manifest_path.parent
    for artifact in artifacts:
        assert isinstance(artifact, dict) and artifact.get('path'), (
            f"{case['id']}: evidence artifact missing path"
        )
        artifact_path = (manifest_dir / artifact['path']).resolve()
        try:
            artifact_path.relative_to(ROOT.resolve())
        except ValueError as exc:
            raise AssertionError(
                f"{case['id']}: evidence artifact escapes repository: {artifact['path']}"
            ) from exc
        assert artifact_path.exists(), (
            f"{case['id']}: evidence artifact does not exist: {artifact['path']}"
        )

        if 'sha256' in artifact:
            assert SHA256_RE.fullmatch(str(artifact['sha256'])), (
                f"{case['id']}: invalid SHA-256 for {artifact['path']}"
            )
            integrity_bound += 1
        if 'git_blob_sha' in artifact:
            assert GIT_SHA_RE.fullmatch(str(artifact['git_blob_sha'])), (
                f"{case['id']}: invalid Git blob SHA for {artifact['path']}"
            )
            integrity_bound += 1

    assert integrity_bound > 0, (
        f"{case['id']}: tested evidence requires at least one integrity-bound artifact"
    )


for c in cases:
    assert c['id'] not in case_ids, f"duplicate case id: {c['id']}"
    case_ids.add(c['id'])
    r = rank[c['status']]

    # Every declared component must have a stated baseline so experiments are
    # reproducible against an explicit, bounded input set.
    missing_baselines = set(c['components']) - set(c['baselines'])
    assert not missing_baselines, f"{c['id']}: missing baselines for {sorted(missing_baselines)}"

    inv_doc = yaml.safe_load((ROOT / c['invariants']).read_text())
    inv = inv_doc.get('invariants', [])
    own = yaml.safe_load((ROOT / c['ownership']).read_text())
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
        assert ev, f"{c['id']}: tested requires evidence manifest"
        validate_tested_evidence(c, ev)

print(
    f"cases: PASS ({len(cases)} evidence-gated maturity claims; "
    f"{len(invariant_ids)} invariants; {len(vector_ids)} candidate vectors)"
)
