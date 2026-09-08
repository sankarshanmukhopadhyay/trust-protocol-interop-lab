# IC-DPAC-ACTUATION-001 — Minimum executable Dual-Path Actuation Control

**Status:** Experimental  
**Initial tracking issue:** [#106](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/106)  
**GovOps pressure-test issue:** [#108](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/108)  
**Enforced-boundary issue:** [#111](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/111)  
**External adversarial-testing issue:** [#170](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/170)

This case tests one architectural/security proposition: a consequential operation executes only when the requested operation is simultaneously within **current, action-specific authority** and an **independently administered capability envelope** at the actuation boundary. Neither path may enlarge, substitute for, synthesize, or directly/transitively capture the other.

## At a glance

| Item | Current state |
|---|---|
| **Status** | Experimental |
| **Purpose** | Test whether a consequential action can occur only when current action-specific authority and an independently administered technical capability both permit it at the actuation boundary. |
| **Current conclusion** | The proposition has survived a semantic model, a GovOps delegated-loan composition, a container-enforced Workspace boundary, and one complete externally driven replay proposition. External governance self-modification evidence is currently partial and several additional adversarial classes remain explicit harness gaps. |
| **Evidence today** | Deterministic semantic scenarios, GovOps pressure tests, a ten-scenario container-enforcement experiment, and pinned Agent Security Harness evidence normalized against the actuator-owned effect oracle. The external evidence is bounded and does not constitute independent certification. |

## Why this matters to a new reader

Most systems have an authorization check somewhere before a tool call. DPAC asks a stricter question: **what prevents the authority-producing path itself from expanding or bypassing the technical capability that makes the action possible?**

The security property is not "two modules" or "two approvals". It is **non-collapsibility of control**: authority cannot manufacture capability, capability cannot manufacture authority, and the Workflow cannot directly or transitively take control of the mechanism that constrains its own capability envelope.

## Concrete scenario

A delegated loan officer is authorized for a particular approval. The Workflow may produce action-specific authority evidence, but only a separately administered Workspace possesses the route and credential required to cause the actual effect.

The Workspace rechecks request binding, current authority, capability scope, capability revision, replay state, and then calls the actuator. The Workflow cannot directly reach the actuator or write the Workspace capability policy.

## Where it resolved

The Lab now has bounded evidence that DPAC can be realized as a runtime-enforced property rather than only a semantic distinction. The enforced-boundary experiment demonstrated policy-mutation denial, direct-actuator isolation, capability overreach rejection, revocation handling, request-substitution rejection, capability-revision TOCTOU protection, replay resistance, helper-path denial, and fail-closed indeterminate state.

The external adversarial tranche adds a second evidence source without changing assurance authority: Agent Security Harness `v4.21.1` can materially exercise the DPAC replay boundary through a narrow translation adapter, while the actuator-owned journal remains the Lab outcome oracle. Where the external harness cannot express a DPAC property without semantic invention, the result is retained as `harness-gap` or `not-observable` rather than converted to PASS.

It remains **Experimental** because the Docker host/daemon, kernel, supply chain, independent administration beyond the test topology, cryptographic upstream authority resolution, and multiple unmapped external attack classes remain outside the claim.

## What remains unresolved

The enforced boundary is still one Lab-authored Docker topology. Host/daemon or kernel compromise, supply-chain compromise, unknown transitive administrative paths, independently operated capability administration, and cryptographic resolution of upstream authority/delegation remain outside the claim.

External adversarial coverage is also intentionally bounded. Replay is materially mapped. Direct governance mutation is exercised but does not externally cover the transitive-helper half of the proposition. Authority bypass, capability-envelope bypass, capability-revision TOCTOU, target/parameter substitution, prompt/tool injection, confused-deputy behavior, and receipt-integrity attacks remain explicit mapping gaps where the pinned harness wire contracts do not losslessly match the current DPAC target. HITL bypass is not applicable because this target has no human approval boundary.

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
| external adversarial payloads/verdicts | Agent Security Harness upstream | harness owns DPAC interpretation or maturity |
| evidence normalization and case interpretation | Interop Lab | retroactive authority or certification |

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

## External adversarial evidence

The fourth tranche is [`../../experiments/dpac-agent-security/`](../../experiments/dpac-agent-security/). It consumes the upstream Agent Security Harness as a pinned external dependency rather than vendoring or forking it.

The Lab retains a five-state interpretation model: `pass`, `fail`, `not-applicable`, `not-observable`, and `harness-gap`. The harness remains an evidence producer; its PASS is insufficient unless the target was materially serviced and the actuator-owned effect oracle independently agrees.

The first complete mapping uses upstream `DCA-005` replay behavior. The adapter maps only the external request identifier to the DPAC nonce; Workspace remains the replay enforcement point. Across two same-ID presentations the expected evidence is exactly one first-use effect and no duplicate effect.

The upstream `GM-001` governance self-modification test is also executed. Its requests are forwarded unchanged to Workspace `/admin/policy`, which owns the explicit refusal. Because this does not externally re-exercise the Workflow-controlled transitive-helper path, the full direct+transitive proposition is retained as `not-observable` rather than promoted to PASS.

All ten #170 classes and their current evidence disposition are recorded in [`../../experiments/dpac-agent-security/vector-map.yaml`](../../experiments/dpac-agent-security/vector-map.yaml).

## Failure semantics

The experiments fail closed. Missing, expired, revoked, replayed, mismatched, stale, or non-current authority does not become authorization. A valid authority record cannot enlarge Workspace capability. Technical capability does not imply permission. A changed capability revision requires fresh concurrence. Missing or unresolvable evidence does not become a pass.

External evidence follows the same rule: unreachable, unserviced, simulated, reference-model-only, partial, or semantically unmappable harness behavior cannot become a Lab PASS. An unexpected actuator effect is a FAIL even when external coverage is otherwise partial.

## What success establishes

Passing deterministic semantic/composition runs establish that the repository-owned reference models preserve their declared DPAC boundaries for recorded scenarios. A passing enforced-boundary run additionally establishes, for the tested Docker topology, that Workflow/helper lack the tested policy mount, actuator credential and actuator network route, while Workspace remains the only bridge to the authenticated actuator and negative cases leave the actuator-owned effect journal unchanged.

A passing external replay mapping adds evidence that a separately developed harness can drive the replay proposition against the real Workspace boundary and that the Lab-owned effect oracle agrees with the external harness verdict. It does **not** establish independent certification, exhaustive adversarial coverage, upstream TEA or GovOps conformance, production security, host/Docker-daemon compromise resistance, exhaustive transitive-control analysis, or resistance to attack classes currently classified as harness gaps.

## Why this remains Experimental

The evidence is materially stronger than logical separation alone and now includes one complete externally driven adversarial proposition, but the implementation remains one Lab-authored topology with bounded external mappings. The Docker host/daemon is outside the modeled adversary boundary, authority authenticity remains abstracted rather than cryptographically resolved from an upstream authority system, and several important external attack classes remain unmapped or only partially observable. Promotion therefore remains a separate evidence-gated maturity judgment.
