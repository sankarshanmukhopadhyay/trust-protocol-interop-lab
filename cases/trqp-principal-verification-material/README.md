# IC-TRQP-PKI-001 — Principal / Verification-Material Separation

Status: experimental independent interoperability evidence.

This Lab case tests downstream TRQP propositions without importing the TRQP fork's reference evaluator as an oracle. The Lab owns observations and evidence only; canonical protocol semantics remain outside this repository.

## At a glance

The case asks whether an implementation can distinguish a principal from the verification material used by that principal, while preserving evidence authority, completeness, freshness, historical applicability, purpose and resource scope. Its primary falsification target is a legacy-style implementation that silently drops a decision-critical material qualifier and returns a broader positive result.

## Concrete scenario

A trust-registry consumer evaluates whether `did:example:issuer-a` may perform an `issue` action for `credential-x` using a specific verification material at a specified time. The fixture contains material rotation, revocation, purpose and resource differences, source completeness and freshness conditions, and historical evidence. The same principal can therefore be recognized while a particular material is revoked, stale, inapplicable, absent or unsupported.

## Traceability

- [Canonical downstream semantic tracker](https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/1)
- [Completed WP7 compatibility tracker](https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/4)
- [Lab tracker](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/205)
- [Evidence-state tracker](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/206)
- [TSPP lifecycle tracker](https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/79)
- [TSPP evidence tracker](https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/80)
- [Motivating Ayra reference](https://github.com/ayraforum/ayra-trust-registry-resources/issues/43)

Relevant upstream TRQP issues will be linked by full URL when available.

## Independent model

The fixture adapter evaluates an explicit proposition:

`principal + authority + action + resource + optional verification material + evaluation time`

It independently applies source authority, completeness, freshness, material lifecycle and purpose/resource matching. It produces one of three observation classes:

- `positive`
- `authoritative-negative`
- `indeterminate`

The vocabulary intentionally mirrors the propositions under test, but the implementation is repository-local and does not import code from `tswg-trust-registry-protocol`.

## Minimum matrix

| ID | Condition | Expected observation |
| --- | --- | --- |
| 01 | authoritative + complete + fresh + exact material | positive |
| 02 | material rotated; successor exact match | positive |
| 03 | revoked queried after revocation | authoritative-negative / revoked |
| 04 | authoritative complete absence | authoritative-negative / not-listed |
| 05 | absence with incomplete source | indeterminate / evidence-incomplete |
| 06 | absence from non-authoritative source | indeterminate / evidence-unavailable |
| 07 | stale positive evidence | indeterminate / evidence-stale |
| 08 | stale negative evidence | indeterminate / evidence-stale |
| 09 | historical query during prior material validity | positive |
| 10 | historical query without sufficient history | indeterminate / historical-evidence-incomplete |
| 11 | wrong purpose | authoritative-negative / not-applicable |
| 12 | wrong resource | authoritative-negative / wrong-resource |
| 13 | unknown decision-critical qualifier | indeterminate / unsupported-critical-context |
| 14 | legacy-v2 style qualifier drop | unsafe false-positive detector MUST fire |

Additional negative vectors cover material mismatch and query-before-validity. The executable evidence is in [`test/trqp-pki-independent.test.js`](../../test/trqp-pki-independent.test.js), with the independent adapter in [`adapter.js`](adapter.js) and deterministic fixtures in [`fixtures.js`](fixtures.js).

## Where it resolved

The Lab resolves the downstream falsification question at the evidence layer: an independent implementation can preserve the distinction between principal recognition and material applicability, can distinguish authoritative negative evidence from indeterminate evidence, and can detect the unsafe false positive produced by qualifier dropping. The dedicated WP8 workflow executes these vectors independently of the TRQP fork's reference evaluator.

## What remains unresolved

This case does not settle normative TRQP wire vocabulary, upstream versioning, or whether candidate TRQP 3.0 semantics will be accepted upstream. It also does not promote this case beyond experimental status. TSPP must independently validate its own evidence-state behaviour, and upstream reconciliation remains a separate authority gate.

## Why this matters

A trust decision that silently broadens `principal P using material M` into `principal P` changes the proposition being evaluated. That can turn revoked, wrong-purpose, wrong-resource or unknown material into an apparently valid authorization. Making that distinction executable gives downstream assurance tooling evidence that can be reproduced and audited rather than relying on narrative interpretation.

## Assurance boundary

Passing this case means the Lab can independently reproduce the safety distinctions required by the downstream proposition. It does not prove upstream acceptance, normative correctness, or generic TRQP interoperability.

No experimental artifact in this branch is eligible for automatic promotion to `main` solely because the tests pass.
