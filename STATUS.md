# Repository and Artifact Status

## Repository status

**Experimental interoperability assurance workbench**

This repository sits between standards-adjacent design discussion and upstream standardization. Its primary unit is now the governed **Interop Case**: a bounded composition with declared baselines, semantic ownership, invariants, scenarios, vectors, and evidence targets.

## Status vocabulary

| Status | Evidence meaning |
|---|---|
| Exploratory | question, components, baselines, and semantic ownership are declared |
| Experimental | invariants and scenarios make the proposed composition testable |
| Candidate | positive/negative vectors, expected behavior, and limitations support structured review |
| Interoperability Tested | reproducible execution results and evidence manifest support the bounded claim |
| Proposed Upstream | evidence is linked to an exact upstream proposal/discussion |
| Upstreamed | authoritative upstream outcome is recorded |
| Superseded | historical baseline retained but replaced by newer work |

See [Evidence-Gated Maturity Model](docs/maturity-model.md).

## Current cases

| Case | Status | Baseline summary |
|---|---|---|
| IC-TT-MCP-001 | Candidate | Trust Tasks ED 0.3 @ 7e0d755; MCP 2026-07-28 |
| IC-TEA-MCP-TT-001 | Experimental | TEA v1.0 Draft; MCP 2026-07-28; Trust Tasks ED 0.3 @ 7e0d755 |
| IC-ARPA-A2A-TT-001 | **Interoperability Tested** | ARPA v0.9.5; ANAB v0.10.0; A2A v1.0; Trust Tasks ED 0.3 @ 7e0d755 |
| IC-TT-TSMM-TIS-001 | Experimental | Trust Tasks ED 0.3 @ 7e0d755; TSMM v0.23.0; TIS v0.12.0 |
| IC-ARPA-TRQP-HIST-001 | Experimental | ARPA v0.9.4; TRQP upstream baseline |
| IC-AGENT-PROVENANCE-AUTH-001 | Candidate | GAAM v0.9.0; TSMM v0.23.0; TIS v0.12.0; ANAB v0.10.0; ARPA v0.9.4; A2A; local CAWG-TRQP agentic baseline; TRQP; DCAS v0.10.0 |
| IC-XSP-001 | **Interoperability Tested** | VC Data Model 2.0; Data Integrity 1.0; OpenID4VCI 1.0; OpenID4VP 1.0 |
| IC-XSP-002 | **Interoperability Tested** | DID Core 1.0; DID Resolution CR 2026-08-06; OpenID Federation 1.0 |
| IC-GOVOPS-EXEC-TRUST-001 | Experimental | GovOps main @ 3191248 (2026-08-12); TSMM v0.23.0; GAAM v0.9.0; TIS v0.12.0 |

The machine-readable source of truth is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Claim boundary

`IC-XSP-001`, `IC-XSP-002`, and `IC-ARPA-A2A-TT-001` claim **Interoperability Tested** only for their executed semantic-composition reference models. Their evidence packages contain deterministic positive/negative vectors, executed results, reproducibility instructions, manifests, and hashes. This status does **not** claim wire-protocol conformance, production interoperability, external certification, or legal authority. Other cases remain at their existing maturity levels.

`IC-GOVOPS-EXEC-TRUST-001` is **Experimental** only: its capability/authority/decision/evidence mapping and seven scenario contracts make the Discussion #6 invariants testable, but no executable vectors or interoperability evidence have yet been published.

## Standards intelligence status

The lab now contains **Standards Intelligence v2**: a governed standards-intelligence corpus that separates discovery provenance, standards-body authority metadata, pinned specification baselines, lifecycle monitoring and assurance candidates.

The corpus currently contains **21 tracked standards/specifications**: 12 entries in the core register plus a nine-entry ISO/TC 307 corpus shard. The ISO/TC 307 shard covers vocabulary, reference architecture, taxonomy/ontology, privacy, DLT identity management, smart contracts, interoperability, governance and trust-anchor publications. Every shard entry is canonically verified against ISO publisher pages, has a pinned analysed baseline, records artifact type and lifecycle state, and carries an explicit monitoring posture.

`standards/bodies.yaml` records the institutional class and authority context of standards-development actors. `standards/sources.yaml` separately records GSMI/GBBC discovery context and canonical publisher catalogues. GSMI 6.0 Technical Standards is used as discovery and standards-ecosystem taxonomy context only; it is not a normative source for admitted specifications.

The assurance layer includes ISO/TC 307 RAHP candidates and three new cross-specification pressure-test candidates covering reference architecture/interoperability/DID resolution, trust anchors/DID resolution/OpenID Federation, and DLT governance/delegated agent execution. Candidate status creates no interoperability or conformance claim.

The repository now runs GitHub Actions assurance CI on pull requests and pushes to `main`, executing catalog, Interop Case, evidence, core standards, Standards Intelligence v2, executable cross-specification and link validation.

**Governance invariant:** discovery is not dependency; mapping is not endorsement; canonical verification is not authority or conformance; cryptographic or technical trust anchors are not automatically governance authority.

### Trust Tasks baseline provenance

Current Trust Tasks-dependent cases are pinned to editor’s-draft commit `7e0d755f5b815498c861cacecee5cae49b3f14eb` (2026-08-16). The upstream document still identifies itself as version 0.3, so the commit pin is the reproducible baseline; older MCP binding v0.2 remains the immutable 2026-08-07 baseline.
