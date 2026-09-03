# IC-ANAB-DCAS-001 — Named Agent Assurance Evaluation

## Proposition

A relying party can receive an ANAB declaration and associated evidence and derive a repeatable DCAS assurance outcome without relying on undocumented implementation knowledge.

## Baselines

- ANAB v0.10.0 implementation-validation surface, introduced by `agent-name-assurance-baseline` commit `e74b83bfa3114773ab2e8efbe629d3b12ae9be4f` and control bindings tracked by ANAB PR #17.
- DCAS v0.10.0 portable evaluator contract at commit `b2808c82073f0ff20a7e92c49bd52a361111dbaa`.

## Evaluation boundary

ANAB remains authoritative for named-agent requirements and evidence expectations. DCAS remains authoritative for the portable evaluation contract and result semantics. The Interop Lab owns only execution, evidence capture and the maturity judgment for this case.

A successful identity/name-assurance result does not establish delegated or action-specific authority.

## Executable vectors

`scenarios/scenarios.json` carries six normalized DCAS inputs corresponding to the ANAB fixture classes:

1. conforming current evidence → `PASS`;
2. stale binding → `FAIL`;
3. revoked binding/operator → `FAIL`;
4. missing freshness evidence → `INDETERMINATE`;
5. assurance overclaim → `FAIL`;
6. valid identity evidence with absent action authority → `INDETERMINATE` for consequential reliance.

The evaluator is `experiments/anab-dcas-assurance/run.py`. It produces an evidence-preserving result rather than treating workflow success as assurance success.

## Promotion rule

This case starts **Experimental**. Promotion requires reproducible execution, governed evidence, and no unresolved divergence between declared ANAB expectations and observed DCAS outcomes. A later Interoperability Tested promotion should require a genuinely independent evaluator implementation, not merely a second invocation of the same code.

## Falsification

If the normalized input plus declared policy is insufficient to reproduce an expected outcome, or two independent evaluators produce materially different decisions from the same normalized input, the discrepancy is routed to the owning source repository. The Interop Lab MUST NOT invent local semantics to hide the disagreement.
