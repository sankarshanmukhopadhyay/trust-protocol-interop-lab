# IC-TEA-MCP-TT-001 — TEA TSP, MCP, and Trust Tasks

## At a glance

| Item | Current state |
|---|---|
| **Status** | Experimental |
| **Purpose** | Explore whether agent trust/authority context can travel alongside MCP execution while Trust Tasks continue to own the semantics of the work being performed. |
| **Current conclusion** | The composition is plausible, but authentication, agreement, delegation, tool invocation, and Trust Task state must remain separate governance facts. |
| **Evidence today** | A governed mapping, machine-readable invariants, and experiment scaffolding exist. This is not yet an executed interoperability claim. |

## Why this matters

A modern agent workflow can involve several layers at once: an agent is authenticated; a relationship or trust session exists; some authority has been delegated; an MCP tool is invoked; and a longer-running Trust Task may be created, suspended, resumed, cancelled, or completed.

It is easy for an implementation to collapse these into one convenient "agent is trusted" state. That is precisely what this case is trying to prevent.

## The composition in plain language

**TEA/TSP** refers here to the Trust-Enabled Agent / Trust Spanning Protocol work used to express authenticated exchange and agent trust/authority context.

**MCP (Model Context Protocol)** provides tool/resource invocation mechanics.

**Trust Tasks** provides portable semantics for governed work: task identity, lifecycle, authorization checkpoints, cancellation/suspension/resumption, duplicate-execution protection, and evidence about what work was requested and performed.

\`\`\`text
TEA/TSP: who/relationship/trust context
MCP:     how an invocation is transported/executed
Trust Tasks: what governed work exists and how its lifecycle is controlled
\`\`\`

## Concrete scenario

An authenticated agent asks an MCP server to perform a consequential operation represented as a Trust Task.

The fact that the MCP connection is authenticated does not prove the agent currently has authority for the requested operation. Likewise, a valid Trust Task identifier does not prove an MCP call should execute. Before effect, current authority and task semantics still have to be evaluated.

If the task is later suspended or cancelled, an MCP retry must not create a second effect merely because the transport invocation is technically valid.

## What this case is testing

The case asks whether the composition can preserve agreement/session state separately from authority; authentication separately from delegation; delegation separately from action-specific authorization; MCP invocation identifiers separately from Trust Task identity; task lifecycle separately from transport lifecycle; duplicate/retry handling before effect; and evidence/correlation without turning identifiers into authority.

See the [semantic mapping](../../mappings/tea-mcp-trust-tasks.md), [invariants](invariants.yaml), and [ownership declaration](ownership.yaml).

## Where it resolved

The current pressure point is Trust Tasks' explicit ownership of cancellation, suspension, resumption, duplicate-execution protection, and pre-effect authority checks. TEA/TSP and MCP may carry context or mechanics around those semantics, but neither should redefine them implicitly.

The case remains **Experimental** because this is still a composition hypothesis with scaffolding rather than a mature executed evidence package.

## Evidence and next gate

Inspect the [experiment scaffolding](../../experiments/tsp-enabled-ai-agents/README.md) and [supporting analysis](../../analysis/tsp-enabled-ai-agents/0.1/README.md).

The next gate is a deterministic end-to-end runner and evidence manifest exercising the combined TEA/TSP, MCP, and Trust Tasks path.

## What remains unresolved

Live protocol interoperability, cryptographic verification, concrete authority resolution, and production runtime enforcement are outside the current claim.
