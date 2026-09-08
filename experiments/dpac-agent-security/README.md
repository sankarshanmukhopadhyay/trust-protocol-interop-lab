# DPAC × Agent Security Harness adversarial integration

This experiment tracks [#170](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/170) and adds an external adversarial evidence producer around the existing `IC-DPAC-ACTUATION-001` runtime boundary.

## Proposition

Determine whether an independently developed adversarial harness can attempt to falsify DPAC non-collapsibility and fail-closed properties against the existing enforced Workspace boundary without allowing the harness to become the authority for the resulting assurance conclusion.

The target remains [`../dpac-enforced-boundary/`](../dpac-enforced-boundary/). This directory contains only the integration contract, test-only translation adapter, evidence normalization machinery, and attributable external-harness execution material. It MUST NOT become a competing DPAC implementation.

## Authority boundary

- `msaleme/red-team-blue-team-agent-fabric` owns Agent Security Harness implementation, attack semantics, releases, and upstream result vocabulary.
- The Interop Lab owns the DPAC propositions, target adapter, effect oracle, normalization, evidence retention, and case/maturity interpretation.
- Harness output is evidence input. It does not establish DPAC conformance, production security, certification, or case promotion by itself.
- RAHP orchestration is outside this tranche.

## Pinned external dependency

The integration baseline is Agent Security Harness `v4.21.1`:

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

## External execution surfaces

The first executable external tranche intentionally maps only what can be translated without moving enforcement into the adapter.

### Replay — complete mapped proposition

Agent Security Harness `DCA-005` sends the same external request identifier twice. The adapter maps only that identifier to the DPAC nonce and constructs an otherwise valid bounded loan-approval request. Workspace therefore remains the replay enforcement point.

A successful mapped run requires:

1. the first presentation reaches Workspace and creates exactly one actuator-owned effect;
2. the second presentation reaches Workspace and is rejected as `replay`;
3. the harness reports its live replay control as PASS; and
4. the actuator journal confirms a total effect delta of exactly one across both presentations.

No delegation-chain attenuation claim is inferred from this adapter mapping.

### Governance self-modification — partial mapped proposition

Agent Security Harness `GM-001` sends real gate-disable/self-modification requests. The adapter forwards each body unchanged to Workspace `/admin/policy`; it does not manufacture a denial. Workspace's explicit 404/405 refusal and an unchanged actuator journal are retained as evidence.

This externally exercises **direct** mutation attempts. It does not externally reproduce the Workflow-controlled helper/transitive-capture half of `DPAC-ENF-009`, so the normalized result remains `not-observable` for the full direct+transitive proposition rather than being promoted to PASS.

### Preserved gaps

Other #170 classes remain `harness-gap` where the pinned harness wire contract cannot be mapped to the DPAC target without inventing authority, capability, prompt/tool, payment, or receipt semantics inside the adapter. HITL bypass is `not-applicable` because the current enforced DPAC target has no real human-approval boundary.

These are evidence outcomes, not unfinished PASS results.

## Normalized result states

Every vector terminates in exactly one Lab state:

- `pass` — the attack was materially exercised and the DPAC proposition held, including the required effect-oracle observation;
- `fail` — the attack materially falsified the expected DPAC property;
- `not-applicable` — the attack class does not apply to the target shape;
- `not-observable` — the target/harness interaction does not expose enough evidence to determine the full property;
- `harness-gap` — a relevant DPAC attack surface exists but the pinned harness cannot express it without Lab-invented behavior.

An upstream PASS is never sufficient on its own for a Lab `pass`. Missing, simulated, reference-model-only, unreachable, indeterminate, or partial evidence cannot be promoted to `pass`.

## Run

The external wheel is deliberately not vendored. Install exactly the pinned release artifact after verifying its SHA-256, then run:

```bash
python experiments/dpac-agent-security/tests/test_normalizer.py
python experiments/dpac-agent-security/run.py --check \
  --output /tmp/dpac-agent-security.json
```

CI performs the download, digest verification, installation, Docker execution, result-schema validation, and evidence upload in `.github/workflows/dpac-agent-security.yml`.

The runner always tears down the test adapter, Workspace/actuator topology, networks, volumes, and transient runtime secrets.

## Machine-readable contract

- [`target-profile.yaml`](target-profile.yaml) — exact target, harness pin, authority boundary, and evidence rules.
- [`vector-map.yaml`](vector-map.yaml) — all ten #170 adversarial classes and their executed/gap/not-applicable disposition.
- [`schemas/result.schema.json`](schemas/result.schema.json) — normalized per-vector evidence schema.
- [`normalizer.py`](normalizer.py) — conservative Lab interpretation rule.

The external harness is additive evidence. Existing first-party DPAC deterministic tests remain repository-owned regression evidence.

## Claim boundary

A successful run establishes only that the pinned external harness materially exercised the stated mapped attack against the stated Lab target and that the independently observed effect state matched the bounded DPAC proposition. It does not establish independent certification, exhaustive security, host/daemon compromise resistance, upstream specification conformance, production readiness, or automatic maturity promotion.
