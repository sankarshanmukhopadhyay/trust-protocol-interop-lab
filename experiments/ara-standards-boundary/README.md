# ARA Phase 11 — standards-native boundary

This phase evaluates each local ARA adapter against the pinned standards/implementation baselines and reruns the affected invariant suites.

It intentionally distinguishes:

- **implementation substitution** — a real independently governed implementation replaced the local adapter in the executable path;
- **normative semantic binding** — a pinned specification owns relevant semantics, but no runtime implementation replacement occurred;
- **residual adapter** — the local test double remains because an exact executable substitution is not yet evidenced.

## Run

```bash
python experiments/ara-standards-boundary/run.py --check
```

The correct result may be **no implementation substitution**. That is preferable to hidden glue or overstated conformance.

## Claim boundary

This phase establishes a standards-native **boundary disposition**, not ToIP/OpenVTC conformance certification.
