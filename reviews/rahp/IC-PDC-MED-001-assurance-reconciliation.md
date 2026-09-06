# IC-PDC-MED-001 assurance reconciliation

## Decision

`IC-PDC-MED-001` remains **Experimental**.

The execution programme is materially stronger than at admission: the case now has a deterministic application core, an explicit Trust Task binding, an execution-time current-authority boundary, runtime privacy evidence, a bounded refill/selective-disclosure extension, and an executable prescription-to-refill lifecycle. Those results are reproducible and useful. They are not sufficient to justify Candidate maturity because the strongest unresolved questions sit exactly at the trust boundaries that the case was intended to pressure-test.

## Why workflow green is not assurance green

Repository CI is expected to be green before any maturity decision. CI demonstrates that the retained experiments and documentation are internally reproducible. It does not resolve a missing upstream authority surface, provider-side privacy observations, or an unresolved protocol/profile semantic boundary.

The maturity decision therefore preserves `INDETERMINATE` as non-green and does not convert successful synthetic execution into a broader interoperability or production claim.

## Reconciled evidence

The deterministic PDC core passes its bounded positive, negative, replay, ambiguity and disclosure scenarios. The Trust Task adapter binds principal/requester, exact action, resource, context and expiry without treating identity as authority. The current-authority tranche then found no exact generic delegated-action evaluator in the pinned VTI/OpenVTC surfaces and correctly fails closed at actuation as `INDETERMINATE/BLOCKED` rather than substituting relationship or room-specific authority semantics.

Runtime privacy evidence establishes application-observable minimum disclosure for routine reminder, caregiver exception and late-ack paths. Stronger claims about provider logs, network/device metadata and cross-service correlation remain `INDETERMINATE` because those surfaces were not observed.

The bounded `IC-PDC-REFILL-001` extension shows that selective disclosure currently improves attribute minimisation over an ordinary contextual-subject presentation without requiring a ZKP claim. The modeled unlinkable-ZKP candidate remains `INDETERMINATE` until real proof generation and verification are exercised. The prescription/refill lifecycle separately demonstrates fail-closed handling of expiry, revocation, supersession, exhausted refill allowance, context mismatch, stale challenge and replay.

## Promotion blockers

1. **Current delegated authority at actuation:** no exact upstream/profile-defined evaluator for the precise delegated action/resource has yet been exercised.
2. **Provider/network privacy:** application-level disclosure controls pass, but provider/network/device confidentiality and broader correlation remain unobserved.
3. **Trust Task proof versus authenticated transport:** the document-proof/authcrypt boundary remains unresolved for a generic Trust Tasks conformance claim.
4. **Relationship versus delegation:** current relationship/member state must not be treated as delegated consequential-action authority without an explicit semantic mapping.

## Promotion rule

Candidate promotion should be reconsidered only after the above blockers are resolved or explicitly scoped out with evidence-backed rationale, followed by a fresh bounded assurance pass. Until then, `Experimental` is the accurate maturity state.

## Claim boundary

This reconciliation does not establish prescribing, clinical decision support, medication ingestion, legal dispensing authority, production pharmacy interoperability, healthcare certification, provider confidentiality, or universal unlinkability.
