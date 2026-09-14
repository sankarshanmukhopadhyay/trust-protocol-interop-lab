# DTG portfolio clean-room evidence trigger — 2026-09-14

RAHP controller: https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/665

This branch is an isolated execution surface for the post-clean-room evidence-acquisition tranche. It does not alter prior evidence or historical assessment pins.

Frozen controller target pins:

- VTI: `76eae3f…`
- Credential Spec: `32aeabf…`
- Trust Tasks: `f40ba07…`
- OpenVTC `dtg-credentials`: `66376c0…`

Required proposition families:

- P02: VDC/OpenVTC realization and conformance evidence.
- P03–P05: action-time authority, effect/outcome closure, replay/idempotency.
- P06–P09: attributable A/B relationship, status/policy, retained-task and verifier observations for DPIP.

Execution rule: evidence must retain exact target provenance. Existing producer evidence may be reused only when it is attributable to the frozen target; semantic similarity or synthetic/local execution is insufficient.
