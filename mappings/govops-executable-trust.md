# GovOps capability, authority, decision, enforcement, and evidence mapping

**Interop Case:** `IC-GOVOPS-EXEC-TRUST-001`  
**Status:** Experimental repository-owned mapping  
**Admission / judgment anchor:** [Discussion #6](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/discussions/6)  
**Implementation issue:** [#82](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/82)

## Purpose

This mapping makes the Discussion #6 boundary mechanically testable without redefining any upstream specification. GovOps remains authoritative for the governed capability and operational-governance boundary while remaining deliberately policy-engine-neutral. TSMM provides a semantic projection, GAAM provides authority/delegation/revocation semantics, and TIS provides portable artifact contracts. The lab owns only the composition profile below.

The mapping MUST preserve the following separation:

```text
capability -> request/context -> authority evidence -> authorization evaluation
           -> decision -> enforcement -> observed effect -> evidence -> assurance
```

No arrow is an equivalence relation. Later stages cannot manufacture the authority required by earlier stages, and an `Allow` decision does not by itself establish enforcement or successful execution.

## Upstream clarification incorporated

Discussion #6 clarified five boundaries that now govern this profile:

1. GovOps is policy-engine-neutral; the experiment MUST NOT imply a required PDP implementation.
2. Portable authority/delegation evidence is authorization input, like identity, credentials, attestations, or other contextual evidence; GovOps does not own authority/delegation/attenuation semantics.
3. The GovOps authorization boundary ends when policy is evaluated and the decision is enforced.
4. Request shape is moving toward PARC; this profile MAY provide a PARC-aligned request projection without making PARC a normative dependency.
5. Correlation and governance observability use multiple identifiers. In addition to `capability_id` and the decision, `decision_id`, `policy_store_id`, `policy_store_version`, and relevant runtime artifact identifiers SHOULD be observable where available.

Decision, execution, and evidence correlation remain outside the GovOps responsibility boundary and are modeled locally for this experiment.

## Local composition profile

The experiment uses the GovOps capability:

```yaml
action: approve
resource: loan
```

The lab profile introduces correlation identifiers only where the experiment requires them. These identifiers are local composition fields unless explicitly described as GovOps-observable fields; none broadens GovOps semantics by assumption.

| Field | Owner/source | Meaning | Prohibited inference |
|---|---|---|---|
| `capability_id` | GovOps | Identifier of the exposed governed capability | identity, entitlement, authority, permission, or transaction identity |
| `request_id` | local request context | Correlates one authorization request | durable capability identity |
| `principal_ref` | request/runtime context | Reference to requesting principal | authority or entitlement |
| `authority_ref` | GAAM projection | Authority/delegation evidence evaluated for this request | `Allow` |
| `decision_id` | authorization runtime | Observable identifier of one authorization decision | successful enforcement or execution |
| `policy_store_id` | authorization runtime | Observable identifier of the evaluated policy store | authority evidence |
| `policy_store_version` | authorization runtime | Exact evaluated policy-store version | current authority or successful effect |
| `runtime_artifact_ids` | runtime | Optional identifiers such as `access_token.jti`, `id_token.jti`, or `transaction_token.jti` | authority, entitlement, or proof of execution |
| `effect_id` | runtime/observer | Identifies the observed runtime effect | authorization by itself |
| `evidence_bundle_id` | TIS evidence profile | Groups immutable evidence references | authority or authorization |
| `assurance_result_id` | local/TIS assurance profile | Identifies a later evaluation | retroactive authorization |

`capability_id` is always carried through as the GovOps-owned capability identifier. Correlation is an explicit graph across independently owned identifiers, not an overloaded common transaction key.

## PARC-aligned request projection

The profile does not require PARC conformance. It records the direction of travel identified in Discussion #6 and keeps the request boundary compatible with an action/resource-oriented request shape:

```yaml
request_id: req:LN-2026-004217:approve:01
principal_ref: credit-officer-a
capability_id: govops:loan:approve
action: approve
resource: loan
context:
  amount_inr: 3500000
  jurisdiction: IN-WB
```

This projection exists so a later PARC binding can be tested without changing the experiment's semantic ownership model.

## Semantic ownership mapping

| Governance concern | Authoritative owner in this experiment | Projection/use |
|---|---|---|
| capability definition and identifier | GovOps | TSMM/TIS MAY reference, never redefine |
| operational-governance / authorization boundary | GovOps | boundary definition only; no mandated policy engine |
| action/resource semantics | GovOps capability, projected through TSMM | semantic classification only |
| principal/request context | requesting/runtime system | input to authorization evaluation |
| source authority | GAAM semantics | evaluated evidence input |
| delegated authority and narrowing | GAAM semantics | authorization input; cannot widen source authority |
| revocation/current validity | GAAM semantics | evaluated relative to decision time |
| policy evaluation | policy-engine-neutral authorization runtime | produces `Allow`, `Deny`, or `Challenge` |
| decision enforcement | policy-engine-neutral authorization runtime | enforces the evaluated outcome |
| request/decision/effect correlation | local experiment/runtime observability | explicit correlation graph outside GovOps responsibility |
| decision/effect evidence packaging | TIS | portable representation of what occurred |
| later assurance conclusion | TIS/local evaluator | evaluates evidence; never creates authority |

## Evaluation pipeline

A conforming experiment processes one request in this order:

1. **Resolve capability.** Resolve the GovOps `capability_id` to the exposed `(action, resource)` operation.
2. **Bind request context.** Assign `request_id` and `principal_ref`; the shape MAY be PARC-aligned, but request representation does not create authority.
3. **Evaluate authority evidence.** Resolve source authority, delegation, validity, revocation state, scope, jurisdiction, limits, time bounds, and re-delegation permission using GAAM semantics.
4. **Construct authorization input.** Preserve capability, request/principal context, authority evidence, identity/credential/attestation context, and policy references as distinct inputs.
5. **Obtain runtime decision.** A policy-engine-neutral authorization system returns `Allow`, `Deny`, or `Challenge` and exposes `decision_id`; it SHOULD expose `policy_store_id`, `policy_store_version`, and relevant runtime artifact identifiers.
6. **Enforce decision.** The runtime MUST make enforcement state observable. `Allow` without established enforcement does not establish successful authorization execution.
7. **Admit or block execution.** Only an enforced admissible `Allow` permits the modeled effect to proceed. `Deny` blocks it; `Challenge` leaves it pending until resolved.
8. **Observe effect.** An executed effect receives `effect_id` and MUST correlate to the admitting `decision_id` and `capability_id`.
9. **Package evidence.** TIS packages immutable references to capability, request, evaluated authority/context evidence, decision, policy store/version, enforcement state, and any observed effect.
10. **Evaluate assurance.** A later evaluator assesses completeness, integrity, correlation, provenance, and policy/evidence consistency. The result cannot change historical authorization or create present authority.

## Required state separation

The model records independently:

```yaml
capability_state: resolved | unresolved
authority_state: valid | invalid | revoked | expired | insufficient | unresolved
policy_decision: allow | deny | challenge | not_evaluated
enforcement_state: enforced | not_enforced | not_established | pending
execution_state: admitted | blocked | pending | not_attempted | not_established
effect_state: observed | absent | mismatched | not_applicable
correlation_state: valid | invalid | indeterminate | not_evaluated
policy_provenance_state: complete | incomplete | indeterminate | not_evaluated
evidence_state: complete | incomplete | inconsistent | not_emitted
assurance_state: pass | fail | indeterminate | not_evaluated
```

A state in one dimension MUST NOT be silently substituted for a state in another dimension.

## Fail-closed transition rules

The experimental evaluator and subsequent vectors MUST reject, block, or preserve indeterminacy for at least these transitions:

- `authority_state=valid` -> implicit `policy_decision=allow`;
- delegated scope/limits broader than source authority;
- `policy_decision=deny|challenge` -> successful execution admission;
- `policy_decision=allow` with `enforcement_state=not_established` -> successful authorization execution;
- an observed effect whose `decision_id`, `request_id`, or `capability_id` does not match its lineage;
- substitution of a valid `decision_id` from another request/capability/effect lineage;
- missing or ambiguous `policy_store_version` -> assurance `pass`;
- authority revoked before decision represented as valid at decision time;
- post-execution revocation rewriting truthful historical effect evidence;
- `evidence_state=complete` -> inferred current authority;
- `assurance_state=pass` -> retroactive authorization.

## Portable decision evidence minimum

The local TIS decision profile MUST preserve, directly or by immutable reference:

```yaml
capability_id: <govops capability id>
request_id: <request correlation id>
principal_ref: <principal context reference>
authority_evidence_refs:
  - <immutable authority/delegation evidence reference>
decision_id: <authorization decision id>
policy_store_id: <evaluated policy store id>
policy_store_version: <evaluated policy store version>
runtime_artifact_ids:
  - <optional runtime artifact identifier>
decision: allow | deny | challenge
decision_time: <timestamp>
decision_point: <authorization system reference>
enforcement_state: enforced | not_enforced | not_established | pending
```

If an effect occurs, runtime evidence additionally records `effect_id`, `decision_id`, `capability_id`, observation time, and effect outcome.

## Correlation and observability rule

The experiment does not treat `capability_id` as a universal lifecycle key. The same capability may be invoked many times and produce different decisions and effects. Correlation therefore uses explicit edges among identifiers:

```text
request_id --invokes--> capability_id
request_id --produces--> decision_id
decision_id --evaluated-against--> policy_store_id@policy_store_version
decision_id --references--> runtime_artifact_ids
decision_id --enforced-as--> effect_id
evidence_bundle_id --references--> request_id + capability_id + decision_id + effect_id
assurance_result_id --evaluates--> evidence_bundle_id
```

Observability makes governance state inspectable; it does not grant authority. `decision_id`, policy identifiers, token `jti`s, telemetry references, and other runtime observability artifacts MUST NOT be interpreted as authority, entitlement, successful enforcement, or successful execution merely because they correlate.

## Revocation and historical truth

Revocation remains time-relative. Current authority validity may differ from historical execution truth. Revoking authority changes whether it may be exercised now or in the future; it does not retroactively invalidate truthful evidence showing that a prior execution occurred when relevant authority and policy conditions were valid.

## Evidence produced at this maturity

Experimental maturity produces mapping and scenario evidence only. It does **not** yet claim implementation conformance or successful interoperability. Candidate maturity requires executable positive/negative vectors plus known limitations. Interoperability Tested requires deterministic execution and a hash-bound evidence manifest.
