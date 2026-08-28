# IC-ARA-REL-001 Phase 10 — visible adversarial-assurance judgment

Issue: #42  
Parent: #32  
Depends on completed Relationship View phase: #41

## Proposition under test

Do the accumulated ARA claims survive systematic attempts to reinterpret, inflate, correlate, stale, bypass, or retroactively legitimize the evidence produced by the walking skeleton?

## Alternatives genuinely considered

### Treat all earlier green phase runs as sufficient assurance

Rejected. Passing functional tests does not establish evidence sufficiency, independence, claim boundaries, or absence of semantic overreach.

### Count credentials/attestations as independent by artifact count

Rejected. Apparent multiplicity can arise from one controller, issuer family, infrastructure operator, or common evidence path.

### Convert missing assurance evidence into failure or PASS

Rejected. Where a required assurance fact is unresolved, the defensible result is `INDETERMINATE`.

### Add a meta-assurance harness and RAHP-style pressure review

Selected. The harness reruns all executable ARA phases, adds explicit assurance-boundary vectors, hashes evidence outputs, and publishes gate-by-gate maturity rather than a blanket maturity label.

## Core judgment

> Assurance must pressure the interpretation of evidence, not merely rerun the mechanism that produced it.

The implementation preserves:

```text
green workflow != assurance green
missing evidence != PASS
evidence != authority
assurance != retroactive authorization
multiplicity != independence
unilateral state != collective state
later state != last defensible checkpoint
```

## Human acceptance boundary

A green Phase 10 run can satisfy `ARA-G10-ADVERSARIAL-EVIDENCE` for this bounded Lab slice. It cannot satisfy standards-native integration or production-security claims.

The standards-native gate remains intentionally partial pending #43.
