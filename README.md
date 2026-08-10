# Trust Protocol Interop Lab

Experimental bindings, profiles, mappings, and interoperability work connecting decentralized trust infrastructure with agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, the Trust Tasks Task Force, the Model Context Protocol project, or any other referenced standards body unless explicitly stated.

## Why this repository exists

Standards-adjacent interoperability work is often spread across issue threads, discussions, working notes, and one-off prototypes. This repository provides a durable place to develop that work without prematurely implying upstream consensus.

The working model is:

**existing standards → candidate mappings/bindings → experiments/test evidence → upstream proposal**

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

## Repository structure

```text
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
