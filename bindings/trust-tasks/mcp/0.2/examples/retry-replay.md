# Example — Retry and replay

The same Trust Task document is delivered twice with the same `id`.

For a consequential task, the second delivery must not trigger the side effect again.

A transport request ID or MCP Task ID must not be used as the semantic duplicate-execution key.
