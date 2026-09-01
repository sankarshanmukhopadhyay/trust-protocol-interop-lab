---
layout: default
title: Evidence & Reproduction
nav_order: 3
nav_exclude: false
permalink: /evidence-assurance/
---
# Evidence & Reproduction

Use this section when the question is **“what does this result prove, and how can I independently inspect or reproduce it?”**

## Evidence path

```text
case claim
   ↓
scenario / vector
   ↓
execution or structured review
   ↓
result + manifest + hashes
   ↓
reproduction instructions
   ↓
review / assurance disposition
```

A result is only as strong as the evidence needed to falsify it. Missing runtime or boundary evidence remains missing evidence; it is not converted into a pass.

## Start here

- [Evidence model](evidence-model.md) — what evidence artifacts mean and how claims bind to them.
- [Evidence packages](../evidence/README.md) — case-specific manifests and retained outputs.
- [RAHP review register](../reviews/rahp/README.md) — pressure reviews and assurance dispositions.
- [Interoperability readiness](interoperability-readiness.md) — which cases have crossed which evidence gates.
- [Publication model](publication-model.md) — how local evidence is exposed without overstating authority.

## Reproducing a case

1. Open the case from [Cases & Assessments](assessments.md).
2. Confirm its pinned baselines and bounded claim.
3. Follow the case reproduction instructions or executable runner referenced by that case.
4. Compare the produced outputs with the retained evidence manifest and hashes.
5. Read any RAHP/adversarial review before interpreting the maturity label.

## Claim boundary

`Interoperability Tested` requires reproducible evidence for the bounded claim that was actually executed. Semantic reference-model testing does **not** become wire-protocol conformance, production security, legal authority, certification or complete upstream implementation merely because vectors pass.
