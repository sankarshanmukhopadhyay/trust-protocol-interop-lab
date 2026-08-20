---
layout: default
title: Standards × GAAM Authority Matrix
parent: Standards Intelligence
nav_order: 13
---
# Standards × GAAM Authority Matrix

> **Source acknowledgement:** Standards discovery is informed by registered sources including GSMI/GBBC. Discovery sources are not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply endorsement.

Baseline: `v0.9.0`. GAAM remains authoritative for GAAM semantics; this lab matrix is an informative crosswalk.

`D` = direct; `P` = partial; `E` = external-or-assumed; `N` = not-core-responsibility. These values are analytical coverage classifications, not claims of conformance. Corpus entries without an explicit mapping remain intentionally unmapped until reviewed.

| Standard | Authority source | Delegation | Scope/constraints | Revocation/suspension | Evidence | Assurance/verification | Trust decision | Operational effect | Accountability/audit | Appeal/remedy | Key boundary |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `STD-C2PA` | P | E | P | D | D | D | P | D | D | E | Provenance/authenticity can establish what was signed and preserved; human/organizational authority and downstream reliance remain separate governance questions. |
| `STD-CAWG-IDENTITY-ASSERTION` | P | E | D | P | D | D | P | P | D | E | Control over a digital identity and asserted lifecycle role should not be treated as unrestricted authority outside the governed role/credential context. |
| `STD-IETF-SD-JWT-VC` | E | E | P | P | D | D | E | E | P | E | Selective disclosure and holder binding improve credential privacy/integrity but do not supply external authority, policy or remedy semantics. |
| `STD-ISO-IEC-18013-5` | P | E | P | P | D | D | P | E | P | E | mDL authenticity and holder binding do not cover how holder consent is obtained and do not by themselves settle relying-party authorization. |
| `STD-ISO-IEC-27560` | P | E | D | D | D | P | E | E | D | P | A consent record is evidence of recorded consent state; whether processing is authorized remains dependent on legal/policy context and lifecycle correctness. |
| `STD-OID4VCI` | P | E | D | P | D | D | E | P | P | E | Issuance transport and authorization do not by themselves establish the legal/governance authority for the claims being issued or downstream reliance. |
| `STD-OID4VP` | P | E | D | P | D | D | P | E | P | E | Presentation protocol verification remains subordinate to credential-format semantics, verifier policy, purpose limitation and authority evaluation. |
| `STD-OPENID-FEDERATION-1` | P | P | D | P | D | D | P | E | D | E | Federation membership and trusted metadata chains are not automatically equivalent to authority for an application-specific action or effect. |
| `STD-W3C-DATA-INTEGRITY` | E | E | P | E | D | D | E | E | P | E | Cryptographic authenticity/integrity is evidence about a proof, not evidence that the signer was authorized to make the underlying claim or effect. |
| `STD-W3C-DID-CORE` | P | P | P | P | P | D | E | E | P | E | Identifier control and verification relationships must not be promoted into registrar, organizational, professional or action authority without another authority source. |
| `STD-W3C-DID-RESOLUTION-1` | E | E | P | P | D | D | E | E | D | E | Successful/verifiable resolution establishes technical resolution confidence within a DID method, not the external governance authority of the DID controller. |
| `STD-W3C-VC-DM-2` | P | E | P | P | D | P | E | E | P | E | Credential validity and issuer/holder/verifier roles do not by themselves establish the issuer’s real-world authority, relying-party policy, or permitted effect. |
