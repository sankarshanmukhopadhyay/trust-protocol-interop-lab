# Credential → Trust Task → actuation — bounded current evidence

## At a glance

- **Status:** Bounded experimental evidence for issue #163; not an integrated OpenVTC conformance claim.
- **Case:** `IC-DTG-CREDENTIAL-TASK-ACTUATION-001`.
- **Purpose:** Pressure-test the credential → Trust Task → consequential-actuation seam to the boundary that current source-pinned implementation and Lab evidence can actually support.
- **RAHP propositions:** P03, P04, P05, P08 and P09.
- **Terminal classifications:** `supported`, `divergent`, `not-implemented`, and `not-observable`.

The experiment is intentionally allowed to terminate with unresolved surfaces. A missing integrated evaluator is evidence about the implementation boundary; it is not permission to manufacture a passing end-to-end path.

See the executable [scenario](scenario.yaml), the [evidence producer](../../experiments/dtg-credential-task-actuation/run.py), and the [contract tests](../../tests/test_credential_task_actuation.py).

## Why this matters

A credential, a delegation or representation artifact, a Trust Task, and possession of a key or capability are not interchangeable grants of consequential authority. The assurance question is whether those independently governed inputs remain bounded when they meet at the point where a system would actually cause an effect.

That seam is especially important for RAHP because component-level success can otherwise be accidentally promoted into a portfolio-level claim. The case therefore asks not merely whether individual structures validate, but whether current authority, representation, exact task semantics, presenter/subject/relationship binding, replay behavior, and any independently administered capability envelope remain distinct at actuation time.

The source epoch is pinned in `scenario.yaml`. Upstream repositories are treated as read-only evidence inputs. The Lab owns only the experiment, classifications, and evidence adapter.

## Concrete scenario

An actor presents otherwise valid credential and delegation material while attempting a consequential Trust Task. The expected positive path requires current authority, valid representation where representation is required, and exact task/invocation binding. The negative vectors remove or perturb one independently necessary condition at a time.

The nine vectors cover: a positive integrated actuation control; withdrawn current authority; missing representation; action outside scope; presenter/subject/relationship mismatch; invocation mismatch; duplicate or replayed consequential requests; key or capability possession without action-specific authority; and authority without a separately required capability envelope.

Run the bounded evidence producer with:

```bash
python experiments/dtg-credential-task-actuation/run.py
```

Validate its machine-readable contract with:

```bash
python -m unittest tests.test_credential_task_actuation
```

CI executes both operations and publishes the generated JSON as the `credential-task-actuation-evidence` artifact.

## Where it resolved

The current evidence can resolve several negative propositions by reusing the existing VDC/VAC action-time evidence within its established claim boundary. In particular, withdrawn authority is not replaced by delegation, required representation is not replaced by authority, narrower or revoked delegation fails closed, invocation mismatch fails closed, and possession of a weaker capability surface is not promoted into action-specific authority.

The case does **not** treat those bounded results as proof of a complete consuming implementation. The positive integrated current-authority evaluator is classified `not-implemented`. The presenter/subject/relationship actuation seam and consequential replay effect counter are classified `not-observable` where no target-native surface is available. The independently administered capability-envelope boundary is likewise `not-implemented` when the current integrated actuation path does not expose it.

This produces a useful assurance result even without an end-to-end PASS: known negative boundaries remain attributable, while absent implementation and observability remain explicit evidence gaps.

## Evidence and auditability

The machine-readable result records the exact source epoch, all nine vector identifiers, per-vector classification, observed bounded outcome, effect-count status, RAHP proposition coverage, and an explicit anti-promotion claim boundary. The producer delegates existing authority semantics to the established action-time experiment instead of creating a second competing authority model.

This separation is deliberate. Semantic-fixture evidence, Lab actuation evidence, component-runtime evidence, and target-native integrated evidence have different authority and assurance scopes. Consumers, including a future RAHP clean-room producer, can therefore distinguish what executed from what remains absent or unobservable.

## What remains unresolved

Current evidence does not establish a target-native integrated positive path in which current authority, representation/delegation, exact Trust Task semantics and consequential effect are evaluated together. It also does not establish an integrated presenter/subject/relationship binding decision at actuation, a target-native one-effect replay counter, or an independently administered capability-envelope decision where the current implementation exposes no such boundary.

Those are legitimate terminal outcomes for issue #163 at this source epoch. They should remain `not-implemented` or `not-observable` until a real upstream or target implementation surface exists. Future source changes can trigger a new evidence run and reclassification; they must not retroactively enlarge the claims made by this case.
