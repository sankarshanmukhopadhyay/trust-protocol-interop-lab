# Governance

## Repository authority

This repository is an independent interoperability laboratory. It has authority only over its own case catalog, experiment definitions, evidence records, maturity claims, and publication process. It does not acquire or delegate authority to redefine any referenced upstream specification.

## Authority boundaries

- **Upstream projects** remain authoritative for their specifications, protocols, schemas, release status, and conformance claims.
- **Interop cases** are repository-owned experimental compositions against explicitly versioned upstream baselines.
- **Experiment results** establish only what was exercised under the recorded assumptions, fixtures, and implementations.
- **Portfolio signals** may nominate questions for investigation but cannot create an interoperability claim or admit a case automatically.
- **External standards catalogues**, including GSMI, may nominate standards for review but cannot create local dependency, compatibility, equivalence, or conformance claims.
- **Standards publishers** remain authoritative for the identity, status, version, and normative content of their specifications. The lab owns only its selection, mappings, evidence, and dispositions.
- **Upstream engagement** remains a human decision and must preserve provenance to the supporting evidence.

## Case admission

A case may enter the catalog when it has a bounded interoperability question, named components, versioned or dated baselines, declared semantic owners, and a maintainer-reviewed scope. A case MUST NOT imply that mere co-deployment or shared identifiers create semantic equivalence.

## Maturity authority

Case maturity is evidence-gated. `scripts/validate_cases.py` checks the minimum repository evidence required by each maturity level. Passing repository validation demonstrates internal publication discipline, not independent certification.

## Revocation and correction

A case may be marked `superseded` when its assumptions or upstream baseline no longer represent the intended experiment. Historical files remain available for audit. Materially incorrect findings should be corrected through a new commit with an explicit note identifying the affected case and evidence.


## Standards-intelligence governance

Standards intelligence is governed by `standards/sources.yaml`, `standards/register.yaml`, and `standards/mappings/portfolio.yaml`. Discovery-source attribution MUST be preserved. A `depends-on` relationship MUST identify the repository-local requirement, profile, or implementation contract that creates the dependency. Source changes create review candidates rather than automatic defect claims.

## Standards-intelligence analysis authority

The standards-intelligence layer is a local analytical control plane. GSMI/GBBC is credited as the initial discovery source, while each standards publisher remains authoritative for its own specification lifecycle and text.

Canonical-source verification may establish the identity, baseline, publication status, and lifecycle state of an external specification. It cannot establish that the specification is interoperable with another system, sufficient for an authority decision, conformantly implemented, safe, privacy preserving, or endorsed by GSMI/GBBC or the publisher.

TSMM and GAAM matrices in this repository are informative crosswalks owned by this lab. They do not amend TSMM or GAAM and do not create conformance claims against those projects.

RAHP assessment candidates and cross-specification candidates are non-finding work items. Promotion requires the evidence and human-review gates defined by the owning RAHP deployment or Interop Case maturity model. Automated monitoring MAY flag baseline drift, but MUST NOT silently move a pinned baseline, publish a finding, or create an interoperability claim.
## Executed semantic interoperability claims

An Interop Case MAY reach `interoperability-tested` through a repository-owned executable semantic reference model when all of the following are true:

- the case question is explicitly about semantic composition rather than wire compatibility;
- upstream baselines and semantic ownership are pinned;
- positive and negative vectors exercise the declared invariants;
- a deterministic evaluator and reproduction command are published;
- an evidence manifest binds the result, vectors, invariants, ownership, source basis, limitations, and evaluator with integrity hashes; and
- the claim scope explicitly excludes protocol implementation conformance, external certification, and any authority not established by the evidence.

This route does not lower the evidence bar. It narrows the claim to what is actually executable and observable. A later wire-level or multi-implementation claim requires additional evidence and MUST NOT inherit broader meaning from the semantic result.

