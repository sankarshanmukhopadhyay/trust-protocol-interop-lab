# IC-DTG-PERSONA-ROOM-001 — Persona × Data Room × Agent composition

## At a glance
- **Status:** Pre-admission experimental; partially source-executable, composition runtime incomplete.
- **Purpose:** Pressure-test cross-context Persona, Data Room and agent authority failures that component-local validation cannot detect.
- **Current conclusion:** Existing evidence resolves only bounded Persona and authority-substitution cases; aggregation, hostile-memory and full lifecycle composition remain evidence-required.

This case pressure-tests failures that can arise even when each component-local access is individually legitimate. Its central invariant is that legitimate access across multiple contexts does not itself authorize aggregation, inference, disclosure or consequential action across those contexts.

The executable definition is in [`scenario.yaml`](scenario.yaml). Related reusable evidence exists in [`../dtg-data-room-actuation/scenario.yaml`](../dtg-data-room-actuation/scenario.yaml), [`../dtg-hidden-subject-binding/scenario.yaml`](../dtg-hidden-subject-binding/scenario.yaml), and [`../dtg-vac-attenuation/scenario.yaml`](../dtg-vac-attenuation/scenario.yaml).

## Concrete scenario

A holder maintains Persona attributes and participates in several room contexts. An agent receives narrow authority in one or more contexts, reads permitted room information, and can perform only explicitly authorized Persona disclosure or action. The adversarial vectors then request over-disclosure, context escape, cross-context aggregation, authority escalation, mixed-principal composition, post-revocation action, hostile shared-memory instruction and use of revoked or superseded content from agent memory.

## Why this matters

The highest-value failure is compositional: every local read can be legitimate while the combined inference or disclosure is not. The case therefore distinguishes possession from authority and information from instruction.

## Where it resolved

Current evidence provides bounded resolution for only part of the surface:

- Persona over-disclosure and context escape are `source-executable` against the pinned OpenVTC Persona implementation surface.
- capability escalation and mixed-principal composition reuse existing Interop Lab cases rather than duplicating them;
- current-authority and stale-state pressure can reuse Data Room actuation evidence where the proposition matches.

Interop Lab supplies composition evidence. RAHP retains the terminal assurance judgment.

## What remains unresolved

Full cross-context aggregation, hostile shared-memory instruction, composed lifecycle and agent-memory behavior still need a real composed runtime. Private membership and correlation evidence routes to DPIP #214. No waiting vector is treated as PASS, and retrospective forgetting by an agent is not assumed.

## Evidence return

For each activated vector retain proposition, source/runtime version, preconditions, authority state, attempted action, expected result, observed result, artifact locations and residual uncertainty. The source pins and vector activation state are recorded in [`scenario.yaml`](scenario.yaml).
