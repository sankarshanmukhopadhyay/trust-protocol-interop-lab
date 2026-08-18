---
layout: default
title: XSP-001 reproduction
parent: XSP-001 — Credential reliance chain
grand_parent: Assessments
nav_order: 3
---
# Reproduce XSP-001

```bash
python3 experiments/xsp-001/run.py
```

The evaluator reads all JSON vectors under `cases/xsp-001/vectors/`, applies the composition rules, and writes `evidence/xsp-001/result.json`, `run-log.json`, and `evidence-manifest.json` with SHA-256 artifact hashes.

The evaluator deliberately models semantic gates rather than wire messages or cryptographic algorithms. A pass establishes only that the modeled composition rules reject/allow the supplied vectors as declared.
