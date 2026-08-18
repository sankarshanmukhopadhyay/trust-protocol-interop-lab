---
layout: default
title: XSP-002 RAHP review
parent: XSP-002 — DID/federation authority chain
grand_parent: Assessments
nav_order: 4
---
# RAHP pressure test — IC-XSP-002

## Boundary

Composition-seam assessment only. It does not assert that DID Core, DID Resolution, or OpenID Federation is unsafe or non-conformant.

## Material harm pathways

| Harm pathway | Failure | Executed control |
|---|---|---|
| Identifier-control laundering | resolved DID treated as organizational authority | `XSP2-NEG-001` |
| Membership laundering | federation membership treated as action scope | `XSP2-NEG-002` |
| Stale identifier reliance | deactivated DID remains actionable | `XSP2-NEG-003` |
| Stale federation reliance | expired trust chain accepted | `XSP2-NEG-004` |
| Resolution failure bypass | federation evidence masks failed resolution | `XSP2-NEG-005` |
| Untraceable authority | effect cannot be traced to authority source | `XSP2-NEG-006` |
| Authority expansion | metadata policy widens source-granted scope | `XSP2-NEG-007` |

## Disposition

The composition is **assurance-viable only with explicit authority-source and scope evidence**. OpenID Federation can prove membership in a federation rooted at a selected trust anchor and derive policy-constrained metadata; DID resolution can provide identifier/controller state. The relying application must still bind those signals to a separately legitimate authority source and permitted effect.
