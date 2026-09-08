---
layout: default
title: Evidence & Reproduction
nav_order: 3
nav_exclude: false
permalink: /evidence-assurance/
---
# Evidence & Reproduction

Use this section when the question is **“what does this result prove, and how can I independently inspect or reproduce it?”** This page is a navigation surface; the evidence semantics themselves are canonical in [Evidence model](evidence-model.md).

## Start here

- [Current assurance evidence](current-assurance-evidence.md) — current RAHP/DPIP evidence-producing tranches, immutable OpenVTC pins, residual owners and claim boundaries.
- [Evidence model](evidence-model.md) — evidence-package semantics, provenance, negative evidence, historical reproducibility and bounded conclusions.
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

Interpret the resulting evidence only within the claim boundary defined by the case and [Evidence model](evidence-model.md). Repository-controlled execution does not by itself create certification, production-wide assurance or broader upstream authority.
