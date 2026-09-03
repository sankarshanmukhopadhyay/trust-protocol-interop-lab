---
layout: default
title: Maturity Model
parent: Methods & Architecture
nav_order: 30
---
# Evidence-Gated Maturity Model

Maturity applies to each Interop Case independently.

| Status | Minimum repository evidence |
|---|---|
| Exploratory | registered case, bounded question, baselines, semantic ownership |
| Experimental | exploratory requirements plus invariants and scenarios |
| Candidate | experimental requirements plus positive and negative/adversarial vectors, expected behavior, known limitations |
| Interoperability Tested | candidate requirements plus executed results, reproducibility instructions, evidence manifest, explicit claim scope, and integrity-bound evidence |
| Proposed Upstream | tested or otherwise evidence-supported case plus exact upstream proposal/discussion reference |
| Upstreamed | recorded authoritative upstream outcome |
| Superseded | replacement or baseline change recorded while historical evidence is retained |

Candidate vectors may use either the repository's `valid/*.json` / `invalid/*.json` catalogue layout or the governed flat YAML experiment layout where each vector declares its `class`, stable `id`, and expected behaviour. The evidence meaning is the same: Candidate status means the proposition is structured for review and falsification, not that execution interoperability has been established.

For semantic composition cases, an executable reference evaluator can satisfy the execution gate when the claim is explicitly bounded to semantic interoperability. It does not establish wire-protocol conformance.

## Interoperability Tested evidence gate

A Tested claim must point to a JSON evidence manifest. `scripts/validate_cases.py` fails closed unless the manifest:

- identifies the same Interop Case as the catalog entry;
- states a non-empty bounded `claim_scope`;
- names a repository-contained runner/reproduction command;
- records `result_summary.status: pass`;
- references evidence artifacts that resolve inside this repository;
- uses syntactically valid SHA-256 or Git blob identifiers when supplied; and
- binds at least one artifact to an integrity identifier.

The validator accepts both SHA-256 content hashes and Git blob SHAs because existing governed evidence packages use both integrity models. This is a compatibility choice, not a reduction in the Tested gate.

The validator rejects maturity claims that lack the minimum local evidence. Passing repository validation demonstrates internal publication discipline and reproducibility; it does not mean an external party independently agrees with the result, certify production behaviour, or establish upstream conformance.
