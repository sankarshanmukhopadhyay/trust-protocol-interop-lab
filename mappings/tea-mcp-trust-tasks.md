# TEA ↔ MCP ↔ Trust Tasks Interoperability Mapping

**Status:** Exploratory  
**Related analysis:** [TSP-Enabled AI Agent Protocols Implementation Analysis 0.1](../analysis/tsp-enabled-ai-agents/0.1/README.md)

## Purpose

This mapping examines how three distinct protocol concerns can compose without collapsing their semantics:

- **TSP-Enabled AI Agent (TEA)** concepts: durable agent identity, authenticated exchange, delegation, authorization evidence, and accountable action;
- **Model Context Protocol (MCP)** concepts: client/server interaction, tool/resource discovery, tool invocation, interactive round trips, and optional asynchronous execution handles; and
- **Trust Tasks** concepts: a verifiable unit of work, parties, task type, payload, integrity, correlation, response semantics, and task-specific result.

The goal is not to assert a final architecture. It is to make cross-specification ownership explicit enough that experiments can reveal where additional bindings or profiles are required.

## Layer ownership

| Concern | Primary semantic owner | Notes |
|---|---|---|
| Durable agent identity | TEA / TSP identity profile | Should not be inferred from MCP connection identity alone |
| Authenticated secure channel | TSP | MCP transport/session should not silently redefine TEA identity |
| Tool/resource discovery | MCP | Discovery may be constrained by TEA authorization policy |
| Tool invocation mechanics | MCP | Invocation is execution mechanics, not semantic delegation |
| Verifiable unit of work | Trust Tasks | Trust Task `id` and type remain Trust Task semantics |
| Multi-step verifiable work | Trust Ceremony | MCP session/MRTR is not automatically a Trust Ceremony |
| Negotiated bilateral agreement | TEA Authenticated Exchange | Distinct from tool invocation and Trust Task correlation |
| Delegation / mandate / capability | TEA / external trust framework | Must be evaluated separately from transport authentication |
| Execution-local interaction | MCP MRTR | Should not mutate Trust Task semantics implicitly |
| Asynchronous execution handle | MCP Task | MCP `taskId` is not a Trust Task identifier |
| Semantic success/error | Trust Tasks | MCP/JSON-RPC errors remain protocol/execution failures |
| Portable signed evidence | TEA / Trust Task profile | Needs an explicit cross-layer binding |
| Accountability chain | TEA delegation/evidence model | Must link authority to concrete action/task evidence |

## Candidate composition model

```text
Principal / governance authority
            │
            │ delegation / mandate / capability
            ▼
      TEA identity + authority
            │
            │ authenticated TSP relationship
            ▼
        MCP interaction
     discovery / invocation
            │
            │ carries or triggers
            ▼
        Trust Task
   verifiable semantic work
            │
            ▼
      signed task result
            │
            └── linked back to TEA authority/evidence
```

This is deliberately a layered model. It avoids treating any of the following as equivalent:

- MCP authentication and TEA authority;
- MCP Task and Trust Task;
- MCP session and Trust Ceremony;
- Authenticated Exchange and tool invocation;
- transport identity and delegation authority.

## Key interoperability questions

### 1. Where does Authenticated Exchange sit relative to Trust Tasks?

Candidate models include:

- **precondition model:** Authenticated Exchange establishes an agreement/relationship before Trust Tasks are sent;
- **envelope model:** a Trust Task is carried within an Authenticated Exchange proposal/acceptance process;
- **orthogonal model:** Authenticated Exchange is used only when bilateral agreement is needed, while ordinary Trust Tasks flow independently over TSP.

The orthogonal model appears least likely to conflate semantics, but should be tested against real workflows.

### 2. Does TEA delegation authorize a Trust Task?

A promising separation is:

1. Trust Task proves what work is being requested and by whom;
2. TEA delegation/mandate/capability proves whether the actor is authorized to request or perform it;
3. local policy evaluates both before consequential execution.

The Trust Task proof should not be treated as proof of authority unless a profile explicitly defines that relationship.

### 3. What does MCP transport?

MCP can transport the invocation that carries a Trust Task document, but MCP should not become the owner of Trust Task identifiers, response correlation, ceremony semantics, or delegation evidence.

The existing [MCP Binding for Trust Tasks 0.2](../bindings/trust-tasks/mcp/0.2/spec.md) follows this approach by keeping Trust Task, Trust Ceremony, MCP execution, and authorization as distinct semantic layers.

### 4. Which layer owns correlation?

Potentially several identifiers can coexist:

| Identifier | Meaning |
|---|---|
| TEA exchange identifier | Bilateral negotiation/agreement context |
| Trust Task `id` | Verifiable work item |
| Trust Task `threadId` / `parentThreadId` | Trust Task correlation/ceremony structure |
| MCP request ID | JSON-RPC request/response correlation |
| MCP Task `taskId` | Asynchronous execution handle |

Profiles should bind these identifiers explicitly when needed, but MUST NOT infer semantic equivalence from string equality.

### 5. Which layer owns agreement state?

If the workflow requires a binding bilateral proposal/accept/ack process, TEA Authenticated Exchange owns that state. MCP request acceptance or Trust Task receipt should not silently imply the same agreement semantics.

### 6. Which layer owns authorization?

Authorization should remain an explicit decision using delegation/mandate/capability evidence plus local policy. MCP authentication and a valid Trust Task proof are necessary inputs in some profiles but are not sufficient authority by themselves.

### 7. How is evidence made portable outside the MCP session?

A useful end state is a result artifact that can be verified without access to the original MCP connection. That likely requires explicit binding among:

- TEA VID/signing key;
- delegation/authority evidence;
- Trust Task identifier and request digest;
- concrete tool/action identifier;
- result/outcome digest;
- relevant time/effect evidence.

This is a natural experiment target for the lab.

## Relationship to the existing MCP Trust Task binding

The current binding already defines two useful interoperability principles:

1. MCP provides execution mechanics; Trust Tasks retain semantic work identity and response semantics.
2. authorization is evaluated independently from document-proof validity and MCP transport/session state.

A TEA/MCP profile should preserve these boundaries unless the upstream TEA specification explicitly chooses a different semantic owner.

## Candidate experiment sequence

1. **Identity-bound MCP session** — bind MCP client/server interaction to TEA VIDs without changing MCP request IDs.
2. **Delegated Trust Task invocation** — present TEA delegation evidence alongside `trust-task.execute` and evaluate authority independently.
3. **Authenticated Exchange precondition** — require a completed exchange before a consequential Trust Task tool call.
4. **Portable result evidence** — produce a signed result linked to TEA authority and Trust Task request.
5. **Replay/downgrade test** — attempt to replay the Trust Task or move the invocation to a non-TSP channel.

## Non-goals

This mapping does not:

- redefine MCP;
- redefine Trust Tasks;
- redefine the upstream TEA draft;
- imply that every MCP tool call should be a Trust Task;
- imply that every Trust Task needs Authenticated Exchange;
- establish legal enforceability of protocol evidence.

## AI-tool usage note

This mapping was prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer.
