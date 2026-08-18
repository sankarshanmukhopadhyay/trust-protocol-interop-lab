---
layout: default
title: Maturity Model
parent: Methods & Architecture
nav_order: 30
---
# Evidence-Gated Maturity Model

Maturity applies to each Interop Case independently.

| Status | Minimum repository evidence |
|---|---|
| Exploratory | registered case, bounded question, baselines, semantic ownership |
| Experimental | exploratory requirements plus invariants and scenarios |
| Candidate | experimental requirements plus positive and negative vectors, expected behavior, known limitations |
| Interoperability Tested | candidate requirements plus executed results, reproducibility instructions, evidence manifest, and an explicit claim scope |
| Proposed Upstream | tested or otherwise evidence-supported case plus exact upstream proposal/discussion reference |
| Upstreamed | recorded authoritative upstream outcome |
| Superseded | replacement or baseline change recorded while historical evidence is retained |

For semantic composition cases, an executable reference evaluator can satisfy the execution gate when the claim is explicitly bounded to semantic interoperability. It does not establish wire-protocol conformance.

The validator rejects status claims that lack the minimum local evidence. The gate is intentionally conservative: it checks whether supporting artifacts exist and are structurally valid, not whether an external party independently agrees with the result.
