# IC-ARPA-A2A-TT-001 — Governed agent discovery to Trust Task execution

**Status:** Experimental

Tests whether governed agent registry state can constrain A2A discovery and invocation while Trust Tasks retain the semantics of the requested work.

## Method

The case declares semantic ownership and invariants before execution. Scenarios cover both successful composition and fail-closed behavior. The current baseline is experiment-ready but has not yet earned an `Interoperability Tested` claim.

## Evidence target

A future run should produce reproducible results plus an evidence manifest linking every conclusion to the exercised vectors and baselines.

## Current Trust Tasks pressure point

The pinned Trust Tasks baseline now requires authorization to remain distinct from identity/proof validation and to be re-evaluated before irreversible effects. For this case, ARPA/A2A delegation or registry authority that is revoked after discovery but before effect admission must therefore fail closed at the pre-effect checkpoint. Semantic task control must likewise not be inferred from A2A or transport cancellation alone.


## Actor-chain extension pressure test

A2A issue #2028 proposes a payload-level actor chain for on-behalf-of attribution. This case treats that proposal as an informative interoperability input, not as adopted A2A v1.0 semantics. The test boundary is deliberately strict: a reported chain can be internally consistent while every asserted grant is fabricated.

The case therefore evaluates attribution lineage, evidence resolution, current authority, and effect admission separately. See [the actor-chain/authority mapping](../../mappings/a2a-actor-chain-authority.md).

Additional scenarios cover fabricated-but-monotone lineage, scope escalation, prior-hop mutation, evidence-state separation, cross-context replay, and privacy-minimized lineage.
