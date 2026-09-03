# Known limitations — IC-DTG-PROTECTED-ACCESS-001

This case is admitted at **Candidate** maturity for bounded semantic-composition review. Candidate status does not establish production interoperability, privacy certification, upstream conformance, or wire-protocol behaviour.

## Not established at Candidate maturity

- The ZKP component is a local experimental fork and the DPIP component is a local implementation profile; neither is represented as upstream normative DTG text.
- `eligible` remains a case-local relying predicate. The case does not assert that the credential baseline defines a universal eligibility or protected-person entitlement semantic.
- `provider_class_authorised` remains dependent on the authority/provenance mapping recorded by the case; relationship evidence alone does not create current entitlement, authorization, or disclosure permission.
- Correlation resistance is evaluated against the modelled verifier-visible interaction. Network timing, infrastructure logs, endpoint behaviour and other unmodelled side channels remain outside the bounded claim.
- Non-discoverability is evaluated against the declared observation surface and does not prove resistance to every possible enumeration strategy.
- The three-vector slice is intentionally small. It establishes structured positive, negative and adversarial propositions, not exhaustive privacy or security coverage.
- Existing deterministic run results support review, but no Candidate → `interoperability-tested` promotion is claimed until a governed evidence manifest binds the evaluator, vectors, invariants, ownership, limitations, baselines, results and claim scope under the strengthened maturity gate.
- No RAHP finding, external DPIP certification, legal entitlement conclusion, upstream defect finding or standards endorsement is created by this case.

## Promotion condition

Promotion to `interoperability-tested` requires a reproducible evidence package satisfying the repository's Tested evidence gate, including a bounded claim scope and integrity-bound execution evidence. The broader interaction must remain fail-closed: cryptographic validity cannot override privacy, authority, context or correlation failures.
