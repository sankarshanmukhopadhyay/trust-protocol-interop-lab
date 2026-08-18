---
layout: default
title: Standards Intelligence Method
parent: Standards Intelligence
nav_order: 5
---
# Standards Intelligence Method

## Purpose

The standards-intelligence layer turns external standards catalogues into governed, reviewable interoperability inputs. It exists to answer **which external specifications matter, why they matter, where they intersect the portfolio, and what evidence is required before relying on them**.

It is not a mirror of any upstream catalogue and it does not convert discovery into authority.

## GSMI acknowledgement

The initial discovery source for this work is the **Global Standards Mapping Initiative (GSMI)**, an initiative of the **Global Blockchain Business Council (GBBC)**. GSMI maintains a technical-standards landscape intended to support understanding and harmonization across blockchain and digital-asset standards activity.

This repository gratefully acknowledges GSMI and GBBC for making that standards-mapping work available as an open discovery resource.

**Authority boundary:** GSMI/GBBC remains authoritative for GSMI materials. Standards bodies and publishers remain authoritative for their specifications. This repository owns only its local selection, mappings, analysis, interoperability evidence, and assurance findings. Inclusion here does not imply endorsement by GSMI, GBBC, or any referenced standards body.

See [`standards/sources.yaml`](sources.yaml) for the machine-readable attribution and source-use policy.

## Pipeline

```text
external catalogue / standards body
            |
            v
      discovery candidate
            |
            v
  canonical-source verification
            |
            v
  local relevance + scope review
            |
            v
      standards register
            |
      +-----+-----+
      |           |
      v           v
 semantic map   assurance candidate
      |           |
      v           v
 Interop Case   RAHP / cross-spec test
      \           /
       \         /
        v       v
       evidence + disposition
```

## Relationship semantics

A standard MUST NOT be described merely as "supported". Each local relationship uses one of the controlled relationships in [`standards/mappings/portfolio.yaml`](mappings/portfolio.yaml): `depends-on`, `profiles`, `implements`, `maps-to`, `compatible-with`, `informs`, `assesses`, `contrasts-with`, `supersedes`, or `out-of-scope`.

Only `depends-on` can create a local normative dependency, and such a claim requires an exact baseline plus repository-level evidence identifying the requirement or conformance profile that creates it.

## Admission states

| State | Meaning | Required evidence |
|---|---|---|
| Candidate | Relevant enough to track | publisher, canonical URI, domain, reason for relevance |
| Mapped | Portfolio relationship is explicit | project lens and relationship type |
| Analysed | Semantic/authority gaps have been reviewed | analysis record or mapping |
| Pressure-tested | Risk/cross-spec assessment exists | durable assessment/evidence reference |
| Retired | No longer tracked as current | reason and replacement/supersession where applicable |

## Relevance scoring

A future automated importer MAY score candidates across architecture, semantics, authority, interoperability, assurance and implementation relevance using values `0..3`. Scores are triage aids only. Human review controls admission and disposition.

Suggested triage bands:

| Score | Default disposition |
|---:|---|
| 0–4 | ignore |
| 5–8 | catalogue |
| 9–12 | map |
| 13–15 | analyse |
| 16–18 | pressure-test |

## Assurance questions

For every materially relevant standard, reviewers should ask:

1. What does the specification actually make verifiable?
2. Which authority does it establish, and which authority does it merely assume?
3. How are delegation and scope represented?
4. How do expiry, suspension, revocation and supersession propagate?
5. Which evidence survives beyond the immediate protocol exchange?
6. Which semantics belong to another specification or governance layer?
7. What failure becomes visible only when this standard is composed with another?
8. What can be tested, and what durable evidence would demonstrate the result?

## Change monitoring

A source change means a mapping **may be stale**. It does not establish a defect. Monitoring should create a review candidate; issue publication remains a governed, human-reviewed action unless a repository explicitly adopts a bounded auto-filing policy.

## Canonical verification contract

Before an entry can be `analysed`, the register records a canonical verification object containing:

- the selected version or draft identifier;
- publisher lifecycle/status;
- a pinned or publisher-stable baseline URI;
- publisher-controlled evidence URIs;
- the verification date; and
- a lifecycle note describing material newer drafts, revisions, expiry, or instability.

Verification is intentionally narrower than assurance. It answers **"what publisher artifact are we analysing?"**, not **"is this sufficient for trust?"**

A baseline MUST NOT automatically advance when an upstream `latest` URI changes. The new upstream version creates a reassessment candidate so mappings and evidence can be reviewed before the local baseline moves.

## TSMM semantic coverage

`standards/mappings/tsmm.yaml` analyses every registered standard against the TSMM v0.23.0 semantic surface used by this lab:

- entity;
- authority;
- delegation;
- policy;
- evidence;
- lifecycle;
- verification;
- trust decision;
- operational effect; and
- runtime governance.

Coverage codes are `D` (direct), `P` (partial), `E` (external or assumed), and `N` (not a core responsibility). These are analytical classifications, not TSMM conformance claims.

## GAAM authority coverage

`standards/mappings/gaam.yaml` analyses the same standards against GAAM v0.9.0 authority and assurance concerns: authority source, delegation, scope, revocation, evidence, assurance, trust decision, effect, accountability, and appeal/remedy.

The purpose is to expose where a technically valid protocol artifact can still leave an authority or governance dependency outside its own scope.

## Candidate promotion gates

The generated RAHP and cross-specification registers deliberately stop short of filing findings or creating Interop Cases.

A **RAHP candidate** requires a separate promotion decision that pins the target baseline, selects a RAHP deployment/review mode, records affected-party and failure hypotheses, produces test evidence, and receives human disposition.

A **cross-specification candidate** requires a separate Interop Case admission decision with pinned component baselines, semantic ownership, invariants, scenarios, negative vectors, expected outcomes, and evidence targets.

This separation keeps standards intelligence useful without turning discovery into issue noise.
