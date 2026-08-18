# MCP ↔ Trust Tasks Interoperability Test Plan

**Status:** Candidate test plan  
**Binding under test:** MCP Binding for Trust Tasks v0.3  
**Trust Tasks baseline:** Editor’s Draft 0.3 at `7e0d755f5b815498c861cacecee5cae49b3f14eb`

## Goal

Demonstrate that MCP can carry and execute Trust Tasks without collapsing Trust Task identity, authorization, correlation, lifecycle, semantic task control, ceremony, validation, or portable evidence semantics into MCP protocol state.

## Test model

Each scenario records four layers of evidence:

1. **Upstream requirement** — the pinned Trust Tasks rule being exercised.
2. **Binding obligation** — the cross-protocol invariant that follows.
3. **MCP stimulus** — the request, retry, cancellation, MRTR, reconnection, or asynchronous transition applied.
4. **Observable evidence** — traces, stored state, response documents, and effect records sufficient to determine pass/fail.

## Core scenarios

| ID | Scenario | Expected result / evidence | Primary invariant |
|---|---|---|---|
| T01 | Synchronous task success | Framework-valid response survives MCP carriage | semantic-layer separation |
| T02 | Trust Task semantic error | Semantic error remains a Trust Task result, not only an MCP protocol error | result ownership |
| T03 | Asynchronous MCP Task | `taskId` remains distinct from Trust Task `id`; mapping is reconstructable | INV-TT-MCP-001 |
| T04 | MRTR input | MRTR does not create Trust Task semantics implicitly | execution-local input |
| T05 | `trust-task-next-step` | MCP completion does not close the blocked originating task | lifecycle separation |
| T06 | Trust Ceremony across reconnect | Ceremony continuity verifies without MCP connection continuity | INV-TT-MCP-002 |
| T07 | Duplicate delivery/retry | Consequential effect executes once; duplicate is absorbed/reported per Framework | INV-TT-MCP-009 |
| T08 | Same `id`, changed content | Conflicting document is rejected; no second effect | INV-TT-MCP-010 |
| T09 | JSON-RPC/MCP identifier collision | Reused/changed MCP IDs do not alter Trust Task duplicate decision | INV-TT-MCP-011 |
| T10 | Authority revoked mid-execution | Revocation after acceptance but before effect prevents the subsequent effect | INV-TT-MCP-008 |
| T11 | MCP `tasks/cancel` only | MCP execution stops where possible; Trust Task is not reported semantically cancelled | INV-TT-MCP-004 |
| T12 | `trust-task-control(cancel)` across reconnect | Semantic cancellation remains effective after MCP session/handle loss | INV-TT-MCP-005 |
| T13 | Suspend before effect | No subsequent irreversible effect occurs while semantically suspended | INV-TT-MCP-006 |
| T14 | Resume with revoked authority | Resume is refused and no further effect occurs | INV-TT-MCP-007 |
| T15 | Resume after `expiresAt` | Suspended task does not resume | INV-TT-MCP-007 |
| T16 | Cancellation after first of two effects | Response/evidence distinguishes partial application; no false rollback claim | INV-TT-MCP-014 |
| T17 | Gateway terminates TLS | Proof omission is rejected absent explicit end-to-end security profile | INV-TT-MCP-012 |
| T18 | MCP schema passes, Trust Task payload invalid | Handler is not invoked; task-specific validation fails | INV-TT-MCP-013 |
| T19 | External citation by `id` only | Relying artifact is not treated as content-bound where task digest is required/recommended | INV-TT-MCP-015 |
| T20 | External citation with equivalent digest encoding | Comparison follows decoded multihash semantics | INV-TT-MCP-015 |
| T21 | Unsupported citation hash | Citation remains unverified; no downgrade to `id` comparison | INV-TT-MCP-015 |
| T22 | `trust-task-ok` on fire-and-forget task | Ack may be returned but client does not rely on its presence | INV-TT-MCP-016 |
| T23 | `trust-task-ok` replacing defined success response | Server is non-conforming / vector fails | INV-TT-MCP-016 |

## Evidence manifest fields

For every execution capture:

- `caseId` and `scenarioId`;
- binding and upstream commit identifiers;
- input Trust Task canonical digest and document `id`;
- MCP request ID, session ID (if any), and MCP `taskId` (if any);
- resolved task schema identifier and validation result;
- proof/security-profile decision;
- authorization evidence identifiers/status (secrets removed);
- pre-effect policy/control checkpoint result;
- effect ledger showing each irreversible effect at most once;
- semantic control documents and responses, where used;
- final Trust Task response/acknowledgement/disposition;
- portable citation digest evidence, where used; and
- pass/fail with the invariant(s) evaluated.

## Exit criteria for `Interoperability Tested`

At least two independently implemented endpoints MUST complete the core positive and negative scenarios without unexplained semantic divergence. Evidence manifests MUST be reproducible, identify the exact binding/upstream baselines, and show that every consequential effect is traceable to a successful pre-effect authorization/control checkpoint and duplicate-execution decision.
