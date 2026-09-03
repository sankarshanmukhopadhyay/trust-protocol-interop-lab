# IC-DTG-PROTECTED-ACCESS-001 — protected-person confidential service access

> **Status: Candidate.** This admitted Interop Case has pinned baselines, declared ownership/invariants, executable scenarios, positive/negative/adversarial vectors, expected outcomes and explicit limitations. It does not claim production interoperability, upstream conformance, external DPIP certification, endorsement, or a normative vertical profile.

## Question

Can a protected person establish a narrowly scoped entitlement from an authorised provider without exposing the protected provider, relationship, location, case identifier, or durable cross-context correlator?

## Pinned DTG baselines

The case is bound to exact repository states in [`baselines.yaml`](baselines.yaml):

- `trustoverip/dtgwg-cred-spec` @ `b89f389abbdae77ba60b673c0836c781c2b54169` — upstream credential/VRC/VWC semantics;
- `trustoverip/dtgwg-trust-tasks-spec` @ `cfcb72aaaeca4478c470b0f571c760626b7177a9` — upstream Trust Tasks specification baseline;
- `sankarshanmukhopadhyay/dtgwg-zkp-tf` @ `6e1356812716dbd0e551272251e3e825132a8268` — local experimental ZKP/composed-presentation baseline;
- `sankarshanmukhopadhyay/dtg-privacy-implementation-profile` @ `3e5d286853178bec9b6579ecbdccd1932c281fc7` — local DPIP composed-privacy evaluation baseline.

Pinning makes the case reproducible. It does **not** establish that any baseline fully supports the case or convert local fork/profile material into upstream normative DTG text.

## Boundary conditions under test

- `BC-AUTH-PROVENANCE` — entitlement evidence has an attributable authority source without requiring disclosure of unnecessary provider identity.
- `BC-MINIMUM-DISCLOSURE` — the verifier learns only the decision predicate and required assurance context.
- `BC-NON-DISCOVERABILITY` — successful verification does not expose or enable enumeration of the protected provider or relationship within the modelled observation surface.
- `BC-CORRELATION-RESISTANCE` — normal artifacts do not expose a stable cross-context subject, case, or provider correlator within the modelled observation surface.
- `BC-REPLAY-RESISTANCE` — a presentation bound to one verifier/context/challenge does not silently authorize another context.

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

## Structured review evidence

| Vector | Class | Expected outcome | Main proposition |
|---|---|---|---|
| `PA-POS-001` | positive | pass | valid entitlement can be proven with minimum disclosure |
| `PA-NEG-001` | negative | fail-privacy | cryptographic validity does not excuse unnecessary protected disclosure |
| `PA-ADV-001` | adversarial | fail-context | replayed proof does not establish current/contextual validity and does not create a discovery path |

The deterministic evaluator and recorded results make the declared propositions inspectable, but Candidate maturity intentionally stops short of `interoperability-tested` until a governed evidence manifest binds the execution under the strengthened Tested gate.

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

[`observations.yaml`](observations.yaml) defines measurements over the complete verifier-visible interaction, including credential claims, issuer/subject metadata, proof metadata, Trust Task/thread identifiers, status or registry traffic, service/endpoint metadata, and derived identifiers.

Selective disclosure at the credential layer is therefore insufficient evidence of non-discoverability or unlinkability if another surface reveals the same protected relationship or durable handle.

## DPIP binding

The case includes a concrete DPIP interaction profile and treats DPIP as an implementation/evaluation input rather than an external certification authority. Privacy failure is evaluated over the composed interaction rather than proof validity alone.

## Promotion boundary

Candidate maturity establishes that the question is structured for review and falsification. Promotion to `interoperability-tested` requires the repository's stronger evidence-manifest gate: reproducible execution evidence, bounded claim scope, integrity references, and explicit preservation of authority/privacy/context limitations.

See [`known-limitations.md`](known-limitations.md) for the current claim boundary.
