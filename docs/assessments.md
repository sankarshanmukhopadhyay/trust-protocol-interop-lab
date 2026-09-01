---
layout: default
title: Cases & Assessments
nav_order: 2
nav_exclude: false
permalink: /assessments/
---
# Cases & Assessments

**Interop Cases are the primary unit of work in the lab.** Start here when you want to know what question was tested, which artifacts were composed, how mature the work is, and where the evidence lives.

## Current admitted case estate

| Case | Status | Composition focus |
|---|---|---|
| [IC-XSP-001](../cases/xsp-001/README.md) | **Interoperability Tested** | Credential reliance chain across VC/Data Integrity/OpenID4VCI/OpenID4VP |
| [IC-XSP-002](../cases/xsp-002/README.md) | **Interoperability Tested** | DID resolution, federation membership, authority and action scope |
| [IC-ARPA-A2A-TT-001](../cases/arpa-a2a-trust-tasks/README.md) | **Interoperability Tested** | Governed agent discovery, name assurance, A2A and Trust Task execution |
| [IC-ARA-REL-001](../cases/ara-minimum-executable-relationship/README.md) | **Interoperability Tested** | Minimum executable agent relationship, lifecycle and adversarial assurance |
| [IC-TT-MCP-001](../cases/trust-tasks-mcp/README.md) | Candidate | Trust Tasks carried over MCP |
| [IC-AGENT-PROVENANCE-AUTH-001](../cases/agentic-provenance-authority/README.md) | Candidate | Provenance, delegated verification and authority composition |
| [IC-TEA-MCP-TT-001](../cases/tea-mcp-trust-tasks/README.md) | Experimental | TSP-enabled agents, MCP and Trust Tasks |
| [IC-TT-TSMM-TIS-001](../cases/trust-tasks-tsmm-tis/README.md) | Experimental | Runtime assurance composition across Trust Tasks, TSMM and TIS |
| [IC-ARPA-TRQP-HIST-001](../cases/arpa-trqp-lifecycle/README.md) | Experimental | ARPA/TRQP lifecycle and historical resolution |
| [IC-GOVOPS-EXEC-TRUST-001](../cases/govops-executable-trust/README.md) | Experimental | GovOps capability, authority, decision, enforcement and evidence composition |

The machine-readable source of truth for admitted cases is [`catalog/interoperability-cases.yaml`](../catalog/interoperability-cases.yaml).

## Pre-admission work

[IC-DTG-PROTECTED-ACCESS-001](../cases/dtg-protected-access/README.md) is currently **pre-admission construction**, not an admitted Interop Case. It is an executable-ready protected-person confidential-service boundary slice and intentionally makes no upstream conformance or implementation claim.

Keeping pre-admission work separate prevents a directory or executable fixture from being mistaken for a governed maturity claim.

## How to read a case

Use this sequence rather than navigating individual artifact files directly:

1. **Question and claim boundary** — what composition proposition is actually under test?
2. **Pinned baselines and semantic ownership** — which source owns each meaning or rule?
3. **Invariants and scenarios** — what must remain true, including negative/adversarial cases?
4. **Execution and evidence** — what ran, what outputs were produced, and can they be reproduced?
5. **Maturity** — what evidence-backed status is justified, and what remains explicitly unproven?

## Supporting views

- [Interoperability readiness](interoperability-readiness.md) — generated/readable portfolio maturity view.
- [Maturity model](maturity-model.md) — evidence gates and status vocabulary.
- [Evidence & Reproduction](evidence-and-assurance.md) — evidence packages, review records and claim discipline.

Statuses are **local evidence claims**, not external certification.
