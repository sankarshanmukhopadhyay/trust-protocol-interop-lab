# IC-ARA-REL-001 Phase 3 — Role Record judgment

Issue: #35

## Proposition tested

Can a persistent Agent Role preserve authoritative local relationship state across Live Agent replacement while rejecting stale, rolled-back, replayed, conflicting, tampered, deleted, or unauthorized state transitions?

## Decision

Use a deliberately small Lab-local hash-linked Role Record state engine before importing Agreement Objects, protected signing, TSP, RCard/VRC, or distributed VRR semantics.

The minimum authoritative substrate is a persistent Agent Role identifier plus independently reconstructable relationship-local events. Every accepted non-genesis event binds the exact current predecessor head and an authorized Workflow/transition class. The current head is separately validated against the reconstructed chain.

## Alternatives actually considered

1. Store only the current state snapshot.
2. Use an append-only event list without content hashes.
3. Integrate KERI/BetterSign/VTA immediately as the persistence substrate.
4. Implement a Lab-local hash-linked chain with explicit limitations, then substitute stronger identity/protected-state mechanisms later.

Selected: **4**.

A current-state snapshot cannot expose rollback or silent historical mutation. An unhashed event list cannot end-verify accepted bytes. Immediate standards-native integration would make a state-semantics failure difficult to distinguish from dependency/integration maturity. The selected mechanism is sufficient to falsify the Phase 3 claims while explicitly remaining local evidence rather than standards conformance.

## Acceptance boundary

The engine demonstrates:

- Agent Role identifier persistence independent of a Live Agent/session;
- relationship-local state branches;
- canonical content-derived event heads;
- exact previous-head binding;
- authorized update classes;
- deterministic accepted/refused transition receipts;
- current-head freshness enforcement;
- stale/rollback rejection;
- replay rejection;
- incompatible-successor/fork detection within the Lab model;
- private/shared/pointer/commitment classification support;
- replacement continuation from persisted state only;
- mutation/deletion/current-head rollback detection;
- corrections as appended evidence rather than historical overwrite.

It does **not** demonstrate KERI, BetterSign, OpenVTC VTA, transparency-log consistency, hardware anti-rollback, Byzantine consensus/fork resolution, or production persistence security.

## Pressure tests and falsifiers

The Phase 3 runner executes a legitimate create → advance → destroy/reload → continue path and requires all of the following unsafe alternatives to fail: unauthorized updater, missing predecessor, stale predecessor, replay, incompatible successor, hidden conversation/session dependency, accepted-event mutation, accepted-event deletion, and persisted current-head rollback.

The correction test adds a new correction event. It does not mutate the original bytes. This preserves the architecture's distinction between current interpretation/state and historical evidence.

## Changed or rejected conclusions

No evidence from Phase 3 justifies upgrading ARPA, KERI, BetterSign, VTA, or another upstream component into owner of the ARA Role Record. Phase 2's `adapter-only` classification for the complete ARA Role Record remains correct.

The experiment also rejects the tempting design that a cryptographically valid old state is sufficient. An old head can remain internally valid while being stale; therefore validity and current defensibility are separate checks.

## Residual uncertainty

The Lab mechanism does not decide the final cryptographic representation of a production Role Record, how historical Agent Role control is resolved across identifier methods, how externally witnessed anti-rollback is achieved, or how conflicting heads across independently observed infrastructures are reconciled. Those remain explicit later substitution/assurance questions.

## Human acceptance point

Merge of the Phase 3 PR is the maintainer acceptance that this bounded evidence is sufficient to satisfy `ARA-G3-ROLE-STATE-EXECUTABLE`; it is **not** acceptance of a production Role Record design or promotion of the overall ARA case beyond pre-admission.
