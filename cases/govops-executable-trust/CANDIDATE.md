# Candidate maturity judgment — IC-GOVOPS-EXEC-TRUST-001

**Decision:** Promote from `experimental` to `candidate`.

## Evidence basis

- 12 explicit invariants preserve capability, authority, authorization, enforcement, execution, evidence, assurance, revocation, observability, and correlation boundaries.
- 10 scenario contracts are materialized as 10 explicit positive/negative JSON vectors.
- The deterministic evaluator checks one-to-one scenario coverage and exact vector/scenario equivalence.
- The upstream-clarification pressure tests cover `Allow` without observable enforcement, decision identifier substitution, and missing policy-store version provenance.
- Known limitations explicitly exclude GovOps conformance, production enforcement correctness, wire interoperability, external certification, and endorsement.

## Claim boundary

Candidate maturity establishes that this repository-owned semantic composition is explicit, falsifiable, and deterministically testable. It does not establish `interoperability-tested` maturity. That requires the additional evidence package and hash-bound manifest governed by `GOVERNANCE.md`.

**Tracking:** issue #85; boundary-alignment issue #82; upstream judgment anchor Discussion #6.
