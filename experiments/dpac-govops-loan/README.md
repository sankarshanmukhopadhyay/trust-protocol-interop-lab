# DPAC × GovOps delegated-loan pressure test

This experiment reuses the delegated-loan semantics of `IC-GOVOPS-EXEC-TRUST-001` to pressure-test the non-collapsibility invariant of `IC-DPAC-ACTUATION-001` in a less synthetic consequential-action composition.

## Proposition

A loan approval may produce a runtime effect only when all of the following remain true at the actuation boundary:

1. delegated authority is current, in scope, and bound to the exact loan and amount;
2. the GovOps policy outcome is `Allow` and that decision was enforced;
3. the independently administered Workspace capability still permits the exact operation and amount under the same capability revision considered by authorization;
4. the actuation authorization has not already been consumed.

Authority/policy state and Workspace capability state are deliberately represented by separate inputs and rechecked at actuation. Neither path may substitute for the other.

## Pressure scenarios

`scenarios.yaml` contains eight deterministic cases covering valid concurrence, authority overreach, capability overreach, revocation between authorization and actuation, capability-state TOCTOU, target substitution, amount widening, and duplicate/retry execution.

Run:

```bash
python experiments/dpac-govops-loan/run.py --check
```

To reproduce the committed result shape:

```bash
python experiments/dpac-govops-loan/run.py --check \
  --output results/dpac-govops-loan/run-results.json
```

## Claim boundary

A passing run establishes that this repository-owned composition model preserves the tested DPAC and GovOps boundaries for the recorded scenarios. It does not establish production isolation, wire-protocol conformance, independent implementation, external certification, or complete adversarial coverage. The Workspace capability controller is logically separate in the model, not demonstrated as OS/container/cloud/hardware isolated.
