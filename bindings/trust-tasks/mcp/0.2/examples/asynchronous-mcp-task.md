# Example — Asynchronous execution using MCP Tasks

1. Client submits a Trust Task through `trust-task.execute`.
2. Server validates the Trust Task before consequential execution.
3. Server creates an MCP Task execution handle.
4. Client retrieves status using MCP Tasks.
5. Server re-checks expiry and revocable authorization before the consequential effect.
6. Final MCP Task result contains a framework-valid Trust Task response.

**Invariant:** `taskId` is not the Trust Task `id`, and MCP Task TTL is not Trust Task expiry.
