# Protected Delegated Care deterministic experiment

This directory contains the first executable reference slice for `IC-PDC-MED-001`.

It consumes the case-owned acceptance contract at:

```text
cases/protected-delegated-care/scenarios/acceptance.yaml
```

and executes all declared positive, negative, boundary, and privacy scenarios against a deliberately small deterministic application core.

Run:

```bash
python experiments/protected-delegated-care/run.py
```

The repository CI installs PyYAML as an existing validation dependency and runs the same command.

## What is implemented

The reference core models:

- relationship and bounded delegation state;
- human-gated medication-plan approval and activation;
- active/superseded plan enforcement;
- reminder dispatch, timeout, escalation, acknowledgement, and late-ack reconciliation;
- one execution-time authorization controller for delegated caregiver action;
- minimum-disclosure exception payload validation;
- replay and duplicate-channel idempotency;
- contextual relationship references for the P0 privacy profile;
- minimized decision and effect evidence.

The evaluator checks the machine-readable expectations from the case contract rather than maintaining a second test oracle in prose.

## Deliberate boundary

This is a **bounded deterministic reference implementation**. It is application-owned and adapter-backed. It is not evidence that DTG Credentials, Trust Tasks, OpenVTC, DPIP, or a messaging provider already implement these semantics.

In particular, the implementation does not locally fill the unresolved DTG/VTC mappings recorded in `cases/protected-delegated-care/gaps.yaml`. The later integration tranche must replace explicit seams with concrete implementation surfaces and compare observed behavior without changing this acceptance contract merely to make the integration pass.

No real medication, prescription, diagnosis, patient identity, phone number, clinical rule, WhatsApp API, OCR/LLM decision, pharmacy flow, selective-disclosure proof, or ZKP is used here.