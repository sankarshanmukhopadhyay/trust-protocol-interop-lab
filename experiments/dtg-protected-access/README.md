# Protected-access executable boundary run

This experiment executes the three-vector semantic boundary slice for `IC-DTG-PROTECTED-ACCESS-001`.

## Reproduce

```bash
python experiments/dtg-protected-access/run.py --check
```

To regenerate the committed deterministic result during development:

```bash
python experiments/dtg-protected-access/run.py --write
```

The evaluator consumes:

- `cases/dtg-protected-access/vectors/PA-POS-001.yaml`
- `cases/dtg-protected-access/vectors/PA-NEG-001.yaml`
- `cases/dtg-protected-access/vectors/PA-ADV-001.yaml`
- `cases/dtg-protected-access/dpip/interaction-profile.yaml`

and compares the computed result with `results/dtg-protected-access/run-results.json`.

## What is executed

The evaluator keeps these propositions independently observable:

- cryptographic verification;
- authority provenance;
- minimum disclosure;
- protected-relationship non-discoverability;
- cross-context correlation resistance;
- verifier/challenge/purpose context binding;
- overall case outcome.

This permits a cryptographically valid presentation to fail for privacy (`PA-NEG-001`) or context (`PA-ADV-001`) reasons without rewriting those failures as cryptographic failures.

## DPIP binding

The interaction fixture is bound to DPIP baseline `3e5d286853178bec9b6579ecbdccd1932c281fc7` and follows the interaction-profile structure used by that baseline, including scoped privacy claims and separation of proof validity from composed privacy results.

The produced `dpip_claim_results` are **lab-owned semantic execution evidence bound to the pinned DPIP model**. They are not an external certification, and this experiment does not claim that the interop lab independently executes the complete DPIP conformance harness.

## Current expected result

The three vectors should match their declared outcomes:

| Vector | Cryptographic result | Composed result | Reason |
|---|---|---|---|
| `PA-POS-001` | pass | pass | narrow result with no prohibited disclosure or stable correlator |
| `PA-NEG-001` | pass | fail | protected provider identity/location are observable and joinable |
| `PA-ADV-001` | pass for original artifact | fail | replay verifier/challenge/purpose does not match the bound context |

If all expected outcomes match, the evaluator recommends `eligible-for-admission-review`. That recommendation is evidence for a maintainer admission decision; it does not itself admit the case or set `interoperability-tested` maturity.
