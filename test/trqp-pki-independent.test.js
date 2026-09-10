const assert = require('node:assert/strict');
const test = require('node:test');
const { evaluate, legacyDropQualifier } = require('../cases/trqp-principal-verification-material/adapter');
const { DAY, fixture, query } = require('../cases/trqp-principal-verification-material/fixtures');

function expect(q, f, decision, reason) {
  assert.deepEqual(evaluate(f, q), { decision, reason });
}

test('01 exact current material is positive', () => expect(query(), fixture(), 'positive', 'evidence-supports-proposition'));
test('02 rotated successor exact match is positive', () => expect(query({ verification_material: 'C2' }), fixture(), 'positive', 'evidence-supports-proposition'));
test('03 revoked material after revocation is authoritative negative', () => expect(query({ time: '2026-09-05T00:00:00Z' }), fixture(), 'authoritative-negative', 'revoked'));
test('04 authoritative complete absence is not-listed', () => expect(query({ entity_id: 'did:example:absent' }), fixture(), 'authoritative-negative', 'not-listed'));
test('05 incomplete absence is indeterminate', () => expect(query({ entity_id: 'did:example:absent' }), fixture({ source: { complete_for_scope: false } }), 'indeterminate', 'evidence-incomplete'));
test('06 non-authoritative source is indeterminate', () => expect(query(), fixture({ source: { authoritative: false } }), 'indeterminate', 'evidence-unavailable'));
test('07 stale positive evidence is indeterminate', () => expect(query({ time: '2026-09-20T00:00:00Z' }), fixture(), 'indeterminate', 'evidence-stale'));
test('08 stale absence evidence is indeterminate', () => expect(query({ entity_id: 'did:example:absent', time: '2026-09-20T00:00:00Z' }), fixture(), 'indeterminate', 'evidence-stale'));
test('09 historical prior material is positive', () => expect(query({ verification_material: 'C1', time: '2026-06-01T00:00:00Z', historical: true }), fixture(), 'positive', 'evidence-supports-proposition'));
test('10 incomplete history is indeterminate', () => expect(query({ verification_material: 'C1', time: '2026-06-01T00:00:00Z', historical: true }), fixture({ source: { history_complete: false } }), 'indeterminate', 'historical-evidence-incomplete'));
test('11 wrong purpose is not-applicable', () => expect(query({ verification_material: 'C3' }), fixture(), 'authoritative-negative', 'not-applicable'));
test('12 wrong resource is authoritative negative', () => expect(query({ verification_material: 'C4' }), fixture(), 'authoritative-negative', 'wrong-resource'));
test('13 unsupported critical qualifier is indeterminate', () => expect(query(), fixture({ source: { supported_context: ['time'] } }), 'indeterminate', 'unsupported-critical-context'));
test('14 legacy qualifier drop exposes unsafe false positive', () => {
  const f = fixture();
  const q = query({ verification_material: 'UNKNOWN' });
  assert.deepEqual(evaluate(f, q), { decision: 'authoritative-negative', reason: 'material-mismatch' });
  assert.deepEqual(legacyDropQualifier(f, q), { decision: 'positive', reason: 'evidence-supports-proposition' });
});

test('unknown material under incomplete evidence is indeterminate', () => expect(query({ verification_material: 'UNKNOWN' }), fixture({ source: { complete_for_scope: false } }), 'indeterminate', 'evidence-incomplete'));
test('material before validity is not-applicable', () => expect(query({ verification_material: 'C2', time: '2026-06-01T00:00:00Z', historical: true }), fixture(), 'authoritative-negative', 'not-applicable'));
test('freshness boundary remains inclusive', () => expect(query({ time: '2026-09-17T00:00:00Z' }), fixture({ source: { fresh_for_ms: 7 * DAY } }), 'authoritative-negative', 'revoked'));
