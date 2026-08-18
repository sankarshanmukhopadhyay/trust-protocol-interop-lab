# Architecture

## Core proposition

MCP and Trust Tasks are complementary rather than competing.

```text
DTG / governance / delegation evidence
              |
              v
      authorization policy
              |
              v
Trust Tasks + Trust Ceremonies
              |
              v
      MCP binding layer
              |
              v
MCP tools / MRTR / MCP Tasks
```

## Responsibility boundaries

### Trust Tasks

Trust Tasks define the portable semantic unit of verifiable work:

- task type;
- parties;
- payload;
- proof and recipient binding;
- correlation;
- responses and errors;
- expiry;
- task-specific semantics.

### Trust Ceremonies

Trust Ceremonies compose Trust Tasks into verifiable multi-step enactments. Ceremony continuity must derive from Trust Task evidence, not from an MCP connection or execution session.

### MCP

MCP provides interaction and execution mechanics:

- tool discovery and invocation;
- runtime interaction;
- MRTR;
- optional asynchronous MCP Tasks.

MCP execution state is not Trust Task semantic state.

The current MCP binding also preserves Trust Tasks semantic task control (`cancel`, `suspend`, `resume`), duplicate-execution protection, pre-effect authority re-evaluation, task-specific payload validation, and task-digest-bound portable evidence. These properties must survive MCP retries, cancellation, asynchronous task handles, and connection changes without being redefined by them.

### DTG and governance evidence

DTG or another trust framework may supply evidence concerning:

- recognition and membership;
- operator relationships;
- delegation or mandate;
- capabilities;
- standing;
- revocation/suspension;
- governance rules.

Evidence informs a consumer authorization decision; it does not compel execution.

## Four mechanisms that must not be conflated

| Mechanism | Meaning |
|---|---|
| MCP MRTR | More execution-local input is needed |
| `trust-task-next-step` | Current Trust Task remains open/blocked pending another Trust Task |
| Trust Ceremony | Verifiable multi-step composition |
| MCP Task | Asynchronous MCP execution handle/state |

This separation is the central interoperability invariant of the MCP binding.
