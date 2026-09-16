# Human-power composition pressure evidence

This experiment implements the bounded evidence program tracked by #121 and child issues #224–#228.

## Purpose

The runner records observable execution facts for four pressure families:

1. disclosure expansion;
2. correlation-scope escalation;
3. refusal consequences and interaction pressure;
4. consequential decision-feature use.

It deliberately does **not** decide whether an observation is harmful, discriminatory, legitimate, privacy-preserving, consensual, or assurance-passing. Those judgments remain with RAHP, DPIP, or another explicitly authorized assessment layer.

## Run

```bash
python experiments/human-power-pressure/run.py --check
python experiments/human-power-pressure/run.py --check --output /tmp/human-power-evidence.json
python -m unittest tests/test_human_power_pressure.py -v
```

With no positional fixture paths, the runner executes every bundled JSON fixture. Individual fixture files may also be supplied.

## Evidence states

`COMPLETE` means the fixture contains the observation fields required for its family. It does not mean the observed interaction is acceptable or safe.

`EVIDENCE_REQUIRED` means one or more required runtime observations are absent. Missing evidence is never promoted to PASS.

## Comparison invariant

Fixtures sharing `comparison_group` must preserve the same task identifier, task semantics, and pressure family. This prevents an A/B result from being manufactured by silently changing the task being compared.

## Adding a fixture

1. copy the closest object in `fixtures.json`;
2. retain `schema: interop-human-power-fixture/v1`;
3. give it a unique `id`, `variant`, and appropriate `comparison_group`;
4. record observations rather than conclusions;
5. preserve `authorization.presented` and `authorization.validity_observed` separately from interaction-pressure observations;
6. run the unit tests and `run.py --check`.

Do not add fields such as `harm_score`, `privacy_score`, `coercive`, `legitimate`, or `assurance_pass`. If a downstream assessment needs such a judgment, it should consume this evidence and make that decision under its own authority.

## Downstream consumption

The output package is deterministic JSON. Every result includes producer revision; source/fixture revision; fixture SHA-256; case family, comparison group, variant, and task identity; raw observations; neutral derived signals; missing-observation paths; and explicit claim boundaries.

RAHP and DPIP consumers should treat the package as evidence input, not as an assessment result.
