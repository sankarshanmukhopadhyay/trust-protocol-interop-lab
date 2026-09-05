# Known limitations — IC-PDC-MED-001

`IC-PDC-MED-001` is an Experimental application-level composition case. Its first increment defines the model and falsification contract; it does not yet provide runtime evidence.

## Current limitations

- No deterministic care-coordination implementation has yet executed these acceptance scenarios.
- No VTC/OpenVTC runtime surface is pinned for this case yet; current-authority evaluation is therefore an explicit integration gap, not an interoperability result.
- DTG relationship semantics for the exact care relationship/delegation separation have not yet been proven by this case.
- Trust Task binding for principal, delegate/requester, exact action, resource and expiry is a candidate mapping until exercised.
- The channel is a simulator. No claim is made about WhatsApp transport confidentiality, metadata, retention, delivery semantics, lock-screen exposure, or provider behaviour.
- Medication-plan data is synthetic. No clinical correctness, prescribing, diagnostic, dosage, interaction, adherence, or patient-safety claim is made.
- `acknowledged` means user-reported acknowledgement only; the case does not verify ingestion.
- The extraction adapter is not yet implemented. Future OCR/LLM evaluation must remain advisory and fail to `REVIEW_REQUIRED` on uncertainty.
- P0 privacy uses compartmentalisation and minimum disclosure. Selective disclosure, unlinkability and ZKP are deferred to a separate refill/entitlement experiment.
- No DPIP or RAHP assessment should be treated as complete until runtime observations exist. Missing runtime evidence is not a PASS.
- Evidence-retention controls are currently contractual rather than measured in a running store.
- The case does not model legal guardianship, incapacity, emergency override, jurisdiction-specific consent, or professional clinical authority.

## Claim boundary

A green repository build for this tranche means only that the case contract is internally valid under repository checks. It does not establish application safety, privacy, medical suitability, DTG/VTC conformance, production readiness, external interoperability, or certification.

The useful next milestone is an executable deterministic core that can produce positive and negative traces against the acceptance contract while keeping all unresolved DTG/VTC mappings visible.