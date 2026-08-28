# ARA Phase 11 — standards-native substitution disposition

Issue: #43  
Case: `IC-ARA-REL-001`

## Decision

Phase 11 does **not** force a standards-native implementation substitution merely to achieve a higher maturity label.

The pinned baselines support three distinct outcomes:

| Boundary | Pinned source | Result | Why |
|---|---|---|---|
| Trust Task codec | Trust Tasks Framework 0.5.0 | normative semantic binding | Generic task/versioning semantics are standards-owned, but `ara/research-query/0.1` remains a Lab-local profile and is not represented as a registered Trust Task |
| Relationship transport | TSP baseline + OpenVTC VTA/TSP implementation candidate | residual adapter | A real independently governed implementation exists, but the Lab has not instantiated an exact compatible endpoint path replacing the Phase 6 file/subprocess transport |
| Protected signer | OpenVTC VTA | residual adapter | VTA has real key custody, ACL/policy, TEE and Trust Task machinery, but the exact ARA context-bound signed-action contract has not been mapped and executed against its API |
| Participant card | DTG Core Credentials / RCard | normative semantic binding | RCard semantic ownership is clear, but no runtime RCard provider has replaced the local fixture |
| Relationship edge | DTG Core Credentials / VRC | normative semantic binding | VRC semantic ownership is clear, but no runtime VRC provider has replaced the local relationship-recognition fixture |

## Why no forced OpenVTC substitution

The pinned OpenVTC baseline is a substantial implementation. Its own README describes VTA key/DID custody, access-control policies, VTA/VTC services, TSP, versioned Trust Tasks, secret backends, TEE/Nitro deployment and SDK/service integration.

That is sufficient to classify it as a credible implementation candidate.

It is **not** sufficient to assert that its signing/Trust Task interface exactly implements the ARA Phase 5 contract:

```text
Agent Role
+ exact Role Record head
+ Agreement
+ authority
+ policy decision
+ capability
+ exact task
+ Phase 4 admission receipt
+ recipient/purpose/payload/nonce/expiry
=> protected cryptographic use
```

Until that exact mapping is executed, substitution would require hidden glue and would blur which project owns which semantics.

## Preserved negative boundaries

The Phase 11 executable checks preserve:

- TSP/channel authenticity != relationship authority;
- protected VTA key use != Workflow/policy authorization;
- RCard self-assertion != verified standing;
- VRC relationship recognition != delegation/agreement/capability;
- registry lookup != permission to act;
- current key/control != historical authority;
- community assurance != universal authorization;
- multiplicity != independent evidence.

## Gate disposition

`ARA-G11-STANDARDS-NATIVE-BOUNDARY` is considered **satisfied as a boundary-review gate**, not as a blanket standards-conformance gate.

The evidence-backed conclusion is:

> The Lab knows exactly which semantics are standards-owned, which independently governed implementations are credible substitution candidates, and which adapters must remain because actual replacement evidence is absent.

## Extraction decision

No ARA implementation component currently demonstrates the observed independent reuse, consumer base, separate lifecycle or release cadence needed to justify extraction into a standalone repository.

The original architectural decision therefore survives Phase 11: **ARA remains in the Protocol Lab.**
