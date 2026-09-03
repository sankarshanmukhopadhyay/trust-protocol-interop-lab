# IC-TT-MCP-001 — Trust Tasks over MCP

## At a glance

| Item | Current state |
|---|---|
| **Status** | Candidate |
| **Purpose** | Define how portable Trust Task semantics can be carried over MCP without MCP transport/execution mechanics taking ownership of task governance. |
| **Current conclusion** | The binding is sufficiently specified for serious review: sixteen testable invariants preserve task identity, lifecycle, authority checks, replay protection, and evidence semantics. |
| **Primary artifact** | [MCP Binding for Trust Tasks v0.3](../../bindings/trust-tasks/mcp/0.3/spec.md) |

## Why this matters

MCP is good at invoking tools and resources. Trust Tasks is concerned with something different: the identity and governed lifecycle of **work**.

A single piece of work may outlive one MCP request. It may be asynchronous, suspended, resumed, cancelled, retried, or require a fresh authority check immediately before effect. If MCP request IDs or transport success are treated as equivalent to Trust Task state, the system can create duplicate effects or lose accountability.

## The composition in plain language

**MCP (Model Context Protocol)** supplies execution/transport mechanics.

**Trust Tasks** supplies the portable governance semantics of the work: task identity, task lifecycle, semantic control operations, pre-effect authority re-evaluation, duplicate-execution protection, response/evidence binding, and ceremony continuity.

\`\`\`text
MCP carries the operation.
Trust Tasks defines the governed work.
\`\`\`

## Concrete scenario

An agent starts a long-running Trust Task through MCP. The initial call succeeds, but before the consequential effect the task may have been cancelled, the actor's authority may have been revoked, the MCP client may retry after a timeout, or the task payload may no longer match the originally admitted task.

The server must resolve those Trust Task semantics rather than treating "valid MCP call" as sufficient authority to execute.

## What this case is testing

The binding derives sixteen invariants from the pinned Trust Tasks editor's draft, including task identity not collapsing into MCP invocation identity; pre-effect authority re-evaluation; semantic cancellation/suspension/resumption; duplicate/replay protection; payload validation; task-digest evidence binding; proof-omission boundaries; and response semantics attributable to the task.

See [invariants.yaml](invariants.yaml), [ownership.yaml](ownership.yaml), [mapping](../../mappings/trust-tasks-mcp.md), and [vectors](vectors/).

## Where it resolved

The Lab has reached a stable **Candidate binding**: the mapping is detailed enough to state exactly what a conforming experiment should accept and reject.

The key resolution is that transport success and task legitimacy remain separate. MCP may execute a request only within the Trust Task lifecycle and authorization conditions that apply to the work instance.

## Evidence and next gate

Inspect the [binding](../../bindings/trust-tasks/mcp/0.3/spec.md), [examples](../../bindings/trust-tasks/mcp/0.3/examples/), [vectors](vectors/), [test plan](../../experiments/mcp-trust-tasks/test-plan.md), and [known limitations](known-limitations.md).

The next gate is execution against a reproducible runner plus a governed evidence manifest.

## What remains unresolved

Multi-implementation and wire-level interoperability remain unclaimed.
