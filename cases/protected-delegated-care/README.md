# IC-PDC-MED-001 — Protected Delegated Care

**Status:** Experimental  
**Workstream:** Protected Delegated Care (PDC)  
**Source decision:** Discussion #127  
**Implementation issue:** #128

## At a glance

`IC-PDC-MED-001` asks whether an ordinary delegated-care application can consume DTG/VTC trust semantics without turning application possession, channel access, identity, relationship, or technical capability into authority.

The first bounded scenario is medication assistance: a principal establishes a caregiver relationship, delegates only exception-handling authority, activates a human-approved synthetic medication plan, receives reminders through a channel simulator, and permits a caregiver to request a re-reminder only when the current delegation authorizes that exact action.

The case is intentionally **application-level**. It is not a medication-reminder product claim and it is not a healthcare conformance profile.

## Why this matters

A familiar care application can look simple while quietly collapsing several consequential trust decisions into one application role: a family member knows about a medication plan, has access to the messaging channel, and is therefore treated as entitled to inspect, alter, or act on care state. That shortcut makes disclosure, revocation, stale authority, and coercive control difficult to reason about or test.

PDC exists to pressure-test the opposite architecture. The principal remains the source of bounded assistance authority; relationship, delegation, task authorization, execution, disclosure, and evidence remain independently observable; probabilistic extraction never becomes authoritative care state; and a revoked caregiver must lose the delegated action even if they still possess old information or a previously authorized task.

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
```

## Actors

- **Principal / care recipient** — owns or controls the delegated-care authority in this prototype unless a separately modelled legal authority exists.
- **Caregiver** — receives only explicitly delegated capabilities; is not an administrator of the principal.
- **Medication-plan operator** — resolves extraction uncertainty and assists human confirmation; extraction itself never activates a plan.
- **Interaction provider / channel simulator** — transports normalized events and messages; is not an authority source.
- **Prescriber / pharmacy** — simulated external actors reserved primarily for follow-on work; no real clinical or pharmacy integration is claimed here.

## Initial capability vocabulary

```text
care.reminder.receive
care.reminder.defer
care.exception.receive
care.exception.respond
care.schedule.view
care.schedule.modify
care.medication.view
care.prescription.view
care.refill.request
care.refill.authorize
care.delegation.modify
```

The first executable slice delegates only `care.exception.receive` and `care.exception.respond` to the caregiver.

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
   PERMIT / DENY
        |
        v
state mutation + evidence
```

No channel webhook receives a privileged bypass around the same controller used by other consequential actions.

## Concrete scenario

1. Create synthetic principal and caregiver.
2. Establish care relationship.
3. Delegate only exception authority.
4. Load a synthetic prescription fixture.
5. Extraction produces a proposed plan.
6. Human approval is required.
7. Approved plan becomes active.
8. Scheduler creates and dispatches a reminder through the channel simulator.
9. No acknowledgement is received.
10. Exception policy selects the caregiver and re-evaluates the current delegation.
11. Caregiver receives a minimum-disclosure exception notice.
12. Caregiver requests a re-reminder.
13. A bounded task is evaluated and, if permitted, executed.
14. Decision and effect evidence are recorded.

The same request is then repeated after revocation. Expected result: `DENY`, no state mutation, denial evidence.

## State model

The normative case-local state contracts are in [`state-machines.yaml`](state-machines.yaml). In summary:

- medication plans require human approval before `ACTIVE`;
- a superseding plan cannot silently mutate an active plan;
- only one applicable plan version may produce reminders;
- reminder dispatch does not imply delivery or ingestion;
- delegation is re-evaluated at consequential execution time.

## Privacy boundary

The initial privacy profile is **P0 — bounded conventional disclosure**: compartmentalisation, scoped authorization, contextual identifiers, minimum-data messages, explicit retention boundaries, revocation, and deterministic evidence.

The machine-readable disclosure contract is in [`disclosure-matrix.yaml`](disclosure-matrix.yaml). A caregiver exception should be renderable as:

```text
The 08:00 care reminder has not been acknowledged.
```

without automatically disclosing medication name, diagnosis, prescription source, or broader clinical history.

Selective disclosure / ZKP is deliberately deferred to a separate refill-entitlement case. ZKP is a treatment to compare against P0, not an architectural assumption.

## Falsification contract

[`scenarios/acceptance.yaml`](scenarios/acceptance.yaml) defines the minimum claims that later implementation must make executable. Important negative cases include:

- over-broad caregiver capability;
- stale/revoked delegation;
- superseded medication plan execution;
- unauthorized prescription access;
- disclosure expansion;
- Trust Task replay;
- duplicate channel webhook;
- late acknowledgement reconciliation;
- extraction ambiguity;
- fabricated extraction;
- cross-context caregiver correlation;
- authority revoked between task creation and execution;
- missing authority/evidence.

The central assurance invariant is:

> **Missing evidence MUST NOT become PASS or PERMIT.**

## DTG/VTC consumption rule

[`dtg-vtc-mapping.yaml`](dtg-vtc-mapping.yaml) records what the application expects from DTG/VTC and whether the current mapping is direct, candidate, adapter-backed, unresolved, or deferred.

The case MUST NOT silently invent DTG semantics to make itself pass. Any mismatch is recorded in [`gaps.yaml`](gaps.yaml) before an upstream/downstream change is proposed.

## Synthetic fixtures

[`fixtures/canonical.yaml`](fixtures/canonical.yaml) contains only synthetic identifiers and non-clinical placeholders. No real prescription, health record, phone number, patient identity, or medication detail is required for this case foundation.

## Where it resolved

The case is admitted only at **Experimental** maturity. This tranche resolves the proposition, ownership, lifecycle contracts, P0 disclosure boundary, synthetic fixture set, falsification scenarios, and the rule for recording DTG/VTC gaps. It does **not** resolve the runtime integration questions.

The repository should therefore treat the current outcome as: **model and acceptance contract established; execution evidence pending**. A green validation run proves internal repository consistency of that claim, not that the delegated-care properties have been demonstrated at runtime.

## What remains unresolved

The exact DTG/VTC realization remains intentionally open. In particular, the case still needs to prove the care-relationship/delegation separation, bind the caregiver request to an exact Trust Task representation, and exercise execution-time revocation against a concrete VTC runtime. The catalog registers the VTC runtime boundary against OpenVTC, but the case has not yet claimed or exercised that integration.

Also unresolved are measured retention properties, real messaging-provider behaviour, DPIP runtime observations, and any selective-disclosure/ZKP benefit. The latter belongs to a later refill-entitlement case rather than being smuggled into this first prototype.

## What this case does not establish

This case is not:

- a medical device, diagnostic, prescribing system, or substitute for medical advice;
- evidence that medicine was ingested;
- a production healthcare record or pharmacy network;
- evidence of WhatsApp/provider confidentiality, retention, metadata, or platform behaviour;
- a claim that ZKP is necessary or sufficient;
- a production-security or privacy certification;
- a claim of DTG/VTC conformance beyond the exact future integration evidence;
- Candidate or Interoperability Tested maturity.

## Maturity path

Experimental is appropriate while the case remains a repository-owned model and acceptance contract. Promotion to Candidate should require an executable positive flow, executable revocation flow, machine-readable decision evidence, negative authorization tests, disclosure-policy tests, documented DTG/VTC mappings and gaps, and reproducible CI.

Promotion beyond Candidate requires actual composition against relevant implementation surfaces rather than mocks or case-local substitutes.

## Next executable increment

After this case contract is reviewed, the next `feat(pdc)` issue should implement the deterministic core: relationship/delegation lifecycle, medication-plan lifecycle, scheduler/reminder lifecycle, one authorization controller, and evidence writer. Real WhatsApp integration remains later work.