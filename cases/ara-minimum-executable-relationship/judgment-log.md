# IC-ARA-REL-001 — visible judgment log

This log records consequential design judgments as they are made. It is intentionally not a retrospective narrative. Later changes should append or amend entries with attributable issue/PR evidence.

## J-001 — implementation home

**Question:** Should ARA implementation begin in a new repository or inside the Trust Protocol Interop Lab?

**Decision:** Begin inside the Lab as a bounded Interop Case.

**Alternatives actually considered:**

1. new standalone ARA implementation repository;
2. specification-first work with no executable case;
3. full standards-native implementation from the first increment;
4. state-first prototype only;
5. adversarial/simulation-only model;
6. executable vertical slice in the existing Lab.

**Selected:** 6.

**Reasoning:** The current architectural problem is composition across independently governed components. The Lab already owns composition, mappings, bindings, positive/negative vectors, evidence, and maturity claims while leaving upstream semantics upstream. A standalone implementation boundary is not yet evidenced. Creating it now would prematurely encode component ownership and lifecycle decisions that the experiment is meant to discover.

**Falsifier / reconsideration trigger:** If implementation yields a component with a stable independently reusable API, more than one credible consumer, distinct lifecycle/versioning needs, and clear semantic ownership, extraction to a dedicated repository should be reconsidered.

**Residual uncertainty:** The eventual reusable boundary may be a Role Record engine, distributed relationship-state library, protected-signing adapter, policy engine, conformance harness, or none of these.

**Evidence:** Program issue #32; foundation issue #33.

## J-002 — first implementation strategy

**Question:** Should the first ARA implementation require every proposed ToIP component to be integrated natively?

**Decision:** Use an adapter-backed vertical slice, then substitute real implementations one boundary at a time.

**Alternatives actually considered:**

- fully mocked simulation;
- adapter-backed execution with real semantics/evidence;
- immediate full TSP/VTA/RCard/VRC/Trust Tasks stack integration.

**Selected:** adapter-backed execution.

**Reasoning:** Fully mocked simulation can make architectural claims look true by construction. Immediate full-stack integration couples architectural debugging to the maturity and availability of every dependency. Adapter-backed execution allows state transitions, authorization conjunctions, negative cases, and evidence boundaries to be real while keeping unintegrated infrastructure explicitly marked as adapters.

**Constraint:** An adapter is not conformance evidence. Every adapter must declare the upstream or implementation contract it stands in for and the evidence required for substitution.

**Reconsideration trigger:** After the walking skeleton has reproducible evidence and the relevant upstream implementation is available/pinned, substitute the adapter and rerun the invariant suite.

## J-003 — initial use case

**Question:** Which relationship should prove the first executable slice?

**Decision:** Synthetic data-owner ↔ research-agent query-only relationship.

**Alternatives considered:**

- delegated document approval;
- controlled information release;
- research-data collaboration from the ARA proposal;
- a broader fiduciary negotiation lifecycle.

**Selected:** a reduced research-data collaboration.

**Reasoning:** It is consequential enough to exercise authority, agreement, capability, execution, evidence, privacy boundaries, challenge, and continuity while remaining synthetic and narrow enough to implement without importing domain-specific legal semantics.

**Constraint:** It must not be presented as a normative research-data governance profile.

## J-004 — first governing proposition

**Decision:** Treat legitimacy as a conjunction rather than a single credential or signature test.

The first implementation must be capable of denying an operation independently at identity/control, authority, agreement/state, policy authorization, task conformance, protected signing, receiver verification, capability, and execution-correlation boundaries.

**Falsifier:** If the implementation cannot keep those decisions independently observable, the ARA proposition is weakened or the component boundaries must be revised.

## J-005 — Live Agent authority

**Decision:** Live Agent output is non-operative proposal media until accepted by a deterministic Workflow and all later required boundaries.

**Reasoning:** This is the central containment claim needed to prevent model output from silently becoming consequential action.

**Required falsification evidence:** direct Live Agent signing and direct Live Agent actuator attempts must fail in the relevant implementation phases.

## J-006 — persistent relationship state

**Decision:** Each Agent Role owns its local Role Record. The distributed Verifiable Relationship Record is a logical verifiable intersection, not a new central jointly writable master database.

**Reasoning:** Centralization would make the first implementation easier but would fail to test the proposal's sovereignty, disagreement, provenance, and independent-verification claims.

**Required boundary cases:** unilateral annotation, inspection-versus-acceptance, dispute preservation, private evidence, pointer-only evidence, opaque commitment, and missing receipt.

**Residual uncertainty:** The minimum cryptographic/state representation is not selected in phase 1. Phase 3 will implement a Lab-local end-verifiable state mechanism; standards-native identity/provenance mechanisms remain later work.

## J-007 — pre-admission posture

**Decision:** Do not add `IC-ARA-REL-001` to the authoritative Interop Case catalog in the foundation PR.

**Reasoning:** The Lab's catalog maturity should be evidence-backed. Design completeness is not execution evidence.

**Admission trigger:** A later issue/PR must produce executable evidence sufficient for an explicitly bounded `experimental` claim and a human maintainer must accept that claim.

## J-008 — test philosophy

**Decision:** Tests must exercise semantic boundaries, not only code paths.

A passing function call is insufficient if the test does not demonstrate what would falsify the governing proposition. The invariant catalog therefore binds claims to candidate negative/adversarial vectors before runtime code exists.

**Examples:**

- valid identity + missing authority must deny;
- valid capability + revoked authority must deny;
- valid signature + wrong relationship must deny;
- successful actuator change + no decision/effect correlation must fail;
- copied bytes must not become inspected state;
- inspection must not become acceptance;
- later assurance must not retroactively authorize a denied action.

## J-009 — uncertainty handling

**Decision:** Use explicit `indeterminate` when required evidence is unavailable.

**Reasoning:** The implementation and assurance pipeline must not convert evidence insufficiency into a PASS simply to maintain a green execution result.

**Required falsification vector:** missing required evidence represented as PASS.

## J-010 — false-independence pressure

**Decision:** Multiplicity of credentials, witnesses, issuers, communities, attestations, votes, or evidence paths will not automatically count as independent support.

**Reasoning:** The ARA architecture may eventually rely on plural trust communities and evidence paths. Apparent multiplicity can create false confidence if the sources share control, provenance, infrastructure, incentives, or upstream evidence.

**Execution timing:** The minimum slice records the invariant now; systematic pressure occurs during the adversarial assurance phase when multiple trust/evidence paths are actually present.

## Open judgments deliberately not resolved in phase 1

The following decisions are intentionally deferred because evidence is not yet sufficient:

- exact long-lived Agent Role identity/control implementation;
- exact canonical Role Record cryptographic representation;
- which ARA operations already have direct Trust Task mappings;
- whether RCard/VRC profiles directly satisfy the minimum participant/relationship evidence needs;
- which VTA/OpenVTC implementation guarantees can replace the protected signer adapter;
- whether TSP integration changes privacy/correlation surfaces materially;
- whether a dedicated reusable component/repository should graduate from the Lab;
- exact criteria for `experimental` vs `interoperability-tested` maturity for this case.

These are not gaps to hide. They are the next judgments the issue → PR sequence is designed to make visible.
