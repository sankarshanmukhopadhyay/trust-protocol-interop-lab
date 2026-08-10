# Implementation Requirements Matrix

This matrix converts the gap analysis into implementation-oriented requirements and evidence needs. It is **not** an upstream conformance table; it is a lab artifact for identifying where interoperable implementation depends on additional specification work.

| ID | Area | Draft requirement / architectural claim | Implementable from draft alone? | Missing definition | Interop impact | Suggested evidence/test |
|---|---|---|---|---|---|---|
| TEA-001 | Conformance | TEAs follow normative requirements | Partial | Conformance classes and applicability | High | Role-specific conformance matrix |
| TEA-002 | Signed payload | TEA implements native signed payload | No | Wire format, canonicalization, signature input, verification | Critical | Golden signed-payload vectors |
| TEA-003 | Identity | TEA uses durable VID with rotation/history | Partial | Method profile, lifecycle, caching, compromise rules | High | Resolution/rotation/recovery vectors |
| TEA-004 | Identity | IVID and AVID distinguish introduction and authorization use | Partial | Binding, transition, multiplicity, rotation behavior | High | IVID/AVID continuity scenarios |
| TEA-005 | Control boundary | Model context/memory/tool access passes through Controller | Partial | Enforcement boundary and remote-component rules | High | Deployment-profile threat tests |
| TEA-006 | Composite TEA | Composite TEA may use one VID | Partial | Component identity, control ownership, attribution | High | Multi-component attribution scenarios |
| TEA-007 | Authenticated Exchange | Propose/Accept/Ack/Withdraw form agreement protocol | Partial | State machine, correlation, races, restart | Critical | Model-based state-machine tests |
| TEA-008 | Authenticated Exchange | Ack is binding act | Partial | Late/duplicate Ack and crossed-message rules | Critical | Concurrency/replay test vectors |
| TEA-009 | Time | Messages/credentials use expiry and validity | Partial | Clock skew, timestamp format, boundary semantics | High | Boundary/skew/offline tests |
| TEA-010 | Delegation | Authorization and duties use ACDC | No | Normative schema and processing algorithm | Critical | Schema validation + issuance vectors |
| TEA-011 | Delegation | Credential status is checked on exercise | Partial | Freshness, unavailability, suspend/revoke behavior | Critical | Fail-closed status scenarios |
| TEA-012 | Capability | Delegation strictly attenuates authority | No | Closed vocabulary, partial order, meet/reduction | Critical | Property/adversarial attenuation tests |
| TEA-013 | Capability | Multiple authority sources compose deterministically | No | AND/OR/nesting and empty-authority semantics | Critical | Composition vectors |
| TEA-014 | Policy | Open policy can further restrict authority | Partial | Language/version/input/failure semantics | High | Unsupported/malicious policy tests |
| TEA-015 | Accountability | Delegation chain supports accountability trace | Partial | Action/effect/duty evidence model | High | End-to-end evidence reconstruction |
| TEA-016 | Accountability | Chain terminates in person/organization | Partial | Principal-to-VID assurance semantics | High | Credential/governance linkage scenarios |
| TEA-017 | Transport | TEA supports specified transports/modes | Partial | Discovery, negotiation, framing, downgrade rules | High | Cross-transport negotiation tests |
| TEA-018 | MCP | MCP can operate over TSP | No | Role/session/message/security mapping | Critical | MCP-over-TSP interoperability harness |
| TEA-019 | Security | Protocol provides secure agent interaction | Partial | Threat model, assumptions, failure requirements | Critical | Threat-control-test traceability |
| TEA-020 | Evolution | Protocol can evolve interoperably | Partial | Versioning, extensions, unknown handling, errors | High | Cross-version compatibility tests |

## Proposed lab test families

### AE — Authenticated Exchange

- `AE-01`: successful Propose → Accept → Ack
- `AE-02`: counter-proposal and supersession
- `AE-03`: duplicate Ack is idempotent
- `AE-04`: Withdraw crossing Ack
- `AE-05`: expired proposal / late acceptance
- `AE-06`: restart before Ack
- `AE-07`: replayed signed message

### DEL — Delegation and attenuation

- `DEL-01`: single-hop valid delegation
- `DEL-02`: multi-hop strict attenuation
- `DEL-03`: attempted authority widening
- `DEL-04`: conflicting duties
- `DEL-05`: revoked ancestor credential
- `DEL-06`: stale/unavailable status service
- `DEL-07`: unsupported open policy

### VID — Identity lifecycle

- `VID-01`: initial resolution
- `VID-02`: valid rotation/pre-rotation
- `VID-03`: invalid rotation
- `VID-04`: compromise recovery
- `VID-05`: deactivation
- `VID-06`: IVID/AVID transition

### MCP — MCP-over-TSP

- `MCP-01`: session establishment with TEA identity binding
- `MCP-02`: tool discovery and authenticated invocation
- `MCP-03`: delegation presented for tool execution
- `MCP-04`: signed/portable tool result
- `MCP-05`: cancellation and error propagation
- `MCP-06`: downgrade attempt

## AI-tool usage note

This matrix was prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer.
