---
layout: default
title: Current Assurance Evidence
nav_order: 4
nav_exclude: false
permalink: /current-assurance-evidence/
---
# Current Assurance Evidence

This page records the current evidence-producing role of the Interop Lab for RAHP and DPIP. It is a **status/navigation surface**, not a new assurance authority: each result remains bounded by its pinned target, runner, evidence package and owning RAHP/DPIP proposition.

Last reconciled: **2026-09-08**.

## Current evidence estate

| Evidence tranche | Interop source | What it establishes | Important boundary |
|---|---|---|---|
| OpenVTC relationship/verifier A/B privacy | PR #176 | Attributable A/B observations for relationship identifiers, verifier transcript/challenge/purpose/transaction context and deliberate join attempts | No deployment/network/device unlinkability claim |
| OpenVTC status / Trust Task / policy A/B privacy | PR #182 (superseding #177/#178/#179) | Attributable current-target evidence for status, retained Trust Task state and policy discovery | Shared public status service is not, by itself, a subject join; privacy result belongs to DPIP |
| WD02 VDC × VAC composition | PR #169 | One positive and seven negative semantic-composition vectors against the adopted WD02 source | Semantic composition evidence, not production conformance |
| WD02 common-control binding | PR #175 | Explicit positive binding plus negative cases showing association, one-identifier control or request-level PoP cannot substitute for common-control proof | Does not define the missing normative same-subject/common-control ZK primitive; RAHP #482 remains the owner |
| WD02 action-time VDC × VAC × Trust Task | PR #184 | Current implementation terminal behavior for semantic intersection, withdrawn authority, missing VDC, invocation mismatch, narrower/revoked delegation and unavailable current policy/authority | Exact production authority evaluator is absent; positive intersection remains `INDETERMINATE/BLOCKED`, with no effect inferred |
| Data Rooms current OpenVTC evidence | PR #186 / issue #185 | Target-native `vti-rooms`, `vti-rooms-dtg`, `room-host` and `vtc-service` room tests; bounded proposition evidence for lifecycle/current-authority and recovery, plus stronger same-subject/mixed-principal observations | Private-room ZK, witnessed anchoring/freshness, operator independence, full migration, and agent/human composed runtimes remain genuine evidence gaps |

## Privacy return to DPIP

The relationship-correlation evidence produced by PRs #176 and #182 was consumed by DPIP #218. DPIP reached **SATISFIED within the exercised current-OpenVTC runtime boundary** for the named relationship/verifier/status/task/policy surfaces. That result is intentionally scoped and does not imply universal unlinkability.

For Data Rooms, the Interop Lab has now exhausted the currently obtainable target-native non-private evidence under RAHP #481. DPIP's E1-E6 private-room observability contract remains evidence-incomplete because the executable private-room same-subject/common-control ZK path is not currently available. Passing non-private room tests must not be promoted into private-tier privacy evidence.

## Current OpenVTC pins

Different tranches preserve the immutable target used when their evidence was produced; do not silently rewrite old evidence to a newer source pin.

- relationship/verifier/status/task/policy A/B evidence: `OpenVTC/verifiable-trust-infrastructure@72bf5794071971da506eb7a5af8e4765c35c137c` for the current Track A/B tranche;
- Data Rooms proposition evidence: `OpenVTC/verifiable-trust-infrastructure@56cd6e5b7116777f1d9734e76c9a7b0569870e19`.

The source pin is part of the evidence identity. Later upstream movement requires selective invalidation/re-execution rather than reinterpretation of an older run.

## Current RAHP residual owners

- [RAHP #481](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/481) — Data Rooms implementation/runtime/deployment evidence maturity. Canonical `P-ROOM-*` definitions live in RAHP `profiles/dtg/coverage/data-rooms.yaml`.
- [RAHP #482](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/482) — WD02 common-control/same-subject proof semantics that remain externally unresolved.

The Interop Lab should create new evidence only when one of those owners identifies an executable proposition and admissible evidence class. Reference behavior and mocks are useful for design pressure-testing but must not be presented as implementation evidence for OpenVTC.

## Interpretation rule

A green Interop workflow means the evidence producer ran successfully. It does **not** mean the assessed system is assured. Terminal interpretation remains with the owning RAHP/DPIP assessment, and `INDETERMINATE`, `EVIDENCE_REQUIRED` and bounded satisfaction are first-class outcomes rather than failures of the evidence pipeline.
