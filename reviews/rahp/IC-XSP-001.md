---
layout: default
title: XSP-001 RAHP review
parent: XSP-001 — Credential reliance chain
grand_parent: Assessments
nav_order: 4
---
# RAHP pressure test — IC-XSP-001

## Boundary

Composition-seam assessment only. It does not label VC Data Model, Data Integrity, OpenID4VCI or OpenID4VP unsafe or non-conformant.

## Material harm pathways

| Harm pathway | Failure | Executed control |
|---|---|---|
| Authority laundering | valid issuer proof treated as trusted authority for any claim | `XSP1-NEG-001` |
| Stale reliance | revoked credential accepted | `XSP1-NEG-002` |
| Cross-verifier replay | presentation accepted by unintended verifier | `XSP1-NEG-003` |
| Transaction replay | stale presentation accepted | `XSP1-NEG-004` |
| False verification elevation | invalid proof accepted because other fields look valid | `XSP1-NEG-005` |
| Purpose confusion | incompatible proof purpose treated as adequate | `XSP1-NEG-006` |
| Decision laundering | protocol success overrides local policy | `XSP1-POS-004` proves policy can still deny |

## Disposition

The composition is **assurance-viable with explicit control-plane separation**. No upstream defect is asserted. Deployment profiles should bind issuer-authority policy, status freshness, proof-purpose expectations, verifier audience/nonce, and effect policy into attributable evidence.
