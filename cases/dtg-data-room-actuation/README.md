# DTG Data Room actuation — experimental umbrella composition

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Combine multiple DTG propositions at one consequential actuation boundary and test whether any one credential or proof can substitute for another.
- **Current conclusion:** The semantic umbrella fails closed unless every applicable predicate is current and compatible.
- **External concept:** the public Verifiable Data Rooms concept is informative pressure-test material, not normative DTG architecture.

## Why this matters
Individually sound credentials can compose unsafely. A valid membership credential, delegation, authority credential, and task request may still be insufficient if one predicate is stale, mismatched, over-broad, outside privacy scope, or already consumed.

## Composition in plain language
At the final "should this operation execute now?" boundary, the model separately checks actor/relationship state, membership, delegation, current authority/action scope, hidden-subject binding, governance policy, Trust Task/invocation binding, privacy limits, one-effect/replay state, and freshness of source pins.

No one item can manufacture another.

## Concrete scenario
A delegate asks to read or write a protected Data Room. The request is rejected if authority was withdrawn, delegation revoked, subject binding is missing, the task no longer matches, policy changed, privacy exceeds scope, or the operation was already consumed.

## What was tested
Positive, negative, adversarial, and stale-source vectors were executed. The committed result records that all expected outcomes matched.

Run:
```bash
python experiments/dtg-data-room-actuation/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-data-room-actuation/run-results.json).

## Where it resolved
Consequential DTG actuation should be treated as a **conjunction of independently owned predicates evaluated at the actuation boundary**. Component validity alone does not create an overall PASS.

## What this status means
This is a pre-admission umbrella pressure test, not an admitted DTG profile.

## What remains unresolved
The experiment does not establish MLS correctness, Data Room storage security, native proof interoperability, production unlinkability, or final upstream DTG semantics.
