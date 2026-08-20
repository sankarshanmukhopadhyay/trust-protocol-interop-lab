# IC-ARPA-A2A-TT-001 — Governed agent discovery to Trust Task execution

**Status:** Interoperability Tested (bounded semantic composition)

Tests whether governed agent registry state and ANAB name/operator assurance can constrain A2A discovery and invocation while Trust Tasks retain the semantics of the requested work.

## Method

The case declares semantic ownership and invariants before execution. Its deterministic runner exercises positive and negative vectors and publishes hash-bound evidence. The resulting `Interoperability Tested` claim is limited to this repository-owned semantic evaluator; it excludes live-network and cryptographic interoperability.

## Evidence target

Run `python3 experiments/arpa-a2a-anab/run.py`. The result, log, and evidence manifest are written under `evidence/arpa-a2a-anab/`.

## ANAB assurance boundary

The experiment admits current, integrity-bound ANAB name and operator evidence before consequential interaction. Name mismatch, stale or revoked assurance, and unbound evidence fail closed. Passing ANAB checks does not create delegation: ARPA authority state, scope, and relying-party policy remain separate gates.

## Current Trust Tasks pressure point

The pinned Trust Tasks baseline now requires authorization to remain distinct from identity/proof validation and to be re-evaluated before irreversible effects. For this case, ARPA/A2A delegation or registry authority that is revoked after discovery but before effect admission must therefore fail closed at the pre-effect checkpoint. Semantic task control must likewise not be inferred from A2A or transport cancellation alone.


## Actor-chain extension pressure test

A2A issue #2028 proposes a payload-level actor chain for on-behalf-of attribution. This case treats that proposal as an informative interoperability input, not as adopted A2A v1.0 semantics. The test boundary is deliberately strict: a reported chain can be internally consistent while every asserted grant is fabricated.

The case therefore evaluates attribution lineage, evidence resolution, current authority, and effect admission separately. See [the actor-chain/authority mapping](../../mappings/a2a-actor-chain-authority.md).

Additional scenarios cover fabricated-but-monotone lineage, scope escalation, prior-hop mutation, evidence-state separation, cross-context replay, and privacy-minimized lineage.
