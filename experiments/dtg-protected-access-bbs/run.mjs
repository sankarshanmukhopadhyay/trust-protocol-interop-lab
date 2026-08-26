import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import * as Bls12381Multikey from '@digitalbazaar/bls12-381-multikey';

const encoder = new TextEncoder();
const decoder = new TextDecoder();

function parseOutputDir() {
  const i = process.argv.indexOf('--output-dir');
  if(i !== -1 && process.argv[i + 1]) {
    return process.argv[i + 1];
  }
  return path.join(os.tmpdir(), 'dtg-protected-access-bbs');
}

function b64url(bytes) {
  return Buffer.from(bytes).toString('base64url');
}

function contextBytes({verifier, challenge, purpose}) {
  // Case-local adapter: bind the three protected-access context fields into
  // the BBS presentation header. This is construction evidence, not a claim
  // that DTG or VC Data Integrity normatively defines this encoding.
  return encoder.encode(JSON.stringify({verifier, challenge, purpose}));
}

const fieldOrder = [
  'eligible',
  'provider_class_authorised',
  'authority_provenance_class',
  'protected_provider_identity',
  'protected_provider_location',
  'protected_relationship_type',
  'case_identifier',
  'durable_subject_identifier',
  'durable_provider_identifier'
];

const source = {
  eligible: true,
  provider_class_authorised: true,
  authority_provenance_class: 'recognized-support-provider',
  protected_provider_identity: 'protected-provider-alpha',
  protected_provider_location: 'confidential-location-alpha',
  protected_relationship_type: 'protected-service',
  case_identifier: 'case-stable-alpha',
  durable_subject_identifier: 'subject-stable-alpha',
  durable_provider_identifier: 'provider-stable-alpha'
};

const messages = fieldOrder.map(name => encoder.encode(`${name}=${source[name]}`));
const header = encoder.encode('IC-DTG-PROTECTED-ACCESS-001:EXP-BBS-2023-01');
const prohibited = new Set([
  'protected_provider_identity',
  'protected_provider_location',
  'protected_relationship_type',
  'case_identifier',
  'durable_subject_identifier',
  'durable_provider_identifier'
]);

const contexts = {
  original: {
    verifier: 'https://verifier.example/r1',
    challenge: 'pa-challenge-001',
    purpose: 'protected-access-entitlement'
  },
  replay: {
    verifier: 'https://verifier.example/r2',
    challenge: 'pa-challenge-999',
    purpose: 'different-service-purpose'
  }
};

const vectors = [
  {id: 'PA-POS-001', disclosed: [0, 1, 2], expected: 'pass'},
  {id: 'PA-NEG-001', disclosed: [0, 1, 2, 3, 4], expected: 'fail-privacy'},
  {id: 'PA-ADV-001', disclosed: [0, 1, 2], expected: 'fail-context'}
];

function disclosedMessages(indexes) {
  return messages.map((message, index) => indexes.includes(index) ? message : undefined);
}

function disclosedFields(indexes) {
  return indexes.map(index => fieldOrder[index]);
}

const keyPair = await Bls12381Multikey.generateBbsKeyPair({
  algorithm: Bls12381Multikey.ALGORITHMS.BBS_BLS12381_SHA256
});
const signer = keyPair.signer();
const verifier = keyPair.verifier();
const signature = await signer.multisign({header, messages});

const outputDir = parseOutputDir();
await fs.mkdir(outputDir, {recursive: true});

const result = {
  case: 'IC-DTG-PROTECTED-ACCESS-001',
  construction: {
    local_profile: 'EXP-BBS-2023-01',
    zkp_fork_commit: '6e1356812716dbd0e551272251e3e825132a8268',
    library: '@digitalbazaar/bls12-381-multikey@2.2.0',
    algorithm: 'BBS_BLS12381_SHA256',
    evidence_boundary: 'Low-level BBS multi-message signature and derived-proof execution aligned to the local experimental profile; not full VC Data Integrity bbs-2023 conformance.'
  },
  source_evidence: {
    artifact_class: 'case-local-signed-message-envelope',
    upstream_semantics_claimed: false,
    field_order: fieldOrder,
    values: source,
    signature: b64url(signature)
  },
  vectors: []
};

for(const vector of vectors) {
  const presentationHeader = contextBytes(contexts.original);
  const proof = await keyPair.deriveProof({
    signature,
    header,
    messages,
    presentationHeader,
    disclosedMessageIndexes: vector.disclosed
  });
  const originalVerified = await verifier.multiverify({
    proof,
    header,
    presentationHeader,
    messages: disclosedMessages(vector.disclosed)
  });

  const fields = disclosedFields(vector.disclosed);
  const privacyPass = !fields.some(name => prohibited.has(name));
  let replayVerified = null;
  let contextPass = true;
  if(vector.id === 'PA-ADV-001') {
    replayVerified = await verifier.multiverify({
      proof,
      header,
      presentationHeader: contextBytes(contexts.replay),
      messages: disclosedMessages(vector.disclosed)
    });
    contextPass = originalVerified && !replayVerified;
  }

  const overall = vector.id === 'PA-NEG-001'
    ? originalVerified && !privacyPass ? 'fail-privacy' : 'unexpected'
    : vector.id === 'PA-ADV-001'
      ? originalVerified && contextPass ? 'fail-context' : 'unexpected'
      : originalVerified && privacyPass && contextPass ? 'pass' : 'unexpected';

  if(!originalVerified) {
    throw new Error(`${vector.id}: BBS derived proof failed original-context verification.`);
  }
  if(vector.id === 'PA-POS-001' && !privacyPass) {
    throw new Error('PA-POS-001: prohibited disclosure observed.');
  }
  if(vector.id === 'PA-NEG-001' && privacyPass) {
    throw new Error('PA-NEG-001: negative vector no longer exposes protected data.');
  }
  if(vector.id === 'PA-ADV-001' && replayVerified) {
    throw new Error('PA-ADV-001: BBS proof unexpectedly verified under changed presentation context.');
  }
  if(overall !== vector.expected) {
    throw new Error(`${vector.id}: expected ${vector.expected}, got ${overall}.`);
  }

  const artifact = {
    vector: vector.id,
    expected: vector.expected,
    construction_verification: {
      original_context: originalVerified,
      replay_context: replayVerified
    },
    presentation_context: {
      original: contexts.original,
      replay_attempt: vector.id === 'PA-ADV-001' ? contexts.replay : null,
      adapter_encoding: 'UTF-8 JSON object carried as BBS presentationHeader'
    },
    disclosure: {
      disclosed_indexes: vector.disclosed,
      disclosed_fields: fields,
      disclosed_messages: vector.disclosed.map(index => decoder.decode(messages[index])),
      prohibited_field_observed: !privacyPass
    },
    proof: b64url(proof),
    case_evaluation: {
      cryptographic_verification: originalVerified ? 'pass' : 'fail',
      minimum_disclosure: privacyPass ? 'pass' : 'fail',
      context_binding: contextPass ? 'pass' : 'fail',
      overall
    }
  };

  result.vectors.push(artifact);
  await fs.writeFile(
    path.join(outputDir, `${vector.id}.json`),
    `${JSON.stringify(artifact, null, 2)}\n`,
    'utf8'
  );
}

await fs.writeFile(
  path.join(outputDir, 'run-result.json'),
  `${JSON.stringify(result, null, 2)}\n`,
  'utf8'
);

process.stdout.write(
  `IC-DTG-PROTECTED-ACCESS-001 BBS construction: PASS (${result.vectors.length}/3 vectors; ` +
  `PA-NEG-001 crypto-pass/privacy-fail preserved; PA-ADV-001 replay rejected)\n`
);
