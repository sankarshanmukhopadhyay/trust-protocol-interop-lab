# GovOps Candidate vectors

These vectors materialize the ten scenario contracts for `IC-GOVOPS-EXEC-TRUST-001` at Candidate maturity.

- `valid/` contains scenarios that preserve the intended governed path and historical-truth semantics.
- `invalid/` contains denial, revocation, correlation, enforcement-observability, and policy-provenance pressure tests.

`experiments/govops-executable-trust/run.py --check` verifies one-to-one scenario coverage, exact input/expected-outcome equivalence, invariant references, and deterministic evaluation. A vector MUST NOT drift from its governing scenario contract.

The vectors test repository-owned semantic composition only. They do not establish GovOps conformance, production enforcement correctness, wire interoperability, external certification, or endorsement.
