# IC-ARA-REL-001 Phase 8 — visible lifecycle-continuity judgment

Issue: #40  
Parent: #32  
Depends on completed distributed-VRR phase: #39

## Proposition under test

Can a persistent Agent Role and relationship continue through Live Agent replacement, challenge, correction, remediation, capability revocation, continuation and closure while preserving historical truth and preventing stale authority from remaining operative?

## Alternatives genuinely considered

### Restore continuity from the replacement model's conversation/context memory

Rejected. Model memory is neither durable relationship state nor independently verifiable evidence.

### Rewrite challenged or corrected historical objects

Rejected. This destroys the ability to prove what was previously asserted, accepted or disputed.

### Reactivate the old capability after remediation

Rejected. Remediation must not silently recreate technical power. A revoked capability stays revoked; fresh authorization must mint fresh capability.

### Treat later revocation as invalidating previously legitimate actions

Rejected. Current authority and historical validity are different temporal claims.

### Close the entire relationship when one Agreement closes

Rejected. Agreement lifecycle and relationship lifecycle are distinct. Relationship-level obligations may survive an Agreement branch.

### Compose lifecycle controls over the existing Role Record, Agreement, Capability and VRR components

Selected. This makes persistence, dispute evidence, revocation and closure separately inspectable while adding only the cross-component resume guards that Phase 8 needs.

## Core judgment

> What persists is the Agent Role's evidence-bearing state, not the Live Agent's memory. What changes after challenge is current authority and remediation state, not historical bytes. What survives closure depends on explicit lifecycle scope.

The implementation preserves:

```text
Live Agent lifetime != Agent Role lifetime
challenge != erase
correction != overwrite
remediation != capability resurrection
current revocation != historical invalidity
agreement closure != relationship closure
relationship closure != disappearance of historical evidence
```

## Falsification evidence

The suite pressures:

- replacement with no persisted relationship context;
- correction attempting to mutate the challenged object;
- use of a revoked capability;
- remediation accidentally restoring revoked capability;
- continuation while a suspect interval remains unreviewed;
- Agreement closure accidentally terminating relationship-level obligations;
- closed relationship being resumed;
- append-only history surviving the whole lifecycle.

## Claim boundary

The implementation is still Lab-local and deterministic. It does not establish production crash recovery, distributed revocation propagation, durable external evidence storage, legal closure semantics, VTA/HSM lifecycle controls, or normative ARA lifecycle ownership.

## Human acceptance boundary

Green CI can satisfy only the bounded claim that the walking skeleton remains coherent through model replacement and adverse lifecycle transitions without hidden memory, destructive history mutation, stale capability use, or lifecycle-scope collapse.

The overall case remains pre-admission.

The judgment to preserve is:

> Durable relationship legitimacy requires temporal reasoning: historical facts remain attributable, present authority can change, and future continuation requires current defensible state rather than remembered intent.
