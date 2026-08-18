# Trust Protocol Interop Lab

Experimental compositions, bindings, profiles, mappings, negative tests, and interoperability evidence connecting decentralized trust infrastructure with agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, the Trust Tasks Task Force, the Model Context Protocol project, or any other referenced standards body unless explicitly stated.

## Mission

The lab is the **experimental integration and interoperability-assurance layer** for independently governed trust protocols and artifacts. It asks a deliberately stronger question than “can these systems exchange messages?”:

> **Can these components compose without losing authority, delegation, lifecycle, evidence, provenance, correlation, or accountability semantics?**

The working model is:

**upstream specifications → bounded Interop Case → semantic ownership + invariants → positive/negative scenarios → experiment evidence → candidate upstream feedback**

## Start here

- **[Rendered documentation home](docs/index.md)** — task-oriented entry point for GitHub Pages.
- **[Assessments](docs/assessments.md)** — executed and in-progress Interop Cases.
- **[Standards Intelligence](docs/standards-intelligence.md)** — GSMI-informed discovery, canonical verification, semantic/authority matrices, and pressure-test pipeline.
- **[Evidence & Assurance](docs/evidence-and-assurance.md)** — evidence packages, RAHP reviews, claim boundaries, and readiness.
- **[Methods & Architecture](docs/methods.md)** — interoperability model, semantic ownership, maturity, architecture, and publication governance.
- **[Repository and artifact status](STATUS.md)** — machine-readable status translated for maintainers.

## Current interoperability cases

| Case | Composition | Status |
|---|---|---|
| `IC-TT-MCP-001` | Trust Tasks ↔ MCP | Candidate |
| `IC-TEA-MCP-TT-001` | TEA/TSP ↔ MCP ↔ Trust Tasks | Experimental |
| `IC-ARPA-A2A-TT-001` | ARPA ↔ A2A ↔ Trust Tasks | Experimental |
| `IC-TT-TSMM-TIS-001` | Trust Tasks ↔ TSMM ↔ TIS | Experimental |
| `IC-ARPA-TRQP-HIST-001` | ARPA ↔ TRQP lifecycle/historical resolution | Experimental |
| `IC-AGENT-PROVENANCE-AUTH-001` | Agent identity ↔ authority ↔ provenance ↔ TRQP ↔ assurance | Candidate |
| `IC-XSP-001` | VC Data Model ↔ Data Integrity ↔ OpenID4VCI ↔ OpenID4VP ↔ relying policy | **Interoperability Tested (semantic scope)** |
| `IC-XSP-002` | DID Core ↔ DID Resolution ↔ OpenID Federation ↔ authority | **Interoperability Tested (semantic scope)** |

The authoritative registry is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Existing versioned artifacts

The original work remains available at stable paths:

- [MCP Binding for Trust Tasks v0.2](bindings/trust-tasks/mcp/0.2/spec.md)
- [MCP / Trust Tasks mapping](mappings/trust-tasks-mcp.md)
- [TSP-Enabled AI Agent Protocols analysis 0.1](analysis/tsp-enabled-ai-agents/0.1/README.md)
- [TEA / MCP / Trust Tasks mapping](mappings/tea-mcp-trust-tasks.md)
- [Agentic provenance and authority mapping](mappings/agentic-provenance-authority.md)

## Standards intelligence

The [`standards/`](standards/README.md) layer turns external standards catalogues into governed discovery, mapping, and assurance inputs. Its initial discovery source is the **Global Standards Mapping Initiative (GSMI)**, an initiative of the **Global Blockchain Business Council (GBBC)**. We gratefully acknowledge GSMI/GBBC for maintaining an open standards-mapping resource. GSMI is used as a discovery source only: canonical standards publishers remain authoritative, and inclusion here does not imply GSMI/GBBC endorsement.

The register records explicit relationship semantics such as `maps-to`, `informs`, `assesses`, and `depends-on`; only an explicit, evidenced `depends-on` relationship can create a local normative dependency. Commit 2 adds publisher-controlled baseline verification, lifecycle tracking, TSMM semantic coverage, GAAM authority coverage, RAHP assessment candidates, and cross-specification pressure-test candidates. Generated views expose these analyses without converting catalogue discovery or cryptographic verification into conformance, authority, compatibility, or endorsement claims.

## Portfolio-aware experimentation

The [`observatory/`](observatory/README.md) accepts convergence and change signals from systems such as `dtg-portfolio-monitor`. Signals can nominate interoperability questions, but they **cannot automatically admit cases or create interoperability claims**. Human review retains that authority.

Consequential cases may also receive a [RAHP pressure-test review](reviews/rahp/README.md) to connect protocol seam failures to affected-party harms and testable prevention, detection, evidence, and redress controls.

## Repository structure

```text
catalog/       Machine-readable component and Interop Case registries
cases/         Governed multi-protocol compositions, invariants, scenarios and vectors
analysis/      Versioned implementation-gap analysis
bindings/      Candidate protocol bindings
mappings/      Cross-protocol semantic mappings
experiments/   Experiment plans and scaffolding
evidence/      Executed, portable interoperability evidence
observatory/   Candidate interoperability signals from portfolio monitoring
reviews/       RAHP and other pressure-test reviews
schemas/       Machine-readable lab governance/evidence contracts
standards/     Governed external-standards discovery, mappings and generated portfolio views
proposals/     Upstream-oriented proposal material
docs/          Architecture, maturity, evidence and publication guidance
scripts/       Deterministic repository validation and readiness generation
```

## Validation

```bash
python scripts/validate_catalog.py
python scripts/validate_cases.py
python experiments/xsp-001/run.py
python experiments/xsp-002/run.py
python scripts/validate_evidence.py
python scripts/validate_standards.py
python scripts/generate_standards.py
python scripts/generate_readiness.py
python scripts/check_links.py
```

A passing validation run demonstrates that repository maturity claims have the required local supporting artifacts. It does not constitute independent interoperability certification.

## Governance boundary

Upstream remains authoritative. The lab owns only its experimental compositions, evidence, findings, and maturity claims. See [GOVERNANCE.md](GOVERNANCE.md).

## License

Unless otherwise stated in an individual artifact, repository content is made available under the terms in [LICENSE](LICENSE).
