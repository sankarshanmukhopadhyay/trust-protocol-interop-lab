# IC-DTG-PROTECTED-ACCESS-001 — protected-person confidential service access

> **Status: pre-admission construction.** This directory defines an executable-ready boundary slice. It is not yet an admitted Interop Case and makes no upstream conformance, endorsement, defect, or implementation claim.

## Question

Can a protected person establish a narrowly scoped entitlement from an authorised provider without exposing the protected provider, relationship, location, case identifier, or durable cross-context correlator?

## Why this slice exists

This is the first vertical slice nominated by the DTG boundary-condition taxonomy and portfolio capability matrix. It converts the protected-person scenario from narrative pressure test into deterministic propositions that a later evaluator can execute.

The slice is intentionally jurisdiction-neutral. It does not define a shelter, domestic-violence, child-protection, social-service, or other vertical profile. `protected_provider` is an abstract service relationship whose disclosure may create safety or privacy harm.

## Pinned DTG baselines

The pre-admission slice is now bound to exact repository states in [`baselines.yaml`](baselines.yaml):

- `trustoverip/dtgwg-cred-spec` @ `b89f389abbdae77ba60b673c0836c781c2b54169` — upstream credential/VRC/VWC semantics;
- `trustoverip/dtgwg-trust-tasks-spec` @ `cfcb72aaaeca4478c470b0f571c760626b7177a9` — upstream Trust Tasks specification baseline;
- `sankarshanmukhopadhyay/dtgwg-zkp-tf` @ `6e1356812716dbd0e551272251e3e825132a8268` — local experimental ZKP/composed-presentation baseline;
- `sankarshanmukhopadhyay/dtg-privacy-implementation-profile` @ `3e5d286853178bec9b6579ecbdccd1932c281fc7` — local DPIP composed-privacy evaluation baseline.

Pinning makes the experiment reproducible. It does **not** establish that any baseline fully supports the case or convert local fork/profile material into upstream normative DTG text.

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

## Concrete mapping status

[`artifact-mapping.yaml`](artifact-mapping.yaml) records each case concept as `direct-mapping`, `candidate-mapping`, or `not-yet-evidenced`. This prevents the local experiment from silently inventing upstream semantics.

In particular, `eligible` remains a **case-local predicate** derived from attributable evidence; the current credential baseline is not claimed to define a universal eligibility predicate. VRC/VWC evidence can contribute relationship provenance, but relationship evidence is not automatically current entitlement, disclosure permission, or authorization.

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

## Observable privacy surface

[`observations.yaml`](observations.yaml) defines measurements over the **complete verifier-visible interaction**, including credential claims, issuer/subject metadata, proof metadata, Trust Task/thread identifiers, status or registry traffic, service/endpoint metadata, and derived identifiers.

This is deliberate: selective disclosure at the credential layer is insufficient evidence of non-discoverability or unlinkability if another surface reveals the same protected relationship or durable handle.

## DPIP handoff

[`dpip-handoff.yaml`](dpip-handoff.yaml) defines the narrow input/output contract for the next implementation gate. It requires DPIP to evaluate minimum disclosure, effective correlation scope, protected-relationship observability and context binding for all three vectors.

The handoff is a contract for future implementation, not a claim that the current DPIP baseline already contains the exact fixture/profile.

## Execution model

A later evaluator should consume the scenario, invariants, vectors, mapping, observations and DPIP result and produce at least:

- `cryptographic_verification` — pass/fail/not-evaluated;
- `authority_provenance` — pass/fail;
- `minimum_disclosure` — pass/fail;
- `non_discoverability` — pass/fail;
- `correlation_resistance` — pass/fail;
- `context_binding` — pass/fail;
- `case_outcome` — pass/fail.

The case outcome is conjunctive for the invariants applicable to each vector. A cryptographic `pass` must not override a privacy or context `fail`.

## Path to admission

The following gates are now complete:

1. exact upstream/local experimental baselines are pinned;
2. abstract case concepts have explicit mapping states;
3. privacy/correlation observations are defined;
4. the DPIP handoff contract is defined.

The construction becomes eligible for case-admission review only after:

1. the candidate artifact mappings are instantiated as concrete fixtures;
2. a deterministic evaluator can run all three vectors;
3. a concrete DPIP interaction fixture/profile binding produces results for the vectors;
4. expected observations are demonstrated in execution rather than only declared;
5. limitations and unresolved ownership questions are reviewed; and
6. the resulting admission claim remains no broader than the executable evidence.

Until those gates are met, this directory remains a pre-admission test design, not a catalog entry.
