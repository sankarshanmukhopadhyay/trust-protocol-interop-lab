# Interoperability Risk Register

This register translates specification gaps into concrete failure modes that can be exercised experimentally.

| Risk ID | Trigger | Failure mode | Likely consequence | Severity | Primary gap | Candidate mitigation |
|---|---|---|---|---|---|---|
| R-01 | Different Ack/expiry interpretation | Peers disagree whether agreement exists | Conflicting actions/accountability | Critical | GAP-06, GAP-07 | Normative state/time model |
| R-02 | Duplicate/replayed exchange message | Consequential operation executed twice | Financial/operational harm | Critical | GAP-06 | Idempotency + replay rules |
| R-03 | Undefined attenuation lattice | Verifier computes broader authority | Unauthorized action | Critical | GAP-05 | Closed core + meet algorithm |
| R-04 | Revoked/stale delegation status | Invalid authority accepted | Unauthorized action | Critical | GAP-04 | Fail-closed status semantics |
| R-05 | Divergent ACDC encoding | Credential rejected or misread | Interop failure / incorrect authorization | Critical | GAP-04 | Normative schema/vectors |
| R-06 | Different signed-payload construction | Evidence cannot be verified cross-implementation | Loss of portability/accountability | Critical | GAP-01 | Canonical payload/signature profile |
| R-07 | VID rotation ambiguity | Valid actor rejected or compromised actor accepted | Availability/security failure | High | GAP-09 | VID lifecycle profile |
| R-08 | IVID/AVID mismatch | Introduction identity incorrectly treated as authority | Identity/authorization confusion | High | GAP-09 | Explicit binding rules |
| R-09 | Remote model bypasses controller | Unmediated tool/data access | Accountability/control failure | High | GAP-10 | Enforced control-boundary profile |
| R-10 | Composite TEA hides component control | Action attributed to wrong principal | Audit/liability ambiguity | High | GAP-10, GAP-11 | Component attribution evidence |
| R-11 | Different open policy engine | Same delegation accepted/rejected differently | Authorization divergence | High | GAP-13 | Profiled deterministic policy evaluation |
| R-12 | Unsupported policy fails open | Restriction silently ignored | Unauthorized action | Critical | GAP-13 | Mandatory fail-closed rule |
| R-13 | Transport fallback | Peer uses weaker path without explicit consent | Downgrade / privacy loss | High | GAP-12 | Negotiation + downgrade resistance |
| R-14 | Crypto mode mismatch | Peers connect insecurely or fail unexpectedly | Security/availability failure | High | GAP-12 | Mandatory common suite |
| R-15 | MCP role/session mapping differs | Tool invocation loses identity/authority context | Incorrect authorization | Critical | GAP-08 | Normative MCP-over-TSP profile |
| R-16 | MCP result is session-bound only | Evidence cannot be verified later/elsewhere | Accountability loss | High | GAP-08, GAP-11 | Portable signed result profile |
| R-17 | No shared conformance claims | Implementations assume unsupported features | Deployment incompatibility | High | GAP-03 | Role-specific conformance classes |
| R-18 | No extension/version rules | New field interpreted inconsistently | Persistent interoperability split | High | GAP-14 | Version/extension registry |
| R-19 | Excessive delegation depth/branching | Resource exhaustion | Denial of service | High | GAP-02, GAP-05 | Complexity/chain limits |
| R-20 | Prompt/tool attack occurs inside authenticated channel | Authenticated malicious content treated as trustworthy | Unsafe model/tool behavior | Critical | GAP-02 | Explicit non-goal + application controls |

## Severity convention

- **Critical** — can plausibly create unauthorized consequential action, conflicting agreement state, non-portable security evidence, or severe control failure.
- **High** — likely to create cross-implementation disagreement, security degradation, audit ambiguity, or significant availability failure.
- **Medium** — primarily affects operational predictability or implementation portability without directly widening authority.

## Experimental use

Each risk should eventually be linked to one or more executable scenarios in `experiments/tsp-enabled-ai-agents/`. The goal is to turn specification uncertainty into reproducible evidence rather than keeping it as prose-only critique.

## AI-tool usage note

This risk register was prepared with assistance from AI tools and subsequently reviewed and adopted by the repository maintainer.
