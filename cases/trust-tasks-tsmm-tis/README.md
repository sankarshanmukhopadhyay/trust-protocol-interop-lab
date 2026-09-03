# IC-TT-TSMM-TIS-001 — Trust Task runtime assurance composition

## At a glance

| Item | Current state |
|---|---|
| **Status** | Candidate |
| **Purpose** | Test whether Trust Task runtime activity can be represented in TSMM governance semantics and packaged through TIS without task state, trust decision, and effect admission becoming the same thing. |
| **Current conclusion** | The semantic projection is reviewable and falsifiable, but execution evidence has not yet been produced. |
| **Evidence today** | Ownership, invariants, scenarios, positive/negative vectors, and limitations. |

## Why this matters

A runtime system often wants one convenient "status" field. Governance systems cannot safely do that when the status is expected to answer several different questions: what state is the work in, was the actor authorized, what trust decision was made, was a consequential effect admitted, and what evidence proves any of those facts?

Collapsing those questions can make an audit record appear to authorize an action merely because the task later completed successfully.

## The composition in plain language

**Trust Tasks** owns the semantics and lifecycle of the work instance.

**TSMM (Trust Systems Meta-Model)** supplies a portable semantic grammar for authority, decision, evidence, revocation, supersession, and effect.

**TIS (Trust Interchange Specification)** supplies portable machine-readable contracts for carrying the resulting artifacts.

\`\`\`text
Trust Task event
   -> TSMM-governed semantic interpretation
   -> TIS-compatible evidence / decision artifact
\`\`\`

The translation must not change who owns the task state or invent authority that was not present at runtime.

## Concrete scenario

A Trust Task reaches a point immediately before a consequential effect. The runtime re-evaluates authority and denies the effect.

A portable evidence package should be able to state all of these at once: the task existed and reached that lifecycle point; the trust/authorization decision was deny; the effect was not admitted; and the evidence records that denial.

It must not summarize the task as "completed successfully" and thereby erase the denied effect decision.

## What this case is testing

The current scenarios exercise [runtime receipt projection](scenarios/01-runtime-receipt.md), [denied effect](scenarios/02-denied-effect.md), [evidence portability](scenarios/03-evidence-portability.md), pre-effect authority re-evaluation, duplicate-execution protection, semantic task control, partial-application disposition, and fail-closed behavior.

See [invariants.yaml](invariants.yaml), [ownership.yaml](ownership.yaml), and [vectors](vectors/).

## Where it resolved

The current design supports a clean separation:

\`\`\`text
task state != trust decision != effect admission != evidence artifact
\`\`\`

That is the Candidate result. The Lab has enough structured material to review and pressure-test the composition, but not yet an executed evidence package.

## Evidence and next gate

Inspect [known limitations](known-limitations.md), scenarios, vectors, and the ownership/invariant files in this directory.

The next gate is a reproducible runner plus an evidence manifest linking each conclusion to the exact vectors, invariants, ownership declarations, limitations, and pinned baselines.

## What remains unresolved

No live TSMM/TIS provider or wire-level exchange is exercised yet. Cryptographic integrity, independent implementation behavior, and production evidence persistence remain outside the current claim.
