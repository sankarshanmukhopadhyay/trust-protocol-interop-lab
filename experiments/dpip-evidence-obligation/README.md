# DPIP evidence-obligation acquisition boundary

This experiment family consumes `dpip-evidence-obligation/v1` work objects and decides only whether the Interop Lab may legitimately acquire the requested evidence.

It does **not** decide privacy PASS/FAIL, discrimination, legitimacy, harm, or portfolio assurance. Those remain with DPIP and RAHP under their respective authority boundaries.

## Admission outcomes

- `ADMISSIBLE`: the observation is target-bound and independently observable through static implementation evidence, black-box runtime evidence, or explicitly delegated Lab white-box access.
- `BLOCKED`: a concrete blocker such as `NO_TARGET`, `OPERATOR_ACCESS_REQUIRED`, or an unbound E3+ target prevents execution.
- `SUPPLIER_OR_AUTHORITY_REQUIRED`: the requested evidence belongs to an operator, governance authority, or another supplier rather than the Lab.

## Scientific rule

The Lab must not manufacture target-runtime or deployment evidence using a synthetic substitute. E3+ obligations require a repository/deployment target bound to an immutable revision. A `NO_TARGET` outcome is therefore a valid and useful result.

The reference fixture mirrors the three residual obligations from DPIP #191. All three are intentionally blocked because no concrete target has been nominated. The correct action is **not** to run another synthetic proxy-inference experiment.

## Reproduction

```bash
python -m unittest tests/test_dpip_evidence_obligation.py -v
python experiments/dpip-evidence-obligation/admit.py \
  --input experiments/dpip-evidence-obligation/dpip-191-obligations.json \
  --check
```

When a future obligation becomes `ADMISSIBLE`, a target-specific experiment may be created under the normal Interop case discipline. Its resulting evidence package must preserve the source obligation ID, observer scope, immutable target revision, experiment provenance, evidence maturity, and claim boundary before returning to DPIP.
