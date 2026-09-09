# Interop Lab workflow rationalisation

Tracking: [#188](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/188) · parent graduation gate: `sankarshanmukhopadhyay/rahp-toolkit#501`

This document is the repository-visible accounting surface for the Lab workflow rationalisation required for graduation. The objective is not a minimum workflow count. The objective is an intentional workflow topology in which reusable execution mechanics are shared and proposition-specific differences are declarative where that boundary is evidence-backed.

## Disposition vocabulary

- `RETAIN-INFRASTRUCTURE` — repository-level CI/release/publication or genuinely cross-cutting workflow identity remains justified.
- `REUSABLE-WORKFLOW` — GitHub-level orchestration is the reusable boundary across materially different cases.
- `COMMON-RUNNER + DECLARATIVE-CASE` — execution mechanics are equivalent and meaningful variation is case/configuration/fixtures/assertions.
- `MERGE-FAMILY` — several workflows implement one semantically equivalent execution family and should converge behind shared machinery.
- `RETIRE` — superseded/duplicate/no-longer-consumed workflow can be removed without deleting historical evidence.
- `DEFER` — insufficient equivalence evidence or target/runtime instability makes rationalisation premature.

## Characterisation gate

No `MERGE-FAMILY`, `COMMON-RUNNER + DECLARATIVE-CASE`, or retirement migration should proceed until materially relevant current behaviour is represented by executable characterisation/equivalence evidence. That evidence must cover relevant positive, negative/adversarial, unavailable/indeterminate, source/runtime pin, evidence provenance, claim-boundary and failure/exit semantics.

`workflow green != assurance green` and `missing evidence != PASS` remain invariants.

## Matrix

| Workflow | Trigger | Family | Runtime/environment | Runner/scripts | Source pin | Evidence output | Failure / claim boundary | Overlap | Current disposition | Rationale / next evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| `anab-dcas-assurance.yml` | pending audit | specialist | pending audit | pending audit | pending audit | pending audit | pending audit | pending audit | `DEFER` | Distinct domain; inspect before proposing reuse. |
| `ci.yml` | pending audit | infrastructure | repository CI | pending audit | n/a | validation results | CI success is not assurance PASS | repository-wide | `RETAIN-INFRASTRUCTURE` | Retain workflow identity; inspect duplicated validation commands for script-level reuse only. |
| `composed-ab-evidence.yml` | pending audit | A/B privacy | pending audit | pending audit | pending audit | pending audit | pending audit | device/observer A/B family | `DEFER` | Analyse against DPIP #221 observer/experiment contract. |
| `current-openvtc-data-room-evidence.yml` | PR/push path filters; manual | current OpenVTC runtime | Ubuntu, Python 3.13, Rust, DBus/pkg-config; target checkout | `experiments/dtg-data-room-runtime/run_current_openvtc.py` | `OpenVTC/verifiable-trust-infrastructure@56cd6e5b7116777f1d9734e76c9a7b0569870e19` | `current-openvtc-data-room-evidence.json` | verifies immutable target pin and clean checkout; artifact absence fails workflow; local execution result is not terminal RAHP/DPIP judgment | Shares checkout/build/pin/cleanliness/upload mechanics with Track A/B, but uses a different target revision, runner and evidence contract | `DEFER` | Do not merge merely on setup similarity. First determine whether target checkout/build/upload should be a reusable workflow while Data Room execution stays distinct. |
| `current-openvtc-track-a-evidence.yml` | PR/push path filters; manual | current OpenVTC runtime / A-B | Ubuntu, Python 3.13, Rust, DBus/pkg-config; target checkout | `capture_ab_runtime.py`, `export_dpip_evidence.py`; context via case | `OpenVTC/verifiable-trust-infrastructure@72bf5794071971da506eb7a5af8e4765c35c137c` | runtime YAML + DPIP `provided_evidence` JSON | verifies immutable pin, clean checkout, bounded classifications; explicitly states evidence is not privacy PASS or RAHP GREEN | Strong mechanics overlap with Track B policy/status/task | `MERGE-FAMILY` candidate | Establish characterisation tests around shared setup, capture/export, provenance and bounded-result semantics before extracting reusable machinery. Track A has additional summary behavior and different assertions. |
| `current-openvtc-track-b-policy-evidence.yml` | PR/push path filters; manual | current OpenVTC runtime / A-B | Ubuntu, Python 3.13, Rust, DBus/pkg-config; target checkout | `capture_ab_runtime.py`, `export_dpip_evidence.py`; policy context via case | `OpenVTC/verifiable-trust-infrastructure@72bf5794071971da506eb7a5af8e4765c35c137c` | runtime YAML + DPIP `provided_evidence` JSON | pin/cleanliness checks; policy surfaces must be fresh/executed; observed join must be `not-detected` | Near-identical orchestration to Track B status/task and substantial overlap with Track A | `MERGE-FAMILY` candidate | Characterise expected assertion set and output names, then test whether a case-declared assertion layer can replace inline workflow assertions safely. |
| `current-openvtc-track-b-status-evidence.yml` | PR/push path filters; manual | current OpenVTC runtime / A-B | Ubuntu, Python 3.13, Rust, DBus/pkg-config; target checkout | `capture_ab_runtime.py`, `export_dpip_evidence.py`; status context via case | `OpenVTC/verifiable-trust-infrastructure@72bf5794071971da506eb7a5af8e4765c35c137c` | runtime YAML + DPIP `provided_evidence` JSON | pin/cleanliness checks; target-derived status correlators must be identical; must-detect join; non-exercised surfaces remain `not-evidenced` | Near-identical orchestration to Track B policy/task and substantial overlap with Track A | `MERGE-FAMILY` candidate | Preserve the deliberately opposite correlation expectation (`must-detect`) as declarative assertion data; never generalise this into a universal `not-detected` privacy expectation. |
| `current-openvtc-track-b-task-evidence.yml` | PR/push path filters; manual | current OpenVTC runtime / A-B | Ubuntu, Python 3.13, Rust, DBus/pkg-config; target checkout | `capture_ab_runtime.py`, `export_dpip_evidence.py`; task context via case | `OpenVTC/verifiable-trust-infrastructure@72bf5794071971da506eb7a5af8e4765c35c137c` | runtime YAML + DPIP `provided_evidence` JSON | pin/cleanliness checks; task/thread/retained evidence must be fresh/executed; observed join `not-detected` | Near-identical orchestration to Track B policy/status and substantial overlap with Track A | `MERGE-FAMILY` candidate | Characterise task-specific assertions before extraction. Shared runner should consume case/assertion declarations rather than hard-code privacy outcome semantics. |
| `device-metadata-ab-evidence.yml` | pending audit | A/B privacy | pending audit | pending audit | pending audit | pending audit | pending audit | observer A/B | `DEFER` | Analyse with DPIP #221. |
| `device-metadata-observer-ab-evidence.yml` | pending audit | A/B privacy | pending audit | pending audit | pending audit | pending audit | pending audit | device A/B | `DEFER` | Analyse with DPIP #221. |
| `dogwood-runtime-evidence.yml` | pending audit | legacy runtime | pending audit | pending audit | Dogwood-era | historical/runtime evidence | historical workflow success must not become current assurance | current OpenVTC evidence family | `DEFER` | Dogwood is a previous release. Determine active consumer and reproducibility value before deciding `RETIRE`; preserve historical evidence regardless. |
| `dpac-agent-security.yml` | pending audit | specialist security | pending audit | pending audit | pending audit | pending audit | pending audit | pending audit | `DEFER` | Distinct specialist domain; inspect before proposing reuse. |
| `dtg-action-vocabulary.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | DTG/VTC family | `DEFER` | Audit execution mechanics. |
| `dtg-data-room-actuation.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | DTG/VTC family | `DEFER` | Audit execution mechanics. |
| `dtg-hidden-subject-binding.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | DTG/VTC family | `DEFER` | Audit execution mechanics. |
| `dtg-vac-attenuation.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | DTG/VTC family | `DEFER` | Audit execution mechanics. |
| `dtg-vdc-vac-action-time.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | DTG/VTC family | `DEFER` | Audit execution mechanics. |
| `install-admin-did-binding.yml` | pending audit | DTG authority/binding | pending audit | pending audit | pending audit | pending audit | pending audit | binding family | `DEFER` | Audit execution mechanics. |
| `pages.yml` | pending audit | infrastructure | GitHub Pages | pending audit | n/a | site | publication success is not assurance result | publication | `RETAIN-INFRASTRUCTURE` | Preserve deployment boundary. |
| `pdc-current-authority.yml` | pending audit | protected delegated care | pending audit | pending audit | pending audit | pending audit | pending audit | PDC family | `DEFER` | Keep authority semantics distinct from privacy even if runner reuse emerges. |
| `pdc-demo.yml` | pending audit | protected delegated care | pending audit | pending audit | pending audit | pending audit | pending audit | PDC family | `DEFER` | Audit demo versus evidence-producing role. |
| `pdc-prescription-refill-lifecycle.yml` | pending audit | protected delegated care | pending audit | pending audit | pending audit | pending audit | pending audit | PDC family | `DEFER` | Audit lifecycle mechanics. |
| `pdc-refill-disclosure.yml` | pending audit | protected delegated care | pending audit | pending audit | pending audit | pending audit | pending audit | PDC family | `DEFER` | Audit disclosure semantics. |
| `pdc-runtime-privacy.yml` | pending audit | protected delegated care / privacy | pending audit | pending audit | pending audit | pending audit | pending audit | PDC + DPIP observability | `DEFER` | Evaluate against DPIP #221; privacy semantics stay DPIP-owned. |
| `publish-release.yml` | pending audit | infrastructure | release | pending audit | pending audit | pending audit | release success is not assurance PASS | release | `RETAIN-INFRASTRUCTURE` | Preserve release boundary; inspect duplicated validation commands only. |
| `vti-personhood-transport-equivalence.yml` | pending audit | specialist composition | pending audit | pending audit | pending audit | pending audit | pending audit | transport equivalence | `DEFER` | Distinct proposition; inspect before reuse. |

## First evidence-backed consolidation hypothesis: current OpenVTC Track A/B

The Track A and Track B policy/status/task workflows share a strong orchestration skeleton:

1. checkout Lab producer;
2. install Python 3.13 + PyYAML;
3. install DBus/pkg-config native dependencies;
4. install Rust;
5. checkout the same immutable OpenVTC revision;
6. verify exact revision and clean checkout;
7. execute `capture_ab_runtime.py` against a case YAML;
8. assert case-specific bounded observations;
9. verify upstream checkout remains clean;
10. execute `export_dpip_evidence.py`;
11. upload runtime evidence + DPIP binding artifact.

The meaningful differences observed so far are primarily:

- context/case declaration;
- case-specific assertion semantics, including a deliberate `must-detect` status case versus `not-detected` policy/task cases;
- output/artifact naming;
- Track A's additional bounded summary.

This is sufficient to classify the family as a **consolidation candidate**, but not sufficient to refactor it yet. The next tranche must encode characterisation tests proving that those differences can be represented declaratively without changing claim boundaries or unavailable/not-evidenced semantics.

The Data Room workflow shares environment/bootstrap/pin-cleanliness/artifact mechanics but uses a different OpenVTC revision and a different runner/evidence shape. It therefore remains `DEFER` rather than being silently absorbed into the A/B family.

## New-workflow admission rule

A new bespoke workflow should be added only when a materially distinct runtime/security boundary, external dependency lifecycle, privilege/secrets requirement, failure semantic, evidence collection mechanism, or reproducibility/claim-boundary isolation requirement cannot safely be expressed by existing reusable workflow/runner/case machinery.

Otherwise new assurance work should normally add a declarative case/experiment, fixture/assertion set, target adapter, or registered evidence producer.

## Completion state

- [x] Establish complete workflow accounting baseline.
- [x] Establish disposition vocabulary and admission rule.
- [x] Deep-audit first consolidation candidate family (current OpenVTC Track A/B) and separate Data Room boundary.
- [ ] Deep-audit A/B privacy family.
- [ ] Deep-audit DTG/VTC authority/binding family.
- [ ] Deep-audit protected delegated care family.
- [ ] Deep-audit specialist workflows.
- [ ] Resolve Dogwood historical-workflow disposition.
- [ ] Add characterisation tests for the first proven-equivalent family before implementation consolidation.
- [ ] Incrementally migrate and retire only after equivalence evidence passes.
