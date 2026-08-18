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
