# Protected-access BBS construction run

This experiment adds **construction-layer cryptographic evidence** for `IC-DTG-PROTECTED-ACCESS-001`.

It reuses the BBS construction selected by the pinned local ZKP-fork profile `EXP-BBS-2023-01` at commit `6e1356812716dbd0e551272251e3e825132a8268` and executes BBS multi-message signing, selective-disclosure proof derivation, proof verification, and presentation-header replay rejection using `@digitalbazaar/bls12-381-multikey@2.2.0`.

## Evidence boundary

This is deliberately narrower than full `bbs-2023` conformance.

The run uses the same BLS12-381/SHA-256 BBS construction layer exercised by the ZKP fork's benchmark. It does **not** claim to execute the complete W3C Data Integrity credential canonicalisation and `DataIntegrityProof` processing pipeline.

The source evidence is also a case-local signed-message envelope. It is used to test the protected-access propositions without asserting that current upstream DTG Credentials/VRC/VWC specifications already define the `eligible` predicate.

## Context binding

The experiment serializes `{verifier, challenge, purpose}` as a UTF-8 JSON object and supplies it as the BBS `presentationHeader`.

That mapping is an Interop Lab adapter. The evidence therefore supports the narrower proposition that the derived proof is cryptographically bound to those supplied context bytes. It does not make the adapter encoding normative DTG or VC Data Integrity behavior.

## Vectors

- `PA-POS-001` derives and verifies a proof disclosing only `eligible`, provider-class authorization, and authority-provenance class.
- `PA-NEG-001` derives and verifies a cryptographically valid proof that additionally discloses protected provider identity and location. The cryptography therefore passes while the case privacy evaluation fails.
- `PA-ADV-001` verifies under its original presentation context, then fails verification when verifier, challenge, and purpose are changed.

## Run

```bash
cd experiments/dtg-protected-access-bbs
npm install --ignore-scripts --no-audit --no-fund
node run.mjs --output-dir /tmp/dtg-protected-access-bbs
```

The output directory contains one serialized result per vector plus `run-result.json`, including the BBS proof bytes, disclosed messages, presentation inputs, and verification outcomes. CI uploads these runtime artifacts rather than committing randomized proof bytes to the repository.

## What this unlocks

This run can satisfy the case's real-cryptography and concrete context-binding promotion gates. It only partially advances serialized-artifact maturity: Trust Task exchanges, status/authority-resolution traffic, DPIP-native results, cross-context correlation observations, and a final hashed evidence manifest remain separate gates.
