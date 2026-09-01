---
layout: default
title: Interop Case landing-page contract
---
# Interop Case landing-page contract

A case landing page is the reader-facing assurance boundary for an admitted Interop Case. It must let a competent reader understand the tested proposition and reach the executable evidence without reconstructing the repository layout.

## Required reader journey

For every case promoted to `interoperability-tested`, the landing page MUST expose, directly or through clearly named links, the following eight elements in a predictable order:

1. **Question** — the bounded proposition under test.
2. **Composition boundary** — which components participate, which semantics or authority each owns, and what must not collapse into another layer.
3. **Admitted claim** — the exact maturity/assurance statement and explicit exclusions.
4. **Scenarios and vectors** — positive, negative, boundary, or adversarial propositions supporting the claim.
5. **Evidence** — result artifacts, manifests, hashes, reviews, or other evidence supporting the disposition.
6. **Reproduce** — an executable command or unambiguous reproduction instructions.
7. **Limitations** — known gaps, exclusions, missing evidence, and non-claims.
8. **Upstream / next disposition** — relevant upstream issue/proposal status or the next evidence boundary where no upstream action is warranted.

The page may contain additional material and may use a more domain-specific heading where the meaning is unambiguous. Detail should live behind the landing page rather than displacing this reader journey.

## Machine-enforced promotion gate

`scripts/validate_case_docs.py` reads `catalog/interoperability-cases.yaml` and applies this contract to every case whose status is `interoperability-tested`.

The validator checks that:

- the catalog declares a landing-page path;
- the landing page exists;
- the reader-facing semantic elements above are present;
- catalogued scenario/vector, evidence, reproduction, and limitation paths exist where declared;
- the page exposes the local claim boundary rather than allowing a green execution result to stand alone.

A future case therefore cannot be promoted to `interoperability-tested` merely by changing its catalog status. The documentation/evidence surface is part of the maturity gate.

## Authoring pattern

A concise case page should normally use this shape:

```markdown
# <case ID> — <title>

**Status:** Interoperability Tested  
**Admitted claim:** <bounded claim>  
**Evidence scope:** <what this does and does not establish>

## Question
...

## Composition boundary
...

## Admitted claim
...

## Scenarios and vectors
...

## Evidence
...

## Reproduce
...

## Limitations
...

## Upstream / next disposition
...
```

Large programmes such as ARA may keep richer internal structure, but the landing page must still expose each required element without making the reader infer it from phase files.

## Governance rule

`Interoperability Tested` is a local evidence claim. Documentation does not create authority, certification, conformance, or interoperability evidence; it makes the evidence basis and claim boundary independently inspectable.
