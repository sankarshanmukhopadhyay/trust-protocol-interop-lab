# Example — Asynchronous execution using MCP Tasks

1. Client submits a Trust Task through `trust-task.execute`.
2. Server validates the Trust Task, including acceptance-time `expiresAt`, before consequential execution.
3. Server creates an MCP Task execution handle.
4. Client retrieves status using MCP Tasks.
5. Immediately before each irreversible effect, the server re-evaluates revocable authorization, applicable task-specific deadlines, and received authorized task-control state. It does not reinterpret `expiresAt` as a generic execution timeout for work already under way.
6. Final MCP Task result contains a framework-valid Trust Task response or disposition.

**Invariant:** `taskId` is not the Trust Task `id`, MCP Task TTL is not Trust Task expiry, and asynchronous execution does not weaken the Trust Tasks pre-effect authority/control checkpoint.
