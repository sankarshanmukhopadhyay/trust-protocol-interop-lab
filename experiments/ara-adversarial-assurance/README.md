# ARA Phase 10 — adversarial assurance

This experiment reruns the executable ARA phases and adds meta-assurance pressure tests for evidence sufficiency, false independence, retroactive authorization, collective-state inflation, and unsafe recovery.

## Run

```bash
python experiments/ara-adversarial-assurance/run.py --check
```

The output includes:

- machine-readable vector outcomes;
- boundary classification for every vector;
- rerun summaries and hashes for prior executable phases;
- gate-by-gate maturity dispositions;
- a deterministic evidence manifest and manifest hash;
- an explicitly bounded maturity recommendation.

## Assurance rule

```text
workflow green != assurance green
missing evidence => INDETERMINATE
evidence != authority
artifact count != independent support
later assurance != retroactive authorization
```

## Claim boundary

This is executable semantic assurance inside the Lab. It is not production penetration testing, external certification, formal verification, standards conformance, or proof that separate evidence lineages are economically/organizationally independent.
