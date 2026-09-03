# IC-DTG-PROTECTED-ACCESS-001 — protected-person confidential service access

> **Status: Candidate.** This admitted Interop Case has pinned baselines, declared ownership/invariants, executable scenarios, positive/negative/adversarial vectors, expected outcomes and explicit limitations. It does not claim production interoperability, upstream conformance, external DPIP certification, endorsement, or a normative vertical profile.

## At a glance

| Item | Current state |
|---|---|
| **Status** | Candidate |
| **Purpose** | Test whether a protected person can prove a narrow entitlement while keeping the provider, relationship, location, case, and durable correlators hidden across the entire verifier-visible interaction. |
| **Current conclusion** | The semantic/privacy design is structured, executable, and pressure-tested enough for Candidate maturity, but runtime unlinkability and independent evidence remain incomplete. |
| **Evidence today** | Pinned baselines, ownership/invariants, positive/negative/adversarial vectors, deterministic evaluation, observation surfaces, DPIP binding, and runtime-evidence contracts. |

## Why this matters to a new reader

Selective disclosure is not enough if another part of the interaction leaks the protected relationship. A credential can hide a provider name while a status lookup, endpoint, task identifier, proof metadata, or durable subject handle reveals the same fact indirectly.

This case therefore treats privacy as a **composition property across the whole observable interaction**, not as a property of one credential format.

## Concrete scenario

A protected person needs to prove that they are eligible for a service from an authorized provider. The verifier needs only the decision predicate and sufficient assurance context.

The successful path should not require disclosure of the provider identity, provider location, relationship type, case identifier, durable subject identifier, or durable provider identifier. Replay into another verifier/context must also fail.

## Where it resolved

The case reached **Candidate** because the privacy and authority boundaries are explicit and mechanically testable. The current result supports minimum disclosure, non-discoverability, correlation-resistance, replay-resistance, and attributable authority provenance within the modeled observation surface.

The remaining gate is stronger governed execution evidence, especially runtime A/B evidence capable of supporting claims about correlation and unlinkability without relying solely on the semantic evaluator.


## What remains unresolved

The largest remaining gap is runtime privacy evidence strong enough to support unlinkability and non-discoverability claims across real observation surfaces. Independent implementation evidence and a governed Tested evidence manifest are also still required.

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
