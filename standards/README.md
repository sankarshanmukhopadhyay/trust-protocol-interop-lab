# Portfolio Standards Intelligence

This directory contains the lab's governed external-standards intelligence layer.

## Source and acknowledgement

The initial discovery source is the **Global Standards Mapping Initiative (GSMI)** from the **Global Blockchain Business Council (GBBC)**. GSMI is used here as a **discovery catalogue**, not as normative authority. The authoritative source for a standard is its publisher. Inclusion in this repository does not imply endorsement by GSMI, GBBC, ISO, or any other standards body.

GSMI 6.0 Technical Standards is also registered as a discovery and standards-ecosystem taxonomy source. Its distinctions among global, regional, national, industry-specific, consortium and initiative actors inform the local standards-body model. The source document is not mirrored; only derived metadata, attribution and publisher links are maintained.

## Standards Intelligence v2

The corpus now has three explicit governance layers:

1. **Sources** — where a candidate was discovered and which publisher-controlled source verifies it.
2. **Bodies** — what kind of standards authority or standards-development actor produced or governs the work.
3. **Standards** — pinned specification baselines, lifecycle state, portfolio relevance and assurance relationships.

The seed register remains in `register.yaml`. Coherent publisher or domain families can be added as validated shards under `corpus/`, allowing the corpus to scale without turning the seed register into an ungoverned monolith.

The first v2 shard is the ISO/TC 307 corpus, covering portfolio-relevant vocabulary, architecture, taxonomy/ontology, privacy, identity-management, smart-contract, interoperability, governance and trust-anchor publications.

## Files

- `sources.yaml` — governed source register, including GSMI and canonical publisher catalogues.
- `bodies.yaml` — standards-body authority metadata.
- `register.yaml` — core portfolio-relevant standards and pinned verification baselines.
- `corpus/` — validated standards-family shards extending the core register.
- `mappings/portfolio.yaml` — relationship vocabulary and project analysis lenses.
- `mappings/tsmm.yaml` — standards × TSMM semantic coverage analysis.
- `mappings/gaam.yaml` — standards × GAAM authority/assurance coverage analysis.
- `assurance/rahp-candidates.yaml` — governed RAHP assessment-candidate register.
- `cross-spec/candidates.yaml` — governed cross-specification pressure-test candidates.
- `schema/standard-entry.schema.json` — machine-verifiable standards-entry contract.
- `schema/standards-body.schema.json` — machine-verifiable standards-body contract.
- `methodology.md` — admission, verification, mapping, assurance and monitoring method.
- `generated/` — deterministic human-readable views; do not hand-edit generated artifacts.

## Validation

Run both generations of standards validation:

```bash
python scripts/validate_standards.py
python scripts/validate_standards_v2.py
```

`validate_standards_v2.py` checks the combined identifier space across the core register and all corpus shards, validates source and standards-body references, requires HTTPS canonical baselines, and enforces baseline-pinning metadata for shard entries.

GitHub Actions now executes repository assurance validation on pull requests and pushes to `main`, including catalog, cases, evidence, standards, executable cross-spec tests, generated-output cleanliness and link checks.

## Governance invariant

**Discovery is not dependency. Mapping is not endorsement. Verification is not authority. Cryptographic validity is not a relying-party trust decision.**

A standard becomes a normative local dependency only where an exact repository requirement, profile or implementation contract explicitly makes it one and identifies its pinned baseline.
