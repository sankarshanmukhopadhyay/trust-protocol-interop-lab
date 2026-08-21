# GovOps capability, authority, decision, and evidence mapping

**Interop Case:** `IC-GOVOPS-EXEC-TRUST-001`  
**Status:** Experimental repository-owned mapping  
**Upstream anchor:** `GovOpsWG/GovOps` main at `319124840565e3ccf82fcf6b8dc45c9582a0186f`

## Purpose

This mapping makes the Discussion #6 boundary mechanically testable without redefining any upstream specification. GovOps remains authoritative for the governed capability and the runtime authorization decision. TSMM provides a semantic projection, GAAM provides authority/delegation/revocation semantics, and TIS provides portable artifact contracts. The lab owns only the composition profile below.

The mapping MUST preserve the following separation:

```text
capability -> authority evidence -> policy input -> authorization decision
           -> admitted execution -> observed effect -> evidence -> assurance
```

No arrow is an equivalence relation. Later stages cannot manufacture the authority required by earlier stages.

## Local composition profile

The experiment uses the GovOps capability:

```yaml
action: approve
resource: loan
```

The lab profile introduces correlation identifiers only where the experiment requires them. These identifiers are local composition fields and are not asserted to be GovOps, TSMM, GAAM, or TIS normative fields.

| Local field | Owner/source | Meaning | Prohibited inference |
|---|---|---|---|
| `capability_id` | GovOps | Identifier of the exposed governed capability | identity, entitlement, authority, or permission |
| `request_id` | local request context | Correlates one authorization request | durable capability identity |
| `principal_ref` | local request context | Reference to the requesting principal | authority or entitlement |
| `authority_ref` | GAAM projection | Reference to authority/delegation evidence evaluated for this request | `Allow` |
| `policy_version` | GovOps/PDP policy layer | Version of policy used for the runtime decision | authority evidence |
| `decision_id` | TIS decision artifact profile | Correlates the runtime authorization decision | successful execution |
| `effect_id` | runtime/observer | Identifies the observed runtime effect | authorization by itself |
| `evidence_bundle_id` | TIS evidence profile | Groups immutable evidence references | authority or authorization |
| `assurance_result_id` | local/TIS assurance profile | Identifies a later evaluation of the evidence | retroactive authorization |

`capability_id` is always carried through as a GovOps-owned identifier. No local or portable identifier replaces it.

## Semantic ownership mapping

| Governance concern | Authoritative owner in this experiment | Projection/use |
|---|---|---|
| capability definition and identifier | GovOps | TSMM/TIS MAY reference, never redefine |
| action/resource semantics | GovOps capability, projected through TSMM | semantic classification only |
| principal context | requesting/runtime system | input to policy evaluation |
| source authority | GAAM semantics | evaluated evidence input |
| delegated authority and narrowing | GAAM semantics | policy input; cannot widen source authority |
| revocation/current validity | GAAM semantics | evaluated at the decision time |
| runtime policy and `Allow`/`Deny`/`Challenge` | GovOps/PDP | sole authorization decision in this experiment |
| execution/effect admission | runtime constrained by GovOps/PDP result | proceeds only from an admissible decision |
| decision/effect evidence packaging | TIS | portable representation of what occurred |
| later assurance conclusion | TIS/local evaluator | evaluates evidence; never creates authority |

## Evaluation pipeline

A conforming experiment processes one request in this order:

1. **Resolve capability.** Resolve the GovOps `capability_id` to the exposed `(action, resource)` operation.
2. **Bind request context.** Assign `request_id` and `principal_ref` without treating either as authority.
3. **Evaluate authority evidence.** Resolve source authority, delegation, validity, revocation state, scope, jurisdiction, monetary/risk limits, time bounds, and re-delegation permission using GAAM semantics.
4. **Construct policy input.** Preserve capability, request/principal context, authority evaluation, and policy version as distinct inputs.
5. **Obtain runtime decision.** The GovOps/PDP policy layer returns `Allow`, `Deny`, or `Challenge` and a `decision_id` is assigned to the portable decision artifact.
6. **Admit or block execution.** Only an admissible `Allow` permits the modeled effect to proceed. `Deny` blocks it; `Challenge` leaves it unexecuted pending the challenge outcome.
7. **Observe effect.** An executed effect receives `effect_id` and MUST reference the admitting `decision_id` and `capability_id`.
8. **Package evidence.** TIS packages immutable references to capability, request context, evaluated authority evidence, policy version, decision, decision time/point, and any observed effect.
9. **Evaluate assurance.** A later evaluator may assess completeness, integrity, correlation, and policy/evidence consistency. The assurance result cannot change the historical authorization decision or create present authority.

## Required state separation

The model records the following independently:

```yaml
capability_state: resolved | unresolved
authority_state: valid | invalid | revoked | expired | insufficient | unresolved
policy_decision: allow | deny | challenge | not_evaluated
execution_state: admitted | blocked | pending | not_attempted
effect_state: observed | absent | mismatched | not_applicable
evidence_state: complete | incomplete | inconsistent | not_emitted
assurance_state: pass | fail | indeterminate | not_evaluated
```

A state in one dimension MUST NOT be silently substituted for a state in another dimension.

## Fail-closed transition rules

The experimental evaluator and subsequent vectors MUST reject or flag at least these transitions:

- `authority_state=valid` -> implicit `policy_decision=allow`;
- delegated scope/limits broader than the source authority;
- `policy_decision=deny` or `challenge` -> `execution_state=admitted`;
- an observed effect whose `decision_id` or `capability_id` does not match the admitting decision;
- authority revoked before the decision being represented as valid at decision time;
- authority revoked after execution causing historical effect evidence to be rewritten or deleted;
- `evidence_state=complete` -> inferred current authority;
- `assurance_state=pass` -> retroactive authorization of an action that lacked an admissible `Allow`.

## Portable decision evidence minimum

The local TIS decision profile MUST preserve, directly or by immutable reference:

```yaml
capability_id: <govops capability id>
request_id: <request correlation id>
principal_ref: <principal context reference>
policy_version: <evaluated GovOps/PDP policy version>
authority_evidence_refs:
  - <immutable authority/delegation evidence reference>
decision: allow | deny | challenge
decision_time: <timestamp>
decision_point: <PDP/runtime decision-point reference>
decision_id: <decision correlation id>
```

If an effect occurs, runtime evidence additionally records `effect_id`, `decision_id`, `capability_id`, observation time, and effect outcome.

## Capability identifier clarification

This mapping intentionally does not answer whether GovOps intends `capability_id` to be the durable cross-stage correlation key for authorization, execution, observation, and external governance evidence. The lab preserves the identifier as a capability reference and adds separate `request_id`, `decision_id`, and `effect_id` fields so the experiment does not broaden GovOps semantics by assumption.

An authoritative GovOpsWG clarification can later tighten this profile without changing the current evidence lineage.

## Evidence produced at this maturity

Experimental maturity produces mapping and scenario evidence only. It does **not** yet claim that an implementation conforms to this profile. Candidate maturity requires positive and negative executable vectors plus known limitations; Interoperability Tested requires deterministic execution and a hash-bound evidence manifest.
