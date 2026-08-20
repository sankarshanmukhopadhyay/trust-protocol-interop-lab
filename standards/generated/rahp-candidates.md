---
layout: default
title: RAHP Assessment Candidates
parent: Standards Intelligence
nav_order: 14
---
# RAHP Assessment Candidate Register

> **Source acknowledgement:** Standards discovery is informed by registered sources including GSMI/GBBC. Discovery sources are not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply endorsement.

Candidates are triage inputs only. Promotion to a durable RAHP assessment requires explicit target/baseline selection, human review, evidence capture and disposition under the RAHP deployment rules.

| ID | Priority | Candidate | Standards | Portfolio targets | Risk hypothesis |
|---|---|---|---|---|---|
| `RAHP-STD-001` | **critical** | DID resolution confidence must not become authority by implication | `STD-W3C-DID-CORE`, `STD-W3C-DID-RESOLUTION-1` | `governance-authority-assurance-metamodel`, `open-national-digital-trust-framework`, `trust-protocol-interop-lab` | A relying system treats successful or verifiable DID resolution, DID controller status, or resolved verification material as sufficient evidence of registrar, organizational, professional, or action authority. |
| `RAHP-STD-002` | **high** | Federation trust-chain scope versus application authority | `STD-OPENID-FEDERATION-1` | `agent-registry-protocol`, `governance-authority-assurance-metamodel`, `open-national-digital-trust-framework` | A valid federation trust chain or accepted entity metadata is interpreted as authorization for an application-level action outside the federation policy or delegated scope. |
| `RAHP-STD-003` | **critical** | Credential verification-to-reliance boundary | `STD-W3C-VC-DM-2`, `STD-W3C-DATA-INTEGRITY`, `STD-OID4VCI`, `STD-OID4VP` | `open-national-digital-trust-framework`, `trust-systems-meta-model`, `governance-authority-assurance-metamodel` | A technically valid credential issuance/presentation/proof chain is treated as sufficient assurance for a trust decision without validating issuer authority, status, purpose, audience, policy or permitted effect. |
| `RAHP-STD-004` | **high** | mDL presentation, consent and verifier-authority seam | `STD-ISO-IEC-18013-5`, `STD-OID4VP` | `open-national-digital-trust-framework`, `trust-protocol-interop-lab` | A composition correctly authenticates mDL data but lacks explicit controls for consent acquisition, verifier purpose/authority or downstream data-use policy. |
| `RAHP-STD-005` | **high** | Content provenance identity versus role authority | `STD-C2PA`, `STD-CAWG-IDENTITY-ASSERTION` | `governance-authority-assurance-metamodel`, `agent-registry-protocol`, `trust-protocol-interop-lab` | A valid C2PA/CAWG identity assertion is interpreted as proof that the named actor had authority to perform, approve, publish or license the represented action. |
| `RAHP-STD-006` | **medium** | Selective disclosure privacy and holder-binding composition | `STD-IETF-SD-JWT-VC`, `STD-OID4VP` | `dtgwg-zkp-tf`, `open-national-digital-trust-framework`, `trust-systems-meta-model` | Selective disclosure is treated as equivalent to unlinkability or sufficient privacy, while verifier correlation, holder-binding choices, stable issuer metadata or repeated disclosure patterns still permit unwanted linkage. |
| `RAHP-CAND-ISO-23516` | **high** | STD-ISO-TS-23516-2026 | `STD-ISO-TS-23516-2026` | — | A system can satisfy a technical interoperability profile while losing authority, lifecycle or accountability semantics across the composition boundary. |
| `RAHP-CAND-ISO-23644` | **high** | STD-ISO-TR-23644-2023 | `STD-ISO-TR-23644-2023` | — | A technically valid trust anchor is treated as sufficient evidence of governance authority or authorization when those semantics are external to the anchor. |
| `RAHP-CAND-ISO-23635` | **medium** | STD-ISO-TS-23635-2022 | `STD-ISO-TS-23635-2022` | — | Governance guidance is documented but cannot be translated into observable enforcement, revocation, accountability and evidence requirements at runtime. |
