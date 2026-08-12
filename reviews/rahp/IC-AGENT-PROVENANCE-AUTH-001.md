# RAHP pressure test — IC-AGENT-PROVENANCE-AUTH-001

## Review boundary

This is a lab-level RAHP pressure test of the **composition seam**, not a claim that any referenced protocol is itself unsafe or RAHP-conformant/non-conformant.

## Affected parties

Principals delegating to agents, people represented by submitted evidence, creators and rights holders, relying parties, operators, recipients of automated decisions, people subject to payments/denials/certification/diagnosis/adjudication, and reviewers attempting later redress.

## Priority harms and corresponding tests

| Harm pathway | Composition failure | Required test/control |
|---|---|---|
| Authority laundering | Strong identity or discoverability is treated as delegation | `APA-NEG-001`, `APA-NEG-002`; explicit delegation and scope check |
| False epistemic elevation | Valid provenance is treated as proof that a claim is true | `APA-NEG-003`; prohibited provenance-to-truth inference |
| Unauthorized consequential action | Verification success is converted directly into approval/payment/certification/etc. | `APA-NEG-004`; separate decision-authority evidence |
| Stale-authority execution | Revoked/suspended authority is not observed | `APA-NEG-005`; freshness + fail-closed current-state check |
| Historical erasure or distortion | Current revocation rewrites what was authoritative when the action occurred | `APA-NEG-006`; requested-time/current-state separation |
| Delegation drift | A sub-agent receives broader authority than its delegator held | `APA-NEG-007`; monotonic scope attenuation |
| Accountability loss | Evidence depends only on an ephemeral session and principal/delegation cannot be reconstructed | `APA-NEG-008`; portable action-evidence bundle |
| Unreviewable automated effect | A person cannot reconstruct why an effect occurred or challenge it | decision/effect receipts, replay path, redress reference |
| Correction destroys history | Remediation overwrites prior provenance/action records | supersession lineage rather than historical rewrite |

## Security/hardening considerations

The eventual executed experiment should additionally pressure-test:

- confused-deputy behavior across verifier/orchestrator agents;
- replay of stale delegation evidence;
- substitution of a different provenance object after authority verification;
- mismatch between resolved agent identity and runtime actor;
- trust-registry response caching past an allowed freshness window;
- sub-agent/tool invocation without principal-visible lineage;
- policy downgrade when one evidence source is unavailable;
- forged or incomplete decision/effect receipts.

## Redress expectation

A consequential action should expose enough durable evidence to answer: who acted, for whom, under what scope, against which resource, using which provenance and trust-state evidence, under which policy, who held decision authority, what effect occurred, and how the result can be corrected or appealed.

## Routing

Findings should be routed to the component that owns the missing semantic or control. The Interop Lab should not patch around an upstream ownership gap by silently redefining authority, provenance, lifecycle, or decision semantics locally.
