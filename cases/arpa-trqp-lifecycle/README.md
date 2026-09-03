# IC-ARPA-TRQP-HIST-001 — ARPA to TRQP lifecycle and historical resolution

## At a glance

| Item | Current state |
|---|---|
| **Status** | Candidate |
| **Purpose** | Test whether agent authority state can be exposed through a read-only trust-registry query without changing who owns that authority or rewriting historical truth. |
| **Current conclusion** | Current state and historical state must be explicitly separated, and the TRQP projection must remain informative rather than authoritative. |
| **Evidence today** | Ownership, invariants, scenarios, positive/negative vectors, and limitations exist. No executed interoperability evidence manifest exists yet. |

## Why this matters

Agent authority is time-dependent. An agent may have been authorized yesterday and revoked today. A verifier may need either answer: **what is true now?** or **what was true at the time of an earlier action?**

If a read-only registry projection answers those questions without preserving time and provenance, it can create serious governance errors. A later revocation could incorrectly erase a legitimate historical action, or an old authorization could be mistaken for current authority.

## The composition in plain language

**ARPA (Agent Registry Protocol)** is the authority/lifecycle source in this case. It represents agent registration, authority state, revocation, and historical lifecycle.

**TRQP (Trust Registry Query Protocol)** is used as a read-only query surface. It helps a verifier ask for trust/authority-related information, but it must not become the source that creates or rewrites ARPA authority.

\`\`\`text
ARPA authoritative lifecycle state
          |
          v
read-only TRQP projection
          |
          v
verifier interpretation for a specified time
\`\`\`

## Concrete scenario

Assume an agent was authorized on 1 August, performed an action on 10 August, and was revoked on 20 August.

A verifier on 25 August may legitimately ask:

- "Is this agent authorized now?" → **No**.
- "Was this agent authorized on 10 August?" → potentially **Yes**, if the historical record supports it.

The projection must not turn today's revocation into "the agent was never authorized", and it must not turn the historical authorization into permission for a new action today.

## What this case is testing

The case protects four boundaries: **authoritative state vs projection state**, **current vs requested-time state**, **historical truth vs present consequence**, and **missing evidence vs success**.

See [ownership.yaml](ownership.yaml), [invariants.yaml](invariants.yaml), and the [scenario set](scenarios/).

## Where it resolved

The current design-time result supports the proposition that ARPA can be projected into a TRQP-facing read model **provided the requested time and provenance remain explicit**.

The vectors include a positive historical case where authority was active at the relevant time and later revoked, and a negative case that rejects rewriting the historical record merely because the current state changed.

This is a **Candidate** result, not an executed interoperability claim.

## Evidence and next gate

Inspect the [current-state query](scenarios/01-current-query.md), [as-of query](scenarios/02-as-of-query.md), [later revocation](scenarios/03-later-revocation.md), [vectors](vectors/), and [known limitations](known-limitations.md).

The next maturity gate is to execute the vectors against a reproducible implementation or adapter path and produce an evidence manifest bound to the exact ARPA/TRQP baselines.

## What remains unresolved

The current case does not yet establish live-query interoperability, cryptographic authenticity of projected records, production registry synchronization, or cross-implementation behavior.
