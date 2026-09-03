# Repository and Artifact Status

## Repository status

**Experimental interoperability assurance workbench**

This repository sits between standards-adjacent design discussion and upstream standardization. Its primary unit is the governed **Interop Case**: a bounded composition with declared baselines, semantic ownership, invariants, scenarios, vectors, and evidence targets.

## Status vocabulary

| Status | Evidence meaning |
|---|---|
| Exploratory | question, components, baselines, and semantic ownership are declared |
| Experimental | invariants and scenarios make the proposed composition testable |
| Candidate | positive/negative vectors, expected behavior, and limitations support structured review |
| Interoperability Tested | reproducible execution results and a validated evidence manifest support the bounded claim |
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
| IC-TT-TSMM-TIS-001 | **Candidate** | Trust Tasks ED 0.3 @ 7e0d755; TSMM v0.23.0; TIS v0.12.0 |
| IC-ARPA-TRQP-HIST-001 | **Candidate** | ARPA v0.9.4; TRQP upstream baseline |
| IC-AGENT-PROVENANCE-AUTH-001 | Candidate | GAAM v0.9.0; TSMM v0.23.0; TIS v0.12.0; ANAB v0.10.0; ARPA v0.9.4; A2A; local CAWG-TRQP agentic baseline; TRQP; DCAS v0.10.0 |
| IC-XSP-001 | **Interoperability Tested** | VC Data Model 2.0; Data Integrity 1.0; OpenID4VCI 1.0; OpenID4VP 1.0 |
| IC-XSP-002 | **Interoperability Tested** | DID Core 1.0; DID Resolution CR 2026-08-06; OpenID Federation 1.0 |
| IC-DTG-PROTECTED-ACCESS-001 | **Candidate** | DTG Credentials/Trust Tasks pinned; local experimental ZKP and DPIP baselines pinned |
| IC-GOVOPS-EXEC-TRUST-001 | **Candidate** | GovOps main @ 3191248 (2026-08-12); TSMM v0.23.0; GAAM v0.9.0; TIS v0.12.0 |
| IC-ARA-REL-001 | **Interoperability Tested** | Trust Tasks 0.5.0; TSP/DTG Credentials/TSMM/TIS pinned; Lab ARA Phases 3–11 |

The machine-readable source of truth is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Claim boundary

`IC-XSP-001`, `IC-XSP-002`, `IC-ARPA-A2A-TT-001`, and `IC-ARA-REL-001` claim **Interoperability Tested** only for their executed semantic-composition reference models. Their evidence packages are now subject to a stronger machine-verifiable gate: the evidence manifest must identify the case, state a bounded claim scope, name a reproducible runner, record a passing result, reference repository-contained evidence artifacts, use valid integrity identifiers where supplied, and contain at least one integrity-bound artifact. This remains repository publication discipline, not independent certification.

For `IC-ARA-REL-001`, the tested claim is specifically **bounded executable semantic composition, adapter-backed at declared boundaries, with adversarial evidence and explicit standards/conformance exclusions**. It does not claim TSP/OpenVTC VTA/RCard/VRC conformance, production security, external certification, legal effect, or standards-native replacement of every adapter.

`IC-DTG-PROTECTED-ACCESS-001`, `IC-TT-TSMM-TIS-001`, and `IC-ARPA-TRQP-HIST-001` are now **Candidate** cases. Each has positive and negative review vectors, expected behaviour and explicit limitations. Candidate maturity means the proposition is structured for review and falsification; it does not inherit a Tested claim from the existence of an evaluator or historical run result.

`IC-GOVOPS-EXEC-TRUST-001` is **Candidate**: its capability/authority/decision/evidence mapping, scenarios, positive/negative vectors, limitations and deterministic evaluator support structured review, but no Tested evidence manifest is yet catalogued.

## Tested evidence gate

`scripts/validate_cases.py` fails closed for `interoperability-tested` claims unless the catalog points to a JSON evidence manifest that:

- matches the Interop Case identifier;
- declares a non-empty bounded `claim_scope`;
- provides a reproducible repository runner command;
- records `result_summary.status: pass`;
- references evidence artifacts that resolve inside this repository;
- validates SHA-256 and Git blob identifiers when present; and
- binds at least one evidence artifact to an integrity identifier.

The validator deliberately accepts both SHA-256 content-addressed packages and Git-blob-addressed executable evidence. This keeps existing tested cases valid while preventing a maturity promotion based only on the presence of an arbitrary evidence file.

## Standards intelligence status

The lab contains **Standards Intelligence v2**: a governed standards-intelligence corpus that separates discovery provenance, standards-body authority metadata, pinned specification baselines, lifecycle monitoring and assurance candidates.

The corpus currently contains **21 tracked standards/specifications**: 12 entries in the core register plus a nine-entry ISO/TC 307 corpus shard. The ISO/TC 307 shard covers vocabulary, reference architecture, taxonomy/ontology, privacy, DLT identity management, smart contracts, interoperability, governance and trust-anchor publications. Every shard entry is canonically verified against ISO publisher pages, has a pinned analysed baseline, records artifact type and lifecycle state, and carries an explicit monitoring posture.

`standards/bodies.yaml` records the institutional class and authority context of standards-development actors. `standards/sources.yaml` separately records GSMI/GBBC discovery context and canonical publisher catalogues. GSMI 6.0 Technical Standards is used as discovery and standards-ecosystem taxonomy context only; it is not a normative source for admitted specifications.

The assurance layer includes ISO/TC 307 RAHP candidates and three cross-specification pressure-test candidates covering reference architecture/interoperability/DID resolution, trust anchors/DID resolution/OpenID Federation, and DLT governance/delegated agent execution. Candidate status creates no interoperability or conformance claim.

The repository runs GitHub Actions assurance CI on pull requests and pushes to `main`, executing catalog, Interop Case, evidence, core standards, Standards Intelligence v2, executable cross-specification and link validation.

**Governance invariant:** discovery is not dependency; mapping is not endorsement; canonical verification is not authority or conformance; cryptographic or technical trust anchors are not automatically governance authority.

### Trust Tasks baseline provenance

Current Trust Tasks-dependent legacy cases remain pinned to editor’s-draft commit `7e0d755f5b815498c861cacecee5cae49b3f14eb` (2026-08-16) where catalogued. The upstream document at that baseline identified itself as version 0.3, so the commit pin is the reproducible baseline; later cases may pin newer explicitly recorded Trust Tasks releases.
