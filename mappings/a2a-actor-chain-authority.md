# A2A actor-chain attribution and ARPA authority mapping

**Status:** Experimental mapping based on A2A issue #2028 as reviewed on 2026-08-20. The issue is an upstream proposal, not an adopted A2A v1.0 requirement.

## Boundary

The proposed A2A `actorChain` answers an attribution question: **who reports acting through whom?** ARPA answers a different authority question: **what current, bounded authority has the relying party independently established for the requested effect?** Trust Tasks retain ownership of the requested-work semantics.

No projection in this mapping converts caller-supplied actor-chain metadata into an ARPA Authority Envelope.

| Proposed A2A actor-chain surface | ARPA / lab treatment | Prohibited inference |
|---|---|---|
| `origin` / originating principal | attribution reference | principal authority |
| actor `(iss, sub)` | actor identity claim/reference | recognized or authorized agent |
| per-hop `scopes` | reported effective scope for well-formedness testing | proof the scope was granted |
| per-hop proof/credential reference | evidence locator to resolve independently | authority from the pointer alone |
| append-only hop order | audit-integrity invariant | proof earlier hops are truthful |
| origin anchor | optional external ordering/anchoring input | privilege or scope expansion |

## Evaluation split

A conforming experiment records at least four independent outcomes:

1. `lineage_well_formed` — ordering and monotonic attenuation checks over the reported chain;
2. `evidence_resolution` — whether referenced evidence is absent, resolvable, unresolvable, or invalid;
3. `authority_decision` — ARPA/rp-policy result after lifecycle, scope and delegation evaluation; and
4. `effect_admission` — whether the Trust Task effect is permitted to proceed.

A `true` value for (1) MUST NOT force an affirmative value for (3) or (4).

## Failure-state discipline

The experiment MUST keep these states distinct: missing evidence, unresolvable evidence, invalid evidence, expired/revoked authority, and an explicit authorization denial. Silence is not a denial, and a malformed or forged proof is not an authorization outcome.

## Mutation and replay

Where append-only lineage is claimed, the receiver SHOULD retain the received representation or its digest before forwarding. A downstream verifier that sees only a rewritten forwarded chain cannot reconstruct the prior bytes. Evidence references SHOULD be content-bound and context/domain-bound so identical bytes cannot be replayed into a different authority context without detection.

## Privacy

Actor lineage can become a durable correlator. Experiments SHOULD test selective or pairwise representations where the relying decision needs proof of bounded upstream authority but not disclosure of every upstream identity.
