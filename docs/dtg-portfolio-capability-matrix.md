---
layout: default
title: DTG Portfolio Capability Matrix
parent: Methods & Architecture
nav_order: 8
---
# DTG Portfolio Capability Matrix

The capability matrix asks a deliberately narrow question:

> For each reusable boundary condition, what evidence do current DTG portfolio surfaces contribute, and where must the property be established by composition rather than inferred from one component?

The matrix is a **repository-owned analytical artifact**. It does not amend upstream DTG specifications, assign normative ownership, or turn uncertainty into a defect.

The machine-readable source is [`analysis/dtg-boundary-conditions/0.1/portfolio-capability-matrix.yaml`](../analysis/dtg-boundary-conditions/0.1/portfolio-capability-matrix.yaml).

## Classification model

| Classification | Meaning |
|---|---|
| `specified` | Direct attributable specification text or executable evidence establishes the relevant capability for this condition |
| `partially-specified` | Relevant capability exists, but semantics, lifecycle, privacy or composition remain incomplete for the condition |
| `composition-dependent` | The property cannot safely be established by one component and must be tested across the composed interaction |
| `unclear` | Current evidence is insufficient; this is explicitly **not** a defect finding |
| `gap-candidate` | Evidence suggests a capability may be missing or incompatible, but promotion requires a bounded executable case or stronger specification evidence |

These classifications describe the **lab's present evidence state**, not the quality or conformance of an upstream project.

## Portfolio surfaces

The initial matrix groups relevant DTG surfaces by function rather than treating repository boundaries as settled semantic ownership:

- **Credentials / VRC** — relationship, credential and provable-fact semantics;
- **Trust Tasks** — trust-task evidence and interaction interfaces;
- **ZKP** — privacy-preserving proof construction and verification semantics;
- **Directory / registry** — authoritative discovery, status and trust-registry resolution surfaces;
- **DPIP** — composed-interaction privacy evaluation and evidence;
- **Assurance / redress** — findings, assurance evidence, correction and redress surfaces.

## Current matrix v0.1

The table below is intentionally compact. The machine-readable artifact carries the rationale for each row.

| Boundary condition | Cred/VRC | Trust Tasks | ZKP | Directory/registry | DPIP | Assurance/redress |
|---|---|---|---|---|---|---|
| Authority provenance | partial | partial | unclear | composition | composition | partial |
| Bounded delegation | partial | partial | composition | unclear | composition | partial |
| Current authority | partial | partial | unclear | composition | composition | partial |
| Historical truth | partial | partial | unclear | partial | unclear | partial |
| Supersession | unclear | unclear | unclear | partial | unclear | partial |
| Lifecycle termination distinctions | partial | partial | composition | partial | composition | partial |
| Explicit state transition | partial | partial | unclear | composition | composition | partial |
| Conflicting authority | unclear | unclear | unclear | partial | composition | **gap-candidate** |
| Minimum disclosure | partial | partial | specified | composition | specified | partial |
| Protected relationship non-discoverability | partial | partial | composition | composition | specified | partial |
| Correlation resistance | partial | partial | specified | composition | specified | partial |
| Temporal validity | partial | partial | composition | partial | composition | partial |
| Replay resistance across state change | composition | partial | partial | composition | composition | partial |
| Authority recovery/restoration | unclear | unclear | unclear | composition | composition | **gap-candidate** |
| Redress and correction | unclear | unclear | unclear | unclear | partial | partial |

`partial` in this rendered view means `partially-specified`; `composition` means `composition-dependent`.

## How to read the matrix

The most important rows are not necessarily the `gap-candidate` rows.

A row dominated by `composition-dependent` can be more significant because it says that individually capable components cannot establish the end-to-end property by themselves. This is especially important for privacy and authority.

For example:

```text
privacy-capable credential
+
privacy-capable proof
+
valid task evidence
+
valid status resolution

≠ automatically privacy-preserving composed interaction
```

Issuer identifiers, status checks, registry queries, task artifacts, verifier requirements or durable identifiers can still create correlation or over-disclosure. This is why DPIP is treated as an evaluation surface rather than proof that upstream components are individually deficient.

Likewise:

```text
valid relationship evidence
+
valid credential

≠ automatically current authority
```

Current authority may depend on supersession, time, authoritative status, delegation scope and relying policy.

## Promotion discipline

A matrix entry moves toward an upstream issue only through evidence:

```text
matrix uncertainty / gap-candidate
        ↓
precise test proposition
        ↓
minimal executable vertical slice
        ↓
recorded result
        ↓
semantic-owner analysis
        ↓
upstream issue if justified
```

An upstream issue should identify the observed result and why the existing composition cannot satisfy the boundary condition. It should not merely cite this matrix.

## First vertical slice nominated by the matrix

The first candidate is **`IC-DTG-PROTECTED-ACCESS-001`**, not yet admitted.

Its minimal question is:

> Can a protected person establish a narrowly scoped entitlement from an authorised provider without exposing the protected provider, protected relationship, location, case identifier, or a durable cross-context correlator?

The initial boundary conditions are:

- `BC-AUTH-PROVENANCE`;
- `BC-MINIMUM-DISCLOSURE`;
- `BC-NON-DISCOVERABILITY`;
- `BC-CORRELATION-RESISTANCE`;
- `BC-REPLAY-RESISTANCE`.

A useful first executable slice should contain only three vectors:

1. **positive** — valid entitlement and authority, minimum necessary proof, expected success;
2. **negative** — relying party requires unnecessary protected-provider or relationship disclosure, expected privacy/conformance failure;
3. **adversarial** — replay or cross-context correlation attempt using artifacts from a successful flow, expected failure or explicit finding.

That is enough to test the methodology before expanding the full protected-person scenario.

## What this matrix does not establish

It does not establish that:

- any upstream specification is defective;
- a component listed as `specified` is conformantly implemented;
- a `gap-candidate` belongs to the component nearest to it in the table;
- DTG provides a jurisdiction-specific legal model for the source scenarios;
- an Interop Case has been admitted;
- a privacy, authority or interoperability claim has passed execution.

Those require the later evidence gates defined by repository governance.
