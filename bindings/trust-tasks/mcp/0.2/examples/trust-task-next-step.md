# Example — `trust-task-next-step`

A handler determines that another verifiable Trust Task is required before the originating task can complete.

The server returns a framework-valid `trust-task-next-step` response.

The originating Trust Task remains open/blocked according to Framework semantics. MCP completion of the current tool call must not be interpreted as completion of the originating Trust Task.
