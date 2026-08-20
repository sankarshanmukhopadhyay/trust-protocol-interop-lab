# Reproduce the ARPA–A2A–ANAB experiment

Run:

```bash
python3 experiments/arpa-a2a-anab/run.py
```

The deterministic evaluator reads the positive and negative vectors for `IC-ARPA-A2A-TT-001` and writes a result, run log, and hash-bound evidence manifest under `evidence/arpa-a2a-anab/`. Its bounded claim covers semantic gate composition only—not live endpoints, cryptographic verification, A2A wire conformance, or external certification.
