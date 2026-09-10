'use strict';

const DAY = 24 * 60 * 60 * 1000;

function fixture(overrides = {}) {
  return {
    source: {
      authoritative: true,
      complete_for_scope: true,
      history_complete: true,
      observed_at: '2026-09-10T00:00:00Z',
      fresh_for_ms: 7 * DAY,
      supported_context: ['verification_material', 'time'],
      ...(overrides.source || {})
    },
    principals: overrides.principals || [{
      id: 'did:example:issuer-a',
      materials: [
        { id: 'C1', purpose: 'issue', resource: 'credential-x', valid_from: '2026-01-01T00:00:00Z', valid_until: '2026-07-01T00:00:00Z' },
        { id: 'C2', purpose: 'issue', resource: 'credential-x', valid_from: '2026-07-01T00:00:00Z', revoked_at: '2026-09-01T00:00:00Z' },
        { id: 'C3', purpose: 'verify', resource: 'credential-x', valid_from: '2026-07-01T00:00:00Z' },
        { id: 'C4', purpose: 'issue', resource: 'credential-y', valid_from: '2026-07-01T00:00:00Z' }
      ]
    }]
  };
}

function query(overrides = {}) {
  return {
    entity_id: 'did:example:issuer-a',
    action: 'issue',
    resource: 'credential-x',
    verification_material: 'C2',
    time: '2026-08-15T00:00:00Z',
    critical_context: ['verification_material'],
    ...overrides
  };
}

module.exports = { DAY, fixture, query };
