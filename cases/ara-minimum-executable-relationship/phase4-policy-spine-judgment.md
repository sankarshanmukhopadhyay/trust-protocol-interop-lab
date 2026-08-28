# IC-ARA-REL-001 Phase 4 — visible authorization-spine judgment

Issue: #36  
Parent: #32  
Depends on completed Role Record phase: #35

## Proposition under test

Can a consequential operation be admitted only when the relevant identity, authority, exact agreement version, deterministic policy/duty decision, current relationship/Role Record state, task semantics, least-privilege capability, recipient, purpose, freshness, and evidence requirements all align?

## Alternatives genuinely considered

### 1. Treat a signed Trust Task as the operative authorization object

Rejected. A valid task/signature can prove attribution and exact bytes while still being outside authority, agreement, policy, capability, or current-state scope.

### 2. Treat authority/delegation evidence as the authorization decision

Rejected. Authority is an input to an instance decision, not the decision itself. A valid delegation may be out of purpose/resource/action scope or locally denied by applicable policy.

### 3. Mint capability before policy evaluation and let the actuator decide

Rejected. This makes possession of technical power precede and potentially bypass legitimate authorization. It also blurs capability, authorization, and execution evidence.

### 4. Build a single `is_authorized()` function returning Boolean

Rejected. A Boolean collapses evidence insufficiency, policy denial, escalation, agreement-state failures, stale state, and capability failures into one opaque outcome. It would make later evidence and falsification substantially weaker.

### 5. Implement an explicit authorization spine with separately attributable stages

Selected:

```text
Agreement lifecycle
    ↓
authority + identity + current Role Record/relationship state
    ↓
deterministic Policy Gate
    ↓
exact task binding
    ↓
least-privilege capability derivation
    ↓
execution admission
    ↓
correlated process/effect evidence
```

## Decision

Implement the Phase 4 path as a Lab-local executable composition with five distinct boundaries: Agreement Ledger, Policy Gate, Capability Service, Trust Task Builder, and Execution Admitter. Reuse the Phase 3 current Role Record head as a required authorization input.

The Policy Gate has a closed decision vocabulary:

- `allow`
- `deny`
- `escalate`
- `indeterminate`

`indeterminate` is not a softer PASS. It means evidence is insufficient to determine authorization and therefore cannot produce an operative capability.

## Core judgment

The minimum authorization claim is conjunctive:

> no individually persuasive artifact — identity, relationship, agreement, authority/delegation, task validity, capability possession, signature, execution effect, or later assurance — is independently sufficient to authorize the consequential operation.

The executable path must preserve the boundaries between:

```text
identity
!= authority
!= policy authorization
!= capability
!= execution admission
!= execution evidence
!= assurance
```

## Agreement Object judgment

Phase 2 found no pinned upstream component that directly owns the complete ARA Agreement Object lifecycle. Phase 4 therefore keeps the Agreement Object a bounded ARA-local hypothesis.

The selected model separates immutable/versioned terms from append-only lifecycle events. The implementation does **not** mutate accepted agreement terms in place to express acceptance, activation, suspension, or closure.

This choice is intended to make later questions observable:

- which exact terms were proposed/accepted?
- was the agreement merely accepted or actually active?
- which event changed current applicability?
- can a later correction or closure preserve the historical object?

It is not yet a normative proposal for upstream ownership.

## Capability judgment

Capability is deliberately derived **after** an `allow` decision and is bound to the exact:

- relationship;
- agreement reference;
- recipient;
- purpose;
- resource;
- action;
- expiry;
- originating authorization decision.

Attenuation may narrow expiry but cannot expand it. Suspension, expiry, and revocation are independently executable denial conditions.

Possession of a capability remains insufficient when authority has subsequently been revoked or the agreement/current state no longer permits execution.

## Trust Task judgment

The generic Trust Tasks framework remains direct reuse at its actual ownership boundary. Phase 4 introduces only a Lab-local ARA task identifier/profile sufficient to bind the experiment to the exact relationship authorization context.

This does not claim a registered/normative ARA Trust Task profile. If later work demonstrates a stable reusable task profile, that can be proposed upstream with evidence rather than assumed now.

## Execution-evidence judgment

The Execution Admitter emits an effect reference derived from the exact relationship, agreement, resource, action, payload digest, task, decision, and capability.

A later observed effect must match that correlation material. An actuator effect that happened but cannot be correlated to the admitted decision/task/capability is not accepted as evidence of a legitimate ARA action.

Execution evidence is not fed back as authority.

## Falsification evidence required

The implementation must fail safely for at least:

- authenticated identity without active authority;
- valid authority outside purpose/resource/action scope;
- accepted but inactive agreement;
- active agreement without capability;
- capability after authority revocation;
- capability bound to another agreement;
- unsupported task version;
- policy denial despite valid authority;
- missing evidence resulting in `indeterminate` rather than PASS;
- an effect not correlated to the admitted decision/task/capability;
- later assurance attempting to substitute for the original authorization decision;
- capability attenuation that expands scope/expiry;
- suspended, expired, or revoked capability;
- stale Role Record head.

## Rejected inferences

Phase 4 must not be read to establish that:

- an agreement creates authority;
- authority automatically means policy authorization;
- a valid Trust Task is authorized;
- capability possession proves legitimate authority;
- an execution effect proves the effect was legitimate;
- later assurance retroactively authorizes a denied/indeterminate action;
- the Lab-local task or capability format is a ToIP/ARA normative profile;
- the local Agreement Ledger settles upstream semantic ownership.

## Residual uncertainty

Still deliberately unresolved:

- normative Agreement Object ownership/schema;
- exact upstream ARA Trust Task profile(s);
- protected signing and cryptographic-use policy, which belongs to #37;
- independent receiver verification, which belongs to #38;
- standards-native authority/delegation substitution details;
- capability realization suitable for production enforcement;
- transport-level freshness/correlation behavior;
- whether any of these local components should become reusable libraries.

## Human acceptance boundary

A green run can satisfy `ARA-G4-POLICY-TASK-CAPABILITY` only for the bounded Lab-local executable proposition. It does not promote the overall ARA case, establish production security, or claim standards-native interoperability.

The judgment that should remain visible after merge is:

> ARA authorization is a sequence of independently inspectable decisions and state bindings, not a property conferred by whichever credential, delegation, agreement, capability, task, signature, or execution artifact happens to be easiest to verify. The implementation must make missing or contradictory conditions deny or remain indeterminate before technical power is exercised.
