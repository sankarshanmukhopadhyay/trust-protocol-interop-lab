---
layout: default
title: Standards Intelligence Method
nav_order: 8
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
