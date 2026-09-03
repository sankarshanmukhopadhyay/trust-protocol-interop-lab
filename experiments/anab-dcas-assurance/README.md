# ANAB × DCAS assurance experiment

Run the deterministic experiment from the repository root:

```bash
python experiments/anab-dcas-assurance/run.py --check
```

`--check` regenerates the evidence ledger in memory and compares it semantically with `results/anab-dcas-assurance/run-results.json`. A mismatch or any expected-versus-observed divergence exits non-zero.

The canonical normalized inputs remain in `cases/anab-dcas-assurance/scenarios/scenarios.json`; the tracked result ledger binds each input using SHA-256. This prevents generated evidence from becoming an undocumented second source of input truth.

The evaluator is intentionally local to the Interop Lab. It demonstrates one implementation of the DCAS contract against ANAB fixtures; it is not itself sufficient evidence for independent evaluator interoperability.
