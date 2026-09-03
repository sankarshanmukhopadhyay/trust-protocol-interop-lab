# IC-DPAC-ACTUATION-001 — Minimum executable Dual-Path Actuation Control

**Status:** Experimental  
**Initial tracking issue:** [#106](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/106)  
**GovOps pressure-test issue:** [#108](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/108)  
**Enforced-boundary issue:** [#111](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/111)

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

The composed experiment is [`../../experiments/dpac-govops-loan/`](../../experiments/dpac-govops-loan/). It adds eight scenarios covering valid concurrence, authority/capability scope divergence, revocation, capability-state TOCTOU, target substitution, amount widening, and duplicate execution.

This tranche makes the time-of-check/time-of-use boundary explicit: authority bindings and current capability revision are re-evaluated at actuation. It also makes retry semantics explicit by treating the bounded actuation authorization as single-use.

## Enforced Workspace boundary

The third tranche is [`../../experiments/dpac-enforced-boundary/`](../../experiments/dpac-enforced-boundary/). It moves from a self-asserted `capability_controller_separate` state to a concrete container-enforced topology:

```text
workflow/helper -- request_net --> workspace -- actuator_net --> actuator
                                      |
                                      +-- read-only capability policy
                                      +-- actuator credential
                                      +-- replay state
```

Workflow/helper and actuator share no Docker network. Only Workspace joins both networks. The actuator credential and capability-policy mount are absent from Workflow/helper containers. Workspace enforces current authority binding, current capability policy, request binding, and replay state before invoking the authenticated actuator. The actuator owns the effect journal, so negative tests confirm no effect by observing journal count rather than trusting a denial response.

Ten falsification scenarios exercise valid concurrence, direct actuator bypass, policy mutation/admin attempts, capability overreach, revocation, request substitution, capability-revision TOCTOU, replay, a Workflow-controlled helper as a bounded transitive path, and indeterminate capability state.

This establishes a stronger bounded proposition: for the tested container principals, compromise of Workflow/helper alone does not provide a tested path to capability-policy mutation or direct actuation.

## Failure semantics

The experiments fail closed. Missing, expired, revoked, replayed, mismatched, stale, or non-current authority does not become authorization. A valid authority record cannot enlarge Workspace capability. Technical capability does not imply permission. A changed capability revision requires fresh concurrence. Missing or unresolvable evidence does not become a pass.

## What success establishes

Passing deterministic semantic/composition runs establish that the repository-owned reference models preserve their declared DPAC boundaries for recorded scenarios. A passing enforced-boundary run additionally establishes, for the tested Docker topology, that Workflow/helper lack the tested policy mount, actuator credential and actuator network route, while Workspace remains the only bridge to the authenticated actuator and negative cases leave the actuator-owned effect journal unchanged.

It does **not** establish upstream TEA or GovOps conformance, production security, host/Docker-daemon compromise resistance, exhaustive transitive-control analysis, independent implementation, independent certification, or resistance to attack classes outside these scenarios.

## Why this remains Experimental

The new boundary evidence is materially stronger than logical separation, but it remains self-authored and bounded to one container topology. The Docker host/daemon is outside the modeled adversary boundary, and authority authenticity remains abstracted rather than cryptographically resolved from an upstream authority system. Promotion therefore remains a separate maturity judgment requiring the repository's normal evidence gate. External adversarial tooling remains intentionally deferred.
