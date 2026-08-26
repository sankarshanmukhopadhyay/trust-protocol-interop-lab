# IC-DTG-PROTECTED-ACCESS-001 — protected-person confidential service access

> **Status: pre-admission construction.** This directory defines an executable-ready boundary slice. It is not yet an admitted Interop Case and makes no upstream conformance, endorsement, defect, or implementation claim.

## Question

Can a protected person establish a narrowly scoped entitlement from an authorised provider without exposing the protected provider, relationship, location, case identifier, or durable cross-context correlator?

## Why this slice exists

This is the first vertical slice nominated by the DTG boundary-condition taxonomy and portfolio capability matrix. It converts the protected-person scenario from narrative pressure test into deterministic propositions that a later evaluator can execute.

The slice is intentionally jurisdiction-neutral. It does not define a shelter, domestic-violence, child-protection, social-service, or other vertical profile. `protected_provider` is an abstract service relationship whose disclosure may create safety or privacy harm.

## Boundary conditions under test

- `BC-AUTH-PROVENANCE` — entitlement evidence must have an attributable authority source without revealing unnecessary provider identity.
- `BC-MINIMUM-DISCLOSURE` — the verifier learns only the decision predicate and required assurance context.
- `BC-NON-DISCOVERABILITY` — successful verification must not expose or enable enumeration of the protected provider or relationship.
- `BC-CORRELATION-RESISTANCE` — normal artifacts must not expose a stable cross-context subject, case, or provider correlator.
- `BC-REPLAY-RESISTANCE` — a presentation bound to one verifier/context/challenge must not silently authorize another context.

## Actors

- `P` — protected person.
- `S` — protected service provider, whose specific identity and location are not required by the relying decision.
- `A` — authority or governance source that establishes the provider class or entitlement basis.
- `R` — relying party that needs the narrow predicate `eligible = true`.
- `X` — adversarial or colluding verifier attempting replay, correlation, or relationship discovery.

## Decision contract

The relying party MAY learn:

```yaml
eligible: true
provider_class_authorised: true
proof_context_valid: true
```

The ordinary successful flow MUST NOT require the verifier to learn:

```yaml
protected_provider_identity: null
protected_provider_location: null
protected_relationship_type: null
case_identifier: null
durable_subject_identifier: null
durable_provider_identifier: null
```

The null values are semantic expectations: the evaluator must confirm that those fields or equivalent correlating information are absent from the observable result, not merely blank in a fixture.

## Three-vector slice

| Vector | Class | Expected outcome | Main proposition |
|---|---|---|---|
| `PA-POS-001` | positive | pass | valid entitlement can be proven with minimum disclosure |
| `PA-NEG-001` | negative | fail-privacy | cryptographic validity does not excuse unnecessary protected disclosure |
| `PA-ADV-001` | adversarial | fail-context | replayed proof does not establish current/contextual validity and does not create a discovery path |

## Critical semantic separations

```text
relationship existence
  ≠ authority provenance
  ≠ entitlement
  ≠ proof validity
  ≠ context validity
  ≠ authorization
  ≠ disclosure permission
  ≠ assurance
```

A verifier may receive a cryptographically valid artifact and the composed interaction may still fail this case because the artifact over-discloses protected information or is invalid for the current context.

## Execution model

A later evaluator should consume the scenario, invariants, and vectors and produce at least:

- `cryptographic_verification` — pass/fail/not-evaluated;
- `authority_provenance` — pass/fail;
- `minimum_disclosure` — pass/fail;
- `non_discoverability` — pass/fail;
- `correlation_resistance` — pass/fail;
- `context_binding` — pass/fail;
- `case_outcome` — pass/fail.

The case outcome is conjunctive for the invariants applicable to each vector. A cryptographic `pass` must not override a privacy or context `fail`.

## Path to admission

This construction becomes eligible for case-admission review only after:

1. upstream baselines and semantic owners are pinned;
2. the abstract proof/input fields are mapped to concrete DTG artifacts;
3. a deterministic evaluator can run all three vectors;
4. expected observations are shown to be measurable rather than assumed;
5. limitations and unresolved ownership questions are reviewed; and
6. the resulting admission claim remains no broader than the executable evidence.

Until those gates are met, this directory is a pre-admission test design, not a catalog entry.