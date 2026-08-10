# TSP-Enabled AI Agent Protocols — Implementation Analysis 0.1

**Status:** Exploratory  
**Artifact version:** 0.1  
**Upstream:** Trust over IP AIMWG, *TSP-Enabled AI Agent Protocols*  
**Reviewed baseline:** v1.0 Draft / Editor's Copy, reviewed 2026-08-10  
**Upstream status:** Independent analysis; not submitted

## Purpose

This artifact examines the draft *TSP-Enabled AI Agent Protocols* specification from the perspective of independent implementation and interoperability.

It does not define an alternative specification and does not represent Trust over IP Foundation, AIMWG, TSP, MCP, Trust Tasks, or any other upstream consensus. Its purpose is to identify places where additional normative definition, protocol mechanics, schemas, security assumptions, conformance criteria, or test evidence appear necessary for independent interoperable implementations.

## Scope

The review focuses on implementation-significant gaps rather than editorial style. In particular, it examines:

- conformance boundaries;
- cryptographic payloads and evidence;
- VID identity and lifecycle semantics;
- TEA control boundaries;
- Authenticated Exchange state and time semantics;
- delegation and authorization credentials;
- capability attenuation;
- policy extensibility;
- accountability evidence;
- security and threat assumptions;
- transport negotiation and downgrade resistance;
- MCP-over-TSP interoperability; and
- protocol evolution, errors, and test vectors.

## Method

Each finding is captured as an implementation gap, then traced to likely interoperability consequences and a candidate path to resolution. The analysis intentionally separates:

1. **specification ambiguity** — text that permits multiple reasonable implementations;
2. **implementation incompleteness** — normative behavior that cannot yet be implemented from the draft alone;
3. **interoperability risk** — plausible cases where independently developed implementations can disagree or fail unsafely; and
4. **candidate upstream feedback** — issue-shaped text that may be submitted upstream later if still relevant.

## Contents

- [Implementation gap analysis](implementation-gap-analysis.md)
- [Requirements matrix](requirements-matrix.md)
- [Interoperability risk register](interoperability-risk-register.md)
- [Candidate upstream issues](upstream-issue-candidates.md)
- [TEA / MCP / Trust Tasks mapping](../../../mappings/tea-mcp-trust-tasks.md)

## Relationship to other lab work

The existing [MCP Binding for Trust Tasks 0.2](../../../bindings/trust-tasks/mcp/0.2/spec.md) already makes explicit choices about conformance, semantic separation, correlation, execution, and authorization boundaries. This analysis uses those choices as interoperability reference points, not as requirements imposed on the TEA draft.

The mapping artifact asks where TEA, MCP, and Trust Tasks should compose without collapsing identity, transport, execution, authority, agreement, or evidence semantics into one layer.

## Maturity and next steps

This artifact remains **Exploratory**. A future version may move to **Experimental** when one or more gaps are expressed as concrete profiles, schemas, state machines, or test vectors and exercised in the corresponding `experiments/tsp-enabled-ai-agents/` workstream.

## AI-tool usage note

This artifact was prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer. This disclosure is included voluntarily; no published AIMWG/TF guidance governing such usage or disclosure was identified at the time of this baseline.
