# Cancellation and semantic task control

MCP cancellation and Trust Task semantic control operate at different layers.

```text
MCP tasks/cancel
      ↓
stops or requests stopping an MCP execution handle

trust-task-control(cancel)
      ↓
portable semantic cancellation of a Trust Task
```

They are not equivalent. A deployment MAY define policy that responds to MCP cancellation by producing or processing a `trust-task-control` document, but the control operation must independently satisfy Trust Tasks validation, proof, authorization, correlation, and lifecycle rules.

## Partial execution

If irreversible effects occurred before semantic cancellation reached a pre-effect checkpoint, the consumer must preserve the Framework disposition describing what was applied. MCP `cancelled` status must not erase that distinction.

## Suspension and resume

`trust-task-control(suspend)` preserves semantic execution state while stopping future effects. `resume` is a fresh decision to proceed: the consumer must re-evaluate required authority and must not resume after the target task's `expiresAt`.
