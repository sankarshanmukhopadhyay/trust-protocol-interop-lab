# IC-DPAC-ACTUATION-001 — Minimum executable Dual-Path Actuation Control

**Status:** Experimental  
**Initial tracking issue:** [#106](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/106)  
**GovOps pressure-test issue:** [#108](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/108)

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

## Initial falsification scenarios

The first tranche pressure-tests five propositions:

1. **DPAC-001 — absent/revoked authority:** valid capability + absent or revoked authority → no actuation.
2. **DPAC-002 — capability overreach:** valid authority + requested operation outside the Workspace capability envelope → no actuation.
3. **DPAC-003 — stale/replayed authority:** technically reachable actuator + stale or replayed authority → no actuation.
4. **DPAC-004 — valid concurrence:** current authority + matching capability → actuation, with evidence that both paths concurred.
5. **DPAC-005 — transitive capability capture:** a Workflow modification that would create a direct or transitive path to changing its own capability controller → rejected.

The machine-readable contracts are in [`scenarios/scenarios.yaml`](scenarios/scenarios.yaml). The deterministic reference implementation is [`../../experiments/dpac-actuation/run.py`](../../experiments/dpac-actuation/run.py).

## GovOps delegated-loan pressure test

The second tranche reuses `IC-GOVOPS-EXEC-TRUST-001` rather than inventing a new domain. It asks whether DPAC still holds when delegated monetary authority, GovOps policy evaluation/enforcement, Workspace capability state, runtime effect, and evidence are separately observable.

The composed experiment is [`../../experiments/dpac-govops-loan/`](../../experiments/dpac-govops-loan/). It adds eight scenarios:

1. valid delegated authority + enforced `Allow` + matching capability → exactly one correlated effect;
2. delegated-authority monetary overreach → blocked even when capability permits the amount;
3. Workspace capability monetary overreach → blocked despite otherwise-valid authority;
4. revocation between authorization and actuation → blocked by authority re-evaluation;
5. capability revision change between authorization and actuation → stale concurrence rejected;
6. loan-target substitution after authorization → rejected;
7. amount widening after authorization → rejected; and
8. duplicate/retry of an already consumed actuation authorization → no second effect.

This tranche makes the time-of-check/time-of-use boundary explicit: authority bindings and current capability revision are re-evaluated at actuation. It also makes retry semantics explicit by treating the bounded actuation authorization as single-use.

## Failure semantics

The experiments fail closed. Missing, expired, revoked, replayed, mismatched, stale, or non-current authority does not become authorization. A valid authority record cannot enlarge Workspace capability. Technical capability does not imply permission. A changed capability revision requires fresh concurrence. Missing evidence does not become a pass.

## What success establishes

A successful deterministic run establishes only that the repository-owned reference models preserve the declared DPAC boundaries for the recorded scenarios. The GovOps pressure test additionally demonstrates those boundaries across a concrete delegated-loan composition with separately observable authority, authorization/enforcement, capability, and effect state.

It does **not** establish upstream TEA or GovOps conformance, production security, independently enforced Workspace isolation, independent implementation, independent certification, or resistance to attack classes outside these scenarios.

## Why this remains Experimental

The implementation and evidence are self-contained and self-authored. The Workspace capability administrator is logically separate and revisioned, but not yet demonstrated as an independently enforced OS/container/cloud/hardware boundary. Promotion requires stronger execution evidence and, for any interoperability-tested claim, an appropriately bounded evidence package under the repository maturity rules. External adversarial tooling remains intentionally deferred.
