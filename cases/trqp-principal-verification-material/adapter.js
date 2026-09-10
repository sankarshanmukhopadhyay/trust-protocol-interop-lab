'use strict';

function iso(value) { return new Date(value).getTime(); }
function currentAt(record, at) {
  if (record.valid_from && at < iso(record.valid_from)) return false;
  if (record.valid_until && at >= iso(record.valid_until)) return false;
  return true;
}

function evaluate(fixture, query) {
  const at = iso(query.time);
  const observed = iso(fixture.source.observed_at);
  if (!fixture.source.authoritative) return { decision: 'indeterminate', reason: 'evidence-unavailable' };
  if (at > observed && at - observed > fixture.source.fresh_for_ms) return { decision: 'indeterminate', reason: 'evidence-stale' };
  if (query.critical_context?.some((name) => !fixture.source.supported_context.includes(name))) {
    return { decision: 'indeterminate', reason: 'unsupported-critical-context' };
  }
  if (query.historical && !fixture.source.history_complete) {
    return { decision: 'indeterminate', reason: 'historical-evidence-incomplete' };
  }

  const principal = fixture.principals.find((p) => p.id === query.entity_id);
  if (!principal) {
    return fixture.source.complete_for_scope
      ? { decision: 'authoritative-negative', reason: 'not-listed' }
      : { decision: 'indeterminate', reason: 'evidence-incomplete' };
  }

  if (!query.verification_material) return { decision: 'positive', reason: 'evidence-supports-proposition' };
  const material = principal.materials.find((m) => m.id === query.verification_material);
  if (!material) {
    return fixture.source.complete_for_scope
      ? { decision: 'authoritative-negative', reason: 'material-mismatch' }
      : { decision: 'indeterminate', reason: 'evidence-incomplete' };
  }
  if (!currentAt(material, at)) return { decision: 'authoritative-negative', reason: 'not-applicable' };
  if (material.revoked_at && at >= iso(material.revoked_at)) return { decision: 'authoritative-negative', reason: 'revoked' };
  if (material.purpose !== query.action) return { decision: 'authoritative-negative', reason: 'not-applicable' };
  if (material.resource !== query.resource) return { decision: 'authoritative-negative', reason: 'wrong-resource' };
  return { decision: 'positive', reason: 'evidence-supports-proposition' };
}

function legacyDropQualifier(fixture, query) {
  return evaluate(fixture, { ...query, verification_material: undefined, critical_context: [] });
}

module.exports = { evaluate, legacyDropQualifier };
