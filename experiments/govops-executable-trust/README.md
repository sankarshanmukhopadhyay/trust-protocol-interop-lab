# GovOps executable-trust boundary evaluator

This experiment executes the machine-readable scenario contracts for `IC-GOVOPS-EXEC-TRUST-001` without binding the case to a particular policy engine.

It validates the governance propositions introduced or tightened after the upstream clarification in Discussion #6:

- authority/delegation evidence remains authorization input, not authorization;
- policy evaluation is implementation-neutral;
- `Allow` is distinct from observable enforcement;
- enforcement is distinct from the intended runtime effect;
- correlation uses explicit identifiers rather than overloading `capability_id`;
- substituted decision identifiers fail correlation;
- missing policy-store version keeps assurance indeterminate;
- revocation preserves the distinction between current authority validity and historical execution truth.

## Run

```bash
python experiments/govops-executable-trust/run.py --check
```

A successful run prints:

```text
PASS IC-GOVOPS-EXEC-TRUST-001: 10 scenarios / 12 invariants
PASS policy-engine neutrality, enforcement observability, correlation, policy provenance
```

## Evidence boundary

This evaluator is deterministic **contract evidence** for the local interoperability profile. It does not claim GovOps conformance, production interoperability, endorsement, or implementation equivalence with a specific PDP, proxy, framework, telemetry system, or PARC implementation.

The case remains Experimental until the project explicitly exercises its maturity gate and records the corresponding judgment. A later Interoperability Tested claim still requires reproducible runtime evidence and a hash-bound evidence manifest.
