# Trust Protocol Interop Lab

Experimental compositions, bindings, profiles, mappings, negative tests, and interoperability evidence connecting decentralized trust infrastructure with agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, the Trust Tasks Task Force, the Model Context Protocol project, GovOpsWG, or any other referenced standards body unless explicitly stated.

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
| [`IC-TT-MCP-001`](cases/trust-tasks-mcp/README.md) | Trust Tasks ↔ MCP | Candidate |
| [`IC-TEA-MCP-TT-001`](cases/tea-mcp-trust-tasks/README.md) | TEA/TSP ↔ MCP ↔ Trust Tasks | Experimental |
| [`IC-ARPA-A2A-TT-001`](cases/arpa-a2a-trust-tasks/README.md) | ARPA ↔ ANAB ↔ A2A ↔ Trust Tasks | **Interoperability Tested (semantic scope)** |
| [`IC-TT-TSMM-TIS-001`](cases/trust-tasks-tsmm-tis/README.md) | Trust Tasks ↔ TSMM ↔ TIS | Candidate |
| [`IC-ARPA-TRQP-HIST-001`](cases/arpa-trqp-lifecycle/README.md) | ARPA ↔ TRQP lifecycle/historical resolution | Candidate |
| [`IC-AGENT-PROVENANCE-AUTH-001`](cases/agentic-provenance-authority/README.md) | Agent identity ↔ authority ↔ provenance ↔ TRQP ↔ assurance | Candidate |
| [`IC-XSP-001`](cases/xsp-001/README.md) | VC Data Model ↔ Data Integrity ↔ OpenID4VCI ↔ OpenID4VP ↔ relying policy | **Interoperability Tested (semantic scope)** |
| [`IC-XSP-002`](cases/xsp-002/README.md) | DID Core ↔ DID Resolution ↔ OpenID Federation ↔ authority | **Interoperability Tested (semantic scope)** |
| [`IC-GOVOPS-EXEC-TRUST-001`](cases/govops-executable-trust/README.md) | GovOps capability ↔ TSMM ↔ GAAM ↔ TIS | Candidate |
| [`IC-ARA-REL-001`](cases/ara-minimum-executable-relationship/README.md) | Trust Tasks ↔ TEA/TSP ↔ ARPA ↔ DTG Credentials ↔ TSMM ↔ TIS | **Interoperability Tested (bounded semantic scope)** |
| [`IC-DPAC-ACTUATION-001`](cases/dpac-actuation/README.md) | TEA/TSP ↔ GovOps ↔ GAAM actuation boundary | Experimental |

The authoritative registry is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Worked real-world case: governed loan approval

`IC-GOVOPS-EXEC-TRUST-001` uses a deliberately ordinary but consequential enterprise action to make executable-governance boundaries concrete: a bank exposes a capability to **approve a loan**, and a delegated credit officer attempts to exercise it.

The capability is only the operation being requested:

```yaml
capability_id: govops:loan:approve
operation:
  action: approve
  resource: loan
```

That does not answer whether the officer is authorized to approve this particular loan. The case walks the request through distinct governance states:

```text
GovOps capability
  → request/principal context
  → GAAM authority and delegation checks
  → GovOps/PDP policy decision
  → execution admission
  → observed runtime effect
  → TIS portable evidence
  → later assurance
```

A representative path is a credit officer with delegated approval authority up to INR 5,000,000 attempting to approve an INR 3,500,000 loan within the applicable product and jurisdiction. Valid delegation is an input to authorization, not an `Allow` decision by itself. The GovOps/PDP policy layer still decides whether the transaction may proceed. If admitted, the resulting loan-status transition must be correlated to the exact authorization decision, and TIS evidence can record what happened without becoming a new source of authority.

The same model exercises the more important failure cases: an INR 7,500,000 request exceeds delegated authority; a revoked delegation cannot authorize a new action; a post-execution revocation does not erase historical evidence of an earlier valid decision; an unrelated database update cannot be presented as the authorized effect; and a later positive assurance result cannot retroactively turn a denied action into an authorized one.

This is the practical purpose of the lab: to make boundaries such as **capability ≠ authority ≠ authorization ≠ execution ≠ evidence ≠ assurance** observable and testable across independently governed systems. See the [GovOps executable-trust case](cases/govops-executable-trust/README.md) and its [mapping](mappings/govops-executable-trust.md).

## Existing versioned artifacts

The original work remains available at stable paths:

- [MCP Binding for Trust Tasks v0.3](bindings/trust-tasks/mcp/0.3/spec.md)
- [MCP / Trust Tasks mapping](mappings/trust-tasks-mcp.md)
- [TSP-Enabled AI Agent Protocols analysis 0.1](analysis/tsp-enabled-ai-agents/0.1/README.md)
- [TEA / MCP / Trust Tasks mapping](mappings/tea-mcp-trust-tasks.md)
- [Agentic provenance and authority mapping](mappings/agentic-provenance-authority.md)
- [GovOps executable trust mapping](mappings/govops-executable-trust.md)

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
python experiments/dpac-actuation/run.py
python experiments/xsp-001/run.py
python experiments/xsp-002/run.py
python experiments/arpa-a2a-anab/run.py
python scripts/validate_evidence.py
python scripts/validate_standards.py
python scripts/validate_standards_v2.py
python scripts/generate_standards.py
python scripts/generate_readiness.py
python scripts/check_links.py
```

A passing validation run demonstrates that repository maturity claims have the required local supporting artifacts. It does not constitute independent interoperability certification.

## Governance boundary

Upstream remains authoritative. The lab owns only its experimental compositions, evidence, findings, and maturity claims. See [GOVERNANCE.md](GOVERNANCE.md).

## License

Unless otherwise stated in an individual artifact, repository content is made available under the terms in [LICENSE](LICENSE).
