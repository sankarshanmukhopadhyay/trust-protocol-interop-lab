# ARA Role Record executable evidence

This experiment implements the Phase 3 state substrate for `IC-ARA-REL-001` under issue #35.

## Proposition

> Can an Agent Role preserve authoritative local relationship state across Live Agent replacement while rejecting stale, rolled-back, conflicting, replayed, tampered, or unauthorized state transitions?

## What is implemented

`engine.py` provides a deliberately small Lab-local `RoleRecordStore` for one persistent Agent Role. Each relationship has an independent local branch consisting of canonical JSON events whose identifiers are SHA-256 digests over the complete transition content. Every non-genesis event binds the exact prior head. The store maintains the current head separately and reconstructs current state by replaying accepted events.

The engine separates the persistent Agent Role identifier from the disposable Live Agent/session identity. The positive continuity vector destroys the first in-memory engine, reconstructs a new instance from disk, and continues only when the required context exists in the persisted Role Record. A second vector attempts to require an unpersisted `conversation_secret` and is refused as `missing_persisted_context`.

Each event carries one evidence visibility class: `private`, `shared`, `pointer`, or `commitment`. Phase 3 proves the state engine can preserve those classifications; it does **not** yet implement the distributed VRR semantics that determine what counterparties can prove was mutually inspected or accepted.

Every accepted or refused transition emits a deterministic receipt containing the transition id, Agent Role, relationship, actor, Workflow, transition class, prior head, resulting/current head, sequence, timestamp, result, and refusal code.

## Executable vectors

Run:

```bash
python experiments/ara-role-record/run.py --check
```

The suite covers:

- create relationship-local state;
- append an authorized shared-evidence transition;
- replace the Live Agent/engine and continue from persisted state only;
- unauthorized updater refusal;
- missing previous-head refusal;
- stale-head/rollback refusal;
- replay refusal;
- incompatible successor/fork refusal;
- hidden prior-session dependency refusal;
- correction by append;
- complete history reconstruction;
- accepted-event mutation detection;
- accepted-event deletion detection;
- persisted current-head rollback detection.

`--output <path>` writes the same deterministic machine-readable JSON evidence to a file.

## State and refusal semantics

The experiment intentionally treats a valid old head as insufficient for a new transition. A caller must bind to the current defensible head. A known but non-current head returns `rollback_or_stale_head`; when a vector explicitly presents an incompatible alternate successor it returns `competing_successor_head`. A persisted current-head pointer that has been rolled back independently of the event chain is detected during history validation as `current_head_mismatch`.

Corrections are new events. The earlier bytes remain in the chain. Logical state may be superseded by a correction event, but accepted historical evidence is never silently rewritten.

## Claim boundary

This experiment is **evidence for bounded ARA state semantics only**. It does not claim:

- KERI conformance;
- BetterSign conformance;
- OpenVTC VTA protected-state conformance;
- transparency-log inclusion or consistency guarantees;
- hardware-backed key/state protection;
- distributed consensus;
- Byzantine fork detection beyond the local evidence model;
- production anti-rollback guarantees;
- production storage security.

The `fork_candidate` marker used by one test is a Lab test-harness signal for classifying an explicitly incompatible successor attempt. It is not proposed as an ARA wire or storage field.

## Judgment preserved

The minimum authoritative substrate is not model conversation memory. It is a persistent, independently verifiable relationship-local state chain whose current head, update authority, transition class, evidence classification, and historical bytes remain inspectable. A cryptographically valid earlier state is still insufficient when it is no longer the current defensible head.
