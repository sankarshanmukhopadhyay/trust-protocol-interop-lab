# Candidate validation

Run:

```bash
python experiments/govops-executable-trust/run.py --check
python scripts/validate_cases.py
```

Expected GovOps evaluator result:

```text
PASS IC-GOVOPS-EXEC-TRUST-001: 10 scenarios / 12 invariants / 10 vectors
PASS policy-engine neutrality, enforcement observability, correlation, policy provenance
PASS candidate vectors remain equivalent to scenario contracts
```

Repository CI runs both checks and the GitHub Pages build. Candidate promotion is valid only while those checks remain green.
