# IC-ARA-REL-001 — Minimum Executable Agent Relationship Architecture

> **Current status: Interoperability Tested**
>
> **Admitted claim:** bounded executable semantic composition, adapter-backed at declared boundaries, with adversarial evidence and explicit standards/conformance exclusions.
>
> This repository is the executable companion to the **July 2026 revised Agent Relationship Architecture (ARA) proposal** used to start programme issue [#32](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/32). The source architecture document itself is not stored in this repository. This directory shows how its principal architectural claims were turned into a staged, falsifiable Interop Lab experiment.

Final admission: [#32](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/32) / [PR #57](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/pull/57)  
Follow-along guide: [FOLLOW-ALONG.md](FOLLOW-ALONG.md)  
Architecture-to-code map: [architecture-to-code.yaml](architecture-to-code.yaml)  
Final claim boundary: [final-claim-boundary.md](final-claim-boundary.md)  
Evidence manifest: [../../evidence/ara-minimum-executable-relationship/evidence-manifest.json](../../evidence/ara-minimum-executable-relationship/evidence-manifest.json)

## At a glance

| Item | Current state |
|---|---|
| **Status** | Interoperability Tested |
| **Purpose** | Determine whether a persistent agent relationship can support one consequential action only when identity, authority, agreement, policy, capability, exact task semantics, protected cryptographic use, counterparty decision, relationship state, and effect evidence all align. |
| **Current conclusion** | The bounded architecture survived the complete staged programme and adversarial pressure. It is executable and evidence-backed at the declared semantic boundaries, while several runtime integrations remain adapter-backed rather than standards-native. |
| **Evidence today** | Ten executable programme phases, lifecycle and counterparty evidence, adversarial assurance, standards-boundary review, a final evidence manifest, and an explicit claim boundary. |

## Why this matters to a new reader

Most agent systems are good at proving one fact at a time: an agent authenticated, a signature verified, a capability existed, a task completed, or a receipt was produced. This case asks the harder systems question: **can a persistent relationship remain legitimate when all of those facts must agree and when the relationship changes over time?**

It also tests whether an ephemeral Live Agent can be replaced without losing the durable authority and relationship state required to explain what happened later.

## Concrete scenario

Two persistent Agent Roles participate in one tightly bounded research-data interaction. The data-owner role controls a protected dataset; the research role requests one query-only operation. A temporary Live Agent may propose the action, but it cannot directly sign or actuate.

Execution occurs only after agreement, current authority, deterministic policy, scoped capability, exact Trust Task semantics, protected signing, receiver-side verification, and current relationship state all concur. The resulting evidence must remain defensible through disagreement, replacement, challenge, correction, remediation, continuation, and closure.

## Where it resolved

This case completed its programme and was admitted as **Interoperability Tested** for a bounded executable semantic composition. The most important result is not a single happy-path transaction; it is the demonstrated preservation of non-substitution boundaries such as identity ≠ authority, capability ≠ legitimate authority, sender allow ≠ receiver allow, execution success ≠ legitimate effect, and assurance ≠ retroactive authorization.

The remaining boundary is explicit: this does not claim TSP wire-protocol conformance, OpenVTC VTA production security, legal effect, external certification, or standards-native replacement of every local adapter.


## What remains unresolved

The admitted claim remains bounded. TSP wire-protocol substitution, OpenVTC VTA production key protection, legal effect, external certification, arbitrary multi-party/quorum relationships, and standards-native replacement of every residual adapter remain outside the current evidence.

## What was tested

The experiment asks whether two independently controlled persistent Agent Roles can perform one consequential bounded action **only when** all of the following align:

- identity/authentication;
- current authority;
- an exact governing agreement;
- deterministic policy authorization;
- a least-privilege capability;
- exact Trust Task semantics;
- protected cryptographic-use context;
- current persistent relationship state;
- independent counterparty verification;
- execution/effect correlation;
- sufficient attributable evidence.

It also asks whether the relationship can remain defensible through:

- counterparty disagreement;
- Live Agent replacement;
- challenge and correction;
- remediation and capability revocation;
- explicit continuation or closure;
- human/machine explanation through an Authorized Relationship View;
- adversarial assurance, including false-independence pressure.

The proposition is deliberately conjunctive. A valid identity, agreement, capability, signature, task, receipt, or assurance result cannot silently substitute for another required boundary.

## The bounded scenario

The synthetic case uses two persistent Agent Roles:

- **A — Data-owner Agent Role** controls a synthetic protected dataset.
- **B — Research Agent Role** requests one query-only operation.

The permitted action is intentionally narrow. Mutation and export are out of scope. This is not a normative research-data governance profile.

A temporary Live Agent may propose intent, but it cannot directly sign or actuate. The consequential path is:

```text
Live Agent proposal
      |
      v
persistent Agent Role + current Role Record
      |
      v
Agreement + authority + deterministic Policy Gate
      |
      v
scoped capability + exact Trust Task
      |
      v
protected cryptographic-use boundary
      |
      v
serialized transport across independent process boundary
      |
      v
counterparty-local verification and policy
      |
      v
execution admission + correlated effect evidence
      |
      v
independent Role Records + distributed relationship evidence
      |
      v
challenge / correction / remediation / continuation / closure
      |
      v
Authorized Relationship View + adversarial assurance
```

## The most important architectural separations

The implementation exists primarily to make these distinctions executable:

```text
discovery != authorization
authentication / identity != authority
relationship recognition != agreement
relationship != delegation
agreement != capability
capability != legitimate authority
valid delegation != policy authorization
valid signature != legitimate action
task conformance != instance legitimacy
sender allow != receiver allow
transport delivery != receiver acceptance
execution success != legitimate effect
evidence != authority
assurance != retroactive authorization
local observation != shared relationship state
delivery / copy / decryption != inspection
inspection != acceptance / agreement / truth
record link != traversal / disclosure / authority
current key or identity state != historical authority
artifact multiplicity != independent evidence
agreement closure != automatic relationship closure
Relationship View != authority
```

These are not only documentation statements. The applicable distinctions are exercised by positive, negative, boundary, or adversarial vectors in the phase runners.

## Follow the architecture into the implementation

If you are reading the ARA architecture proposal, use [architecture-to-code.yaml](architecture-to-code.yaml) as the machine-readable crosswalk or [FOLLOW-ALONG.md](FOLLOW-ALONG.md) as the human guide.

The implementation is intentionally split into independently inspectable boundaries:

| Architecture concept | Primary implementation | Executable evidence |
|---|---|---|
| Persistent Agent Role / Role Record | `experiments/ara-role-record/engine.py` | `python experiments/ara-role-record/run.py --check` |
| Agreement + policy + capability + task + execution admission | `experiments/ara-policy-spine/authorization.py` | `python experiments/ara-policy-spine/run.py --check` |
| Protected signing | `experiments/ara-protected-signing/signer.py` | `python experiments/ara-protected-signing/run.py --check` |
| Independent counterparty | `experiments/ara-independent-counterparty/sender.py`, `receiver.py` | `python experiments/ara-independent-counterparty/run.py --check` |
| Distributed relationship evidence / VRR semantics | `experiments/ara-distributed-vrr/vrr.py` | `python experiments/ara-distributed-vrr/run.py --check` |
| Replacement, challenge, remediation, revocation, closure | `experiments/ara-lifecycle-continuity/lifecycle.py` | `python experiments/ara-lifecycle-continuity/run.py --check` |
| Authorized Relationship View | `experiments/ara-relationship-view/view.py` | `python experiments/ara-relationship-view/run.py --check` |
| Adversarial / RAHP assurance | `experiments/ara-adversarial-assurance/assurance.py` | `python experiments/ara-adversarial-assurance/run.py --check` |
| Standards-native boundary review | `experiments/ara-standards-boundary/run.py` | `python experiments/ara-standards-boundary/run.py --check` |
| Final programme admission | `experiments/ara-program-admission/run.py` | `python experiments/ara-program-admission/run.py --check` |

## Implementation programme and what each phase established

The programme deliberately moved from architecture hypothesis to executable evidence one boundary at a time.

| Phase | Issue / PR | Question exercised | Result |
|---|---|---|---|
| Foundation | #33 / #44 | Can the proposal be reduced to falsifiable ownership boundaries, invariants, vectors and gates without premature admission? | Established executable-ready pre-admission case |
| Baselines / reuse | #34 / #45 | Which existing DTG/ToIP/Lab assets are direct reuse, composition dependencies, candidates or adapters? | Pinned baselines and explicit gap register |
| Role Record | #35 / #47 | Can persistent relationship state survive Live Agent replacement and reject stale/rollback/fork state? | Executable persistent state boundary |
| Authorization spine | #36 / #49 | Do Agreement, authority, policy, capability, exact task and execution admission remain separate? | Executable conjunctive authorization path |
| Protected signing | #37 / #50 | Can cryptographic use be non-bypassable and bound to exact admitted context? | Context-bound cryptographic-use receipts |
| Independent counterparty | #38 / #51 | Can the receiver decide independently across a real process/serialization boundary? | Sender allow no longer implies receiver allow |
| Distributed VRR | #39 / #52 | Can shared relationship evidence be reconstructed without a jointly writable master dossier? | Evidence intersection + explicit dispositions/checkpoints |
| Lifecycle continuity | #40 / #53 | Can the relationship survive replacement, challenge, correction, remediation, revocation and closure? | Temporal legitimacy and history preservation |
| Relationship View | #41 / #54 | Can an authorized reviewer understand the basis and uncertainty without unrestricted private access? | Source-traceable scoped explanation artifact |
| Adversarial assurance | #42 / #55 | Do accumulated claims survive semantic inflation, false independence and assurance overreach? | RAHP-style pressure review + evidence manifest |
| Standards boundary | #43 / #56 | Which adapters can actually be replaced or semantically bound without hidden glue? | Per-component standards disposition; residual adapters preserved |
| Final admission | #32 / #57 | Is the bounded claim sufficiently evidenced for catalog admission? | Admitted as `interoperability-tested` |

The phase judgment documents in this directory preserve alternatives considered, rejected approaches, residual uncertainty and the human acceptance boundary for each major step.

## Run the experiment

From the repository root with Python available:

```bash
python experiments/ara-role-record/run.py --check
python experiments/ara-policy-spine/run.py --check
python experiments/ara-protected-signing/run.py --check
python experiments/ara-independent-counterparty/run.py --check
python experiments/ara-distributed-vrr/run.py --check
python experiments/ara-lifecycle-continuity/run.py --check
python experiments/ara-relationship-view/run.py --check
python experiments/ara-adversarial-assurance/run.py --check
python experiments/ara-standards-boundary/run.py --check
python experiments/ara-program-admission/run.py --check
```

The final admission runner rechecks the high-level evidence gates and catalog state. The adversarial runner reruns the executable ARA phase stack and adds assurance-boundary pressure.

Repository Assurance also executes these checks in CI.

## What to inspect when a test passes

A green exit code is not the whole evidence story. For each phase, inspect:

1. the phase `README.md`;
2. the implementation module;
3. the `run.py` vectors and expected refusal codes;
4. the corresponding `phase*-judgment.md`;
5. the final [evidence manifest](../../evidence/ara-minimum-executable-relationship/evidence-manifest.json);
6. the [promotion gates](promotion-gates.yaml);
7. the [final claim boundary](final-claim-boundary.md).

The phase runners emit deterministic JSON when run normally and can be inspected directly. Several also accept an output path for persisted evidence.

## Evidence and state model

The experiment keeps several kinds of state/evidence deliberately separate:

- **Live Agent state** — ephemeral reasoning/context; never the durable authority or trust root.
- **Role Record state** — persistent relationship-local state controlled by each Agent Role.
- **Agreement state** — immutable/versioned governing terms and lifecycle.
- **Policy decision** — deterministic allow/deny/escalate/indeterminate result.
- **Capability state** — derived technical permission with scope, expiry and revocation.
- **Task state** — exact operation semantics and instance bindings.
- **Cryptographic-use evidence** — proof that the protected-use boundary exercised technical power for the admitted context.
- **Counterparty decision** — independent recipient-side judgment.
- **Execution/effect evidence** — correlated outcome of the exact admitted operation.
- **Distributed relationship evidence** — exact shared objects, pointers, commitments, receipts, dispositions and checkpoints.
- **Relationship View** — derived explanation; never a new source of authority.
- **Assurance evidence** — evidence about the claim; never retroactive authorization.

## Distributed relationship evidence: what "shared" means

The Phase 7 model deliberately rejects a central master relationship dossier.

It distinguishes:

- `shared_object` — exact content is relationship-shareable;
- `source_pointer` — attributable reference without automatic traversal;
- `opaque_commitment` — commitment exists but hidden content is not collectively known;
- `private_role_evidence` — local evidence excluded from shared exports/checkpoints.

Receipt stages and semantic dispositions also remain distinct. Delivery, decryption or inspection never automatically mean acceptance.

## Adversarial assurance

Phase 10 pressures not only mechanisms but **interpretation of evidence**.

Examples:

- missing required evidence becomes `INDETERMINATE`, not PASS;
- assurance cannot create authority;
- later assurance cannot retroactively authorize an originally refused action;
- one party's state cannot masquerade as collective state;
- disagreement remains visible;
- recovery cannot outrun the last defensible checkpoint;
- multiple artifacts under one control/source lineage do not count as independent support merely by number.

See [phase10-rahp-pressure-review.md](phase10-rahp-pressure-review.md).

## Standards-native result

Phase 11 intentionally distinguishes three outcomes:

1. **implementation substitution** — an independently governed implementation actually replaces the Lab adapter in the executed path;
2. **normative semantic binding** — a pinned specification owns the relevant semantics, but no runtime replacement occurred;
3. **residual adapter** — the local test double remains because exact executable substitution evidence is absent.

The final result did **not** force standards substitutions for appearances.

- Trust Tasks: normative semantic binding.
- RCard: normative semantic binding.
- VRC: normative semantic binding.
- TSP transport: residual adapter.
- OpenVTC VTA protected signer: residual adapter.

See [phase11-standards-substitution-disposition.md](phase11-standards-substitution-disposition.md).

## Final claim

The admitted maturity statement is:

> **Interoperability Tested — bounded executable semantic composition, adapter-backed at declared boundaries, with adversarial evidence and explicit standards/conformance exclusions.**

This means the Lab has reproducible evidence for the bounded ARA composition semantics described above.

It does **not** establish:

- TSP wire-protocol conformance;
- OpenVTC VTA conformance or hardware-backed key protection;
- normative RCard/VRC runtime conformance;
- production deployment security;
- external certification or independent audit;
- legal effect of authority, agreement, remediation or closure;
- arbitrary multi-party/quorum ARA semantics;
- proof that distinct evidence lineages are economically or organizationally independent;
- universal ToIP ARA profile conformance;
- standards-native replacement of every local adapter.

See [final-claim-boundary.md](final-claim-boundary.md) for the authoritative statement.

## Historical context: how this began

The foundation version of this README correctly described the case as **pre-admission** and the later phases as planned work. That historical posture remains visible in the Issue → PR → merge trail beginning with #33 / #44 and in [judgment-log.md](judgment-log.md).

The current landing page intentionally reports the **final programme state** instead of retaining stale pre-admission language. This is not a rewrite of the judgment history; it is a separation between:

- the initial hypothesis and implementation plan; and
- the final evidence-backed disposition.

## Extending the experiment

New work should preserve the same rule used throughout the programme:

> Do not broaden a claim merely because a nearby standard, implementation, signature, credential, receipt, or green workflow appears persuasive.

Likely follow-on experiments include:

- real TSP endpoint substitution;
- exact OpenVTC VTA protected-use mapping;
- executable RCard/VRC providers;
- an upstream ARA-specific Trust Task profile if warranted;
- richer evidence-lineage independence provenance;
- multi-party/quorum relationship semantics;
- production persistence/recovery/key-management controls;
- human-factors testing of Relationship Views.

The architecture-to-code map and documentation-foundation check are intended to keep those future additions traceable to the architecture rather than accumulating as disconnected features.
