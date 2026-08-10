# Example — Synchronous Trust Task over MCP

1. Client calls `trust-task.execute` with a valid Trust Task document.
2. Server validates framework, payload, identity, proof/transport assumptions, expiry, and authorization.
3. Handler completes synchronously.
4. Server returns a framework-valid Trust Task response in MCP structured content.

**Invariant:** MCP request completion does not replace Trust Task semantic completion.
