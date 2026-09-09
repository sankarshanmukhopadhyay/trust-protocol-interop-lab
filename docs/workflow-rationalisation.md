# Interop Lab workflow rationalisation

Tracking: [#188](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/188) · parent graduation gate: `sankarshanmukhopadhyay/rahp-toolkit#501`

This is the repository-visible workflow accounting and disposition record for graduation. The objective is not a minimum workflow count. It is an intentional topology in which shared execution mechanics are reused when equivalence is evidenced, while materially different runtimes, privileges, evidence contracts, failure semantics and claim boundaries remain isolated.

## Disposition vocabulary

- `RETAIN-INFRASTRUCTURE` — repository CI, release, publication or application-test infrastructure whose workflow identity remains justified.
- `REUSABLE-WORKFLOW` — GitHub-level orchestration is itself the reusable boundary.
- `COMMON-RUNNER + DECLARATIVE-CASE` — execution mechanics are shared and proposition differences are expressed by characterized case/configuration/assertion data.
- `MERGE-FAMILY` — candidate state used while equivalence is being established; not a final graduation disposition.
- `RETIRE` — superseded/duplicate/no-longer-consumed workflow may be removed without losing required evidence/history.
- `DEFER` — current evidence shows a distinct boundary or does not yet justify safe consolidation/retirement.

`workflow green != assurance green` and `missing evidence != PASS` remain invariants.

## Final workflow matrix

| Workflow | Family / role | Material mechanics and evidence | Final disposition | Graduation rationale |
|---|---|---|---|---|
| `anab-dcas-assurance.yml` | Specialist assurance | Python 3.13; deterministic ANAB/DCAS decision reproduction via `experiments/anab-dcas-assurance/run.py --check` | `DEFER` | Domain-specific decision semantics already live in its runner. The thin path-scoped wrapper is not enough duplication to justify a universal workflow abstraction. |
| `ci.yml` | Repository infrastructure | Repository-wide validation, executable cross-spec/ARA/PDC/DPAC evidence, generated-tree checks, link checks, BBS/Node evidence and Pages build | `RETAIN-INFRASTRUCTURE` | Canonical repository assurance boundary. Its breadth and branch-gate role are materially different from proposition-specific evidence workflows. |
| `composed-ab-evidence.yml` | Reusable A/B evidence producer | Registered-producer validation, A/B self-tests, `run_composed_ab.py`, dispatch correlation/evidence-requirement inputs, durable 30-day evidence outbox | `REUSABLE-WORKFLOW` | Already exposes the correct cross-case GitHub-level producer boundary. Privacy interpretation remains DPIP-owned. |
| `current-openvtc-data-room-evidence.yml` | Current OpenVTC Data Rooms | Immutable OpenVTC `56cd6e5...`; target-native Data Room runner; legacy + `rahp-evidence-producer-result/v1`; runtime-drift capture and source-tree restore; three artifacts | `DEFER` | Different target revision, runner, evidence envelope and runtime-drift semantics from the A/B family. Setup similarity alone is insufficient for consolidation. |
| `current-openvtc-track-a-evidence.yml` | Current OpenVTC A/B | Thin caller of `reusable-current-openvtc-ab-evidence.yml`, characterized as `track-a`; same immutable `72bf579...` target | `COMMON-RUNNER + DECLARATIVE-CASE` | Migrated after #195 characterization and live-equivalence evidence in #200. Status/task remain explicitly `not-evidenced`; no privacy PASS/RAHP GREEN inference. |
| `current-openvtc-track-b-policy-evidence.yml` | Current OpenVTC A/B + specialist integration | OpenVTC + immutable DPIP + immutable RAHP checkouts; DPIP privacy result; DPIP evaluator; RAHP `rahp-assessor-result/v1` validation; four artifacts | `DEFER` | Characterization proved this workflow materially deeper than the two-artifact evidence-export family. Retain until a reusable specialist-integration boundary is independently demonstrated. |
| `current-openvtc-track-b-status-evidence.yml` | Current OpenVTC A/B positive control | Thin caller of reusable A/B workflow, characterized `track-b-status`; target-derived identical correlators; `must-detect` / `detected` | `COMMON-RUNNER + DECLARATIVE-CASE` | Migrated after characterization; live #200 evidence proved the opposite correlation expectation remains preserved rather than flattened. |
| `current-openvtc-track-b-task-evidence.yml` | Current OpenVTC A/B | Thin caller of reusable A/B workflow, characterized `track-b-task`; fresh executed task/thread/retained evidence; `not-detected` | `COMMON-RUNNER + DECLARATIVE-CASE` | First migrated consumer. #198 proved repository and live source-pinned evidence equivalence before the family expanded. |
| `reusable-current-openvtc-ab-evidence.yml` | Reusable current OpenVTC A/B orchestration | `workflow_call`; common Python/native/Rust setup; immutable target checkout; characterization admission; common runner; clean-tree check; upload | `REUSABLE-WORKFLOW` | Graduated reusable boundary for characterized two-artifact A/B members. It fails closed for unknown/deeper-integration members, including policy. |
| `device-metadata-ab-evidence.yml` | Historical/device A/B privacy | Lab + immutable `OpenVTC/openvtc` and VTI checkouts; Rust/native/PCSC; historical device-metadata runner | `DEFER` | Observer-bound replacement exists, but retirement requires explicit output/provenance equivalence and active-consumer/history analysis. Do not delete historical evidence by implication. |
| `device-metadata-observer-ab-evidence.yml` | Observer-bound device A/B privacy | Same external pins/runtime class; observer-scoped runner; DPIP-ready evidence | `DEFER` | Current semantic direction is observer-bound and aligned with DPIP #221, but its external target/runtime mechanics remain distinct from generic composed A/B execution. |
| `dogwood-runtime-evidence.yml` | Historical Dogwood runtime | Immutable Dogwood RC-1 target; positive-control + pressure A/B; four attributable evidence artifacts | `DEFER` | Dogwood is a previous release. Workflow has reproducibility/regression value; retirement must be a separate historical-evidence retention decision, not a side effect of current-source convergence. |
| `dpac-agent-security.yml` | Specialist external adversarial security | Downloads pinned external harness wheel; verifies SHA-256; installs no-deps; normalization tests; ten-record schema validation; artifact | `DEFER` | Materially distinct external dependency/security/evidence-normalization lifecycle positively justifies a bespoke workflow. |
| `dtg-action-vocabulary.yml` | DTG semantic proposition | Checkout → Python 3.13 → PyYAML → case-owned `run.py --check` | `DEFER` | Wrapper is intentionally tiny and semantics already live in the case runner. Generalizing four lines of orchestration would add indirection without consolidating assurance meaning. |
| `dtg-data-room-actuation.yml` | DTG authority/actuation proposition | Checkout → Python 3.13 → PyYAML → case-owned `run.py --check` | `DEFER` | Same low-cost wrapper pattern as other DTG checks, but no evidence that another GitHub-level abstraction improves isolation or reproducibility. |
| `dtg-hidden-subject-binding.yml` | DTG subject/common-control proposition | Checkout → Python 3.13 → PyYAML → case-owned `run.py --check` | `DEFER` | Subject-binding semantics remain case-owned and common-control itself remains externally coordinated through RAHP #500. Do not freeze unresolved semantics into a generalized workflow. |
| `dtg-vac-attenuation.yml` | DTG authority attenuation | Checkout → Python 3.13 → PyYAML → case-owned `run.py --check` | `DEFER` | Mechanically small wrapper; semantic logic is already reusable at runner/case level. No meaningful orchestration debt remains to remove. |
| `dtg-vdc-vac-action-time.yml` | WD02 action-time composition | Produces JSON; asserts all vectors, `INDETERMINATE/BLOCKED`, no mutation, bounded terminal evidence; uploads artifact | `DEFER` | Distinct artifact and action-time failure/non-inference semantics justify isolation from the simple `run.py --check` wrappers. |
| `install-admin-did-binding.yml` | Source-pinned binding falsifier | Lab + immutable VTI + immutable Trust Tasks; Rust/native deps; semantic alignment falsifier; artifact | `DEFER` | Distinct multi-repository source-pin and build lifecycle. Genericizing it would obscure the evidence attribution boundary. |
| `pages.yml` | Publication infrastructure | Repository validation + Jekyll + Pages artifact/deployment with `pages:write` and OIDC | `RETAIN-INFRASTRUCTURE` | Publication permissions and deployment lifecycle are a distinct infrastructure boundary. |
| `pdc-current-authority.yml` | Protected delegated care authority | Python current-authority actuation-boundary runner with `--check`; JSON evidence uploaded even on failure | `DEFER` | Authority-specific failure/effect evidence must not be conflated with PDC privacy or lifecycle evidence merely because the scenario is shared. |
| `pdc-demo.yml` | PDC runnable application test | Python compile + application unit tests; no assurance-evidence artifact | `RETAIN-INFRASTRUCTURE` | This is prototype/application CI, not an evidence producer. Keeping it separate prevents application green from being confused with assurance green. |
| `pdc-prescription-refill-lifecycle.yml` | PDC lifecycle evidence | Dedicated prescription-to-refill lifecycle runner and JSON artifact | `DEFER` | Lifecycle proposition/output is distinct; shared Python setup alone is insufficient basis for consolidation. |
| `pdc-refill-disclosure.yml` | PDC disclosure evidence | Dedicated disclosure comparison runner and JSON artifact | `DEFER` | Disclosure semantics and artifact are distinct from authority/lifecycle; retain until characterization proves a common evidence runner is actually beneficial. |
| `pdc-runtime-privacy.yml` | PDC privacy evidence | DPIP-consumable privacy runner with `--check`, JSON evidence uploaded even on failure | `DEFER` | Privacy interpretation is DPIP-owned; this target-specific producer retains a distinct claim boundary from other PDC evidence workflows. |
| `publish-release.yml` | Release infrastructure | Triggered only after successful repository assurance on `main`; release/tag immutability checks; `contents:write` | `RETAIN-INFRASTRUCTURE` | Release publication is a privileged lifecycle boundary and should not share proposition-evidence orchestration. |
| `vti-personhood-transport-equivalence.yml` | Specialist implementation equivalence | Immutable VTI; native/Rust + cache; REST/DIDComm/TSP cargo tests; shared-core source assertions; attributable artifact | `DEFER` | Distinct target-native multi-transport execution and Rust build semantics positively justify a bespoke workflow. |

## Proven convergence: current OpenVTC A/B evidence-export subset

The original Track A / Track B policy/status/task candidate was deliberately narrowed by executable characterization in #195 / PR #196. The characterization showed that policy now carries a materially deeper specialist integration chain, while Track A, status and task share one two-artifact execution boundary.

Migration followed the required sequence:

1. characterize all four workflows and encode deliberate differences;
2. introduce `scripts/run_current_openvtc_ab_member.py` and `reusable-current-openvtc-ab-evidence.yml`;
3. migrate Track B task first in #197 / PR #198;
4. prove repository assurance **and a live source-pinned Track B task run** green;
5. migrate Track A and Track B status in #199 / PR #200;
6. prove both live source-pinned runs green, including status `must-detect` / `detected` semantics;
7. retain Track B policy outside the reusable two-artifact boundary.

This is the intended graduation result: common mechanics are shared without erasing proposition-specific semantics.

## Why there are no forced `RETIRE` dispositions

The audit did not identify a workflow that can currently be removed with sufficient evidence **and** without losing an active execution boundary, historical reproducibility, privileged lifecycle or specialist claim boundary. In particular:

- Dogwood and historical device-metadata execution carry reproducibility/history questions that require an explicit retention decision;
- the observer-bound device workflow is not yet equivalence evidence for deleting the older producer;
- small DTG Python wrappers contain little orchestration debt because the semantics already reside in their case-owned runners;
- specialist, PDC and external-target workflows have materially distinct runtime or claim boundaries.

Graduation does not require deletion for its own sake. `RETIRE` is reserved for evidence-backed supersession.

## New-workflow admission rule

A new bespoke workflow should be created only when at least one materially distinct requirement cannot safely be represented by existing reusable workflow/runner/case machinery, such as:

- different runtime or security boundary;
- materially different external dependency lifecycle or source-pin set;
- distinct privilege/secrets requirement;
- incompatible failure/unavailable semantics;
- distinct evidence collection, packaging or return mechanism;
- isolation needed for reproducibility or claim-boundary integrity.

Otherwise new assurance work should normally add a declarative case/experiment, fixture/assertion set, target adapter or registered evidence producer.

## Completion state

- [x] Complete workflow accounting baseline.
- [x] Give every current workflow an explicit final disposition and rationale.
- [x] Establish disposition vocabulary and new-workflow admission rule.
- [x] Deep-audit current OpenVTC A/B and Data Room boundaries.
- [x] Deep-audit A/B privacy/device family.
- [x] Deep-audit DTG/VTC authority/binding family.
- [x] Deep-audit protected delegated care family.
- [x] Deep-audit specialist workflows and infrastructure.
- [x] Resolve Dogwood to historical/reproducibility `DEFER`, not accidental deletion.
- [x] Add characterization/equivalence tests before the first consolidation.
- [x] Migrate one consumer first and prove live equivalence.
- [x] Incrementally migrate the remaining eligible consumers.
- [x] Preserve deliberately distinct policy/specialist/runtime boundaries.
- [x] Record why no further retirement is currently evidence-safe.

## Graduation conclusion

The Lab can now add a normal assurance proposition without normally creating a new end-to-end Actions architecture. Where the proposition fits an existing execution class, it should add case/configuration/assertion data or a registered producer. A bespoke workflow remains appropriate only when the runtime, privilege, external dependency, evidence or claim boundary is materially distinct.

That is the intended steady state: **shared mechanics where proven equivalent, explicit isolation where meaning or evidence differs.**
