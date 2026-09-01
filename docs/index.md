---
layout: default
title: Trust Protocol Interop Lab
nav_order: 1
nav_exclude: false
permalink: /
---
# Trust Protocol Interop Lab

A governed workbench for testing whether independently authoritative trust protocols and artifacts compose **without semantic loss, authority inflation, or evidence ambiguity**.

The lab is organised around **Interop Cases**. Each case states a bounded composition question, pins the relevant baselines, identifies semantic ownership, defines claims and invariants, executes positive and negative scenarios where maturity permits, and preserves evidence for independent review.

## Choose your path

| You want to… | Start here | What you should get |
|---|---|---|
| Understand what has actually been tested | [Cases & Assessments](assessments.md) | Complete case estate, maturity, bounded claims and direct case entry points |
| Inspect evidence or reproduce a result | [Evidence & Reproduction](evidence-and-assurance.md) | Evidence model, manifests, review records and reproduction paths |
| Understand external standards used by the lab | [Standards Intelligence](standards-intelligence.md) | Verified baselines, authority metadata, mappings and assessment candidates |
| Understand how the lab reasons about interoperability | [Methods & Architecture](methods.md) | Semantic ownership, interoperability model, maturity gates and boundary taxonomy |
| Understand authority, status and contribution rules | [Governance & Status](governance-status.md) | Governance boundaries, current repository state and contribution path |

## The lab in one flow

```text
external specifications / portfolio artifacts
                    ↓
          governed Interop Case
                    ↓
     semantic ownership + invariants
                    ↓
      positive / negative scenarios
                    ↓
       executable or review evidence
                    ↓
       bounded maturity / assurance claim
                    ↓
      upstream proposal when warranted
```

The important separation is intentional: **discovery is not authority; mapping is not interoperability; execution is not certification; and a local result cannot enlarge the normative scope of an upstream specification**.

## Current evidence-bearing estate

The current case estate includes credential-reliance, DID/federation authority, governed agent discovery, agent relationship architecture, Trust Tasks/MCP composition, historical resolution, protected-access privacy, agentic provenance and GovOps executable-trust work. Several cases are now locally **Interoperability Tested** for their explicitly bounded semantic-composition claims; others remain Candidate or Experimental pending further evidence.

[Browse all current cases and their status](assessments.md).

## What is intentionally *not* in the sidebar

Experiment phases, scenarios, vectors, generated matrices, mappings, raw evidence, implementation notes and historical baselines are still published and searchable. They are reached through the case or method that gives them meaning rather than being exposed as independent top-level destinations.

This keeps the site useful as the repository grows without weakening traceability or evidence preservation.
