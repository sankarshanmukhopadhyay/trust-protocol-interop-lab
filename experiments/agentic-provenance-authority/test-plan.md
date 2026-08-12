# Experiment plan — IC-AGENT-PROVENANCE-AUTH-001

## Objective

Execute the Candidate vectors against concrete implementations or deterministic adapters and determine whether agent identity, delegated authority, provenance, registry verification, decision authority, and effect evidence remain independently inspectable.

## Required test harness inputs

- frozen component/baseline identifiers;
- agent identity declaration and assurance evidence;
- principal/delegation artifact with action/resource/purpose/time scope;
- ARPA authority/lifecycle state fixture or implementation endpoint;
- provenance-bearing content fixture;
- TRQP query fixture or implementation endpoint;
- policy/decision-authority fixture;
- TIS-aligned evidence bundle and decision-receipt target;
- DCAS evaluation profile or adapter for bounded evidence sufficiency.

## Execution phases

### Phase A — Positive composition

Run all `vectors/valid/*.json`. Record the exact source evidence used for identity, authority, provenance, trust state, and decision evaluation.

### Phase B — Semantic-collapse negatives

Run all `vectors/invalid/*.json`. Each MUST fail at the earliest responsible control plane and record which invariant prevented admission.

### Phase C — Lifecycle/time

Exercise an action valid at T1, revoked at T2, and queried at T3. Capture both requested-time and current state without allowing either to overwrite the other.

### Phase D — Delegation chain

Exercise Principal → Agent A → Agent B with scope attenuation. Attempt a prohibited scope expansion and verify fail-closed behavior.

### Phase E — Portable evidence

Produce one evidence package that can be reviewed without the original A2A/session context. At minimum it must reference agent, principal, delegation, provenance, registry verification, policy, decision, and effect/absence-of-effect.

## Evidence output

An executed run should create a case-specific directory under `evidence/` containing:

```text
evidence/<run-id>/
  manifest.json
  environment.json
  baseline-checksums.json
  vector-results.json
  authority-evidence.json
  provenance-verification.json
  trqp-results.json
  decision-receipt.json
  effect-evidence.json          # when applicable
  dcas-evaluation.json
  replay.md
```

The evidence manifest must conform to the repository evidence model before the case can be promoted to `Interoperability Tested`.

## Pass condition

All positive vectors behave as declared; all negative vectors fail closed or route to explicit review as declared; no evidence artifact collapses identity, authority, provenance, verification, decision, or effect semantics.
