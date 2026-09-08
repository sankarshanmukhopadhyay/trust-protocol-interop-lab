# IC-DTG-PERSONA-ROOM-001 — Persona × Data Room × Agent composition

This case is the composed assurance surface defined by issue #167. It exists to test failures that can arise even when each component-local access is individually legitimate.

## Core invariant

Legitimate access across multiple contexts does not itself authorize aggregation, inference, disclosure or consequential action across those contexts.

## Current executability

The case deliberately distinguishes what can already be grounded from what still needs a composed runtime:

- Persona over-disclosure and context escape are `source-executable` against the pinned OpenVTC Persona implementation surface.
- capability escalation and mixed-principal composition reuse existing Interop Lab cases rather than duplicating them;
- full cross-context aggregation, hostile shared-memory instruction, composed lifecycle and agent-memory semantics remain waiting on an executable composition path;
- private membership/correlation evidence routes to DPIP #214.

No waiting vector is treated as PASS.

## Evidence reuse

Existing Lab cases provide reusable negative evidence contracts:

- `dtg-data-room-actuation` — current authority, subject binding, task binding, replay and privacy-scope failures;
- `dtg-hidden-subject-binding` — common/hidden-subject binding pressure;
- `dtg-vac-attenuation` — bounded authority and attenuation pressure.

`scenario.yaml` records which vectors reuse these cases and which remain runtime-dependent.

## RAHP return discipline

For each activated vector, retain proposition, source/runtime version, preconditions, authority state, attempted action, expected result, observed result, artifact locations and residual uncertainty. Interop Lab supplies composition evidence; RAHP owns the terminal assurance judgment.
