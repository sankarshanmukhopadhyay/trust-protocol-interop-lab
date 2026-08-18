---
layout: default
title: Canonical Verification
nav_order: 11
---
# Canonical Source Verification

> **Source acknowledgement:** Initial standards discovery is informed by the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC). GSMI is a discovery source, not normative authority. Canonical publishers remain authoritative. Inclusion here does not imply GSMI/GBBC endorsement.

Every entry is verified against publisher-controlled sources and pinned to a deliberate baseline. A newer draft does not automatically move the portfolio baseline.

| Standard | Baseline | Publisher status | Publication | Verified | Lifecycle note |
|---|---|---|---|---|---|
| `STD-C2PA` | `2.4` | Current C2PA specification set | not recorded | 2026-08-18 | Pinned to current C2PA Specifications 2.4. C2PA establishes content provenance/authenticity mechanisms; semantic authority for a human or organization may depend on companion assertions, trust lists, governance and relying-party policy. |
| `STD-CAWG-IDENTITY-ASSERTION` | `1.2` | DIF Ratified Specification | 2025-12-15 | 2026-08-18 | Stable Identity Assertion 1.2 baseline. CAWG also publishes 1.3 working drafts; implementers needing a stable specification are directed to 1.2. |
| `STD-IETF-SD-JWT-VC` | `draft-ietf-oauth-sd-jwt-vc-16` | IETF Internet-Draft — intended Standards Track | 2026-04-24 | 2026-08-18 | Work in progress, not an RFC. Draft -16 expires 2026-10-26 unless replaced or advanced. The underlying SD-JWT mechanism is published separately as RFC 9901. |
| `STD-ISO-IEC-18013-5` | `ISO/IEC 18013-5:2021` | Published International Standard | 2021-09 | 2026-08-18 | Published baseline is under revision and a Draft International Standard for the next version is in development. Holder-consent acquisition and private-key storage requirements are outside the published baseline scope. |
| `STD-ISO-IEC-27560` | `ISO/IEC TS 27560:2023` | Published Technical Specification | 2023-08 | 2026-08-18 | Published baseline is marked by ISO as to be revised. It models consent record information and lifecycle; it does not by itself establish every legal basis or authorization decision. |
| `STD-OID4VCI` | `1.0` | OpenID Final Specification | 2025-09-16 | 2026-08-18 | Final Specification. The specification itself references some pre-final dependencies at pinned revisions, so downstream profiles must not assume dependency versions can be substituted without review. |
| `STD-OID4VP` | `1.0` | OpenID Final Specification | 2025-07-10 | 2026-08-18 | Final Specification. Credential-format semantics remain external to the presentation protocol and must be evaluated through the selected format/profile. |
| `STD-OPENID-FEDERATION-1` | `1.0` | OpenID Final Specification | 2026-02-17 | 2026-08-18 | Final Specification. Federation trust chains establish governed metadata trust but do not by themselves prove every application-level authority or permitted effect. |
| `STD-W3C-DATA-INTEGRITY` | `1.0` | W3C Recommendation | 2025-05-15 | 2026-08-18 | Stable Recommendation baseline. W3C has also published Data Integrity 1.1 as a Working Draft; the local baseline remains 1.0 until reviewed. |
| `STD-W3C-DID-CORE` | `1.0` | W3C Recommendation | 2022-07-19 | 2026-08-18 | Stable Recommendation baseline. DID Core v1.1 is on the W3C Recommendation track; mappings remain pinned to v1.0 until deliberately reviewed. |
| `STD-W3C-DID-RESOLUTION-1` | `1.0` | W3C Candidate Recommendation Snapshot | 2026-08-06 | 2026-08-18 | Candidate Recommendation baseline. DID URL dereferencing is explicitly marked at risk; implementation experience can still change the specification. |
| `STD-W3C-VC-DM-2` | `2.0` | W3C Recommendation | 2025-05-15 | 2026-08-18 | Stable Recommendation baseline. W3C also publishes Verifiable Credentials Data Model v2.1 as a Working Draft; this register does not silently move the baseline. |
