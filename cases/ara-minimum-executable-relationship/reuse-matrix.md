# IC-ARA-REL-001 — Phase 2 reuse and capability matrix

Issue: #34  
Parent programme: #32  
Baseline register: [`baselines.yaml`](baselines.yaml)  
Machine-readable mapping: [`reuse-mapping.yaml`](reuse-mapping.yaml)

## Judgment

The minimum ARA relationship is **not a greenfield implementation**. Several of its hardest semantic separations already have attributable specification, implementation, Interop Lab, privacy, or assurance evidence. The work that remains is concentrated at the relationship-composition layer.

This matrix does not upgrade semantic proximity into ownership. `direct` means the cited source actually owns the identified generic semantic or executable contract. It does **not** mean that source implements the whole ARA requirement end-to-end.

## Mapping classes

| Class | Meaning |
|---|---|
| `direct` | A pinned source directly owns the needed generic semantic/executable contract. |
| `composition-dependent` | The ARA requirement exists only in the conjunction among separately owned components. |
| `adapter-only` | The Lab can exercise it now, but no standards-native implementation evidence is currently attributable. |
| `candidate` | A plausible source exists; evidence is not yet sufficient to rely on it for the exact ARA requirement. |
| `not-yet-evidenced` | No pinned source currently supports the required behavior sufficiently. |

## Capability matrix

| ARA surface | Classification | Reusable source/evidence | What remains for ARA |
|---|---|---|---|
| Persistent Agent Role continuity | composition-dependent | TEA, ARPA, TSMM/TGA; ARPA lifecycle cases | Bind persistent accountable role to an executable Role Record and prove continuation after Live Agent destruction. |
| Live Agent cannot directly actuate/sign | composition-dependent | TEA Controller boundary, TGA governance patterns, OpenVTC protected functions | Enforce and falsify direct Live Agent signing/actuation in the Lab runtime. |
| Role Record state | adapter-only | ARPA historical state; DTG durable identifier considerations | Build current-head, previous-head, rollback/fork and append-only relationship branch semantics. |
| Historical identity/control | candidate | ARPA + DTG credential/DID history guidance; ARPA↔TRQP case | Bind historical control state to each consequential ARA action and verify it later. |
| RCard | direct | DTG Credentials | Define only the ARA/fiduciary profile additions actually required by the slice. |
| VRC relationship edge | direct | DTG Credentials | Exercise it without treating recognition as delegation, agreement, capability or record access. |
| Agreement Object | not-yet-evidenced | none pinned | Define the minimum immutable/versioned proposal, acceptance and activation contract locally and keep it explicitly ARA-local until ownership is resolved. |
| Authority/delegation | direct | ARPA, TSMM, TGA, TIS; ARPA/A2A/TT case | Bind authority to relationship/agreement state without making it the Policy Gate decision. |
| Deterministic Policy Gate | composition-dependent | GovOps executable-trust; TSMM/TGA/TIS | Implement the ARA-specific conjunction and explicit `indeterminate` state. |
| Exact Trust Task | direct | Trust Tasks 0.5.0; several Lab cases | Define/profile only ARA-specific operation fields and relationship-state effects. |
| Task ↔ relationship/agreement/state binding | composition-dependent | Trust Tasks + ARPA + TIS | Produce one canonical signed-action request that carries the exact conjunction. |
| Capability derivation | composition-dependent | GovOps case + TSMM/TGA/TIS | Implement least-privilege issuance/attenuation/revocation under the exact ARA decision. |
| Protected signing | candidate | OpenVTC VTA + TEA | First implement a Lab signer contract; later prove which OpenVTC guarantees substitute it. |
| TSP transport | direct | TSP + TEA | Substitute after independent receiver verification is proven over a simpler transport; measure new correlation surfaces. |
| Independent counterparty verification | composition-dependent | TEA + Trust Tasks + authority/evidence artifacts | Execute two separately controlled runtimes and reject sender-local conclusions as insufficient. |
| Execution/effect correlation | direct | GovOps case + TSMM/TGA/TIS | Reuse the decision→execution→evidence pattern inside the ARA relationship. |
| Portable execution evidence | direct | TIS + TSMM | Bind evidence to ARA task/agreement/state without letting evidence become authority. |
| Distributed VRR | adapter-only | none directly | Build the independent Role Record intersection without a master shared database. |
| Inspection/receipt/disposition distinctions | composition-dependent | Trust Tasks lifecycle + TIS receipts | Add content-digest-bound relationship inspection and semantic disposition semantics. |
| Collective Knowledge Certificate/checkpoint | not-yet-evidenced | none pinned | Treat as an ARA-local hypothesis and pressure-test it before proposing any normative owner. |
| Private/pointer/commitment evidence classes | adapter-only | DPIP helps test observability only | Implement the relationship evidence classes locally; DPIP evaluates disclosure/correlation, not relationship membership. |
| Link does not grant traversal/authority | composition-dependent | TSMM/TGA/TIS governance boundaries | Build linked-record denial vectors over actual local relationship records. |
| Live Agent replacement continuity | adapter-only | TEA/ARPA concepts | Kill the original process and resume solely from persisted authorized state. |
| Challenge/remediation/closure | composition-dependent | TSMM/TGA/TIS/ARPA lifecycle and redress | Execute append-only dispute/correction/revocation/closure over the same relationship. |
| Relationship View | adapter-only | TIS evidence packaging is adjacent | Generate a source-traceable, privacy-bounded view that exposes uncertainty and material dependencies. |
| VTC assurance/governance | candidate | OpenVTC VTC + TSMM/TGA/TIS | Defer plural-community execution; prove membership/certification never becomes universal authorization. |
| Privacy/correlation | direct | Trust Tasks 0.5.0 + DTG Credentials + DPIP; protected-access case | Apply those observation disciplines to ARA transport, state, identifiers and retained relationship evidence. |
| False independence | direct (assurance scope) | RAHP false-independence corpus | Apply during multi-source assurance; do not turn it into runtime authorization semantics. |
| Evidence insufficiency / INDETERMINATE | direct (assurance/evaluation scope) | DPIP, RAHP, Lab patterns | Preserve through ARA Policy Gate and maturity review instead of manufacturing PASS. |
| Standards-native substitution | composition-dependent | Protocol Lab methodology | Replace one adapter at a time and rerun the same invariant suite before making broader claims. |

## What is already strong enough to reuse

The strongest reuse surfaces are: **authority/delegation**, **Trust Task semantics**, **TSP/TEA communication/control concepts**, **capability/authorization/effect separation**, **portable evidence**, **privacy/correlation observation**, and **adversarial assurance**. Existing Interop Cases already give us bounded evidence that these concerns can remain semantically separate across compositions.

That means Phase 3 should not rebuild those domains. It should consume them through explicit ports and spend engineering effort on the missing relationship-state spine.

## Where ARA is genuinely adding implementation work

The main implementation gaps are:

1. the **Role Record** as authoritative persistent local relationship state;
2. an exact **Agreement Object** lifecycle for the minimum ceremony;
3. the **ARA-specific authorization conjunction** across agreement, authority, policy, state, task and capability;
4. the **TEA↔protected-signer binding** with denial evidence;
5. the **distributed VRR** and exact receipt/disposition semantics;
6. **Live Agent replacement continuity**;
7. **collective-knowledge/checkpoint semantics** if they survive pressure testing;
8. an authorized **Relationship View**.

These are therefore the areas where the Lab should be willing to discover that the proposal needs revision.

## Important changed conclusion from Phase 1

Phase 1 left the direct Trust Task mapping unresolved. The Phase 2 baseline shows the generic Trust Tasks framework is stronger than the earlier Lab baseline: Framework 0.5.0 now has explicit document lifecycle, freshness, identifier-correlation and retention/ingest/identifier-scope rules. We can therefore classify the **generic exact-task framework as direct reuse**, while keeping **ARA-specific task profiles and relationship-state effects composition-dependent**.

Similarly, the current DTG Credentials baseline now makes durable-identifier historical verification and pairwise-resolution privacy requirements more explicit. That strengthens the historical-control mapping from a vague dependency to a **candidate with concrete properties**, but it still does not implement an ARA Role Record.

## Boundary that remains unchanged

A nearby implementation is not semantic authority. OpenVTC having a VTA, ARPA having relationships/authority, TIS having evidence schemas, or DTG Credentials having VRCs does not make any of those sources the owner of the whole ARA relationship. The Lab will keep gaps explicit rather than hide them in glue code.
