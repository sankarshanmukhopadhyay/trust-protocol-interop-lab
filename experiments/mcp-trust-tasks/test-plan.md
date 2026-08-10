# MCP ↔ Trust Tasks Interoperability Test Plan

**Status:** Skeleton  
**Binding under test:** MCP Binding for Trust Tasks v0.2

## Goals

Validate that MCP can carry and execute Trust Tasks without collapsing Trust Task identity, authorization, correlation, lifecycle, ceremony, or evidence semantics into MCP protocol state.

## Initial scenarios

| ID | Scenario | Expected invariant |
|---|---|---|
| T01 | Synchronous task success | Framework-valid response survives MCP carriage |
| T02 | Trust Task semantic error | Semantic error is not misreported as MCP protocol failure |
| T03 | Asynchronous MCP Task | `taskId` remains distinct from Trust Task `id` |
| T04 | MRTR input | MRTR does not create Trust Task semantics implicitly |
| T05 | `trust-task-next-step` | MCP completion does not close blocked originating task |
| T06 | Trust Ceremony across calls | Ceremony continuity does not depend on MCP connection continuity |
| T07 | Duplicate delivery | Consequential effect executes once |
| T08 | Same `id`, changed content | Conflicting document is rejected |
| T09 | Expiry before side effect | Consequential effect does not begin |
| T10 | Authority revoked mid-execution | Execution-time policy check prevents subsequent effect |
| T11 | MCP Task cancellation | Execution cancellation is not semantic Trust Task revocation |
| T12 | Gateway terminates TLS | Proof omission is not assumed without an explicit end-to-end profile |

## Evidence to capture

For each scenario record:

- input Trust Task document;
- MCP request/result trace with secrets removed;
- identity and authorization assumptions;
- execution state changes;
- final Trust Task response;
- observed divergence from binding text;
- implementation-specific behavior.

## Exit criteria for “Interoperability Tested”

At least two independently implemented endpoints should complete the core scenarios without semantic divergence, or divergences should be documented and resolved in a newer binding revision.
