# IC-TRQP-PKI-001 — Principal / Verification-Material Separation

Status: experimental independent interoperability evidence.

This Lab case tests downstream TRQP propositions without importing the TRQP fork's reference evaluator as an oracle. The Lab owns observations and evidence only; canonical protocol semantics remain outside this repository.

## Traceability

- Canonical downstream semantic tracker: https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/1
- Completed WP7 compatibility tracker: https://github.com/sankarshanmukhopadhyay/tswg-trust-registry-protocol/issues/4
- Lab tracker: https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/205
- Evidence-state tracker: https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/206
- TSPP lifecycle tracker: https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/79
- TSPP evidence tracker: https://github.com/sankarshanmukhopadhyay/TRQP-TSPP/issues/80
- Motivating Ayra reference: https://github.com/ayraforum/ayra-trust-registry-resources/issues/43

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

Additional negative vectors cover material mismatch and query-before-validity.

## Assurance boundary

Passing this case means the Lab can independently reproduce the safety distinctions required by the downstream proposition. It does not prove upstream acceptance, normative correctness, or generic TRQP interoperability.

No experimental artifact in this branch is eligible for automatic promotion to `main` solely because the tests pass.
