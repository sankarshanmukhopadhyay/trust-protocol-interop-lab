# Trust Protocol Interop Lab

Experimental bindings, profiles, mappings, and interoperability work connecting decentralized trust infrastructure with agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, the Trust Tasks Task Force, the Model Context Protocol project, or any other referenced standards body unless explicitly stated.

## Why this repository exists

Standards-adjacent interoperability work is often spread across issue threads, discussions, working notes, and one-off prototypes. This repository provides a durable place to develop that work without prematurely implying upstream consensus.

The working model is:

**upstream specifications → implementation analysis → mappings/bindings/profiles → experiments/test evidence → candidate upstream feedback → upstream proposal**

## Current work

### Trust Tasks ↔ MCP

The first candidate artifact is an MCP binding for the Trust Tasks Framework:

- [MCP Binding for Trust Tasks v0.2](bindings/trust-tasks/mcp/0.2/spec.md)
- [Architecture note](docs/architecture.md)
- [MCP / Trust Tasks concept mapping](mappings/trust-tasks-mcp.md)
- [Interoperability test plan](experiments/mcp-trust-tasks/test-plan.md)

Baseline:

- Trust Tasks Framework 0.3 (repository baseline dated 2026-08-07)
- MCP 2026-07-28

### TSP-Enabled AI Agent Protocols

The lab now also carries an exploratory implementation and interoperability analysis of the AIMWG TSP-Enabled AI Agent Protocols draft:

- [Implementation analysis 0.1](analysis/tsp-enabled-ai-agents/0.1/README.md)
- [Implementation gap analysis](analysis/tsp-enabled-ai-agents/0.1/implementation-gap-analysis.md)
- [Requirements matrix](analysis/tsp-enabled-ai-agents/0.1/requirements-matrix.md)
- [Interoperability risk register](analysis/tsp-enabled-ai-agents/0.1/interoperability-risk-register.md)
- [TEA / MCP / Trust Tasks mapping](mappings/tea-mcp-trust-tasks.md)
- [Experiment scaffolding](experiments/tsp-enabled-ai-agents/README.md)

Baseline:

- TSP-Enabled AI Agent Protocols v1.0 Draft / Editor's Copy, reviewed 2026-08-10

## Repository structure

```text
analysis/      Implementation-gap analysis and interoperability risk assessment
bindings/      Candidate protocol bindings
mappings/      Cross-protocol concept and semantic mappings
experiments/   Test plans, scenarios, vectors, and observations
proposals/     Upstream-oriented proposal material
docs/          Architecture, terminology, status, and publication model
```

## Artifact maturity

Artifacts progress independently through:

`Exploratory → Experimental → Candidate → Interoperability Tested → Proposed Upstream → Upstreamed / Superseded`

See [STATUS.md](STATUS.md) and [Publication model](docs/publication-model.md).

## Design principles

1. **Do not collapse semantic layers.** Transport, execution, trust, authority, and governance remain distinct unless a referenced specification explicitly binds them.
2. **Upstream remains authoritative.** This repository never silently replaces or reinterprets upstream specifications.
3. **Version the baseline.** Each artifact records the upstream versions against which it was developed.
4. **Test before upstreaming.** Candidate bindings should accumulate examples and interoperability evidence before being proposed as normative upstream text.
5. **Prefer portable evidence.** Protocol convenience must not erase identity, authorization, audit, lifecycle, or provenance semantics.

## Disclaimer

This is an independent research and interoperability workspace maintained by the repository owner. References to standards, specifications, organizations, and projects are descriptive. No affiliation, endorsement, or adoption is implied.

## License

Unless otherwise stated in an individual artifact, repository content is made available under the terms in [LICENSE](LICENSE).
