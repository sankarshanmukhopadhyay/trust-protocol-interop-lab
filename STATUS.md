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

The machine-readable source of truth is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml).

## Claim boundary

No case currently claims `Interoperability Tested`. Repository-controlled scenarios and vectors are preparation and candidate evidence until an executed, reproducible evidence package is recorded.
