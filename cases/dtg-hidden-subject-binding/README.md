# DTG hidden-subject binding — experimental composition evidence

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Prevent independently valid privacy-preserving credentials from being pooled into a joint claim unless the required same-subject or common-control relation is proven.
- **Current conclusion:** Component validity and identifier association are insufficient; the binding relation must be independently evidenced and context-bound.
- **Source basis:** adopted Credential Spec WD02 at `67149716032318f7f29770e5d3e6f0d35e52b8c3`, with current OpenVTC implementation-boundary observation at `72bf5794071971da506eb7a5af8e4765c35c137c`.

## Why this matters
Privacy-preserving credentials intentionally hide stable identifiers. That creates a composition risk: two individually valid proofs can be combined as though they refer to the same person, delegate, or controller when they do not. WD02 still depends on common-control/shared-subject propositions whose full proof construction remains unresolved upstream.

## Composition in plain language
The evaluator asks separate questions: are the component credentials valid, and is the required relation between their hidden subjects proven? The second cannot be inferred from the first. Proof of control over one identifier also cannot be promoted into proof of control over another identifier or into a reusable subject-equivalence assertion.

The WD02 source basis is VDC PR #19 merged as `37074bdcd861c51f3e5b7868ce700832b17b73ce` and VAC PR #29 merged as `4f7e66b6dfcd8eddc212c8002351a6ad814c60e1`.

Current OpenVTC relationship/persona implementation explicitly documents the same boundary: a VPC does not itself bind a persona identifier to the relationship DID, and request-level proof of control is used without claiming that it resolves Credential Spec #9. That is implementation evidence that the unresolved boundary is being preserved, not a normative solution to common control.

## Concrete scenario
A verifier receives individually valid membership, delegation or authority evidence whose subjects are hidden or represented by different identifiers. The combined predicate is accepted only if evidence separately establishes the required same-subject/common-control relation for this context.

## What was tested
The evaluator covers a positive explicitly-bound case and negative cases for mismatched hidden subjects/delegates/controllers, context replay, durable-correlator leakage, identifier association without proof, proof of one identifier promoted to another, and request-level proof-of-possession promoted into credential-level subject equivalence.

Run:
```bash
python experiments/dtg-hidden-subject-binding/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-hidden-subject-binding/run-results.json).

## Where it resolved
> **A composite hidden-subject/common-control predicate is valid only when every component is valid and the required binding relation is independently established for the current context.**

## What this status means
This is semantic composition evidence against adopted WD02 plus a source-pinned implementation-boundary observation. It is not evidence that a production zero-knowledge same-subject/common-control construction has been demonstrated.

## What remains unresolved
A native cryptographic common-control/same-subject construction, target-runtime proof interoperability, and any upstream normative resolution of Credential Spec #9 remain separate requirements. Missing proof remains `EVIDENCE_REQUIRED` / `INDETERMINATE`; it becomes an assurance failure only where an implementation incorrectly admits a claim or action without the required proof.
