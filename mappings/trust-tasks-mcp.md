# Trust Tasks ↔ MCP Concept Mapping

**Status:** Experimental mapping  
**Baseline:** Trust Tasks Framework 0.3; MCP 2026-07-28

| Trust Tasks / related concept | MCP concept | Relationship |
|---|---|---|
| Trust Task document | Tool input/output content | Carried by MCP; not replaced by MCP |
| Trust Task `id` | JSON-RPC `id` | Distinct |
| Trust Task `id` | MCP Task `taskId` | Distinct |
| `threadId` | MCP request/session context | No direct equivalence |
| `parentThreadId` | MCP execution nesting | No direct equivalence |
| `inResponseTo` | MCP request correlation | Similar purpose at different semantic layer |
| `trust-task-next-step` | MRTR | Related but not equivalent |
| Trust Ceremony | Sequence of MCP calls | MCP may carry it; sequence alone does not establish it |
| Trust Task expiry | MCP Task TTL | Independent |
| Trust Task proof | MCP authentication | May overlap in assurance only through an explicit binding/profile |
| Trust Task authorization | MCP OAuth/scopes | MCP authorization may be an input, not automatic semantic authority |
| Trust Task semantic error | MCP tool error/result | Preserve semantic error document where possible |
| Task cancellation/withdrawal | MCP `tasks/cancel` | MCP cancellation is execution-local, not portable semantic revocation |

## Key invariant

A mapping identifies interaction points. It does not convert one protocol's identifiers, authorization, lifecycle, or trust semantics into another's by implication.
