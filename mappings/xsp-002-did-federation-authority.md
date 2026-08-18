---
layout: default
title: XSP-002 semantic ownership map
parent: XSP-002 — DID/federation authority chain
grand_parent: Assessments
nav_order: 2
---
# XSP-002 semantic ownership map

| Semantic | Upstream owner | Composition obligation |
|---|---|---|
| DID/controller material | DID Core | do not infer legal or organizational identity solely from controller data |
| Resolution result + metadata | DID Resolution | expose current/deactivated/error state and freshness |
| Federation membership + metadata policy | OpenID Federation | preserve trust anchor, chain validity, expiry and resolved policy |
| Organizational/role authority | Deployment governance | provide an attributable authority source |
| Delegated action scope | Authority/delegation layer | enforce scope attenuation and current state |
| Final decision/effect | Relying party | keep local policy explicit |

## Non-substitution rule

DID resolution success ≠ organizational authority. Federation membership ≠ unrestricted action authority. Resolved federation metadata may constrain or inform an application decision, but cannot silently expand the authority granted by its authoritative source.
