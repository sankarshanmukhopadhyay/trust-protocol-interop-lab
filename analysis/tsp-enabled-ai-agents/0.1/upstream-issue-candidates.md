# Candidate Upstream Issues

**Status:** Exploratory issue candidates; not filed upstream.

These issue-shaped findings preserve possible upstream feedback while allowing the lab to validate whether each issue remains necessary, correctly scoped, and experimentally supportable. They are intentionally not treated as upstream consensus or as a substitute for the upstream specification.

Each candidate carries a stable lab identifier so later upstream references can be recorded without changing the historical analysis baseline.

---

## TEA-ISSUE-01 — Complete the TEA Signed Payload normative definition

### Summary

The draft requires a TEA to implement a native signing scheme and relies on TEA Signed Payloads for third-party verification, authorization, delegation-chain presentation, accountability, and duty evidence, but the actual signing scheme is incomplete.

### Impact of the issue identified

Implementers cannot produce or verify the payloads required by multiple normative clauses. Independent choices around canonicalization, signature suites, key/VID references, replay protection, timestamps, message identifiers, audience/purpose binding, and nested payloads are likely to be incompatible.

### Suggested path to resolution

Define the payload container, canonical serialization, required fields, signature input, supported algorithms, VID/key binding, timestamp/expiry semantics, unique identifiers, audience/purpose/context binding, nonce/replay rules, nesting/detachment, verification failures, algorithm agility, and test vectors.

---

## TEA-ISSUE-02 — Complete Security and Trust Considerations with a normative threat model

### Summary

The draft introduces security-sensitive identity, authorization, delegation, negotiation, status, and accountability mechanisms, but does not yet define a structured threat model, security assumptions, attacker capabilities, trust boundaries, or residual risks.

### Impact of the issue identified

Implementers cannot determine expected behavior under controller/key compromise, malicious models/tools, replay, downgrade, stale status, identifier-resolution attack, policy attack, clock manipulation, resource exhaustion, or component compromise.

### Suggested path to resolution

Define protected assets, trust boundaries, trusted/untrusted components, attacker capabilities, cryptographic/resolver/status/time assumptions, availability expectations, and normative controls for secure failure, key lifecycle, replay, downgrade, status checking, chain limits, logging, privacy, and algorithm agility.

---

## TEA-ISSUE-03 — Define explicit conformance classes and implementation targets

### Summary

The draft applies normative language across TEAs, Controllers, TSP Gateways, exchange roles, delegation roles, verifiers, Trust Task support, composite TEAs, and MCP-over-TSP behavior without defining the unit of conformance.

### Impact of the issue identified

Implementers cannot determine which requirements apply to partial or role-specific implementations, and users cannot compare conformance claims meaningfully.

### Suggested path to resolution

Define role/component conformance classes, mandatory and optional features, applicable normative clauses, required error handling, and testable criteria. Clarify whether a complete TEA must implement every role or may declare a subset.

---

## TEA-ISSUE-04 — Define the authorization ACDC schema, issuance, and status-processing rules

### Summary

The draft requires authorization and duties to be represented in authorization ACDCs, but the complete normative schema and issuance/verification lifecycle are not defined.

### Impact of the issue identified

Independent implementations cannot produce mutually verifiable authorization credentials or consistently process validity, suspension, revocation, delivery, proof-of-possession, and Ack binding.

### Suggested path to resolution

Publish a versioned normative authorization ACDC schema and stepwise issuance/verification algorithms, including field/cardinality rules, issuer/issuee binding, resource/ability/caveat/duty encoding, validity/status references, Ack linkage, duplicate issuance, proof of possession, caching/freshness, and fail-closed status behavior.

---

## TEA-ISSUE-05 — Specify the closed capability core and deterministic attenuation semantics

### Summary

The draft depends on a bounded capability vocabulary, deterministic partial order, meet operation, and chain reduction, but the concrete lattice and composition rules are incomplete.

### Impact of the issue identified

The central safety property of strict attenuation cannot be implemented or tested consistently. Verifiers can disagree on resource subsets, abilities, caveats, duties, empty authority, and `AND`/`OR` composition.

### Suggested path to resolution

Define the resource model, ability vocabulary, supported constraint classes, duty composition, bottom authority, partial-order rules, meet algorithm, nesting/group semantics, deterministic failure, executable pseudocode, and adversarial reduction vectors.

---

## TEA-ISSUE-06 — Specify Authenticated Exchange as a complete state machine

### Summary

The draft defines Propose, Accept, Ack, and Withdraw and makes Ack consequential, but does not fully define state transitions, correlation, retransmission, duplicates, ordering, concurrent proposals, supersession, abort, restart recovery, replay, and invalid transitions.

### Impact of the issue identified

Peers can disagree about whether an agreement exists or which proposal is authoritative, creating duplicate or conflicting actions and audit records.

### Suggested path to resolution

Define normative state machines for each role, complete message schemas, correlation/idempotency/replay rules, proposal lineage, timeout/restart handling, terminal states, errors, sequence diagrams, and concurrency/race test vectors.

---

## TEA-ISSUE-07 — Define clock, validity, and expiry semantics consistently

### Summary

Authenticated Exchange and delegation use expiry/validity timestamps and a clock-skew tolerance that is not fully defined.

### Impact of the issue identified

Implementations can disagree about whether the same proposal, Ack, or delegation was valid, especially near boundaries, under skew, or during offline verification/status-service failure.

### Suggested path to resolution

Define canonical timestamp format/precision, inclusive/exclusive expiry boundaries, future-offset limits, clock-skew tolerance, unreliable-clock behavior, event-time versus verification-time rules, local receipt time, offline verification, stale status, and retained adjudication evidence.

---

## TEA-ISSUE-08 — Complete the MCP-over-TSP interoperability profile

### Summary

MCP integration is central to the draft, but the normative MCP-over-TSP profile is incomplete and does not define how MCP roles, sessions, JSON-RPC messages, tool discovery/invocation, errors, authorization, signed results, and transports bind to TSP/TEA semantics.

### Impact of the issue identified

Independent implementations can create incompatible MCP-over-TSP stacks and can lose identity, authority, or portable evidence at the MCP/TSP boundary.

### Suggested path to resolution

Define role mapping, session establishment, VID binding, JSON-RPC encapsulation, correlation, notifications, errors, cancellation, discovery, tool invocation, signed results, delegation presentation, coexistence with MCP security mechanisms, downgrade prevention, and transport mappings. Add an end-to-end example and vectors.

---

## TEA-ISSUE-09 — Define the normative TEA identifier profile and VID lifecycle

### Summary

The draft requires durable VIDs with rotation/pre-rotation/history and references `did:webvh`, while also distinguishing IVID and AVID, but lifecycle and binding behavior are incomplete.

### Impact of the issue identified

Implementations may resolve, rotate, cache, recover, deactivate, or bind the same identifier differently, weakening identity continuity and authorization decisions.

### Suggested path to resolution

Define required method/version, key purposes/algorithms, resolution, caching/freshness, rotation/pre-rotation, compromise recovery, deactivation, migration, historical signatures, privacy properties, and precise IVID/AVID equality/separation/binding/rotation rules.

---

## TEA-ISSUE-10 — Clarify TEA control boundary and composite/external component requirements

### Summary

The draft requires context, memory, and tool use to pass through the Controller while allowing externally hosted models/components and composite TEAs represented by one VID.

### Impact of the issue identified

Deployments can make equivalent TEA claims despite different mediation, egress, component identity, operator, and audit properties. A single VID may conceal materially different control domains.

### Suggested path to resolution

Define the TEA security boundary and controller enforcement requirements; remote model/tool authentication/logging; component identity; whole-agent VID ownership; attribution; and profiles for fully local, remote-model, remote-tool, multi-controller, and independently operated composite deployments.

---

## TEA-ISSUE-11 — Expand accountability into an implementable evidence and audit model

### Summary

The draft treats delegation chains as accountability traces but does not fully define action, authority-use, outcome/effect, and duty-performance evidence, or how a terminal VID connects to a responsible person/organization.

### Impact of the issue identified

A verifier may establish that authority existed without establishing which authority was exercised for a particular action, what effect occurred, or whether duties were discharged.

### Suggested path to resolution

Define separate evidence classes and minimum cryptographic links among acting TEA, presented authority, concrete operation, resource, task/exchange identifier, input, outcome, time, and duty evidence. Add privacy, access, retention, selective disclosure, dispute, and principal-linkage rules.

---

## TEA-ISSUE-12 — Define transport negotiation, mandatory behavior, and downgrade rules

### Summary

The draft is transport agnostic but references Streamable HTTP, `stdio`, and multiple confidentiality/metadata-protection modes without complete discovery, negotiation, framing, reconnect, error, or downgrade semantics.

### Impact of the issue identified

Otherwise conforming TEAs may fail to connect, select incompatible modes, or silently downgrade to weaker transport/security behavior.

### Suggested path to resolution

Define transport discovery metadata, endpoint syntax, preference/negotiation, framing/content types, lifecycle/resumption, message limits, flow control, cancellation, transport errors, cryptographic-mode negotiation, mandatory common suites, downgrade rejection, and the intended status of `stdio`.

---

## TEA-ISSUE-13 — Define semantics and interoperability rules for open policy extensions

### Summary

The draft permits open policy expressions to restrict authority beyond the closed core, but does not define the policy model, version, inputs, execution environment, determinism, external dependencies, unsupported-policy behavior, or proof that policy cannot broaden authority.

### Impact of the issue identified

The same delegation may be accepted, rejected, or broadened differently by different verifiers, reintroducing ambiguity into the authorization model.

### Suggested path to resolution

Require every policy to identify language/model/version, canonical digest, required inputs, evaluation time, dependencies, determinism, and fail behavior. Evaluate policy only after closed-core reduction and require the result to be equal authority, narrower authority, or denial; unsupported/invalid policy should fail closed.

---

## TEA-ISSUE-14 — Add protocol versioning, extension rules, error registries, and interoperability test vectors

### Summary

The draft lacks general rules for protocol versions, feature negotiation, extensions, unknown fields/messages, mandatory-to-understand behavior, error codes, backward compatibility, deprecation, and interoperability vectors.

### Impact of the issue identified

Early implementations can diverge permanently in ways that are difficult to repair once deployed, especially around signed payloads, state transitions, delegation reduction, identity rotation, and MCP integration.

### Suggested path to resolution

Define protocol/version identifiers, feature negotiation, extension registration, mandatory-to-understand semantics, unknown handling, downgrade protection, standard errors, deprecation, and normative/reference vectors for valid, invalid, boundary, and adversarial inputs.

---

## Filing order if upstream engagement becomes useful

1. TEA-ISSUE-01 — TEA Signed Payload
2. TEA-ISSUE-02 — Security/threat model
3. TEA-ISSUE-03 — Conformance
4. TEA-ISSUE-04 — Authorization ACDC
5. TEA-ISSUE-05 — Capability attenuation
6. TEA-ISSUE-06 — Authenticated Exchange state machine
7. TEA-ISSUE-07 — Time semantics
8. TEA-ISSUE-08 — MCP-over-TSP
9. TEA-ISSUE-09 — VID lifecycle
10. TEA-ISSUE-10 — TEA control boundary
11. TEA-ISSUE-11 — Accountability evidence
12. TEA-ISSUE-12 — Transport negotiation
13. TEA-ISSUE-13 — Open policy extension
14. TEA-ISSUE-14 — Versioning/errors/test vectors

## AI-tool usage declaration

These candidate issue texts were prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer. This disclosure is included voluntarily because no published WG/TF guidance governing the use or disclosure of such tools was identified for the reviewed baseline.
