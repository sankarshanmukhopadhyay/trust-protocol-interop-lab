# ARA decision-resolution pressure test

This extension to **IC-ARA-REL-001** asks a narrow executable question:

> Can a material unresolved condition survive non-authoritative pressure and workflow progression, while resolving or reopening for the right authority, evidence, policy, or lifecycle reason?

It does not add another authority source. A condition is state that must be resolved; it is not permission, a veto, or a substitute for governing policy.

## Executable propositions

The deterministic vectors prove that:

- an unauthorised peer does not clear an authority condition;
- repetition does not manufacture authority;
- unrelated delegated scope does not become relevant scope;
- valid in-scope delegation can resolve an authority condition;
- authoritative evidence can resolve a factual predicate without creating authority;
- a legitimate policy change remains a policy-based resolution;
- workflow progression alone does not resolve the condition;
- revocation before commitment reopens authority evaluation;
- stale evidence before commitment reopens the evidence/lifecycle condition.

Run:

```bash
python experiments/ara-decision-resolution/run.py --check
```

## Relationship to ARA

This pressure test extends the existing ARA proposition that identity, authority, relationship, capability, workflow authorization, protected signing, task semantics, and current state must align before consequential action. It adds no new normative component; it tests whether unresolved material state is preserved until those inputs actually change.

## Research provenance

This tranche was informed by TSMM/TIS decision-resolution work and a read-only review of the independent **Protocol of Care for Agents** project:

- https://github.com/JessHines360/protocol-of-care-for-agents
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/BRIEF.md
- https://github.com/JessHines360/protocol-of-care-for-agents/blob/main/experiments/SIMULATION_01_RUNBOOK.md

ARA does not adopt `CareSignal`, `DeliberativeHold`, or the upstream normative vocabulary. No upstream repository content was modified.
