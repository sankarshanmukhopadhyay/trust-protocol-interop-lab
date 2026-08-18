---
layout: default
title: Cross-Spec Test Candidates
parent: Standards Intelligence
nav_order: 15
---
# Cross-Specification Pressure-Test Candidates

> **Source acknowledgement:** Initial standards discovery is informed by the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC). GSMI is a discovery source, not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply GSMI/GBBC endorsement.

A candidate is not an Interop Case. Promotion requires pinned baselines, semantic ownership, invariants, scenarios, negative vectors and evidence targets under the lab maturity model.

| ID | Priority | State | Composition | Standards | Suggested owner | Interop Case | Pressure-test question |
|---|---|---|---|---|---|---|---|
| `XSP-001` | **critical** | executed | Verifiable credential issuance → proof → presentation → reliance | `STD-W3C-VC-DM-2`, `STD-W3C-DATA-INTEGRITY`, `STD-OID4VCI`, `STD-OID4VP` | `trust-protocol-interop-lab` | `IC-XSP-001` | Can a verifier preserve issuer authority, credential lifecycle, proof purpose, audience/purpose and relying-party policy as separately testable semantics across the full exchange? |
| `XSP-002` | **critical** | executed | DID resolution × federation metadata × authority | `STD-W3C-DID-CORE`, `STD-W3C-DID-RESOLUTION-1`, `STD-OPENID-FEDERATION-1` | `trust-protocol-interop-lab` | `IC-XSP-002` | When identifiers and federation metadata are resolved successfully, which layer proves identifier control, federation membership, organizational authority and action scope? |
| `XSP-003` | **high** | candidate | ISO mDL × OpenID4VP presentation profile | `STD-ISO-IEC-18013-5`, `STD-OID4VP` | `open-national-digital-trust-framework` | — | Can an mDL presented over OpenID4VP preserve reader/verifier authentication, purpose, consent boundary, minimal disclosure and issuer trust without semantic gaps? |
| `XSP-004` | **high** | candidate | C2PA provenance × CAWG identity assertion × authority | `STD-C2PA`, `STD-CAWG-IDENTITY-ASSERTION` | `trust-protocol-interop-lab` | — | Can content provenance, identity control, lifecycle role and organizational/action authority remain distinguishable when a relying party evaluates a content claim? |
| `XSP-005` | **medium** | candidate | Selective disclosure credential × OpenID4VP privacy boundary | `STD-IETF-SD-JWT-VC`, `STD-OID4VP` | `dtgwg-zkp-tf` | — | What privacy and correlation properties survive when a selectively disclosable credential is repeatedly presented to different verifiers? |
| `XSP-006` | **medium** | candidate | Consent records × portable policy evaluation | `STD-ISO-IEC-27560` | `PolicyMesh` | — | Can a portable consent record remain meaningful when policy, jurisdiction, purpose, controller/processor roles and withdrawal state are evaluated by another system? |
