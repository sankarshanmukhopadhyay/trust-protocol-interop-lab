# Trust Tasks ↔ MCP Concept Mapping

**Status:** Experimental mapping  
**Baseline:** Trust Tasks Editor’s Draft 0.3 at `7e0d755f5b815498c861cacecee5cae49b3f14eb`; MCP 2026-07-28

| Trust Tasks / related concept | MCP concept | Relationship |
|---|---|---|
| Trust Task document | Tool input/output content | Carried by MCP; not replaced by MCP |
| Trust Task `id` / document identity | JSON-RPC `id`, MCP `taskId` | Distinct; MCP identifiers are not replay/dedup keys |
| `threadId` / `parentThreadId` | MCP request/session context | No direct equivalence |
| `inResponseTo` | MCP request correlation | Similar purpose at a different semantic layer |
| `trust-task-next-step` | MRTR | Related but not equivalent |
| Trust Ceremony | Sequence of MCP calls | MCP may carry it; sequence alone does not establish it |
| Trust Task acceptance expiry | MCP Task TTL | Independent |
| Trust Task proof | MCP authentication/transport security | Proof omission only through an explicit security profile |
| Trust Task authorization | MCP OAuth/scopes | MCP authorization may be input evidence, never automatic semantic authority |
| Pre-effect authority re-evaluation | Long-running MCP execution checkpoint | MCP runtime must preserve the Trust Tasks requirement |
| Duplicate-execution protection | MCP retries/reconnect/redelivery | MCP mechanics must not repeat consequential effects |
| `trust-task-control(cancel)` | MCP `tasks/cancel` | Portable semantic cancellation vs execution-local cancellation; not equivalent |
| `trust-task-control(suspend/resume)` | MCP execution pause/restart mechanics | Semantic state remains owned by Trust Tasks |
| `trust-task-ok` | MCP success/ack | Courtesy acknowledgement only; cannot replace task-specific success |
| Task-digest citation | MCP trace/log correlation | Portable content binding; MCP IDs do not substitute |
| Task payload schema | MCP tool input schema | Both may validate structure, but MCP validation cannot replace the resolved task schema |
| Trust Task semantic error | MCP tool error/result | Preserve semantic error document where possible |

## Key invariants

1. Mapping does not convert one protocol’s identifiers, authority, lifecycle, or trust semantics into another’s by implication.
2. MCP cancellation controls an execution handle; Trust Task control changes portable semantic task state.
3. A long-running MCP execution must preserve Trust Tasks pre-effect authority/control checks.
4. Evidence intended to survive the MCP session should bind to Trust Task content, not merely MCP/session identifiers.
