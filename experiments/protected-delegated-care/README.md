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

## Runnable application demonstrator

A dependency-free local web demonstrator now exposes the application-owned semantics through a small API and browser UI:

```bash
python experiments/protected-delegated-care/app.py
```

Open <http://127.0.0.1:8080/>.

The demonstrator starts directly in the canonical synthetic exception state. It has three visible surfaces:

- **Principal** — inspect and revoke the bounded caregiver delegation, reset the synthetic scenario, or deliberately remove authority evidence to pressure-test the fail-closed boundary.
- **Caregiver** — inspect only the minimum-disclosure exception payload and request a bounded re-reminder.
- **Evidence** — inspect authorization, revocation, and effect records emitted by the deterministic core.

A useful manual walkthrough is:

1. select **Request re-reminder** and observe `PERMIT` plus one `re_reminder_scheduled` effect;
2. select **Revoke delegation**;
3. select **Request re-reminder** again and observe `DENY · AUTHORITY_REVOKED` with no additional reminder effect;
4. select **Reset demo**, then **Remove authority evidence** and request again to observe `INDETERMINATE · MISSING_AUTHORITY_EVIDENCE`.

The HTTP layer does not implement a second authorization path. Every consequential caregiver request creates a fresh bounded task and calls `CareCore.execute_exception_response()`, which re-evaluates current authority immediately before effect.

Run the prototype regression tests with:

```bash
cd experiments/protected-delegated-care
python -m unittest -v test_app.py
```

The tests cover the permit → revoke → deny sequence, missing-authority-evidence handling, minimum caregiver disclosure, evidence production, deterministic reset, and malformed/oversized JSON input. `.github/workflows/pdc-demo.yml` runs the same checks for relevant pull requests and pushes to `main`.

### Prototype boundary

The browser/API surface is an adoption demonstrator, not a new assurance claim. It remains synthetic and application-owned. It does not resolve the upstream generic delegated-action evaluator gap, provider/network/device confidentiality, Trust Task document-proof versus authenticated-transport semantics, or real selective-disclosure/ZKP construction recorded by the case assurance decision.

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
