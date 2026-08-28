# ARA Phase 8 — lifecycle continuity, challenge, remediation, revocation and closure

This experiment is executable evidence for `IC-ARA-REL-001` issue #40.

## Proposition

Can a durable Agent Role and relationship survive Live Agent replacement and adverse events without relying on model memory, rewriting historical evidence, or leaving stale technical power active?

## Composition

Phase 8 reuses rather than replaces prior ownership boundaries:

- Phase 3 Role Record persists durable relationship state;
- Phase 4 Agreement and Capability components own agreement/capability lifecycle;
- Phase 7 distributed-VRR evidence owns dispute/correction history;
- a small `LifecycleCoordinator` checks cross-component resume/closure conditions.

No new master lifecycle database is introduced.

## Run

```bash
python experiments/ara-lifecycle-continuity/run.py --check
```

## Key distinctions

The executable suite preserves:

- Live Agent process != persistent Agent Role;
- replacement model memory != persisted relationship state;
- challenge != deletion;
- correction != overwrite;
- remediation != restoration of revoked authority;
- later revocation != retroactive invalidation of a historical legitimate action;
- agreement closure != whole-relationship closure;
- suspect interval != safe continuation;
- closure != implicit disappearance of surviving obligations.

## Claim boundary

This is a Lab-local lifecycle composition. It does not claim production durable storage, disaster recovery, revocation distribution, HSM/VTA lifecycle integration, standards-native ARA lifecycle conformance, or legal effect of closure/remediation.
