---
layout: default
title: Standards × TSMM Semantic Matrix
parent: Standards Intelligence
nav_order: 12
---
# Standards × TSMM Semantic Matrix

> **Source acknowledgement:** Initial standards discovery is informed by the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC). GSMI is a discovery source, not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply GSMI/GBBC endorsement.

Baseline: `v0.23.0`. TSMM is the canonical semantic model; this lab mapping is informative analysis and does not modify TSMM.

`D` = direct; `P` = partial; `E` = external-or-assumed; `N` = not-core-responsibility. These values are analytical coverage classifications, not claims of conformance.

| Standard | Entity/actor semantics | Authority source and bounded authority | Delegation and lineage | Policy context/evaluation | Evidence semantics | Lifecycle state/change | Technical verification | Relying-party trust decision | Authorized/observed effect | Runtime governance/enforcement | Key boundary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `STD-C2PA` | D | P | E | P | D | D | D | P | D | P | Provenance/authenticity can establish what was signed and preserved; human/organizational authority and downstream reliance remain separate governance questions. |
| `STD-CAWG-IDENTITY-ASSERTION` | D | P | E | P | D | P | D | P | P | P | Control over a digital identity and asserted lifecycle role should not be treated as unrestricted authority outside the governed role/credential context. |
| `STD-IETF-SD-JWT-VC` | P | E | E | E | D | P | D | E | E | E | Selective disclosure and holder binding improve credential privacy/integrity but do not supply external authority, policy or remedy semantics. |
| `STD-ISO-IEC-18013-5` | D | P | E | P | D | P | D | P | E | P | mDL authenticity and holder binding do not cover how holder consent is obtained and do not by themselves settle relying-party authorization. |
| `STD-ISO-IEC-27560` | D | P | E | D | D | D | P | E | E | P | A consent record is evidence of recorded consent state; whether processing is authorized remains dependent on legal/policy context and lifecycle correctness. |
| `STD-OID4VCI` | P | P | E | P | D | P | D | E | P | P | Issuance transport and authorization do not by themselves establish the legal/governance authority for the claims being issued or downstream reliance. |
| `STD-OID4VP` | P | P | E | P | D | P | D | P | E | P | Presentation protocol verification remains subordinate to credential-format semantics, verifier policy, purpose limitation and authority evaluation. |
| `STD-OPENID-FEDERATION-1` | D | P | P | D | D | D | D | P | E | P | Federation membership and trusted metadata chains are not automatically equivalent to authority for an application-specific action or effect. |
| `STD-W3C-DATA-INTEGRITY` | P | E | E | E | D | P | D | E | E | E | Cryptographic authenticity/integrity is evidence about a proof, not evidence that the signer was authorized to make the underlying claim or effect. |
| `STD-W3C-DID-CORE` | D | P | P | E | P | P | D | E | E | E | Identifier control and verification relationships must not be promoted into registrar, organizational, professional or action authority without another authority source. |
| `STD-W3C-DID-RESOLUTION-1` | P | E | E | E | D | D | D | E | E | P | Successful/verifiable resolution establishes technical resolution confidence within a DID method, not the external governance authority of the DID controller. |
| `STD-W3C-VC-DM-2` | D | E | E | E | D | P | P | E | E | E | Credential validity and issuer/holder/verifier roles do not by themselves establish the issuer’s real-world authority, relying-party policy, or permitted effect. |
