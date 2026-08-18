# Portfolio Standards Intelligence

This directory contains the lab's governed external-standards intelligence layer.

## Source and acknowledgement

The initial discovery source is the **Global Standards Mapping Initiative (GSMI)** from the **Global Blockchain Business Council (GBBC)**. We gratefully acknowledge GSMI/GBBC for maintaining an open, crowdsourced standards-mapping resource that helps identify relevant technical standards bodies and standards activity.

GSMI is used here as a **discovery catalogue**, not as normative authority. The authoritative source for a standard is its publisher. Inclusion in this register does not imply endorsement by GSMI, GBBC, or any standards body.

The portfolio also does not claim that every locally selected specification is itself a GSMI-listed row. GSMI supplies the landscape/discovery context; local reviewers select adjacent specifications where they materially intersect portfolio architecture and then verify those specifications against publisher-controlled sources.

## Commit 2 assurance state

The seed register has now moved from discovery-only candidates to **canonical-source-verified and analysed** entries. Each entry records:

- a deliberate version or draft baseline;
- publisher status;
- a publisher-controlled baseline URI;
- verification evidence URIs;
- lifecycle notes where a newer draft, revision, or unstable dependency exists; and
- an explicit local non-dependency posture unless a repository separately establishes `depends-on`.

Canonical verification proves only that the local record accurately identifies the publisher baseline/status. It does **not** prove interoperability, implementation conformance, legal effect, authority sufficiency, security, privacy, or endorsement.

## Files

- `sources.yaml` — governed source register and GSMI/GBBC attribution.
- `register.yaml` — portfolio-relevant standards, canonical verification and local dispositions.
- `mappings/portfolio.yaml` — relationship vocabulary and project analysis lenses.
- `mappings/tsmm.yaml` — standards × TSMM semantic coverage analysis.
- `mappings/gaam.yaml` — standards × GAAM authority/assurance coverage analysis.
- `assurance/rahp-candidates.yaml` — governed RAHP assessment-candidate register.
- `cross-spec/candidates.yaml` — governed cross-specification pressure-test candidates.
- `schema/standard-entry.schema.json` — machine-verifiable standards-entry contract.
- `methodology.md` — admission, verification, mapping, assurance and monitoring method.
- `generated/` — deterministic human-readable views; do not hand-edit.

## Governance invariant

**Discovery is not dependency. Mapping is not endorsement. Verification is not authority. Cryptographic validity is not a relying-party trust decision.**

A standard becomes a normative local dependency only where an exact repository requirement, profile or implementation contract explicitly makes it one and identifies its pinned baseline.
