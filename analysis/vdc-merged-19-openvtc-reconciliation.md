---
layout: default
title: Merged VDC #19 — OpenVTC source reconciliation
parent: Analysis
---

# Merged VDC #19 — OpenVTC source reconciliation

## Purpose

This is a source-pinned implementation pressure test for Interop Lab issue #160. It compares the adopted VDC semantics in `trustoverip/dtgwg-cred-spec#19` with the VDC surface currently exposed by `OpenVTC/dtg-credentials`.

It is **not** a certification result and it does not modify or reinterpret either upstream repository. A missing implementation surface is recorded as missing rather than simulated locally.

## Source pins

| Source | Pin | Role |
|---|---|---|
| `trustoverip/dtgwg-cred-spec#19` | merge `37074bdcd861c51f3e5b7868ce700832b17b73ce`; final PR head `873a473e9aa9564b6751eee10e2561bcb7d767aa` | adopted VDC semantic baseline |
| `OpenVTC/dtg-credentials` | `5cb04fab2d9272ee891b352a4886343ccc86b52b` | implementation under inspection |
| `OpenVTC/dtg-credentials#15` | merge `f9790d7b6804c8e18fe8066450c82b7c28290bee`; PR head `72ff7740d6434ec48708ca0c2d5522c000057f9f` | provenance of current VAC/VDC implementation |

The OpenVTC implementation itself documents the VDC API as tracking the then-draft credential-spec PR #19 and warns that its shape may move.

## Observed implementation surface

At the pinned OpenVTC main source, `DTGCredential::new_vdc` is:

```text
new_vdc(
    issuer,
    subject,
    valid_from,
    valid_until: Option<...>
)
```

It constructs a basic credential subject containing only `id` and tags the credential as `DelegationCredential`. No VDC-specific grant, acceptance, scope, parent/depth, invocation-binding, or status structure is represented in this constructor.

This is sufficient to establish a **source-version divergence** from the merged #19 contract. It is not evidence that the merged specification is defective.

## Pressure-test matrix

Status vocabulary:

- `supported`: the inspected implementation materially exposes the merged semantic surface;
- `divergent`: the implementation exposes the concept but with semantics incompatible with the adopted contract;
- `not-implemented`: the adopted surface is absent from the inspected implementation;
- `not-observable`: the requested runtime/privacy proposition cannot be observed from this implementation surface.

| Merged #19 surface | Status | Evidence / judgment |
|---|---|---|
| Delegation is distinct from authority | `supported` at type/API boundary; semantic non-substitution evidence passes; current OpenVTC actuation remains `not-observable` | OpenVTC has distinct `DelegationCredential` and `AuthorityCredential` types and the `new_vdc` documentation says VDC never supplies authority. Interop Lab's `dtg-vdc-vac-composition` negative vectors separately prove the semantic rule that valid delegation cannot substitute for current principal authority. No current OpenVTC consuming actuation path is evidenced here, so this does not claim end-to-end OpenVTC enforcement. |
| Required non-empty `delegation.scope` | `not-implemented` | `new_vdc` accepts no scope and uses a basic `{id}` subject. |
| Grant + matching acceptance required | `not-implemented` | no acceptance object/API or grant-reference surface is exposed by the inspected VDC constructor. |
| Acceptance references grant by digest | `not-implemented` | no VDC acceptance/binder field is exposed. |
| Single-hop default / explicit `maxDepth` | `not-implemented` | no VDC parent or depth field is exposed. |
| Attenuation-only VDC redelegation | `not-implemented` | attenuation machinery in the inspected library belongs to VAC, not VDC. |
| Request-time invocation binding | `not-implemented` in credential surface; consuming protocol `not-observable` | no VDC invocation-binding field/mechanism is exposed here. The merged spec intentionally leaves invocation mechanics to the Trust Task layer, so a separate consuming-path test is required once an implementation exists. |
| `validUntil` required | `divergent` | OpenVTC accepts `valid_until: Option`, while merged #19 requires expiry. |
| Conditional `credentialStatus` / freshness policy | `not-implemented` | no VDC-specific status/freshness surface is exposed by the constructor. |
| Directed, context-scoped delegation identifier | `not-observable` | the constructor accepts arbitrary issuer/subject strings but does not enforce or expose the merged delegation-specific correlation-scope contract. |
| Per-principal acceptance identifier | `not-implemented` | acceptance itself is absent. |
| Scope-term correlation surface | `not-observable` | scope is absent, so effective correlation cannot be measured. |
| Status-lookup correlation surface | `not-observable` | status lookup is absent from the VDC surface under inspection. |
| Parent-chain disclosure | `not-observable` | VDC chain fields are absent. |
| `parent` / `accepts` digest-valued binder joinability | `not-implemented` | those VDC binders are absent; this does not resolve upstream #38 for conforming implementations. |

## Negative invariant: VDC alone must not satisfy authority

Interop Lab already carries an executable semantic composition experiment at `experiments/dtg-vdc-vac-composition/run.py`. Its negative vectors include a valid VDC with no current principal authority and require `deny`; the inverse case, authority without representation, also requires `deny`. The experiment therefore provides executable **semantic non-substitution evidence** for the merged #19 rule.

As part of this reconciliation, that experiment is re-pinned so VDC #19 is `adopted-upstream-main` at final head `873a473e9aa9564b6751eee10e2561bcb7d767aa` / merge `37074bdcd861c51f3e5b7868ce700832b17b73ce`, while VAC #29 remains `proposed-upstream`. Its claim boundary now states that asymmetry explicitly.

The inspected OpenVTC VDC surface still does **not** supply a consuming authority-decision API aligned to merged #19. Thus the semantic invariant is executable and passes in the Lab, while end-to-end enforcement by the current OpenVTC realization remains `not-observable`. This prevents either a documentation statement or a model-level fixture from being over-read as production implementation assurance.

## Privacy evidence disposition

The merged #19 privacy surfaces cannot be turned into meaningful A/B runtime observations by adding synthetic fields in Interop Lab. Doing that would test an Interop Lab invention rather than current OpenVTC.

Accordingly:

- existing #30 Track A runtime evidence remains **unaffected** because it did not claim VDC execution;
- VDC grant/acceptance identifiers, scope terms, status lookups, chain disclosure and digest binders remain **evidence-required / INDETERMINATE** for current runtime assurance;
- upstream `dtgwg-cred-spec#38` remains the normative owner of binder blinding/enumerability work;
- an OpenVTC implementation update to the adopted #19 contract is the retest trigger for the unavailable runtime surfaces.

## RAHP proposition return

This source inspection and the re-pinned semantic experiment support the following bounded return to RAHP #445/#397:

| Proposition | Result |
|---|---|
| `P02` | merged semantic change confirmed; runtime VDC correlation evidence unavailable |
| `P03` | adopted identifier-scope rule not enforceable/observable in current VDC API |
| `P06` | delegation/authority non-substitution has executable semantic evidence; current OpenVTC consuming-path enforcement remains unproven |
| `P07` | required acceptance is adopted upstream but absent in current OpenVTC implementation |
| `P09` | expiry semantics divergent; status/freshness absent in current OpenVTC implementation |
| `P13` | VDC effective-correlation surfaces remain unobservable in the current implementation |
| `P14` | merged binder semantics not implemented by the current target; #38 residual remains external |
| `P10` | invocation/common-control composition remains unresolved at the current implementation pin |

No historical #371 source-pinned evidence is rewritten by this result.

## Completion judgment

**Interop source reconciliation: COMPLETE. VDC semantic non-substitution evidence: PASS. Current OpenVTC VDC conformance/privacy assurance: NOT COMPLETE / EVIDENCE REQUIRED.**

That is an intentional terminal result for this source pin: the remaining runtime evidence is blocked by a demonstrable implementation-version gap. Re-running unrelated Track A cases cannot close it. The next reassessment should be triggered by material movement in the OpenVTC VDC implementation or the remaining upstream dependencies, not by repeated execution against the same unavailable surfaces.
