# IC-ARA-REL-001 — minimum executable Agent Relationship Architecture relationship

> **Status: pre-admission construction.** This directory defines the first executable-ready ARA vertical slice. It is not yet an admitted Interop Case and makes no claim of ToIP approval, upstream conformance, production security, external certification, or complete implementation of the July 2026 ARA proposal.

Parent program: [#32](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/32)  
Foundation issue: [#33](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/33)

## Governing question

Can two independently controlled persistent Agent Roles perform one consequential relationship action **only when** identity, authority, exact agreement or other governing basis, deterministic Workflow authorization, exact task semantics, protected signing authority, capability scope, current relationship state, recipient-side verification, and evidence requirements all permit it — while preserving verifiable relationship evidence that survives Live Agent replacement and supports challenge, correction, remediation, continuation, and closure?

The question is intentionally conjunctive. A PASS at one boundary does not compensate for a FAIL or missing evidence at another boundary.

## Why this slice exists

The ARA proposal integrates TSP, TSP-Enabled Agents, Trust Tasks, RCards, VRCs, VTAs, VTCs, persistent Agent Roles, Role Records, distributed Verifiable Relationship Records, Agreement Objects, capabilities, and Relationship Views. Implementing all of those simultaneously would make it difficult to distinguish an architectural failure from component immaturity or integration plumbing.

This slice therefore starts with a deliberately small **adapter-backed walking skeleton**. The relationship semantics, state transitions, invariants, failure classes, and evidence obligations are real and machine-testable. Where a standards-native implementation is not yet integrated, the case uses an explicit Lab adapter and records the missing substitution evidence.

The case is intended to discover specification and implementation boundaries, not to pre-ordain them.

## Initial synthetic relationship

A **data-owner Agent Role** permits a **research Agent Role** to perform one query-only operation against a synthetic protected dataset.

The relationship is intentionally narrow:

- the dataset is synthetic;
- the permitted operation is query-only;
- mutation and export are prohibited;
- an exact Agreement Object governs the action;
- authority is independently represented from identity and agreement;
- a deterministic Policy Gate decides whether the task may proceed;
- capability is derived only after authorization and is scoped to the exact agreement/relationship/action;
- protected signing is a separate decision boundary;
- the receiver independently verifies rather than trusting the sender's internal conclusion;
- each Agent Role maintains its own Role Record;
- externally meaningful shared evidence is reconstructed as a distributed relationship intersection, not a central jointly writable master record;
- the relationship can be challenged, corrected, remediated, revoked, continued, or closed without rewriting accepted history.

This is not a normative research-data governance profile.

## Actors and implementation roles

| Symbol | Role | Accountability boundary |
|---|---|---|
| `A` | Data-owner Agent Role | Persistent accountable role controlling the protected dataset relationship |
| `A-live` | Live Agent for A | Temporary generative process that may propose media/intents but cannot directly sign or actuate |
| `A-wf` | Deterministic Workflow / Policy Gate for A | Interprets the proposal against authority, agreement, policy, relationship state, and evidence requirements |
| `A-ps` | Protected signer adapter for A | Exercises cryptographic use only for an authenticated, admitted, exact request |
| `B` | Research Agent Role | Persistent counterparty role requesting the bounded query |
| `B-live` | Live Agent for B | Temporary generative process; no independent consequential authority |
| `B-wf` | Deterministic Workflow / verifier for B | Independently evaluates received artifacts and local policy/state |
| `EXEC` | Query actuator | Performs only the capability-bounded synthetic query |
| `RR-A` / `RR-B` | Role Records | Independently controlled persistent local state and evidence |
| `VRR` | Distributed relationship evidence | Logical verifiable intersection reconstructed from exact shared objects, receipts, attestations, commitments, and checkpoints |
| `H` | Authorized human reviewer | May receive a bounded Relationship View and perform required acceptance/escalation decisions |

## Minimum ceremony

The first executable ceremony is deliberately smaller than the complete ARA lifecycle:

1. Resolve or instantiate persistent Agent Roles `A` and `B`.
2. Create relationship-local branches in `RR-A` and `RR-B`.
3. Construct an immutable Agreement Object proposal.
4. Counterparty independently inspects the exact Agreement Object.
5. Record exact acceptance/activation only when required conditions are satisfied.
6. Bind authority evidence separately from identity and agreement.
7. A Live Agent proposes the bounded query intent as non-operative media.
8. The deterministic Workflow retrieves current Role Record head, relationship state, exact agreement, authority, applicable policy/duties, recipient, and evidence requirements.
9. The Policy Gate emits `allow`, `deny`, `escalate`, or `indeterminate`.
10. On `allow`, derive a narrow relationship/agreement-scoped capability.
11. Construct the exact Trust Task / signed-action request.
12. Submit it to the protected signer adapter.
13. Sign only if the Workflow, Role Record head, authority, task type/version, recipient, payload, purpose, capability, nonce, and expiry are permitted.
14. Serialize and transmit across an independent process/transport boundary.
15. Counterparty independently verifies the signed task and its own relationship/policy state.
16. Execute only the admitted query-only capability.
17. Produce process and execution-effect evidence correlated to the exact decisions/task/capability.
18. Advance `RR-A` and `RR-B` independently.
19. Produce shared receipts/attestations/checkpoint material sufficient to reconstruct the distributed relationship intersection.
20. Terminate a Live Agent and demonstrate continuation using persisted authorized state rather than conversation memory.
21. Exercise challenge/correction/remediation/revocation.
22. Continue or close without rewriting historical evidence.

## State boundaries

### Agent Role state

Persistent identity, authority references, approved Workflow information, relationship branches, agreements, capability status, disputes, and authorized evidence required for continuity.

### Live Agent state

Ephemeral reasoning/context. It is not the trust root, relationship record, source of authority, signing boundary, or durable history.

### Local Role Record state

Each party's own state, including private evidence, local observations, exact copies of shared artifacts, receipts, and relationship-local transitions.

### Distributed relationship evidence

A logical intersection assembled only from source-attributed relationship-bearing material. It does not imply that all private Role Record contents are shared.

The minimum model distinguishes:

- exact shared object;
- visible attestation/pointer to private or external evidence;
- opaque commitment block whose contents are not yet collectively inspectable;
- private local evidence outside the shared relationship state.

## Critical semantic separations

The case treats the following as executable non-implication rules:

```text
discovery != authorization
authentication / identity != authority
relationship recognition != agreement
relationship != delegation
agreement != capability
capability != legitimate authority
valid delegation != policy authorization
valid signature != legitimate action
task conformance != profile conformance
profile conformance != instance legitimacy
execution success != legitimate effect
evidence != authority
assurance != retroactive authorization
local observation != shared relationship state
delivery / copy / decryption != inspection
inspection != acceptance / agreement / truth
record link != traversal / disclosure / authority
current key or identity state != historical authority
agreement closure != automatic closure of every larger relationship
```

A later implementation must turn each materially applicable distinction into a positive or falsification test. Documentation alone does not satisfy the gate.

## Decision boundaries

The slice must keep three authorization decisions separately observable:

1. **Workflow authorization** — may the deterministic Workflow construct/submit this exact operation under current authority, agreement, policy, duties, state, and evidence?
2. **Protected-signing authorization** — may the protected signer exercise the requested signing identity for this exact admitted object/context?
3. **Counterparty verification** — will the receiver independently accept the signed task as current, authorized, conformant, and compatible with its own policy/relationship state?

A fourth boundary, **execution admission**, must correlate the accepted request to the actual actuator effect.

## Outcome vocabulary

The minimum slice uses explicit outcomes rather than a generic boolean:

- `allowed`;
- `denied`;
- `escalated`;
- `indeterminate`;
- `unsupported`;
- `invalid`;
- `expired`;
- `replayed`;
- `stale-state`;
- `revoked`;
- `disputed`;
- `remediated`;
- `closed`.

`indeterminate` means evidence is insufficient. It MUST NOT be converted into PASS merely to keep a workflow green.

## Initial vector families

The canonical vector inventory is machine-readable in [`vectors.yaml`](vectors.yaml). The initial families are:

- legitimate end-to-end positive action;
- identity without authority;
- agreement without capability;
- capability after authority revocation;
- valid signature over illegitimate action;
- direct Live Agent signing attempt;
- stale Role Record head;
- unilateral local annotation presented as shared state;
- inspection represented as acceptance;
- record link used as traversal/authority permission;
- actuator effect not correlated to admitted decision;
- Live Agent replacement continuity;
- correction/remediation without history rewrite.

## Evidence model

Each executable vector should ultimately preserve, where applicable:

- input fixture identifiers and content hashes;
- Agent Role and relationship identifiers;
- exact Agreement Object/version;
- authority/delegation evidence references;
- applicable Role Record head(s);
- Workflow identifier/version;
- Policy Gate decision and reasons;
- exact Trust Task identifier/version and instance;
- capability identifier/scope/status;
- protected-signing request/result and cryptographic-use receipt;
- serialized transport artifact;
- receiver verification result;
- actuator admission and actual effect;
- local Role Record transitions;
- shared inspection/acknowledgment/disposition receipts;
- relationship checkpoint/evidence package;
- challenge/remediation/closure effects;
- Relationship View source references.

Evidence proves only the claims its generating boundary owns. For example, an execution receipt does not become authority and an assurance result does not retroactively authorize a denied action.

## Promotion model

[`promotion-gates.yaml`](promotion-gates.yaml) defines twelve evidence gates. At this foundation stage only the semantic-ownership/design gate may become satisfied. All implementation gates remain `not-started` until executable evidence exists.

A green repository build is necessary but not sufficient for promotion.

## Planned implementation route

The parent program decomposes implementation into issues #34–#43:

- #34 — pin baselines and map reuse;
- #35 — persistent Role Record/state engine;
- #36 — Agreement Object, Policy Gate, Trust Task, capability, execution admission;
- #37 — protected-signing boundary;
- #38 — two independent Agent Roles/processes and receiver verification;
- #39 — distributed VRR/shared-state evidence;
- #40 — continuity, challenge, correction, remediation, revocation, closure;
- #41 — Authorized Relationship Views;
- #42 — adversarial assurance, RAHP, maturity review;
- #43 — standards-native substitution.

## Pre-admission boundary

This case MUST NOT be added to `catalog/interoperability-cases.yaml` merely because the foundation artifacts exist.

Formal admission requires at least:

- exact baselines and mapping status;
- executable Role Record/state behavior;
- deterministic Policy Gate/task/capability path;
- protected-signing evidence;
- independent sender/receiver execution boundary;
- distributed relationship-state evidence;
- deterministic positive/negative/adversarial results;
- explicit limitations and claim boundary;
- evidence-backed human admission decision.

Until then, `IC-ARA-REL-001` is a pre-admission experimental construction.

## Judgment to preserve

The first merged increment should make one architectural judgment durable:

> **ARA implementation begins as a falsifiable Lab composition with explicit semantic boundaries and adapter substitution points, not as a prematurely normative standalone stack.**
