# DTG hidden-subject binding — experimental composition evidence

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Prevent independently valid privacy-preserving credentials from being pooled into a joint claim unless the required same-subject or common-control relation is proven.
- **Current conclusion:** Component validity is insufficient; the binding relation must be independently evidenced and context-bound.
- **Source basis:** proposed VAC and VDC work pinned to the upstream proposal commits identified below.

## Why this matters
Privacy-preserving credentials intentionally hide stable identifiers. That creates a composition risk: two individually valid proofs can be combined as though they refer to the same person, delegate, or controller when they do not.

## Composition in plain language
The evaluator asks two separate questions: are the component credentials valid, and is the required relation between their hidden subjects proven? The second cannot be inferred from the first.

The immediate source basis is proposed VAC work in `trustoverip/dtgwg-cred-spec#29` at `84650749afd48798e1c8919a95be359c0367a1c9`, plus proposed VDC work in PR #19 at `ad5876f1b96e2149adec84d37d6595b4a212db9c`.

## Concrete scenario
A verifier receives one valid membership proof and one valid authority proof, both hiding the subject. The combined predicate is accepted only if the proof also establishes the necessary same-subject/common-control relation for this context.

## What was tested
The evaluator covers a positive same-subject case plus mismatched subjects/delegates/controllers, replay into another context, and durable-correlator leakage. All expected outcomes match.

Run:
```bash
python experiments/dtg-hidden-subject-binding/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-hidden-subject-binding/run-results.json).

## Where it resolved
> **A composite hidden-subject predicate is valid only when every component is valid and the required binding relation is independently established for the current context.**

## What this status means
This is semantic composition evidence, not evidence that a production zero-knowledge same-subject/common-control construction has been demonstrated.

## What remains unresolved
Native cryptographic construction, unlinkability guarantees, and final upstream credential semantics remain separate requirements.
