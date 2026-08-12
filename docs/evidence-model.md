---
layout: default
title: Evidence Model
---
# Interoperability Evidence Model

Evidence records what was actually exercised. It must remain narrower than the claim it supports.

## Evidence package

An `evidence-manifest.json` identifies the case, baseline, execution timestamp when applicable, test/vector references, implementation or runner identity, result summary, and integrity references for generated artifacts.

## Evidence principles

1. **Provenance before assertion.** A result points to the scenario and vector that produced it.
2. **Negative evidence matters.** Fail-closed behavior and prohibited inferences are first-class tests.
3. **Session independence.** Where the case claims portable evidence, verification must not require the original transport session.
4. **Historical reproducibility.** Baselines and fixtures must remain identifiable after upstream changes.
5. **Bounded conclusions.** Repository-controlled tests are not independent certification or universal interoperability claims.

## Evidence consumers

Evidence may support local maturity, upstream feedback, portfolio assurance, regression checks, or a later independent assessment. Those consumers remain responsible for deciding whether the evidence is sufficient for their own assurance claim.
