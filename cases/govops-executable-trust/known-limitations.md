# IC-GOVOPS-EXEC-TRUST-001 — known limitations

`Candidate` maturity is limited to the repository-owned semantic composition and deterministic vectors.

- The evaluator is a reference governance model, not a GovOps implementation, PDP, proxy, or enforcement product.
- The PARC-aligned request projection is informative; PARC is not a normative dependency of this case.
- Authority, delegation, attenuation, identity, credentials, and attestations are modeled as authorization inputs; the experiment does not standardize those mechanisms for GovOps.
- Runtime observability is tested through identifiers and state relationships. The experiment does not require a specific telemetry stack, kernel mechanism, or vendor implementation.
- `decision_id`, `policy_store_id`, `policy_store_version`, and optional artifact identifiers are correlation evidence; they do not confer authority or prove an effect by themselves.
- The model tests that policy evaluation and enforcement remain distinct observable facts. It does not establish production enforcement correctness, race-free actuation, or transactional atomicity.
- Revocation is tested as a time-relative authority condition and historical-evidence property; distributed revocation propagation latency is not exercised.
- No wire-protocol, multi-implementation, performance, security certification, external conformance, GovOps endorsement, or production-interoperability claim is made.
- Promotion to `interoperability-tested` requires additional evidence under `GOVERNANCE.md`, including a bound evidence manifest and appropriately scoped executable evidence.
