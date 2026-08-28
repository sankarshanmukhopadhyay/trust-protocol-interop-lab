# IC-ARA-REL-001 — final claim boundary and admission decision

Program issue: #32  
Decision date: 2026-08-28

## Maintainer decision

**Admit `IC-ARA-REL-001` to the Interop Case catalog at `interoperability-tested` maturity for a bounded executable semantic-composition reference model.**

This is a human acceptance decision over the accumulated evidence. It is not an automatic consequence of green CI.

## Claim admitted

The Lab has executable evidence for the following bounded proposition:

> Two independently controlled persistent Agent Roles can perform a consequential action only when identity, authority, governing agreement, deterministic policy authorization, scoped capability, exact task semantics, protected cryptographic-use context, and current relationship state permit it; the counterparty can independently verify and disagree; relationship evidence survives Live Agent replacement; challenge, correction, remediation, revocation, continuation and closure preserve historical truth; and an authorized reviewer can inspect the material basis and uncertainty of the action.

For the synthetic query-only relationship, the implementation demonstrates:

- persistent Role state independent of Live Agent memory;
- append-only/current-head state and rollback/fork refusal;
- agreement, authority, policy decision, capability, task and execution as separate observable boundaries;
- protected signing that cannot be exercised by direct Live Agent or arbitrary-byte paths;
- separately controlled sender/receiver processes with receiver-local policy and disagreement;
- distributed relationship evidence without a jointly writable master dossier;
- receipt/inspection/disposition distinctions;
- challenge, correction and remediation without historical overwrite;
- capability revocation and explicit continuation/closure;
- historical validity distinct from present authority;
- privacy-scoped Relationship Views with verified/historical/disputed/restricted/indeterminate distinctions;
- adversarial assurance including false-independence pressure;
- a per-component standards-native boundary review.

## What is NOT claimed

`interoperability-tested` does **not** mean:

- production deployment security;
- external certification or independent audit;
- TSP protocol implementation conformance;
- OpenVTC VTA conformance or hardware-backed key protection;
- normative RCard or VRC implementation conformance;
- registration of `ara/research-query/0.1` as an upstream Trust Task;
- legal validity of authority, agreement, remediation or closure;
- Byzantine/distributed-consensus correctness;
- arbitrary multi-party/quorum ARA semantics;
- proof that different evidence lineages are economically or organizationally independent;
- universal ToIP ARA profile conformance;
- standards-native replacement of every local adapter.

The Phase 11 result is intentionally narrower: standards-owned semantics and credible implementation candidates are pinned, but local adapters remain where exact executable substitution evidence does not exist.

## Gate disposition

All twelve programme gates are satisfied **for their declared question and claim boundary**.

`ARA-G11-STANDARDS-NATIVE-BOUNDARY` is satisfied as a standards-native **boundary review**, not as blanket standards conformance.

`ARA-G12-CLAIM-BOUNDARY-REVIEW` is satisfied by this explicit maintainer-reviewed decision.

## Residual uncertainty

The following remain legitimate future work, not blockers to the bounded semantic-composition admission:

- real TSP endpoint substitution;
- exact OpenVTC VTA protected-use mapping;
- executable RCard/VRC providers;
- registered ARA-specific Trust Task profile if upstream work warrants it;
- external/independent assurance;
- richer correlation/independence provenance;
- multi-party/quorum relationships;
- production persistence, recovery, compromise response and key-management controls;
- human-factors testing of Relationship Views.

## Repository extraction decision

**Do not extract ARA or any implementation component into a new repository at this time.**

No component yet has observed independent downstream reuse, a distinct consumer base, a separately justified release cadence, or a stable semantic lifecycle sufficient to overcome the original reason for keeping ARA in the Protocol Lab.

The architectural conclusion therefore remains:

> ARA is presently an executable relationship-composition capability of the Trust Protocol Interop Lab, not a separately proven protocol implementation boundary.

## Final judgment

The programme has moved ARA from architectural prose to a falsifiable, executable relationship architecture.

The defensible maturity statement is:

> **Interoperability Tested — bounded executable semantic composition, adapter-backed at declared boundaries, with adversarial evidence and explicit standards/conformance exclusions.**
