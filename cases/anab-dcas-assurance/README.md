# IC-ANAB-DCAS-001 — Named Agent Assurance Evaluation

**Status:** Experimental  
**Assurance posture:** executable evidence present; independent evaluator equivalence not yet established.

## At a glance

This case tests whether a relying party can receive an ANAB declaration and associated evidence and derive a repeatable DCAS assurance outcome without relying on undocumented implementation knowledge. It deliberately separates **identity/name assurance** from **action-specific authority** and preserves `PASS`, `FAIL`, and `INDETERMINATE` as distinct evidence states.

The canonical normalized vectors are in [`scenarios/scenarios.json`](scenarios/scenarios.json), and the tracked execution ledger is in [`../../results/anab-dcas-assurance/run-results.json`](../../results/anab-dcas-assurance/run-results.json).

## Proposition

A relying party can receive an ANAB declaration and associated evidence and derive a repeatable DCAS assurance outcome without relying on undocumented implementation knowledge.

## Baselines

- ANAB v0.10.0 implementation-validation surface, introduced by `agent-name-assurance-baseline` commit `e74b83bfa3114773ab2e8efbe629d3b12ae9be4f`; explicit control bindings were added in ANAB PR #17.
- DCAS v0.10.0 portable evaluator contract at commit `b2808c82073f0ff20a7e92c49bd52a361111dbaa`.

## Concrete scenario

A relying party receives a named-agent assurance claim plus evidence describing binding, freshness, revocation, and—where consequential reliance is requested—action-specific authority. The same input shape is exercised across six bounded vectors:

1. conforming current evidence → `PASS`;
2. stale identity/name binding → `FAIL`;
3. revoked binding/operator → `FAIL`;
4. missing freshness evidence → `INDETERMINATE`;
5. assurance overclaim → `FAIL`;
6. valid identity evidence with absent action authority → `INDETERMINATE` for consequential reliance.

The Interop Lab evaluator at [`../../experiments/anab-dcas-assurance/run.py`](../../experiments/anab-dcas-assurance/run.py) recomputes the decision ledger deterministically and binds each normalized input using SHA-256.

## Evaluation boundary

ANAB remains authoritative for named-agent requirements and evidence expectations. DCAS remains authoritative for the portable evaluation contract and result semantics. The Interop Lab owns experiment execution, evidence capture, and the maturity judgment for this case only.

A successful identity/name-assurance result does **not** establish delegated or action-specific authority. Where a relying decision requires such authority, it must be independently evidenced from the applicable authority source.

## Where it resolved

The first bounded execution resolves six declared vectors with expected-versus-observed agreement: one `PASS`, three `FAIL`, and two `INDETERMINATE`. Missing evidence is not promoted to success; stale and revoked evidence remain separately observable; an assurance overclaim fails; and the authority-absent vector remains indeterminate despite valid identity evidence.

The reproducibility check is executable with:

```bash
python experiments/anab-dcas-assurance/run.py --check
```

Workflow green is evidence that the recorded ledger is reproducible, not evidence by itself that the case has reached a higher interoperability maturity.

## What remains unresolved

This case does not yet demonstrate live evidence retrieval, production cryptographic verification, independent upstream conformance, or genuinely independent evaluator equivalence. The current Lab evaluator is one implementation of the DCAS contract. A separate DCAS reference implementation now exists upstream, but cross-repository equivalence evidence must be captured before that fact is used for any maturity promotion.

Interoperability Tested status should remain gated on at least one genuinely separate evaluator implementation consuming identical normalized inputs and producing materially equivalent overall decisions and source-requirement findings.

## Why this matters

The case tests a central executable-governance property: a trust decision should be reproducible from explicit requirements, evidence state, and declared policy rather than hidden evaluator judgment. Just as importantly, it prevents identity assurance from silently expanding the authority envelope. That boundary is consequential for agent systems because a well-identified agent can still lack permission to perform a specific action.

## Promotion rule

This case remains **Experimental**. Candidate promotion requires reproducible execution, governed evidence, catalog registration, and no unresolved divergence between declared ANAB expectations and observed DCAS outcomes. A later Interoperability Tested promotion requires genuinely independent evaluator evidence, not merely a second invocation of the same code.

## Falsification

If the normalized input plus declared policy is insufficient to reproduce an expected outcome, or two conforming evaluator implementations produce materially different decisions from the same normalized input, the discrepancy is routed to the owning source repository. The Interop Lab MUST NOT invent local semantics to hide the disagreement.
