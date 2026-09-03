# IC-DPAC-ACTUATION-001 — Minimum executable Dual-Path Actuation Control

**Status:** Experimental  
**Tracking issue:** [#106](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/106)

This case tests one architectural/security proposition: a consequential operation executes only when the requested operation is simultaneously within **current, action-specific authority** and an **independently administered capability envelope** at the actuation boundary. Neither path may enlarge, substitute for, synthesize, or directly/transitively capture the other.

## Claim boundary

DPAC is treated here as an experimental property, not a prescribed token, credential, process boundary, harness topology, upstream specification, or certification scheme. The Lab owns only this composition, reference implementation, vectors, and evidence.

The authority path is modeled as an evaluation chain:

```text
principal
  -> relationship/delegation
  -> applicable policy/duty
  -> workflow authorization
  -> action-specific authority
```

The resulting authority object records the outcome of that evaluation; it is not itself the source of authority.

The capability path is administered by the Workspace. It constrains what the runtime is technically able to do. A Workflow cannot expand that envelope, directly or through another modifiable Workflow.

## Core invariant

```text
ACTUATE(request)
  iff
CURRENT_ACTION_SPECIFIC_AUTHORITY(request)
  AND
REQUEST_WITHIN_INDEPENDENT_CAPABILITY_ENVELOPE(request)
```

with the additional non-collapsibility rule:

```text
AUTHORITY_PATH !-> enlarge CAPABILITY_PATH
CAPABILITY_PATH !-> synthesize AUTHORITY
WORKFLOW !-> directly_or_transitively control its own capability controller
```

## Ownership boundaries

| Concern | Owner in this experiment | Does not imply |
|---|---|---|
| principal, relationship, delegation, policy/duty inputs | upstream/domain authority sources | local Workflow may manufacture authority |
| Workflow authorization | Workflow authority evaluation | ability to enlarge Workspace capability |
| capability envelope | independently administered Workspace | authority to exercise a capability |
| actuation concurrence | actuator boundary | either path may substitute for the other |
| runtime effect | actuator/runtime | authorization evidence by itself |
| evidence | Interop Lab reference evidence | normative TIS profile or certification |
| assurance interpretation | downstream consumer | retroactive authority |

## Falsification scenarios

The case is deliberately small and pressure-tests five propositions:

1. **DPAC-001 — absent/revoked authority:** valid capability + absent or revoked authority → no actuation.
2. **DPAC-002 — capability overreach:** valid authority + requested operation outside the Workspace capability envelope → no actuation.
3. **DPAC-003 — stale/replayed authority:** technically reachable actuator + stale or replayed authority → no actuation.
4. **DPAC-004 — valid concurrence:** current authority + matching capability → actuation, with evidence that both paths concurred.
5. **DPAC-005 — transitive capability capture:** a Workflow modification that would create a direct or transitive path to changing its own capability controller → rejected.

The machine-readable contracts are in [`scenarios/scenarios.yaml`](scenarios/scenarios.yaml). The deterministic reference implementation is [`../../experiments/dpac-actuation/run.py`](../../experiments/dpac-actuation/run.py).

## Failure semantics

The experiment fails closed. Missing, expired, revoked, replayed, mismatched, or non-current authority does not become authorization. A valid authority record cannot enlarge Workspace capability. Technical capability does not imply permission. Missing evidence does not become a pass.

## What success establishes

A successful deterministic run establishes only that this repository-owned reference model preserves the declared DPAC invariants for the five recorded vectors. It does **not** establish upstream TEA conformance, production security, independent implementation, independent certification, or resistance to attack classes outside these scenarios.

## Why this remains Experimental

The implementation and vectors are self-contained and self-authored. Promotion requires stronger execution evidence and, for any interoperability-tested claim, an appropriately bounded evidence package under the repository maturity rules. External adversarial tooling is intentionally deferred from this wave.
