# Interoperability Cases — reader guide

This directory is the quickest way to understand what the Trust Protocol Interop Lab is actually testing.

An **Interop Case** is a bounded, falsifiable composition of independently governed specifications, protocols, governance models, or implementation artifacts. The Lab does not make those upstream components authoritative over one another. Instead, each case asks a narrower systems question: **when these pieces are combined, do authority, delegation, capability, policy, lifecycle, evidence, privacy, effect, and assurance semantics remain intact?**

## How to read a case

Each case README is intended to stand on its own. Start with the **At a glance** section and then read:

1. **Why this matters** — the failure mode or ambiguity that motivated the case.
2. **The composition in plain language** — what each component contributes.
3. **Concrete scenario** — the smallest useful mental model.
4. **What is being tested** — the separations and invariants the case protects.
5. **Where it resolved** — what the Lab currently believes the evidence supports.
6. **Evidence / reproduction** — what was actually executed or reviewed.
7. **What remains unresolved** — the boundary beyond which the current claim must not be stretched.

The authoritative maturity and component registry remains [`catalog/interoperability-cases.yaml`](../catalog/interoperability-cases.yaml). This page is a reader-oriented guide, not a second source of truth.

## What the maturity labels mean

| Status | Reader interpretation |
|---|---|
| **Experimental** | The proposition is admitted for exploration. Evidence may be executable, but the claim is still deliberately narrow and may depend on self-authored models or proposed upstream semantics. |
| **Candidate** | The composition has stable ownership, invariants, scenarios/vectors, and structured evidence sufficient for serious review. It is **not** yet an executed cross-implementation interoperability claim. |
| **Interoperability Tested** | The bounded claim has reproducible executed evidence that satisfies the Lab's Tested gate. The label applies only to the exact claim boundary documented by that case; it does not imply certification, production security, or blanket standards conformance. |
| **Pre-admission experimental evidence** | A pressure-test artifact exists under `cases/`, but it has not been admitted into the authoritative Interop Case catalog. Its purpose is usually to test a proposed upstream change or a narrow semantic risk before deciding whether a full case is warranted. |

## Admitted Interop Cases

### Interoperability Tested

| Case | What it is trying to establish |
|---|---|
| [ARA — Minimum Executable Agent Relationship](ara-minimum-executable-relationship/) | Whether a consequential agent relationship remains legitimate when identity, authority, agreement, policy, capability, task semantics, protected signing, counterparty decision, lifecycle, effect, and evidence are separately enforced. |
| [ARPA × A2A × Trust Tasks](arpa-a2a-trust-tasks/) | Whether discovery, name/operator assurance, reported actor lineage, authority, Trust Task semantics, and effect admission can compose without identity or attribution metadata becoming authority. |
| [XSP-001 — Credential reliance chain](xsp-001/) | Whether issuer authority, credential lifecycle, proof validity, presentation binding, and relying-party authorization remain distinct from issuance through reliance. |
| [XSP-002 — DID/federation authority chain](xsp-002/) | Whether DID resolution and federation membership can contribute evidence without being mistaken for organizational authority or action-specific permission. |

### Candidate

| Case | What it is trying to establish |
|---|---|
| [Trust Tasks over MCP](trust-tasks-mcp/) | Whether MCP can carry Trust Task execution while Trust Tasks retain work identity, authorization boundaries, lifecycle control, replay protection, and evidence semantics. |
| [Trust Tasks × TSMM × TIS](trust-tasks-tsmm-tis/) | Whether Trust Task runtime events can be represented and packaged as governance/evidence artifacts without collapsing task state, decision, and effect. |
| [ARPA → TRQP lifecycle](arpa-trqp-lifecycle/) | Whether current and historical agent-authority state can be projected for read-only verification without rewriting history or confusing projection state with authoritative state. |
| [Agentic provenance and delegated verification](agentic-provenance-authority/) | Whether agent identity, delegated authority, content provenance, registry verification, and later assurance can compose without any of them silently becoming decision authority. |
| [DTG protected-person confidential service access](dtg-protected-access/) | Whether a person can prove a narrow entitlement while keeping the provider, relationship, case, and durable correlators hidden across the whole observable interaction. |
| [GovOps executable trust](govops-executable-trust/) | Whether a governed capability can move through authority, policy, enforcement, execution, evidence, and assurance without those stages collapsing into one another. |

### Experimental

| Case | What it is trying to establish |
|---|---|
| [TEA/TSP × MCP × Trust Tasks](tea-mcp-trust-tasks/) | Whether authenticated agent exchange, execution mechanics, delegated authority, and portable Trust Task semantics can coexist without one layer taking ownership of another. |
| [Dual-Path Actuation Control](dpac-actuation/) | Whether a consequential action can occur only when current action-specific authority and an independently administered capability envelope concur at the actuation boundary. |

## Pre-admission DTG pressure-test evidence

These directories are intentionally not represented as admitted cases in the catalog. They exist to test proposed or evolving DTG semantics and to keep upstream uncertainty visible.

| Evidence track | Question |
|---|---|
| [DTG VDC × VAC composition](dtg-vdc-vac-composition/) | Does delegation/representation remain distinct from authority? |
| [DTG VAC attenuation](dtg-vac-attenuation/) | Can delegated/derived authority only become narrower, never broader, and remain current? |
| [DTG hidden-subject binding](dtg-hidden-subject-binding/) | Can independently valid hidden-subject credentials be combined only when their same-subject/common-control relation is actually proven? |
| [DTG cross-governance action vocabulary](dtg-action-vocabulary/) | Does lexical equality of an action token remain distinct from a governed semantic mapping across domains? |
| [DTG Data Room actuation](dtg-data-room-actuation/) | Do the individual DTG control predicates still hold when combined at one consequential actuation boundary? |

## A recurring rule across the estate

Many cases differ in protocol and domain, but they repeatedly defend one architectural principle:

```text
identity != authority
delegation != authority
capability != authority
authority != authorization
authorization != enforcement
enforcement != effect
evidence != authority
assurance != retroactive authorization
```

The exact set differs by case, but the Lab treats these distinctions as executable governance boundaries rather than documentation conventions.
