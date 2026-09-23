# RAHP #767 — proof-REQUIRED Trust Task enforcement evidence

**Interop owner:** #241  
**Assurance owner:** sankarshanmukhopadhyay/rahp-toolkit#767  
**Observed OpenVTC revision:** `95955004e2d9b8d1f456696674bf06648f52d45a`  
**Assessment date:** 2026-09-23  
**Evidence class:** source-pinned target-native executable evidence already present in the observed implementation, plus route/census inspection. This report does **not** claim that the Lab independently executed an OpenVTC deployment.

## Proposition

Can an implementation preserve task-level authentication, freshness, attribution and replay semantics when a Trust Task declaring `proof: REQUIRED` is exposed through bearer-session routes?

## Finding

**PARTIALLY REMEDIATED / PRESERVED DIVERGENCE (narrowed).**

The historical dispatcher-wide proof/freshness weakness is remediated at the observed revision. A distinct route-level divergence remains: 49 proof-REQUIRED tasks were identified as bearer-served; six now also have signed-document bindings, but their bearer routes remain transitional. The implementation itself states that the divergence closes per task only when the bearer route is removed.

The broad RAHP proposition can therefore be narrowed. It is no longer correct to describe the document dispatcher as generally accepting proofless documents for proof-REQUIRED tasks.

## Evidence

### E1 — declared proof is now unconditional across transports

OpenVTC commit `a84df7fa89b427b5ffbfe20da5dab842f7270a9c` removes the transitional `require_declared_proof` relaxation. The implementation now applies the registry policy directly. A stale configuration requesting `require_declared_proof = false` fails to load rather than weakening enforcement.

The repository-native test tranche was rewritten to drive the same unsigned document over REST, DIDComm and TSP and require refusal on each, with a signed counterpart as positive control.

**Classification:** remediated.

### E2 — freshness and issuer/proof binding

OpenVTC commit `2f7ba5f49089ea53ef3bcafca26b9d9407af4b42` introduced policy enforcement for proof, recipient and `issuedAt`, an acceptance window, proof-to-document-issuer binding, and bounded replay retention.

The target-native tests include missing proof, freshness/retention bounds and document-ID conflict/replay behaviour.

**Classification:** remediated for signed-document dispatch.

### E3 — replay state is shared/bounded for document dispatch

The proof-enforcement design note at the observed revision records that the accepted-ID record is store-backed and shared across bindings, and bounds retention against the acceptance window. The migrated join-decision path includes a target-native replay test demonstrating that redelivery does not issue a second credential.

**Classification:** remediated for signed-document dispatch.

### E4 — current authority is evaluated on migrated signed paths

Commit `9bcacb3d33d7ee087382d1750cd09f936f9b68c8` migrates four admin member tasks to signed-document dispatch. Commit `95955004e2d9b8d1f456696674bf06648f52d45a` adds join-request decision and community-profile update.

For these signed paths, authorization is derived from the verified signer's ACL entry at execution time rather than from a bearer session minted earlier. This is stricter with respect to removed/expired authority.

**Classification:** remediated on the signed path.

### E5 — bearer-route divergence remains

At the observed revision, the implementation design note states:

- 51 relevant tasks declare proof REQUIRED;
- two already verified a document proof on their REST route;
- 49 were therefore bearer-served divergences;
- six of those 49 now additionally have signed-document bindings;
- the six bearer routes remain mounted;
- opening a signed door does not close the divergence for that task.

The remaining removal dependency is concrete rather than hypothetical. The admin console lacks a signing primitive. OpenVTC #1684 and commit `1b45ce1c5c456288b5133ba832277cc35ac90b1a` describe the signing-key design needed to retire console-dependent bearer routes; 34 of the 49 bearer-served proof-REQUIRED tasks are console-reachable.

**Classification:** preserved divergence, with an explicit removal dependency.

## Required-case disposition

| Case | Current evidence | Disposition |
|---|---|---|
| Valid signed/current-authority document | target-native signed-path tests and migrated handlers | remediated |
| Missing required proof | unconditional registry policy; cross-transport negative tests | remediated |
| Invalid proof | dispatcher proof verification remains mandatory | remediated |
| Proof not controlled by document issuer | proof/issuer binding added by #1659 | remediated |
| Missing `issuedAt` | registry policy enforcement | remediated |
| Stale/future `issuedAt` | acceptance-window enforcement | remediated |
| Replay of accepted document ID | shared accepted-ID record; join-decision replay test | remediated for document path |
| Removed/expired ACL authority | migrated handlers read ACL at execution time | remediated for migrated signed paths |
| Cross-transport document consistency | proof requirement unconditional on REST/DIDComm/TSP | remediated |
| Transitional bearer route | no signed document/proof/ID exists on that route | preserved divergence |

## Assurance boundary

Bearer authentication is not credited as equivalent to a Trust Task document proof. The remaining bearer routes therefore cannot establish the signed-document proposition, even where the same operation is also available through a conforming signed path.

This report also does not convert target-native tests into an independent interoperability certification. It records what the observed implementation and its executable tests establish.

## Recommended RAHP disposition

RAHP #767 should be narrowed from a generic dispatcher/proof-enforcement concern to the **retirement of proof-REQUIRED bearer routes**.

The dispatcher-wide proof/freshness/replay concern is materially remediated. The remaining durable trigger is:

> Reassess when the bearer routes for proof-REQUIRED tasks are retired, or when the producer/client signing work changes the remaining census.

Until then, the appropriate current-epoch result is **PARTIALLY REMEDIATED**, not PASS and not INDETERMINATE.
