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
| IC-TT-MCP-001 | Candidate | Trust Tasks 0.3; MCP 2026-07-28 |
| IC-TEA-MCP-TT-001 | Experimental | TEA v1.0 Draft; MCP 2026-07-28; Trust Tasks 0.3 |
| IC-ARPA-A2A-TT-001 | Experimental | ARPA v0.9.4; A2A portfolio reference; Trust Tasks 0.3 |
| IC-TT-TSMM-TIS-001 | Experimental | Trust Tasks 0.3; TSMM v0.23.0; TIS v0.12.0 |
| IC-ARPA-TRQP-HIST-001 | Experimental | ARPA v0.9.4; TRQP upstream baseline |
| IC-AGENT-PROVENANCE-AUTH-001 | Candidate | GAAM v0.9.0; TSMM v0.23.0; TIS v0.12.0; ANAB v0.10.0; ARPA v0.9.4; A2A; local CAWG-TRQP agentic baseline; TRQP; DCAS v0.10.0 |
| IC-XSP-001 | **Interoperability Tested** | VC Data Model 2.0; Data Integrity 1.0; OpenID4VCI 1.0; OpenID4VP 1.0 |
| IC-XSP-002 | **Interoperability Tested** | DID Core 1.0; DID Resolution CR 2026-08-06; OpenID Federation 1.0 |

The machine-readable source of truth is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Claim boundary

`IC-XSP-001` and `IC-XSP-002` now claim **Interoperability Tested** only for their executed semantic-composition reference models. Their evidence packages contain deterministic positive/negative vectors, executed results, reproducibility instructions, manifests, and hashes. This status does **not** claim wire-protocol conformance, production interoperability, external certification, or legal authority. Other cases remain at their existing maturity levels.


## Standards intelligence status

The lab contains an **analysed standards register** with governed source attribution, explicit portfolio relevance, relationship semantics, canonical publisher verification, lifecycle notes, TSMM semantic mappings, GAAM authority mappings, RAHP assessment candidates, and cross-specification pressure-test candidates. GSMI/GBBC is acknowledged as the initial discovery source. All 12 current seed standards have canonical-source verification records; none currently creates a normative portfolio dependency. RAHP entries remain governed candidates. Cross-spec candidates `XSP-001` and `XSP-002` have been promoted to executed Interop Cases with bounded evidence; the remaining cross-spec entries are still candidates.
