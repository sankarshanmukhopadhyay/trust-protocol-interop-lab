# Implementation Gap Analysis

## Executive assessment

The draft establishes a useful architectural direction for TSP-enabled agents, but several implementation-critical areas remain underspecified. The most consequential gaps are not editorial: they concern wire formats, conformance boundaries, state transitions, authorization semantics, security assumptions, and protocol composition.

For this lab, the central question is not whether the draft is conceptually persuasive, but whether two independent implementers can build compatible systems from it and reach the same security-relevant conclusions from the same evidence.

The findings below are ordered approximately by implementation impact.

---

## GAP-01 — TEA Signed Payload is not normatively complete

### Observation

The draft requires TEAs to implement a native signing scheme and relies on signed payloads for third-party verification, authorization, delegation-chain presentation, accountability, and duty evidence. The concrete payload and signing definition is incomplete.

### Implementation consequence

An implementer cannot determine the canonical payload form, signature input, key binding, replay protection, timestamp processing, message identifiers, nested payload behavior, or verification algorithm from the draft alone.

### Interoperability consequence

Implementations can produce signatures that are individually valid but mutually unverifiable, or can disagree about whether the signed material is sufficiently bound to sender, audience, purpose, time, or exchange context.

### Candidate resolution

Define a complete TEA Signed Payload format and verification algorithm, including canonical serialization, required fields, signature suites, VID/key binding, audience/purpose binding, timestamps, expiry, replay resistance, nesting, failure conditions, algorithm agility, and test vectors.

---

## GAP-02 — Security and trust considerations lack a normative threat model

### Observation

The draft introduces identity, negotiation, delegation, credential status, authorization, and accountability mechanisms for autonomous agents, but the security section does not yet define attacker capabilities, trust boundaries, protected assets, or residual risks.

### Implementation consequence

Implementers cannot distinguish required controls from deployment assumptions, nor determine expected behavior when keys, controllers, models, tools, resolvers, clocks, status services, or policy engines are compromised or unavailable.

### Interoperability consequence

Security-sensitive behavior can diverge across deployments, especially for replay, fail-open/fail-closed status handling, chain depth, downgrade, key compromise, stale state, and malicious extension handling.

### Candidate resolution

Add a structured threat model and trace security claims to explicit assumptions and verification procedures. Include key compromise, prompt injection, tool poisoning, confused deputy, replay, downgrade, delegation abuse, status-registry compromise, identifier-resolution attacks, metadata correlation, resource exhaustion, malicious policies, clock manipulation, and composite-agent compromise.

---

## GAP-03 — Conformance classes and implementation targets are undefined

### Observation

The draft contains normative requirements for TEAs and describes controllers, gateways, wallets, exchange roles, delegation roles, verifiers, Trust Task usage, composite agents, and MCP-over-TSP behavior, but it does not define which role or component is the unit of conformance.

### Implementation consequence

A partial implementation cannot determine which requirements apply to it or which subset it may claim to conform to.

### Interoperability consequence

Product and test-suite claims become incomparable. A deployment may advertise TEA conformance while omitting functionality another implementation assumes to be mandatory.

### Candidate resolution

Define conformance classes such as TEA Endpoint, Controller, TSP Gateway, Authenticated Exchange Initiator/Responder, Delegation Issuer/Holder/Verifier, Trust Task Profile, and Composite TEA. For each, identify mandatory features, applicable normative clauses, error handling, and testable criteria.

---

## GAP-04 — Authorization ACDC schema and processing rules are incomplete

### Observation

The draft requires authorization and duty information to be represented using authorization ACDCs, but the schema, issuance mechanics, Ack binding, delivery, proof-of-possession, status lookup, suspension/revocation handling, and verifier behavior are not fully defined.

### Implementation consequence

Independent implementations cannot reliably issue and verify mutually understood authorization credentials.

### Interoperability consequence

The same delegation may be accepted, rejected, or interpreted differently across implementations, particularly when credential status is unavailable, stale, suspended, or revoked.

### Candidate resolution

Publish a versioned authorization ACDC schema and stepwise issuance/verification algorithms, including issuer/issuee binding, resource/ability/caveat/duty fields, validity, status references, Ack-to-credential linkage, duplicate issuance, proof of possession, and fail-closed status behavior.

---

## GAP-05 — Closed capability core and attenuation semantics are undefined

### Observation

The draft relies on a bounded vocabulary, deterministic partial order, meet operation, and chain reduction to guarantee strict authority attenuation. The actual vocabulary and reduction semantics are not yet defined.

### Implementation consequence

Implementers cannot determine whether one delegation is narrower than another, how caveats intersect, how duties accumulate, or what constitutes empty authority.

### Interoperability consequence

This can create authorization widening: one verifier may compute broader effective authority than another from the same delegation chain.

### Candidate resolution

Define the interoperable closed core: resource model, ability vocabulary, temporal/numeric/enumerated constraints, duty composition, bottom authority, partial-order rules, meet algorithm, `AND`/`OR` semantics, deterministic failure, executable pseudocode, and adversarial test vectors.

---

## GAP-06 — Authenticated Exchange lacks a complete state machine

### Observation

The draft defines `Propose`, `Accept`, `Ack`, and `Withdraw`, and treats Ack as a binding act, but does not fully specify exchange states, correlation, retransmission, duplicate handling, reordering, concurrent proposals, supersession, abort, restart recovery, replay, and invalid transitions.

### Implementation consequence

An implementation must invent significant state-management behavior.

### Interoperability consequence

Peers may disagree about whether an agreement exists, which proposal is live, whether an Ack is effective, or whether a duplicated or late message is actionable.

### Candidate resolution

Specify normative Initiator and Responder state machines, complete message schemas, correlation identifiers, idempotency rules, timeout and replay behavior, restart recovery, terminal states, errors, sequence diagrams, and test cases for race conditions and duplicate messages.

---

## GAP-07 — Time, validity, and expiry semantics are incomplete

### Observation

Authenticated Exchange and delegation rely on `validUntil`, Ack timestamps, credential validity, and an undefined clock-skew tolerance.

### Implementation consequence

Implementers lack a common rule for time format, precision, boundary inclusion, future-dated messages, skew, unreliable clocks, status evidence, or offline verification.

### Interoperability consequence

Two conforming peers can reach different conclusions about whether the same proposal, Ack, or delegation was valid at the relevant time.

### Candidate resolution

Define common time-processing rules across the specification, including canonical timestamps, boundary semantics, skew tolerance, future offset, authoritative verification time, local receipt time, offline verification, stale status, service unavailability, and evidence retention.

---

## GAP-08 — MCP-over-TSP profile is incomplete

### Observation

MCP integration is a prominent use case, but the normative MCP-over-TSP profile is not complete. The draft also references Streamable HTTP and `stdio` without defining the mapping between MCP sessions/messages and TSP identities/relationships.

### Implementation consequence

Implementers cannot determine JSON-RPC encapsulation, role mapping, session binding, tool discovery, authorization interaction, result signing, error handling, cancellation, or compatibility with existing MCP security mechanisms.

### Interoperability consequence

Different implementations may build incompatible “MCP over TSP” stacks even while following the same high-level draft.

### Candidate resolution

Define an MCP-over-TSP profile covering role mapping, session establishment, VID binding, JSON-RPC encapsulation, correlation, notifications, errors, cancellation, discovery, tool invocation, signed results, authorization/delegation presentation, coexistence with MCP authorization, downgrade protection, and transport profiles.

---

## GAP-09 — TEA identifier profile and VID lifecycle are incomplete

### Observation

The draft requires durable VIDs, key rotation, pre-rotation, and verifiable key history, and references `did:webvh`, while also distinguishing Introduction VIDs and Authorization VIDs.

### Implementation consequence

Creation, resolution, key-purpose rules, rotation, recovery, deactivation, migration, caching, compromise handling, and IVID/AVID binding are not sufficiently deterministic.

### Interoperability consequence

Peers may resolve or validate the same identifier differently, or disagree about continuity after rotation and compromise.

### Candidate resolution

Define a TEA VID profile with required method/version, key purposes/algorithms, resolution, caching, rotation/pre-rotation, compromise recovery, deactivation, historical verification, privacy properties, and precise IVID/AVID relationship semantics.

---

## GAP-10 — TEA control boundary and composite-agent semantics are ambiguous

### Observation

The draft requires model context, memory, and tool use to pass through the Controller, while permitting externally hosted models/components and composite TEAs represented by one VID.

### Implementation consequence

It is unclear what the Controller must technically mediate or enforce, how remote components authenticate, when components require distinct VIDs, and how internal actions are attributed.

### Interoperability consequence

Different deployments can claim equivalent TEA properties despite materially different security/control boundaries.

### Candidate resolution

Define the TEA security boundary and deployment profiles for local, remote-model, remote-tool, composite, and independently operated components. Specify mediation, egress, logging, authentication, component identity, control ownership, and evidence linkage requirements.

---

## GAP-11 — Accountability chain is not yet a complete evidence model

### Observation

The draft treats delegation chains as accountability traces, but does not fully define action records, task linkage, authority-use evidence, outcomes, duty-performance evidence, retention, selective disclosure, audit access, or linkage from terminal VID to accountable legal/organizational principal.

### Implementation consequence

A verifier may know that authority existed without being able to establish which authority was exercised for a specific action or whether duties were satisfied.

### Interoperability consequence

Implementations can produce incompatible or insufficient audit records, undermining portable accountability evidence.

### Candidate resolution

Separate authority provenance, exercise-of-authority evidence, outcome/effect evidence, and duty-performance evidence. Define minimum fields and cryptographic links, privacy and retention controls, dispute handling, and the role of governance/credentials in connecting a VID to a responsible principal.

---

## GAP-12 — Transport negotiation and downgrade rules are incomplete

### Observation

The draft is transport agnostic but requires Streamable HTTP and `stdio`, and references multiple confidentiality/metadata-protection modes without complete negotiation semantics.

### Implementation consequence

Peers lack a deterministic method to advertise transport capabilities, select endpoints/modes, map errors, resume sessions, or reject weaker fallback paths.

### Interoperability consequence

Conforming peers may fail to connect or may silently downgrade to weaker transport/security behavior.

### Candidate resolution

Define transport discovery, endpoint syntax, preference/negotiation, framing, connection lifecycle, resumption, message limits, flow control, cancellation, error mapping, cryptographic-mode negotiation, common mandatory suites, and downgrade prevention. Clarify the intended status of `stdio`.

---

## GAP-13 — Open policy extension lacks portable evaluation semantics

### Observation

The draft permits open policy expressions for restrictions that cannot be represented in the closed core, while requiring them only to attenuate authority.

### Implementation consequence

Policy language, version, inputs, evaluation time, determinism, external dependencies, failure mode, and proof of non-expansion are unspecified.

### Interoperability consequence

A delegation can be accepted by one policy engine and rejected or broadened by another.

### Candidate resolution

Define an extension framework identifying language/model, version, canonical digest, required inputs, evaluation semantics, external dependencies, and fail-closed behavior. Require open policy evaluation to occur only after closed-core authority reduction and to return equal authority, narrower authority, or denial.

---

## GAP-14 — Versioning, extension processing, errors, and interoperability vectors are incomplete

### Observation

The draft lacks a general model for protocol versioning, feature negotiation, extension registration, unknown fields/messages, mandatory-to-understand behavior, error registries, backward compatibility, deprecation, and test vectors.

### Implementation consequence

Early implementations must invent evolution and error behavior.

### Interoperability consequence

Small independent choices can become persistent incompatibilities, particularly for signed payloads, identifier rotation, exchange state, delegation reduction, and MCP integration.

### Candidate resolution

Define version and capability negotiation, extension rules, downgrade protection, unknown-field/message behavior, standard errors, deprecation, and normative/reference vectors for valid and adversarial cases.

---

## Priority grouping

### Implementation-blocking

- GAP-01 TEA Signed Payload
- GAP-02 Security/threat model
- GAP-03 Conformance
- GAP-04 Authorization ACDC
- GAP-05 Capability attenuation
- GAP-06 Authenticated Exchange state machine
- GAP-07 Time semantics
- GAP-08 MCP-over-TSP

### High-priority interoperability hardening

- GAP-09 VID lifecycle
- GAP-10 TEA control boundary
- GAP-11 Accountability evidence
- GAP-12 Transport negotiation
- GAP-13 Open policy extension
- GAP-14 Versioning/errors/test vectors

## AI-tool usage note

This analysis was prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer. The disclosure is voluntary; no published AIMWG/TF guidance governing such usage or disclosure was identified for the reviewed baseline.
