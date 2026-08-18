---
layout: default
title: XSP-001 semantic ownership map
parent: XSP-001 — Credential reliance chain
grand_parent: Assessments
nav_order: 2
---
# XSP-001 semantic ownership map

| Semantic | Upstream owner | Composition obligation |
|---|---|---|
| Credential claims, validity period, status hook | VC Data Model | preserve without treating claim validity as issuer trust |
| Proof verification, verification method, proof purpose | VC Data Integrity | expose verification outcome and purpose |
| Issuance authorization and credential delivery | OpenID4VCI | preserve issuance context; do not extend it into later relying authority |
| Presentation request, verifier binding, nonce/state | OpenID4VP | validate audience and transaction freshness |
| Issuer authority for claim/purpose | Deployment governance | evaluate independently |
| Final decision/effect | Relying party | record policy and decision authority |

## Non-substitution rule

No successful lower-layer operation upgrades another control plane. In particular: proof validity ≠ issuer authority; issuance authorization ≠ relying authorization; successful presentation ≠ permission to produce an effect.
