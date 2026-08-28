# Following the Agent Relationship Architecture into the executable Lab

This guide is for a reader who has the July 2026 revised Agent Relationship Architecture proposal open and wants to see where its architectural ideas were exercised in code.

The proposal itself is not committed to this repository. The repository therefore does not claim to be a normative copy of that document. Instead, `IC-ARA-REL-001` is an executable companion: it identifies a bounded proposition, maps architecture concepts to implementation boundaries, pressure-tests those boundaries, and records what remains adapter-backed or unresolved.

## 1. Start with the architectural proposition, not the code

Read the case [README](README.md) and [final claim boundary](final-claim-boundary.md) first.

The experiment is not "an implementation of every ARA feature." It is a minimum relationship slice designed to falsify the proposition that consequential action legitimacy is conjunctive across identity, authority, agreement, policy, capability, task, signing, current state, counterparty verification and evidence.

The synthetic relationship is:

```text
Data-owner Agent Role A
        |
        | permits one query-only action
        v
Research Agent Role B
```

The dataset is synthetic and the action is deliberately narrow so failures can be attributed to architectural boundaries rather than domain complexity.

## 2. Persistent Agent Role and Role Record

**Architecture idea:** an Agent Role persists beyond one Live Agent process and has durable relationship state.

Read:

- `experiments/ara-role-record/README.md`
- `experiments/ara-role-record/engine.py`
- `cases/ara-minimum-executable-relationship/phase3-role-record-judgment.md`

Run:

```bash
python experiments/ara-role-record/run.py --check
```

Look for:

- current-head binding;
- stale/rollback/fork refusal;
- append-only correction;
- history reconstruction;
- replacement of the in-memory engine/Live Agent without importing hidden conversation memory.

**Boundary preserved:** historical valid state is not necessarily current defensible state.

## 3. Agreement, authority, policy, capability and exact task

**Architecture idea:** identity, agreement, authority, policy authorization, technical capability and task semantics are different things.

Read:

- `experiments/ara-policy-spine/README.md`
- `experiments/ara-policy-spine/authorization.py`
- `cases/ara-minimum-executable-relationship/phase4-policy-spine-judgment.md`

Run:

```bash
python experiments/ara-policy-spine/run.py --check
```

Look for the separate classes:

- `AgreementLedger`;
- `PolicyGate`;
- `CapabilityService`;
- `TrustTaskBuilder`;
- `ExecutionAdmitter`.

Key attacks include identity without authority, inactive agreement, missing/revoked/wrong capability, unsupported task version, missing required evidence, stale Role Record head and uncorrelated effects.

**Boundary preserved:** no single persuasive artifact confers relationship legitimacy.

## 4. Protected cryptographic use

**Architecture idea:** possessing or reaching a key is not the same as being authorized to use it.

Read:

- `experiments/ara-protected-signing/README.md`
- `experiments/ara-protected-signing/signer.py`
- `cases/ara-minimum-executable-relationship/phase5-protected-signing-judgment.md`

Run:

```bash
python experiments/ara-protected-signing/run.py --check
```

The Lab signer has no unrestricted `sign(bytes)` path. It binds cryptographic use to the exact admitted relationship context and emits a cryptographic-use receipt.

The HMAC operation is deliberately only a Lab stand-in. It does not claim VTA/HSM/TEE conformance.

## 5. Independent counterparty

**Architecture idea:** an independently controlled counterparty must be able to disagree.

Read:

- `experiments/ara-independent-counterparty/README.md`
- `experiments/ara-independent-counterparty/sender.py`
- `experiments/ara-independent-counterparty/receiver.py`
- `cases/ara-minimum-executable-relationship/phase6-independent-counterparty-judgment.md`

Run:

```bash
python experiments/ara-independent-counterparty/run.py --check
```

The sender and receiver are separate Python processes exchanging serialized JSON. The receiver has its own relationship state, policy and replay state.

The important vector is not simply a successful exchange. It is:

```text
sender says allow
receiver independently says deny
```

**Boundary preserved:** transport delivery and sender admission do not compel receiver acceptance.

## 6. Distributed Verifiable Relationship Record semantics

**Architecture idea:** a relationship is not a central master dossier and local knowledge is not automatically shared knowledge.

Read:

- `experiments/ara-distributed-vrr/README.md`
- `experiments/ara-distributed-vrr/vrr.py`
- `cases/ara-minimum-executable-relationship/phase7-distributed-vrr-judgment.md`

Run:

```bash
python experiments/ara-distributed-vrr/run.py --check
```

Inspect the evidence classes:

- shared object;
- source pointer;
- opaque commitment;
- private Role evidence.

Also inspect the difference between procedural receipt stages and semantic dispositions.

**Boundary preserved:** delivery, decryption, inspection and acceptance are not synonyms.

## 7. Live Agent replacement and adverse lifecycle

**Architecture idea:** the Agent Role and relationship must survive process replacement and failure without rewriting history or resurrecting stale authority.

Read:

- `experiments/ara-lifecycle-continuity/README.md`
- `experiments/ara-lifecycle-continuity/lifecycle.py`
- `cases/ara-minimum-executable-relationship/phase8-lifecycle-continuity-judgment.md`

Run:

```bash
python experiments/ara-lifecycle-continuity/run.py --check
```

Look for:

- reconstruction only from persisted state;
- challenge and dispute;
- correction without overwrite;
- capability revocation;
- remediation that does not resurrect the revoked capability;
- suspect-interval review before continuation;
- distinction between Agreement closure and relationship closure;
- historical validity surviving later revocation.

## 8. Authorized Relationship View

**Architecture idea:** a human or machine reviewer needs an explanation of legitimacy without unrestricted graph traversal or private-record disclosure.

Read:

- `experiments/ara-relationship-view/README.md`
- `experiments/ara-relationship-view/view.py`
- `cases/ara-minimum-executable-relationship/phase9-relationship-view-judgment.md`

Run:

```bash
python experiments/ara-relationship-view/run.py --check
```

Material assertions carry evidence references and explicit status such as:

- verified;
- historical;
- disputed;
- restricted;
- indeterminate;
- reported.

**Boundary preserved:** the view explains authority/evidence; it does not create authority.

## 9. Adversarial assurance and false independence

**Architecture idea:** assurance must pressure the interpretation of evidence as well as the mechanism that produced it.

Read:

- `experiments/ara-adversarial-assurance/README.md`
- `experiments/ara-adversarial-assurance/assurance.py`
- `cases/ara-minimum-executable-relationship/phase10-rahp-pressure-review.md`

Run:

```bash
python experiments/ara-adversarial-assurance/run.py --check
```

The assurance harness reruns the executable phases and adds meta-level attacks:

- missing evidence cannot become PASS;
- assurance cannot create authority;
- later assurance cannot retroactively authorize a refused action;
- unilateral state cannot become collective state;
- recovery cannot move beyond the last defensible checkpoint;
- artifact count cannot be treated as evidence independence.

Three attestations under one control lineage count as one support group in the bounded model.

## 10. Standards-native substitution boundary

**Architecture idea:** independently governed specifications/components should replace Lab adapters only when the exact contract has actually been executed.

Read:

- `experiments/ara-standards-boundary/README.md`
- `cases/ara-minimum-executable-relationship/phase11-standards-substitution-disposition.md`
- `cases/ara-minimum-executable-relationship/phase11-standards-boundary-judgment.md`

Run:

```bash
python experiments/ara-standards-boundary/run.py --check
```

The result intentionally includes residual adapters.

A real OpenVTC implementation exists, but the experiment does not relabel the Lab signer as VTA-conformant because the exact ARA context contract has not been executed through that API.

## 11. Final admission

Read:

- `cases/ara-minimum-executable-relationship/final-claim-boundary.md`
- `cases/ara-minimum-executable-relationship/promotion-gates.yaml`
- `evidence/ara-minimum-executable-relationship/evidence-manifest.json`
- `experiments/ara-program-admission/README.md`

Run:

```bash
python experiments/ara-program-admission/run.py --check
```

The final runner verifies that the evidence-gated programme state and catalog admission agree. It does not itself create the human admission decision; PR #57 records that judgment.

## 12. Use the machine-readable crosswalk

`architecture-to-code.yaml` is designed for tooling and maintenance. Each row names:

- an architecture concept;
- the semantic claim being exercised;
- implementation files;
- executable runner;
- judgment/evidence documents;
- substitution status;
- claim boundary.

The CI documentation-foundation check verifies that mapped artifacts continue to exist and that the landing page does not regress to the old pre-admission status.

## 13. How to extend the architecture responsibly

When substituting a real standard/native implementation or adding a new ARA ceremony:

1. identify the architecture concept and owning semantic boundary;
2. add or update the architecture-to-code map;
3. preserve the existing negative non-implication tests;
4. substitute only one responsibility at a time;
5. rerun the affected phase plus adversarial assurance;
6. record changed observables and failure modes;
7. do not broaden conformance or security claims merely because the replacement is real;
8. update the final claim boundary only if new evidence genuinely changes it.

The experiment is valuable as a foundation precisely because the code is organized around **claims and refusal boundaries**, not around one monolithic ARA runtime.
