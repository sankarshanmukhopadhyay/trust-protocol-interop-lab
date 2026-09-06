# Current OpenVTC Track A runtime evidence

This tranche implements Interop Lab #153 without treating Dogwood RC-1 as current evidence.

The runtime producer pins `OpenVTC/verifiable-trust-infrastructure@e393e38da4941202143e293b555413d8c86ef3b3` and executes the current VTI E2E support surface through a temporary additive observation probe. The upstream checkout is verified before and after execution and is never committed or modified upstream.

The A/B pressure case deliberately varies verifier, purpose, challenge and deterministic client identity. It therefore exercises the current relationship-equivalent binder and verifier transcript surfaces while testing whether an unseeded stable join emerges across the two contexts.

`ER-REL-DID-AB` and `ER-VERIFIER-AB` are materially exercised by this bounded path. Named relationship DID and edge identifier fields are observed as absent on the executed path. `ER-STATUS-AB` and `ER-TASK-AB` are not executed by this path and must remain `not-evidenced`; the producer must not turn non-execution into an implementation-wide absence claim.

Dogwood RC-1 remains an immutable historical/regression comparator. Its observations cannot discharge a current-baseline evidence requirement.

A successful workflow or a `not-detected` pressure join is evidence only. It does not establish privacy PASS, composition sufficiency, or RAHP GREEN. DPIP remains responsible for evidence acceptance and privacy judgment; RAHP remains responsible for reconciliation.
