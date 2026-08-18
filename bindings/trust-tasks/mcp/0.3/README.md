# MCP Binding for Trust Tasks — v0.3

**Status:** Candidate / Experimental  
**Upstream status:** Not submitted  
**Trust Tasks baseline:** Editor’s Draft document version 0.3, pinned to commit `7e0d755f5b815498c861cacecee5cae49b3f14eb` (2026-08-16)  
**MCP baseline:** 2026-07-28

- [Candidate specification](spec.md)
- [Examples](examples/)
- [Interop test plan](../../../../experiments/mcp-trust-tasks/test-plan.md)
- [Previous immutable baseline: v0.2](../0.2/spec.md)

This is independent exploratory work and is not an approved specification of Trust over IP, DTGWG, the Trust Tasks Task Force, or the Model Context Protocol project.

## Main design proposition

Trust Tasks own portable work semantics and semantic task control. MCP owns interaction and execution mechanics. Trust Ceremonies own verifiable composition. Authorization remains an independent consumer-policy decision informed by relevant trust/governance evidence.

Version 0.3 rebases the binding on upstream Trust Tasks changes that make duplicate-execution protection, authorization separation, pre-effect authority re-evaluation, task control, task-digest citations, acknowledgement semantics, transport security profiles, and payload validation directly testable interoperability obligations.
