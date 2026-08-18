# MCP Binding for Trust Tasks

**Status:** Candidate Binding Draft  
**Binding version:** 0.3  
**Target Trust Tasks framework:** Editor’s Draft document version 0.3, commit `7e0d755f5b815498c861cacecee5cae49b3f14eb` (2026-08-16)  
**Target MCP specification:** 2026-07-28  
**Binding identifier (provisional):** `https://trusttasks.org/binding/mcp/0.3`

## Abstract

This specification defines how Trust Task documents are transported and executed using the Model Context Protocol (MCP) 2026-07-28.

The binding preserves distinct semantic layers:

1. **Trust Tasks** define the verifiable unit of work, parties, task type, payload, integrity requirements, correlation, response semantics, and task-specific result.
2. **Trust Ceremonies** define cryptographically linked composition of Trust Tasks across a multi-step enactment.
3. **MCP** provides tool invocation and interactive execution, including Multi Round-Trip Requests (MRTR).
4. **MCP Tasks** optionally provide asynchronous execution handles and execution status.
5. **Authorization and trust evaluation** determine whether a valid Trust Task may be executed, using applicable delegation, mandate, capability, membership, standing, status, governance evidence, and consumer policy.

An MCP Task is an execution handle. It is not a Trust Task. An MCP session or sequence of tool calls is not a Trust Ceremony. MCP authentication or authorization does not, by itself, establish semantic authority to execute a Trust Task.

---

## 1. Conformance and normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in BCP 14 when they appear in all capitals.

This binding defines two conformance classes:

- **conforming MCP Trust Task client**
- **conforming MCP Trust Task server**

A deployment MAY additionally claim an assurance profile defined by another specification.

This binding does not modify the Trust Tasks Framework. This version is pinned to a specific Trust Tasks editor's-draft commit because the upstream document version remains `0.3` while normative text continues to evolve. Where this binding adds MCP-specific safeguards beyond the pinned Framework, those safeguards apply only to implementations claiming conformance to this binding.

---

## 2. Terminology

Trust Task terms including *producer*, *consumer*, *issuer*, *recipient*, *VID*, *Trust Task document*, `id`, `threadId`, `parentThreadId`, `inResponseTo`, `proof`, *Type URI*, and *Trust Ceremony* have the meanings defined by the Trust Tasks Framework.

MCP terms including *client*, *server*, *tool*, *MRTR*, and *MCP Task* have the meanings defined by MCP 2026-07-28.

**execution handle** — an MCP Task identifier used to query or manage asynchronous execution state.

**transport-derived VID** — a Trust Task VID deterministically derived from authenticated MCP transport or authorization context according to an explicit deployment profile.

**semantic failure** — a failure represented by a valid Trust Task response, including `trust-task-error`.

**protocol failure** — an MCP or JSON-RPC failure that prevents a valid Trust Task semantic response from being produced.

---

## 3. Semantic separation

A conforming implementation MUST preserve these boundaries:

| Concept | Purpose | Semantic authority |
|---|---|---|
| Trust Task `id` | Identifies a Trust Task document | Trust Tasks |
| `threadId` / `parentThreadId` | Correlates Trust Task exchanges | Trust Tasks |
| `inResponseTo` | Identifies the request answered by a response | Trust Tasks |
| Trust Ceremony fields | Establish verifiable multi-step enactment structure | Trust Tasks |
| MRTR | Obtains execution-local interaction/input | MCP |
| MCP Task `taskId` | Identifies asynchronous execution state | MCP |
| MCP session/connection | Provides protocol interaction context | MCP |
| Delegation/mandate/capability | Supports authorization decisions | External trust framework / policy |
| Semantic success/error | States Trust Task outcome/disposition | Trust Tasks |
| Transport/protocol failure | States inability to complete MCP processing | MCP |

String equality between identifiers from different rows MUST NOT be used to infer semantic equivalence.

---

## 4. Capability declaration

A conforming MCP Trust Task server MUST expose an MCP tool named:

`trust-task.execute`

Presence of this tool means only that the server supports this binding. It MUST NOT be interpreted as support for every Trust Task type or as willingness or authority to execute a particular task.

Individual Trust Task support SHOULD be determined through Trust Task discovery, deployment configuration, or another explicit profile.

---

## 5. `trust-task.execute`

### 5.1 Input

The tool input MUST contain one required member:

```json
{
  "document": {
    "...": "Trust Task document"
  }
}
```

The MCP tool input schema SHOULD constrain `document` as an object but MUST NOT replace framework or task-specific schema validation.

### 5.2 Processing

Before consequential execution, the server MUST:

1. validate the Trust Tasks framework envelope;
2. resolve the Trust Task `type`;
3. validate the task-specific payload against the resolved task schema;
4. resolve and validate party identity;
5. validate `expiresAt` as an acceptance condition;
6. validate `proof` where required;
7. enforce recipient/audience and identity-consistency rules;
8. validate response/correlation, task-digest citation, or ceremony fields where applicable;
9. evaluate authorization independently of document-proof validation;
10. resolve the expected task handler;
11. determine authoritative runtime side-effect and exposure characteristics;
12. apply the Framework duplicate-execution rule for consequential tasks; and
13. establish the pre-effect conditions that MUST be re-evaluated before each irreversible effect.

MCP tool-schema validation is not task-payload validation. A server MUST NOT treat successful MCP input validation, static TypeScript typing, deserialization alone, or handler selection as proof that the task payload satisfies the resolved Trust Task schema.

The server MUST NOT invoke a consequential handler before all applicable validation and authorization checks succeed.

---

## 6. Discovery

MCP discovery and `tools/list` describe MCP protocol/tool capability. They do not establish semantic authorization or willingness to perform a Trust Task.

A conforming client MAY submit the Trust Tasks discovery task through `trust-task.execute`.

Discovery results are capability information. They MUST NOT be treated as authorization.

---

## 7. Party identity and authorization

### 7.1 Descriptive MCP metadata

MCP `clientInfo`, `serverInfo`, tool names, server names, and similar descriptive metadata MUST NOT, by themselves, be treated as authenticated Trust Task party identity.

### 7.2 Transport-derived identity

OAuth/OIDC or another MCP access-control context MAY contribute to party identification only where an explicit profile defines:

1. the authoritative credential or claim;
2. its issuer or trust anchor;
3. deterministic mapping to a VID;
4. canonical representation;
5. audience/scope;
6. status or revocation checks; and
7. mismatch behavior.

A server MUST NOT silently rewrite an in-band VID to make it agree with MCP metadata.

### 7.3 Authorization boundary

Successful validation of a VID, issuer, recipient, transport-derived identity, or ordinary document proof MUST NOT, by itself, be treated as sufficient authority to execute the requested outcome.

A verified assertion MAY constitute authorization evidence where the applicable Trust Task specification explicitly gives that assertion such semantic meaning and consumer policy accepts it for that purpose.

Authorization MAY consider delegation, mandate, capability, membership, standing, credential status, subject relationship, purpose limitation, governance rules, MCP scopes, and local policy.

Trust Ceremony membership MUST NOT, by itself, grant execution authority.

---

## 8. Proof and MCP transport assurance

MCP carriage alone does not satisfy the Trust Tasks Framework condition for omission of an in-band proof.

A deployment profile that permits `proof` omission MUST document the security properties that justify the omission, including:

- authenticated producer identity and deterministic VID mapping;
- intended-consumer or audience binding;
- integrity of the Trust Task document across relevant intermediaries;
- whether any intermediary can modify or re-originate the document;
- freshness/replay protection; and
- relevant credential/key status assumptions.

Hop-by-hop TLS to an MCP gateway, reverse proxy, tool router, or server host MUST NOT, by itself, be treated as producer-to-consumer end-to-end assurance when that intermediary can modify or re-originate the Trust Task without detection.

Where these properties are not established, `proof` remains subject to the Framework and individual task specification requirements.

A profile permitting proof omission MUST identify the exact security boundary at which producer authentication, document integrity, audience binding, freshness/replay assumptions, and key/status semantics are established. Silence about any of these properties MUST NOT be interpreted as permission to omit proof.

---

## 9. Result mapping

### 9.1 Semantic completion

A synchronously completed Trust Task SHOULD return the framework-valid response document in MCP structured content.

### 9.2 Semantic error

A task rejection or task-specific failure that can be represented by a valid `trust-task-error` SHOULD be returned as a semantic tool result rather than converted into an MCP/JSON-RPC protocol error.

The MCP result MAY indicate `isError: true`, but the Trust Task document remains authoritative for Trust Task error semantics.

### 9.3 Courtesy acknowledgement (`trust-task-ok`)

Where the originating Trust Task specification defines no success-response document, a server MAY return `trust-task-ok` in accordance with the pinned Framework. It MUST NOT return `trust-task-ok` in place of a success response that the task specification defines.

A client MUST NOT make continued execution, state transition, or audit-critical reliance depend on receiving `trust-task-ok`; absence of the acknowledgement carries no semantic information. Data placed in its advisory references MUST NOT become an undeclared continuation contract.

### 9.4 Protocol failure

An MCP/JSON-RPC error SHOULD be used when the server cannot produce a framework-valid semantic result, including malformed MCP invocation or infrastructure failure before sufficient Trust Task processing has occurred.

---

## 10. MRTR, `trust-task-next-step`, ceremonies, and MCP Tasks

These mechanisms are distinct:

| Mechanism | Meaning |
|---|---|
| MCP MRTR | More interaction/input is needed within an MCP execution context |
| `trust-task-next-step` | The originating Trust Task remains open/blocked and another verifiable Trust Task is required |
| Trust Ceremony step | A Trust Task participates in a cryptographically linked multi-step enactment |
| MCP Task | Asynchronous execution state for an MCP request |

### 10.1 MRTR

MRTR SHOULD be used for transient execution-local input such as confirmation, missing runtime parameters, step-up authentication, or selection among alternatives.

MRTR input does not create a Trust Task unless an application explicitly constructs and validates one.

A server MUST NOT use opaque MRTR input to replace a required Trust Task where doing so would remove required identity, proof, authorization, ceremony, correlation, audit, or evidence semantics.

### 10.2 `trust-task-next-step`

When a Trust Task returns `trust-task-next-step`, the MCP execution MUST preserve the Framework meaning that the originating Trust Task is blocked/open pending the required next Trust Task.

An MCP tool call completing successfully MUST NOT be interpreted as semantic completion of the originating Trust Task in this case.

The required next task SHOULD be submitted as a new Trust Task document with the correlation fields required by the Framework and individual task specification.

### 10.3 Trust Ceremonies

MCP MAY transport and execute Trust Tasks that participate in a Trust Ceremony.

An MCP session, connection, MRTR exchange, MCP Task, or sequence of tool calls MUST NOT, by itself, establish:

- membership in a Trust Ceremony;
- ceremony continuity;
- predecessor/successor relationships;
- ceremony authorization; or
- terminal ceremony state.

Those semantics MUST be derived from the Trust Task ceremony fields, correlation data, proofs/digests, and applicable Trust Tasks rules.

MCP reconnect or migration to another server process MUST NOT break ceremony semantics where the Trust Task evidence remains valid.

### 10.4 MCP Tasks

Where the MCP Tasks extension is negotiated, a server MAY execute `trust-task.execute` asynchronously.

The server MUST preserve or reconstruct the mapping between:

`MCP taskId → Trust Task id → inResponseTo/threadId/parentThreadId/ceremony context as applicable`

An MCP Task status describes MCP execution state. It MUST NOT replace Trust Task response, next-step, or ceremony semantics.

---

## 11. Long-running execution and pre-effect authority

MCP Task TTL and Trust Task `expiresAt` are independent. Trust Task `expiresAt` bounds acceptance; it MUST NOT be silently reinterpreted as a generic execution deadline once work has begun. A task-specific payload MAY define a completion deadline with its own semantics.

An extant MCP `taskId` is not evidence that the underlying Trust Task remains authorized or executable.

For consequential runtime behavior, immediately before each irreversible effect the server MUST re-evaluate every condition that the applicable Trust Task specification and consumer policy require to remain true, including received authorized task-control state. These inputs MAY include delegation, mandate, credential/capability status, membership/standing, subject authority, task-specific deadlines, suspension/revocation state, or other governance conditions.

If a required condition is no longer valid, the server MUST NOT perform the subsequent irreversible effect. Where earlier effects already occurred, the disposition MUST distinguish partial execution from a task that never began whenever the Framework or task specification provides such a response path.

Stopping is not automatically equivalent to rollback. The server MUST NOT claim that earlier irreversible effects were undone merely because later effects were prevented.

## 12. Duplicate execution, replay, and retries

The pinned Framework's consequential-task duplicate-execution rule is authoritative. JSON-RPC request IDs, MCP Task IDs, transport message identifiers, session IDs, or tool-call IDs MUST NOT substitute for Trust Task document identity.

A server MUST retain enough state for the applicable acceptance/execution window to distinguish:

1. the same canonical Trust Task document received again, which MUST NOT repeat a consequential effect; and
2. reuse of the same Trust Task `id` with different document content, which MUST be rejected as a conflict.

MCP retry, reconnect, status retrieval, subscription delivery, MRTR continuation, asynchronous recovery, or mediator redelivery MUST NOT re-trigger a completed consequential effect.

A retry/replay decision based only on string equality of `id` is insufficient: the consumer MUST preserve the Framework's distinction between identifier and document-content identity.

## 13. Task control, cancellation, suspension, and resumption

The pinned Framework defines portable semantic task control through `trust-task-control` for `cancel`, `suspend`, and `resume`. MCP `tasks/cancel` remains an execution-local operation over an MCP execution handle.

The following invariant is normative for this binding:

```text
MCP tasks/cancel != trust-task-control(cancel)
```

A conforming implementation MUST NOT infer that one operation occurred merely because the other occurred. A deployment profile MAY define an explicit policy that causes an MCP cancellation request to issue or process a Trust Task control document, but the resulting control document MUST independently satisfy Framework identity, proof, authorization, correlation, and processing requirements.

### 13.1 Semantic cancellation

An authorized `trust-task-control(cancel)` MUST prevent future effects at the Framework's next required pre-effect checkpoint. Cancellation is terminal for the target task and MUST NOT be represented as rollback of effects that already occurred.

Where the control response reports an outcome with applied effects, the MCP layer MUST preserve that evidence and MUST NOT collapse it into a generic `cancelled` execution status.

### 13.2 Suspension

An authorized `trust-task-control(suspend)` halts future effects while preserving execution state. MCP MAY keep, pause, release, or reconstruct an execution handle according to local policy, but those mechanics MUST NOT redefine the Trust Task's semantic suspended state.

### 13.3 Resumption

Before an authorized `trust-task-control(resume)` causes execution to continue, the consumer MUST perform the Framework's required acceptance/authority checks for resumption. A suspended task MUST NOT resume after its Trust Task `expiresAt`.

### 13.4 MCP cancellation

On MCP `tasks/cancel`, a conforming server:

1. MUST attempt to stop the MCP execution attempt at a safe boundary;
2. MUST NOT claim portable semantic cancellation unless a valid Trust Task control operation has established it;
3. MUST NOT assume other copies of the Trust Task became invalid; and
4. SHOULD retain evidence needed to distinguish an execution-local stop from semantic cancellation and from partial application.

Silence from either control path carries no portable semantic conclusion unless the pinned Framework explicitly defines one.

## 14. Side effects, exposure, and approval

Trust Task side-effect and exposure declarations MAY inform MCP host UI, policy routing, approval prompts, MRTR, isolation, and observability.

They MUST NOT themselves be treated as authorization.

Before consequential execution, the server MUST determine the authoritative behavior of the actual handler as required by the Framework.

If runtime behavior is more consequential than the declaration used to obtain policy approval, the server MUST stop before the additional effect and re-evaluate policy or approval.

---

## 15. External citations and portable evidence

Where an artifact outside the Trust Task exchange relies on a citation to a Trust Task, the binding SHOULD preserve the pinned Framework's task-digest binding rather than relying on Trust Task `id` equality alone.

For such evidence:

- the task digest identifies the cited task content;
- digest comparison MUST follow the Framework's decoded multihash semantics;
- an unsupported hash algorithm leaves the citation unverified and MUST NOT be downgraded to `id`-only matching; and
- the task digest does not itself establish authenticity; authenticity derives from the evidence artifact that commits to the digest and the applicable proof/trust evaluation.

MCP request IDs, MCP Task IDs, trace IDs, or log correlation IDs MUST NOT substitute for this portable content binding.

## 16. Sensitive data

Trust Task payloads, proofs, VIDs, credentials, delegation evidence, authorization artifacts, or secrets MUST NOT be copied into MCP routing metadata solely for routing, metering, or convenience.

Implementations SHOULD minimize Trust Task data exposed through model-visible context, logs, traces, errors, telemetry, caches, and headers.

Secret material SHOULD be kept out of model-visible context unless the individual Trust Task specification and applicable policy require its use there.

---

## 17. Security considerations

Implementations MUST account for at least:

- **confused deputy** — an authenticated MCP client may lack semantic authority;
- **identity substitution** — descriptive MCP metadata is not party identity;
- **duplicate execution** — retries/replay must not duplicate consequential effects;
- **stale authority** — long-running work can outlive expiry or revocable authority;
- **intermediary substitution** — gateways can alter the true end-to-end security boundary;
- **tool substitution** — the executed handler must match the evaluated handler;
- **risk-declaration mismatch** — more consequential runtime behavior requires renewed policy evaluation;
- **cancellation races** — cancellation must not conceal already committed effects;
- **ceremony confusion** — MCP session continuity must not be mistaken for ceremony continuity; and
- **information leakage** — MRTR, task status, logs, errors, and model context can expose sensitive Trust Task material.

---

## 18. Processing algorithm

A conforming server SHOULD implement the following logical sequence:

```text
1. Receive MCP tools/call
2. Extract Trust Task document
3. Validate Framework envelope
4. Resolve task type and validate task payload against the resolved schema
5. Validate correlation / response / ceremony / citation structure where applicable
6. Resolve party identities and enforce identity consistency
7. Validate proof where required
8. Validate acceptance expiry
9. Evaluate authorization / delegation / governance policy
10. Resolve expected handler
11. Determine authoritative runtime side-effects/exposure
12. Apply Framework duplicate-execution/document-conflict guard
13. Process any valid task-control state applicable to the target task
14. Obtain MRTR input/approval if policy requires it
15. If asynchronous, create or associate an MCP Task execution handle
16. Immediately before each irreversible effect:
      re-evaluate required authority/policy/control conditions
17. Execute only the permitted effect
18. Produce Framework-valid success, error, acknowledgement, control response, or next-step response
19. Preserve Trust Task identifiers, task-digest citations, and ceremony semantics
20. Return synchronously or as MCP Task result
```

Implementations MAY optimize the sequence provided they preserve the same semantic and security invariants.

---

## 19. Conformance requirements

### 18.1 Client

A conforming client MUST:

- submit Trust Task documents through `trust-task.execute`;
- preserve Framework identifiers, correlation, response, proof, expiry, and ceremony semantics;
- distinguish Trust Task identifiers from MCP request/task identifiers;
- validate returned Trust Task response documents before relying on them; and
- not interpret MCP completion as Trust Task completion where the result is an error or `trust-task-next-step`.

### 18.2 Server

A conforming server MUST:

- expose `trust-task.execute`;
- validate Framework and task-specific requirements before execution;
- enforce identity consistency;
- evaluate authorization independently of ordinary document-proof validation;
- preserve Trust Ceremony semantics independently of MCP session/execution state;
- distinguish semantic failures from MCP protocol failures;
- apply duplicate-execution safeguards for consequential tasks;
- keep MCP cancellation separate from `trust-task-control` cancellation/suspension/resumption;
- re-evaluate required authority and task-control conditions before each irreversible effect;
- preserve task-digest-bound citations when Trust Task evidence is relied upon outside the exchange;
- treat `trust-task-ok` only as the Framework-defined non-reliable courtesy acknowledgement;
- avoid treating descriptive MCP metadata as party identity; and
- preserve all identifier and lifecycle separations defined by this binding.

---

## 20. Relationship to DTG

This binding does not require a Decentralized Trust Graph.

A DTG profile MAY provide evidence used during authorization, including:

- party recognition;
- Verifiable Trust Community membership;
- agent/operator relationships;
- delegation or mandate;
- capability constraints;
- subject relationships;
- standing;
- suspension/revocation state; and
- applicable governance rules.

Such evidence is an input to the consumer's authorization decision. Recognition, membership, identity, or possession of evidence does not by itself compel execution.

---

## 21. Interoperability profile

A future interoperability profile SHOULD define at least:

- supported MCP transport/authentication profile;
- mapping of authenticated MCP principals to VIDs;
- whether in-band `proof` is mandatory;
- supported Trust Task framework/schema versions;
- supported Trust Task types;
- MCP Tasks support;
- MRTR support;
- duplicate-execution retention and document-conflict expectations;
- `trust-task-control` support and any explicit MCP-cancel-to-semantic-control policy;
- task-specific payload validator/draft/resource-limit profile;
- portable evidence citation/digest support; and
- security/assurance requirements for consequential execution.

---

## 22. References

- Trust Tasks Framework pinned baseline: `https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/7e0d755f5b815498c861cacecee5cae49b3f14eb/SPEC.md`
- Trust Tasks current editor’s draft: `https://github.com/trustoverip/dtgwg-trust-tasks-tf/blob/main/SPEC.md`
- MCP 2026-07-28: `https://modelcontextprotocol.io/specification/2026-07-28`
- MCP Tasks extension: `https://modelcontextprotocol.io/extensions/tasks/overview`
- MCP 2026-07-28 release: `https://blog.modelcontextprotocol.io/posts/2026-07-28/`

---

## Appendix A — Design rationale (non-normative)

The central design rule is that MCP should carry and execute Trust Tasks without absorbing their trust semantics.

This produces a stable layering:

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

The separation permits Trust Tasks to remain transport-independent while allowing MCP-native agents and tools to participate in verifiable work without treating MCP identity, session state, or task execution state as substitutes for trust, authority, or governance.
