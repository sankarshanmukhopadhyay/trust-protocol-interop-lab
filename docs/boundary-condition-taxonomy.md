---
layout: default
title: DTG Boundary-Condition Taxonomy
parent: Methods & Architecture
nav_order: 7
---
# DTG Boundary-Condition Taxonomy

This analysis turns difficult real-world scenarios into reusable architectural pressure conditions before the lab admits an executable Interop Case or proposes an upstream change.

The source scenario set currently covers three distinct pressure axes:

- protected-person confidential service access;
- child protection, care, adoption and transition to majority;
- incapacity, emergency authority, recovery and death.

These are **boundary scenarios, not vertical DTG profiles**. They do not define how shelters, adoption, guardianship, health care, succession, or any jurisdiction must operate. Their purpose is to expose conditions that a composed trust flow may need to survive.

The machine-readable source is [`analysis/dtg-boundary-conditions/0.1/taxonomy.yaml`](../analysis/dtg-boundary-conditions/0.1/taxonomy.yaml).

## Why a taxonomy exists

Without an intermediate taxonomy, a scenario can too easily produce a speculative component issue: a difficult fact pattern is observed, one repository appears related, and an implementation requirement is inferred before the portfolio has been tested as a composition.

The lab instead uses this path:

```text
boundary scenario Discussion
        ↓
reusable boundary condition
        ↓
portfolio capability evidence
        ↓
minimal vertical slice
        ↓
executable Interop Case
        ↓
observed result / finding
        ↓
upstream issue where justified
        ↓
remediation and rerun
```

A boundary condition therefore describes **what the composed system must be able to distinguish or preserve**, not which component must implement the answer.

## Core distinctions

The current scenario set repeatedly demonstrates that the following concepts cannot safely collapse into one another:

```text
relationship existence
≠ relationship validity
≠ current authority
≠ delegated authority
≠ authorization
≠ disclosure permission
≠ discoverability
≠ historical truth
≠ assurance
```

Likewise, lifecycle events need not be semantically equivalent:

```text
expiry ≠ suspension ≠ revocation ≠ supersession ≠ termination
```

An implementation may use common status machinery for more than one event, but the lab must preserve the different consequences when a scenario depends on them.

## Boundary conditions v0.1

| ID | Condition | What the lab tests |
|---|---|---|
| `BC-AUTH-PROVENANCE` | Authority provenance | Why an actor is authorised and what source/rule establishes it |
| `BC-BOUNDED-DELEGATION` | Bounded delegation | Whether delegated action remains constrained by scope, purpose, time and context |
| `BC-CURRENT-AUTHORITY` | Current authority | Whether operative authority can be separated from older valid evidence |
| `BC-HISTORICAL-TRUTH` | Historical truth | Whether earlier valid states remain auditable without granting present authority |
| `BC-SUPERSESSION` | Supersession | Whether a later authoritative state can govern future decisions without erasing history |
| `BC-STATE-TERMINATION` | Lifecycle termination distinctions | Whether expiry, suspension, revocation, supersession and termination retain meaningful differences |
| `BC-STATE-TRANSITION` | Explicit state transition | Whether the applicable state and the event that changed it are attributable |
| `BC-CONFLICTING-AUTHORITY` | Conflicting authority | Whether contradictory current-state assertions are surfaced rather than silently resolved |
| `BC-MINIMUM-DISCLOSURE` | Minimum disclosure | Whether a relying party receives only the information needed for its legitimate decision |
| `BC-NON-DISCOVERABILITY` | Protected relationship non-discoverability | Whether a proof creates an unintended relationship-enumeration path |
| `BC-CORRELATION-RESISTANCE` | Correlation resistance | Whether normal artifacts introduce avoidable cross-context correlators |
| `BC-TEMPORAL-VALIDITY` | Temporal validity | Whether valid-at-T1 and valid-now are distinguishable |
| `BC-REPLAY-RESISTANCE` | Replay resistance across state change | Whether old presentations fail safely after relevant state changes |
| `BC-RECOVERY` | Authority recovery and restoration | Whether temporary authority ends cleanly and the applicable authority state resumes |
| `BC-REDRESS` | Redress and correction | Whether incorrect or contested states can be challenged, corrected and evidenced |

The definitions and test questions in the YAML file are authoritative for this repository version.

## Use rules

### 1. Keep conditions jurisdiction-neutral

A condition may be discovered through an adoption or shelter scenario, but its definition should remain useful in unrelated domains such as enterprise delegation, disaster response, agent authority, fiduciary representation, or cross-border service delivery.

### 2. Do not infer semantic ownership from relevance

A component may contribute evidence to a condition without owning the condition. For example, selective-disclosure proof construction may contribute to minimum disclosure, while the composed flow can still leak an issuer, status endpoint, registry identifier or task artifact.

### 3. Unknown does not mean missing

If the lab has not established what an upstream specification says or how implementations compose, the correct classification is `unclear`. A gap requires evidence.

### 4. Preserve negative semantics

The taxonomy exists partly to test things that must **not** happen: historical authority must not become current authority; proof must not become discovery; possession must not become authority; and cryptographic verification must not become a relying-party authorization decision.

### 5. Promote only through evidence

A boundary condition can nominate an experiment. It cannot by itself create a finding, defect claim, upstream requirement, or interoperability claim.

## Versioning

The taxonomy is expected to evolve as additional scenarios expose genuinely reusable conditions. New scenario-specific language should not be added unless it can be normalized into a testable architectural distinction.

The next analytical layer is the [DTG Portfolio Capability Matrix](dtg-portfolio-capability-matrix.md).
