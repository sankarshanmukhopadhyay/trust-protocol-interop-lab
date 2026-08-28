# IC-ARA-REL-001 — next-stage adapter plan

Issue: #34  
Next implementation issue: #35

## Purpose

The ARA walking skeleton will use **ports with explicit evidence boundaries**. A port is not a claim that an upstream component already implements the ARA contract. Each adapter declares what it provides locally, which pinned source informs it, and what evidence is required before standards-native substitution.

## Adapter rules

1. A local adapter may emulate an implementation boundary, but it must not redefine upstream semantics.
2. The ARA invariant suite is stable across substitutions; replacing an adapter does not waive negative tests.
3. Substitution occurs one boundary at a time so changed observables and failures remain attributable.
4. A green adapter-backed run proves only the bounded ARA composition implemented by the Lab.
5. Missing evidence is `indeterminate` or an explicit gap, never inferred conformance.

## Planned ports

| Port | Phase-3/4 local contract | Pinned source influence | First standards-native candidate | Substitution evidence required |
|---|---|---|---|---|
| `RoleStateStore` | append/end-verifiable Role Record branch, head, transition receipt, history | ARPA lifecycle/historical work; DTG durable-history guidance | unresolved | same stale/rollback/fork/continuity vectors pass; historical verification is externally reproducible |
| `IdentityControlResolver` | resolve current and historical local Agent Role control state | ARPA, DTG Credentials | ARPA/DID-method implementation candidate | historical key/control event can be verified independently; rotation/recovery does not rewrite prior authority |
| `AuthorityResolver` | return scoped attributable authority/delegation evidence | ARPA, TSMM/TGA/TIS | ARPA Authority | direct, multi-hop, revoked, out-of-scope and conflicting-source vectors preserve results |
| `AgreementStore` | immutable/versioned proposal, acceptance, activation and lifecycle | ARA-local hypothesis | unresolved | execution identifies stable necessary semantics before external ownership is proposed |
| `PolicyDecisionPoint` | deterministic `allow/deny/escalate/indeterminate` over exact evidence/state | GovOps case, TSMM/TGA/TIS | implementation-specific PDP | same decision vectors pass and authority/capability/evidence remain non-authoritative inputs where appropriate |
| `TrustTaskCodec` | exact type/version, canonical payload and lifecycle/error handling | Trust Tasks 0.5.0 | Trust Tasks implementation/registry artifacts | wire object validates against pinned task contract; ARA profile additions remain separately attributable |
| `CapabilityBroker` | derive, attenuate, expire, suspend and revoke relationship/agreement-scoped capability | GovOps/TGA/TIS patterns | unresolved | valid capability cannot bypass revoked authority, wrong agreement or denied policy decision |
| `ProtectedSigner` | authenticated exact-request signing/refusal with use receipt | OpenVTC VTA, TEA | OpenVTC VTA | direct Live Agent/arbitrary-byte/stale/substitution/replay vectors still fail; accepted signature binds exact ARA decision context |
| `RelationshipTransport` | serialized sender/receiver exchange only | TSP, TEA | TSP | transport authenticity/confidentiality is real while transport success remains distinct from receiver acceptance; correlation surfaces are measured |
| `ParticipantCardProvider` | bounded participant description fixture | DTG RCard | RCard implementation | self-asserted vs verified fields remain distinct; disclosure/correlation profile observed |
| `RelationshipEdgeProvider` | typed relationship-recognition fixture | DTG VRC | VRC implementation | VRC proves only its defined edge; delegation/agreement/capability/traversal substitution vectors fail |
| `EvidencePackager` | source-attributed decision/execution receipts and hashes | TIS, TSMM | TIS-compatible contracts | runtime artifacts validate and remain evidence rather than authority |
| `RelationshipEvidenceStore` | independent local exact/shared/private/pointer/commitment evidence and receipts | ARA-local; TIS/Trust Tasks adjacent | unresolved | no master record; copy/inspection/acceptance/dispute distinctions survive independent reconstruction |
| `PrivacyEvaluator` | evaluate observable correlation/disclosure surfaces supplied by runtime | DPIP, Trust Tasks 0.5.0, DTG Credentials | DPIP | ARA runtime observations can be consumed without DPIP generating or owning the relationship execution |
| `AssuranceEvaluator` | adversarial disposition and claim-boundary review | RAHP | RAHP | threat proposition, falsifier, legitimate counter-case and residual uncertainty remain attributable; assurance does not authorize runtime actions |

## Phase 3 implementation order

Issue #35 should implement only the minimum ports needed to prove persistent state:

```text
IdentityControlResolver (local)
        ↓
RoleStateStore (local)
        ↓
relationship-local Role Record branch
        ↓
transition receipts + current head
        ↓
Live Agent A1 terminated
        ↓
Live Agent A2 resumes from persisted state only
```

It should **not** pull Agreement, Trust Task, capability, signer, TSP or VRC implementation into Phase 3 unless required by a state invariant. This keeps the judgment attributable: if continuity/rollback semantics fail, the failure belongs to the state model rather than the rest of the stack.

## Phase 4 composition order

Issue #36 adds:

```text
AgreementStore
AuthorityResolver
PolicyDecisionPoint
TrustTaskCodec
CapabilityBroker
EvidencePackager
```

The implementation should reuse the already-proven GovOps boundary that **capability ≠ authority ≠ authorization ≠ execution ≠ evidence**, while adding the new ARA relationship/agreement/current-state conjunction.

## Deferred standards-native substitutions

TSP, OpenVTC VTA, RCard, VRC and a concrete historical identity/control implementation are deliberately not prerequisites for the walking skeleton. They become Phase 11 substitutions only after the ARA-local contracts have executable positive and falsification evidence.

This sequencing is intentional: it lets us determine whether a substitution preserves the architecture rather than allowing the integrated component to define the architecture by accident.

## Extraction rule

No port becomes a new repository merely because it has an interface. Extraction requires observed independent reuse: stable semantic ownership, independent lifecycle/versioning need, and credible downstream consumers. Until then, it remains an Interop Lab experiment component.
