# IC-PDC-MED-001 — Protected Delegated Care

**Status:** Experimental  
**Workstream:** Protected Delegated Care (PDC)  
**Source decision:** Discussion #127  
**Initial implementation issue:** #128

## At a glance

`IC-PDC-MED-001` asks whether an ordinary delegated-care application can consume DTG/VTC trust semantics without turning information possession, channel access, identity, relationship, or technical capability into authority.

The first bounded scenario is medication assistance: a principal establishes a caregiver relationship, delegates only exception-handling authority, activates a human-approved synthetic medication plan, receives reminders through a channel simulator, and permits a caregiver to request a re-reminder only when the current delegation authorizes that exact action.

The case is intentionally **application-level**. It is not a medication-reminder product claim, clinical system, prescribing system, pharmacy network, or healthcare conformance profile.

## Why this matters

A familiar care application can look simple while quietly collapsing consequential trust decisions into one role: someone knows about a medication plan, can reach the care recipient, and is therefore treated as entitled to inspect or act on care state. PDC pressure-tests the opposite architecture. Relationship, delegation, current authority, task authorization, execution, disclosure, and evidence remain independently observable, while stale or missing authority fails closed.

The medical-prescription extension adds another important separation: a prescription or medication order can exist and be possessed without thereby proving current refill eligibility or legal dispensing authority. That distinction lets the Discussion be tested as trust architecture rather than smuggled into application convenience.

## Governing proposition

A consequential care action may execute only when the current relationship, bounded delegation, applicable policy, requested action, resource, lifecycle state, and available evidence all permit it. Information possession, identity, relationship, channel access, or technical capability is never sufficient on its own.

The case also requires minimum disclosure: proving or exercising authority should not reveal information unnecessary to the permitted action.

## Core separations

```text
identity != relationship
relationship != delegation
delegation != authority decision
capability != authority
authority != task authorization
task authorization != execution
execution != evidence
evidence != authority
reminder dispatched != delivered != seen != acknowledged != medicine taken
prescription exists != holder possesses != refill eligible != dispensing authorized
```

## Deterministic architecture boundary

OCR, LLM interpretation, translation, and channel integrations are adapters. They may propose structured commands or candidate plan data, but they do not own authoritative care state.

```text
external/probabilistic input
        |
        v
adapter -> proposed command/data
        |
        v
deterministic validation + current-authority evaluation
        |
   PERMIT / DENY / INDETERMINATE
        |
        v
bounded state mutation + evidence
```

No channel webhook receives a privileged bypass around the same controller used by other consequential actions. Missing evidence never becomes `PASS` or `PERMIT`.

## Concrete scenario

The base executable path creates synthetic principal and caregiver identities, establishes a care relationship, delegates only bounded exception-handling capabilities, activates a human-approved synthetic medication plan, dispatches a reminder, records a timeout, sends a minimum-disclosure caregiver exception, and evaluates a bounded re-reminder request against current authority immediately before actuation. The same class of request is exercised after revocation and must fail without authoritative state mutation.

The bounded refill extension then evaluates a synthetic medication order with one remaining refill. The verifier receives only the proposition needed for the refill decision; expired, revoked, superseded, exhausted, context-mismatched, stale-challenge, or replayed requests fail closed or are idempotent. Prescription existence, holder possession, refill eligibility, and any later dispensing authority remain distinct states.

## Executed implementation chain

The original Discussion has now been translated into a linked implementation sequence rather than a single monolithic prototype:

1. **#128 / PR #129 — case foundation**: admitted `IC-PDC-MED-001` as Experimental with ownership, invariants, state machines, disclosure matrix, synthetic fixtures, negative scenarios, DTG/VTC mapping and explicit gap handling.
2. **#130 / PR #131 — deterministic core**: implemented relationship/delegation lifecycle, medication-plan approval/activation, reminder/timeout/escalation, bounded authorization, idempotency, disclosure checks and decision evidence.
3. **#132 / PR #134 — Trust Task/OpenVTC binding**: bound the caregiver exception action to a Trust Task-shaped request while preserving the unresolved document-proof versus authenticated-transport boundary.
4. **#135 / PR #144 — current-authority actuation boundary**: inspected pinned VTI/OpenVTC authority surfaces and found no exact generic delegated-action evaluator for the PDC action/resource. The integration therefore fails closed as `INDETERMINATE/BLOCKED` rather than substituting relationship or domain-specific authority semantics.
5. **#136 / PR #148 — runtime privacy evidence**: produced DPIP-consumable synthetic traces. Application-observable minimum-disclosure properties pass, while provider/network/device confidentiality and broader correlation remain `INDETERMINATE` where not observed.
6. **#137 / PR #152 — bounded refill disclosure extension**: introduced `IC-PDC-REFILL-001` and compared ordinary minimisation, selective disclosure, and a modeled unlinkable-ZKP candidate. Selective disclosure is preferred at the current evidence level; ZKP is not declared necessary and remains unproven until real cryptographic construction is exercised.
7. **#150 / PR #154 — prescription-to-refill lifecycle**: separates prescription/order existence, holder possession, refill eligibility and any later dispensing authority/effect; exercises expiry, revocation, supersession, exhausted allowance, context mismatch, stale challenge and replay.
8. **#138 / PR #155 — assurance reconciliation**: records a machine-readable maturity decision. The case remains **Experimental** because material assurance boundaries remain unresolved or `INDETERMINATE`.

Issue #141 and #151 track the reader/documentation closure represented by this update.

## State and privacy artifacts

- [`state-machines.yaml`](state-machines.yaml) — medication-plan, reminder and delegation lifecycle contracts.
- [`disclosure-matrix.yaml`](disclosure-matrix.yaml) — P0 minimum-disclosure boundaries.
- [`trust-task-profile.yaml`](trust-task-profile.yaml) — PDC application profile for bounded Trust Task requests.
- [`authority-surface-observations.yaml`](authority-surface-observations.yaml) — pinned upstream authority-surface observations.
- [`dpip-runtime-evidence-profile.yaml`](dpip-runtime-evidence-profile.yaml) — runtime privacy evidence boundary.
- [`refill-profile.yaml`](refill-profile.yaml) — bounded `IC-PDC-REFILL-001` disclosure comparison.
- [`prescription-refill-lifecycle.yaml`](prescription-refill-lifecycle.yaml) — synthetic prescription/order-to-refill lifecycle.
- [`assurance-decision.yaml`](assurance-decision.yaml) — current machine-readable maturity decision.
- [`dtg-vtc-mapping.yaml`](dtg-vtc-mapping.yaml) and [`gaps.yaml`](gaps.yaml) — observed mappings, implementation gaps and unresolved semantics.

## Privacy result

The base case uses **P0 — bounded conventional disclosure**: scoped authorization, contextual identifiers, minimum-data messages, explicit retention boundaries, revocation and deterministic evidence.

Runtime evidence establishes that routine acknowledged reminders do not produce caregiver-facing disclosure and that exception/late-ack payloads remain inside the declared minimum-data boundary. Those are application-observable properties only. Provider logs, network/device metadata and cross-service join behavior are not inferred from absence of evidence and remain `INDETERMINATE` where unobserved.

The refill extension tests whether stronger disclosure technology is justified. At the current evidence level, selective disclosure removes an application-visible contextual subject reference while still satisfying the verifier's bounded refill proposition. The repository therefore does **not** make ZKP mandatory merely because it is available. A stronger unlinkability construction is justified only if measured residual linkability cannot be brought within the privacy requirement by the simpler mechanism.

## Current assurance decision

`IC-PDC-MED-001` remains **Experimental**. Repository workflows are reproducible and green, but workflow green is not assurance green.

Promotion is blocked by four material boundaries:

1. no exact upstream/profile-defined generic delegated-action authority evaluator has been exercised for the precise action/resource at actuation time;
2. provider/network/device confidentiality and broader cross-service correlation remain unobserved;
3. the Trust Task document-proof versus OpenVTC authenticated-transport boundary remains unresolved for a generic conformance claim;
4. relationship/current-membership state must not be substituted for delegated consequential-action authority without an explicit semantic mapping.

These blockers are recorded in [`assurance-decision.yaml`](assurance-decision.yaml) and the RAHP review register. `INDETERMINATE` remains non-green by design.

## Where it resolved

The implementation programme resolved the application-owned portions of the original Discussion into executable contracts and evidence: deterministic care-state transitions, bounded caregiver action, Trust Task-shaped request binding, application-level disclosure enforcement, replay/idempotency behavior, selective-disclosure comparison, and prescription-to-refill lifecycle checks are all now reproducible.

It also resolved the maturity question for this tranche: the correct current disposition is **Experimental**, not Candidate. That is an assurance result rather than an incomplete implementation state. The remaining blockers are explicitly upstream/runtime evidence questions and are retained as such instead of being hidden behind case-local substitutions.

## What the work established

The Discussion-to-implementation sequence now demonstrates that the medical-prescription/medication-assistance topic can be decomposed into executable trust boundaries without collapsing application convenience into authority. It established a reusable pattern for:

- keeping relationship distinct from delegated action authority;
- binding consequential requests to exact action/resource/context;
- re-evaluating current authority immediately before actuation;
- failing closed when the upstream authority surface is missing;
- treating runtime disclosure and correlation as evidence questions rather than assumptions;
- preferring the simplest privacy construction that satisfies the measured requirement;
- separating prescription/order lifecycle from refill eligibility and any later dispensing authority;
- preserving negative, replay and stale-state evidence as first-class assurance artifacts.

## What remains unresolved

The strongest unresolved questions are intentionally still visible. The exact generic upstream current delegated-action evaluator has not been found or exercised; provider/network privacy remains only partially observed; Trust Task proof/authenticated-transport semantics need reconciliation for a broader interoperability claim; and the refill ZKP candidate has not been cryptographically exercised.

Those are not reasons to call the implementation incomplete. They are the current assurance findings produced by the implementation pressure test.

## What this case does not establish

This case is not:

- a medical device, diagnostic, prescribing system, clinical decision-support system, or substitute for medical advice;
- evidence that medicine was ingested;
- legal authority to dispense medication;
- a production healthcare record, e-prescription implementation, or pharmacy network;
- evidence of WhatsApp/provider confidentiality, retention, metadata, or platform behaviour;
- a claim that ZKP is necessary or sufficient;
- production-security/privacy certification;
- generic DTG/VTC/OpenVTC conformance beyond the exact exercised surfaces;
- Candidate or Interoperability Tested maturity.

## Reproduction

The executable evidence producers are under [`experiments/protected-delegated-care/`](../../experiments/protected-delegated-care/). Dedicated workflows retain artifacts for the current-authority boundary, runtime privacy evidence, refill disclosure comparison and prescription-to-refill lifecycle. The repository-wide `validate` context remains the canonical required status check.

The central assurance invariant remains:

> **Missing evidence MUST NOT become PASS or PERMIT.**
