# ARA minimum executable relationship — implementation architecture

> **Historical design snapshot.** This document records the implementation shape selected before runtime code was introduced. The programme is now complete and admitted at bounded `interoperability-tested` maturity. For the current experiment narrative and actual architecture→code mapping, start with [README.md](README.md), [FOLLOW-ALONG.md](FOLLOW-ALONG.md), and [architecture-to-code.yaml](architecture-to-code.yaml).

This document records the implementation shape selected for `IC-ARA-REL-001` before runtime code is introduced.

## Architectural decision

Use an **adapter-backed executable vertical slice** inside the Trust Protocol Interop Lab.

The case will make relationship semantics, state transitions, decision boundaries, and evidence contracts concrete first. Standards-native implementations are substituted later one boundary at a time, using the same invariant suite.

This choice is intentionally reversible. The Lab can later extract a reusable component if execution demonstrates an independently useful API/lifecycle; no such repository boundary is assumed now.

## Component envelope

```text
+----------------------------- Agent Role A ------------------------------+
|                                                                         |
|  Live Agent A                                                           |
|      | proposal media                                                   |
|      v                                                                  |
|  deterministic Workflow / Policy Gate                                   |
|      | decision + exact action request                                  |
|      v                                                                  |
|  capability service -----> execution admission                          |
|      |                                                                  |
|      +----------> protected signer adapter                              |
|                         | signed exact task                             |
|                         v                                               |
|                    transport adapter --------------------+              |
|                                                         |              |
|  Role Record A <---- decisions / receipts / evidence    |              |
+---------------------------------------------------------|--------------+
                                                          |
                                                          v
+----------------------------- Agent Role B ------------------------------+
|  transport receiver                                                      |
|      | serialized signed request                                          |
|      v                                                                    |
|  independent verifier / deterministic Workflow                            |
|      | receiver decision                                                   |
|      v                                                                    |
|  capability-bounded synthetic query actuator                              |
|      | process/effect evidence                                             |
|      v                                                                    |
|  Role Record B                                                            |
+---------------------------------------------------------------------------+

      RR-A relationship material  <---- verifiable intersection ----> RR-B
                                  distributed VRR
                                           |
                                           v
                                 Authorized Relationship View
```

## Mandatory ports

The first executable implementation should code against explicit ports rather than hard-wire one upstream implementation.

### `RoleRecordStore`

Responsibilities:

- append state transition against exact previous head;
- return current defensible head;
- retrieve relationship-scoped authorized context;
- reconstruct history;
- preserve private/shared evidence classifications;
- reject stale, replayed, rollback, or conflicting transitions within the Lab model.

Must not decide:

- whether a relationship action is legitimate;
- whether a counterparty accepts evidence;
- whether shared evidence is true.

### `AuthorityResolver`

Responsibilities:

- resolve attributable authority/delegation evidence for the exact action context;
- return evidence state and scope rather than a blanket `allow`.

Must not decide:

- policy authorization;
- capability issuance;
- execution admission.

### `AgreementStore`

Responsibilities:

- preserve immutable/versioned Agreement Objects;
- expose exact proposal/acceptance/activation status;
- preserve amendment/supersession lineage used by the bounded case.

Must not create:

- authority;
- capability;
- shared relationship state merely because an agreement object exists locally.

### `PolicyGate`

Inputs should include:

- Agent Role;
- current Role Record head;
- relationship state;
- exact Agreement Object/version;
- authority/delegation evidence;
- policy/duty bundle version;
- proposed operation;
- recipient;
- purpose;
- required evidence/freshness.

Output vocabulary:

- `allowed`;
- `denied`;
- `escalated`;
- `indeterminate`.

The decision artifact should identify all material input references and reasons.

### `TrustTaskFactory`

Responsibilities:

- construct one exact supported task/action representation from an `allowed` decision;
- bind task identifier/version, relationship, agreement, authority decision, Role Record head, recipient, purpose, payload digest, nonce, expiry, and expected evidence.

It must not accept arbitrary free-form Live Agent output as an operative signed payload.

### `CapabilityService`

Responsibilities:

- derive least-privilege capability only after required authorization;
- bind it to relationship/agreement/action/purpose/resource/duration;
- support attenuation, suspension, expiry, and revocation;
- expose status to execution admission.

Capability possession must not itself answer whether the operation remains legitimate.

### `ProtectedSigner`

Responsibilities:

- accept only canonical signed-action requests from authenticated deterministic Workflows;
- verify current state/context binding;
- deny arbitrary bytes, direct Live Agent calls, substitution, replay, stale state, and revoked authority;
- emit cryptographic-use receipt.

Initial implementation class: **Lab adapter**.

Substitution target: pinned VTA/OpenVTC or another implementation only after exact semantics and guarantees are mapped.

### `RelationshipTransport`

Responsibilities:

- carry serialized signed request/response/evidence across an independently controlled process boundary;
- preserve payload bytes and observable metadata for evidence capture.

Initial implementation class: **Lab adapter**.

Substitution target: TSP/TEA integration in phase 11.

Transport success must not imply task acceptance or relationship legitimacy.

### `CounterpartyVerifier`

Responsibilities:

- independently verify sender identity/control evidence, exact task, signature, authority reference, agreement/relationship state, freshness/replay, and receiver-local policy;
- emit its own decision artifact.

It must not trust the sender's private Policy Gate conclusion as sufficient evidence.

### `ExecutionBroker`

Responsibilities:

- admit only capability-bounded operations that correlate to the exact receiver-accepted task;
- capture actual effect;
- reject unrelated or broader actuator calls;
- emit effect evidence.

### `RelationshipEvidenceStore`

Responsibilities:

- classify exact shared objects, visible attestations/pointers, opaque commitments, and private local evidence;
- bind receipts to exact content identifiers;
- keep semantic disposition independent of inspection;
- construct/cross-anchor the bounded relationship checkpoint;
- preserve disagreement and corrections without overwrite.

Must not become a central master dossier.

### `RelationshipViewBuilder`

Responsibilities:

- generate an authorized rendering/proof package from attributable source evidence;
- expose material uncertainty and dependencies;
- enforce no automatic record/link traversal;
- keep view assertions traceable to source evidence.

Must not become authority.

## Initial object contracts

The exact schemas will be introduced by the implementation issues, but the following minimum identifiers should remain stable across the walking skeleton:

```text
agent_role_id
relationship_id
role_record_head
agreement_id + agreement_version
authority_evidence_id
policy_decision_id
trust_task_type + trust_task_version + task_instance_id
capability_id
signed_action_id
sender_verification_state
receiver_decision_id
execution_effect_id
content_id
receipt_id
relationship_checkpoint_id
challenge_or_remediation_id
relationship_view_id
```

Every consequential artifact should carry enough correlation references to reconstruct the decision/effect chain without requiring model traces.

## Trust boundary matrix

| Boundary | Accepts | Refuses to infer |
|---|---|---|
| Identity/control | attributable signer/role control evidence | action authority |
| Authority resolver | scoped authority evidence | policy `allow` |
| Policy Gate | current relationship/governance conjunction | signing or receiver acceptance |
| Protected signer | exact admitted cryptographic-use request | instance legitimacy from key possession |
| Transport | bytes between endpoints | substantive relationship |
| Receiver verifier | independently verified current request | sender-local decision as authority |
| Execution broker | accepted exact capability/action | legitimacy from actuator success |
| Role Record | attributable local state/evidence | mutual/shared status |
| VRR evidence | exact shared/receipt/checkpoint proofs | truth or universal agreement |
| Relationship View | authorized rendering of source evidence | new authority or hidden certainty |
| Assurance | later bounded evaluation | retroactive authorization |

## Failure classification

The implementation should not collapse failures into `invalid` when the boundary is knowable. Prefer classes such as:

- identity/control failure;
- authority insufficiency;
- policy denial;
- policy indeterminate;
- agreement inactive/mismatch;
- task structural/version failure;
- stale relationship state;
- protected-signing refusal;
- receiver-verification refusal;
- capability denial/revocation;
- execution-correlation failure;
- relationship-evidence inconsistency;
- privacy/authorization-view violation;
- assurance insufficiency.

This makes architectural falsification observable.

## Standards-native substitution rule

An adapter can be replaced only through a PR that records:

1. exact pinned source/implementation baseline;
2. adapter contract being replaced;
3. semantic ownership mapping;
4. before/after positive and falsification results;
5. changed observable/privacy surfaces;
6. missing guarantees or semantic mismatch;
7. claim boundary.

The same invariant suite remains authoritative for the Lab case after substitution.

## Extraction rule

Do not create a new ARA implementation repository merely because a local module becomes non-trivial.

Candidate extraction requires observed evidence of:

- independently reusable API;
- more than one consumer or credible reuse context;
- lifecycle/versioning needs distinct from the Lab case;
- clear semantic ownership;
- test/evidence obligations that make sense outside the case;
- maintainer decision recorded in the judgment trail.
