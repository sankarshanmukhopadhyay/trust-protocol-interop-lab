---
layout: default
title: XSP-002 reproduction
parent: XSP-002 — DID/federation authority chain
grand_parent: Assessments
nav_order: 3
---
# Reproduce XSP-002

```bash
python3 experiments/xsp-002/run.py
```

The evaluator reads all JSON vectors under `cases/xsp-002/vectors/`, applies the bounded composition rules, and writes `evidence/xsp-002/result.json`, `run-log.json`, and `evidence-manifest.json` with SHA-256 artifact hashes.

It does not implement a DID method, resolver network stack, JWT validation, or Federation Entity Discovery. It tests the semantic non-substitution and lifecycle rules declared by this case.
