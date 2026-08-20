# Standards Corpus Shards

This directory contains governed corpus shards that extend the core `standards/register.yaml` without turning that file into a single monolithic catalogue.

Each shard MUST:

- identify a coherent standards family, publisher family, or analytical domain;
- use globally unique `STD-*` identifiers;
- preserve canonical publisher URIs and a pinned analysed baseline;
- identify discovery sources separately from canonical publisher sources;
- record artifact type and lifecycle state;
- keep `normative_dependency: false` unless a repository requirement explicitly establishes a dependency; and
- pass `scripts/validate_standards_v2.py` before merge.

## Current shards

- [`iso-tc307.yaml`](iso-tc307.yaml) — portfolio-relevant ISO/TC 307 blockchain and distributed ledger technology publications.

## Governance boundary

Corpus admission means **tracked and analysed**. It does not mean implemented, compatible, conformant, endorsed, legally binding, or sufficient for authority. A specification becomes a local normative dependency only through an explicit repository requirement with a pinned baseline and evidence.

## Why shards

The core register remains useful for high-priority cross-portfolio specifications. Shards allow the corpus to grow by standards family while preserving deterministic validation, provenance, lifecycle monitoring and review ownership.
