# DPAC × Agent Security Harness adversarial integration

This experiment tracks [#170](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/170) and adds an external adversarial evidence producer around the existing `IC-DPAC-ACTUATION-001` runtime boundary.

## Proposition

Determine whether an independently developed adversarial harness can attempt to falsify DPAC non-collapsibility and fail-closed properties against the existing enforced Workspace boundary without allowing the harness to become the authority for the resulting assurance conclusion.

The target remains [`../dpac-enforced-boundary/`](../dpac-enforced-boundary/). This directory contains only the integration contract, adapter/evidence normalization machinery, and attributable external-harness execution material. It MUST NOT become a competing DPAC implementation.

## Authority boundary

- `msaleme/red-team-blue-team-agent-fabric` owns Agent Security Harness implementation, attack semantics, releases, and upstream result vocabulary.
- The Interop Lab owns the DPAC propositions, target adapter, effect oracle, normalization, evidence retention, and case/maturity interpretation.
- Harness output is evidence input. It does not establish DPAC conformance, production security, certification, or case promotion by itself.
- RAHP orchestration is outside this tranche.

## Pinned external dependency

The first integration baseline is Agent Security Harness `v4.21.1`:

- upstream repository: `msaleme/red-team-blue-team-agent-fabric`
- annotated tag: `v4.21.1`
- release commit: `455fa46d35c0c13539c835bd758baced04ca2aa9`
- wheel: `agent_security_harness-4.21.1-py3-none-any.whl`
- wheel SHA-256: `3daa21b6216ae81d9e5f1fe2e0016a064ac73db1b2a8a2fd71d6893683a1a99d`

The upstream tag is annotated but unsigned. Reproducibility therefore anchors on the explicit release commit plus release-asset digest; this repository does not represent the tag as cryptographically verified.

`v4.21.1` is deliberately preferred over a floating default branch because it repaired live-target false-PASS behavior in which unreachable targets could be graded from a reference-model verdict. The release now preserves unreachable/unserviced live targets as inconclusive rather than PASS.

## Target

The strongest current DPAC target is the container-enforced Workspace experiment:

```text
workflow/helper -- request_net --> workspace -- actuator_net --> actuator
                                      |
                                      +-- read-only capability policy
                                      +-- actuator credential
                                      +-- replay state
```

The actuator-owned effect journal is the outcome oracle. A harness denial or refusal is never sufficient evidence that no consequential effect occurred.

## Normalized result states

Every mapped vector terminates in exactly one Lab state:

- `pass` — the attack was materially exercised and the DPAC proposition held, including the required effect-oracle observation;
- `fail` — the attack materially falsified the expected DPAC property;
- `not-applicable` — the attack class does not apply to the target shape;
- `not-observable` — the target/harness interaction does not expose enough evidence to determine the property;
- `harness-gap` — a relevant DPAC attack surface exists but the pinned harness cannot express it without Lab-invented behavior.

An upstream PASS is never sufficient on its own for a Lab `pass`. Missing, simulated, reference-model-only, unreachable, or indeterminate evidence cannot be promoted to `pass`.

## Initial vector set

The first executable tranche is deliberately bounded to six already-observable DPAC properties:

1. revoked/insufficient authority;
2. capability-envelope overreach;
3. replay/duplicate execution;
4. stale capability state / TOCTOU;
5. target or parameter substitution;
6. direct/transitive capability-controller capture.

The mapping is in [`vector-map.yaml`](vector-map.yaml). Candidate upstream modules are recorded only where their published live surface materially overlaps the DPAC property. A candidate mapping is not treated as an executed mapping until the adapter proves that the harness request reached and exercised the intended DPAC enforcement point.

## Evidence discipline

Normalized records conform to [`schemas/result.schema.json`](schemas/result.schema.json) and preserve separate fields for:

- harness-produced verdict/evidence;
- Lab target observation;
- actuator-owned effect counts or identifiers;
- exact Lab and harness revisions;
- mapping status and limitations.

The external harness is additive evidence. Existing first-party DPAC deterministic tests remain authoritative regression evidence for the repository-owned implementation.

## Claim boundary

A successful run can establish only that the pinned external harness materially exercised the mapped attack against the stated Lab target and that the independently observed effect state matched the DPAC proposition. It does not establish independent certification, exhaustive security, host/daemon compromise resistance, upstream specification conformance, or production readiness.
