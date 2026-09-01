---
layout: default
title: Standards Intelligence
nav_order: 4
nav_exclude: false
permalink: /standards-intelligence/
---
# Standards Intelligence

The standards-intelligence layer turns externally discovered standards into verified, governed portfolio inputs.

**Source acknowledgement:** the Global Standards Mapping Initiative (GSMI), an initiative of the Global Blockchain Business Council (GBBC), is an initial standards-discovery source. GSMI/GBBC does not become normative authority for referenced specifications; canonical publishers remain authoritative.

## Standards Intelligence v2

The corpus now separates **discovery provenance**, **standards-body authority metadata**, **pinned specification baselines**, and **assurance candidates**. This prevents a catalogue row, an international standard, a technical report, an Internet-Draft and an industry specification from being treated as equivalent merely because they appear in the same inventory.

Corpus families can be maintained as validated shards under `standards/corpus/`. The first shard adds nine portfolio-relevant ISO/TC 307 publications spanning vocabulary, architecture, taxonomy/ontology, privacy, DLT identity management, smart contracts, interoperability, governance and trust anchors.

Every shard entry records its artifact type, canonical publisher baseline, lifecycle note and monitoring posture. Admission means tracked and analysed; it does not establish implementation, interoperability, conformance, authority sufficiency, endorsement or local normative dependency.

## Browse

- [Method and governance](../standards/methodology.md)
- [Standards layer README](../standards/README.md)
- [Standards-body authority registry](../standards/bodies.yaml)
- [ISO/TC 307 corpus](../standards/corpus/iso-tc307.yaml)
- [Verified standards register](../standards/generated/standards-register.md)
- [Canonical verification report](../standards/generated/verification-report.md)
- [Standards × portfolio](../standards/generated/portfolio-matrix.md)
- [Standards × TSMM semantics](../standards/generated/tsmm-semantic-matrix.md)
- [Standards × GAAM authority](../standards/generated/gaam-authority-matrix.md)
- [RAHP candidates](../standards/generated/rahp-candidates.md)
- [Cross-spec candidates and promotions](../standards/generated/cross-spec-candidates.md)

## Validation contract

Pull requests and pushes to `main` run repository assurance CI. The standards layer is validated by both the core validator and `scripts/validate_standards_v2.py`, which checks the combined ID space across the seed register and corpus shards, source references, standards-body references, HTTPS canonical baselines and pinned lifecycle monitoring metadata.
