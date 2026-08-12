---
layout: default
title: Semantic Ownership
---
# Semantic Ownership

Every Interop Case declares which component is authoritative for each semantic concern used by the composition.

## Ownership rule

A binding MAY transport, reference, or project another component's state without becoming the semantic owner of that state. Where two layers use superficially similar identifiers or states, the case MUST state whether they are linked, projected, or independent.

## Minimum ownership questions

| Concern | Required question |
|---|---|
| Identity | Which artifact identifies the actor, principal, operator, or service? |
| Authority | Which evidence establishes permission to produce the relevant effect? |
| Delegation | Who issued it, what scope applies, and how is attenuation enforced? |
| Lifecycle | Which source determines active, suspended, revoked, expired, or historical state? |
| Correlation | Which identifiers correlate protocol exchange, work item, ceremony, or execution? |
| Execution | Which layer controls invocation and execution-local state? |
| Evidence | Which artifacts survive the transport/session and can be independently verified? |
| Revocation | Which authority may revoke what, and how does that propagate? |
| Decision | Which local policy admits or rejects the requested effect? |

## Prohibited inference pattern

Cases should include negative invariants whenever an implementer could incorrectly infer equivalence, for example:

- authenticated transport ≠ delegated authority;
- discoverable agent ≠ authorized agent;
- valid credential ≠ permission to execute;
- name resolution ≠ identity assurance;
- protocol success ≠ semantic success;
- current state ≠ historical state at a requested time.
