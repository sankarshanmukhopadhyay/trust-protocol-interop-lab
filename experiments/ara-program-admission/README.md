# ARA final programme admission check

This directory contains the final evidence-gated consistency check for `IC-ARA-REL-001`.

## Why this runner exists

The ARA programme deliberately separates:

```text
green phase tests
!= complete programme evidence
!= human admission decision
```

The phase implementations establish bounded executable propositions. Phase 10 adds adversarial assurance. Phase 11 records the standards-native boundary. The final admission runner verifies that those evidence states, the 12 programme gates, the final claim boundary, and the catalog entry agree.

It does **not** create the human admission decision. That decision was recorded in programme issue #32 and PR #57.

## Run

From the repository root:

```bash
python experiments/ara-program-admission/run.py --check
```

A successful result reports `admission_evidence_satisfied`.

## What it checks

The runner verifies:

- Phase 10 adversarial assurance remains green;
- Phase 11 standards-boundary evidence remains green;
- all 12 ARA promotion gates are marked `satisfied`;
- `promotion_ready` is true;
- the gate document reports `interoperability-tested`;
- the authoritative catalog contains `IC-ARA-REL-001` at that maturity;
- the final claim-boundary document exists;
- the final evidence manifest exists.

## What it does not prove

A passing admission check does not establish:

- production security;
- wire-protocol conformance;
- external certification;
- legal validity;
- blanket TSP/OpenVTC VTA/RCard/VRC conformance;
- standards-native replacement of every adapter.

For the authoritative admitted scope, read:

- `cases/ara-minimum-executable-relationship/final-claim-boundary.md`;
- `evidence/ara-minimum-executable-relationship/evidence-manifest.json`;
- `cases/ara-minimum-executable-relationship/promotion-gates.yaml`.
