# Trust Protocol Interop Lab

**Current stable release: v0.6.0 — Current Implementation Evidence & Semantic Preservation**

Experimental compositions, bindings, profiles, mappings, negative tests and interoperability evidence connecting independently governed trust infrastructure, agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, Trust Tasks Task Force, OpenVTC, MCP, GovOpsWG or any other referenced standards body unless explicitly stated.

## Mission

The Lab is the **experimental integration and interoperability-assurance layer**. It asks a stronger question than “can these systems exchange messages?”:

> **Can these components compose without losing authority, delegation, lifecycle, evidence, provenance, privacy, correlation or accountability semantics?**

The working model is:

**upstream specifications → bounded Interop Case → semantic ownership + invariants → positive/negative scenarios → executable evidence → bounded findings → candidate upstream/downstream feedback**

## What v0.6.0 adds

v0.6.0 packages the major post-v0.5 transition from primarily modelled executable-governance experiments to **source-pinned current implementation evidence**. The release includes:

- current VTI/OpenVTC evidence for resolved-effect binding, credential issuance replay convergence, VAC use-time authority, personhood transport equivalence and Trust Task credential paths;
- current OpenVTC Data Rooms evidence across room, membership, policy/status/task and vetted-admission surfaces where the implementation exposes testable behavior;
- protected delegated care evidence for current authority, prescription/refill lifecycle, refill disclosure and runtime privacy boundaries;
- explicit separation between evidence a target currently exposes and propositions that remain untestable or deployment-dependent;
- stronger portable evidence packages and A/B harnesses consumed by RAHP and DPIP without allowing the Lab to become the authority for their assurance/privacy conclusions;
- retained claim boundaries for closed execution issues: bounded evidence proves the exercised proposition only, not universal implementation or ecosystem conformance.

## Start here

- [Rendered documentation home](docs/index.md)
- [Assessments](docs/assessments.md)
- [Standards Intelligence](docs/standards-intelligence.md)
- [Evidence & Assurance](docs/evidence-and-assurance.md)
- [Methods & Architecture](docs/methods.md)
- [Repository and artifact status](STATUS.md)
- [Roadmap](ROADMAP.md)
- [v0.6.0 release notes](docs/releases/v0.6.0.md)

## Current evidence families

### Current VTI / OpenVTC

The Lab contains independently bounded evidence pipelines for current implementation behavior, including resolved-effect binding, replay convergence, use-time authority, Trust Task credential paths and transport-sensitive/personhood behavior. Evidence is pinned to the target revision and observation surface. Where a live status lookup, upstream semantic primitive or independent implementation is absent, the Lab records that absence rather than fabricating a substitute.

### Data Rooms and vetted admission

Current target-native OpenVTC probes exercise the Data Rooms and vetted-admission surfaces that are actually observable. Private-room ZK, same-subject/common-control semantics, witnessed anchoring/freshness, migration, operator-control and other missing surfaces remain separate evidence triggers.

### Protected delegated care

`IC-PDC-MED-001` remains an important composed application case. v0.6 evidence covers deterministic delegated-care behavior, current-authority checks, prescription-to-refill lifecycle, disclosure comparisons and runtime privacy observations. Passing these bounded experiments does not establish production clinical suitability or legal authorization.

## Interop cases

The authoritative registry is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml). Current notable cases include Trust Tasks ↔ MCP, TEA/TSP ↔ MCP ↔ Trust Tasks, ARPA/A2A/Trust Tasks, cross-spec VC/DID cases, GovOps executable trust, minimum executable agent relationships, protected delegated care and DPAC actuation.

Maturity labels such as **Interoperability Tested (bounded semantic scope)** describe only the evidence and semantics named by the case. They are not certification or blanket wire-level interoperability claims.

## Evidence discipline

A passing validation or experiment demonstrates that the named repository artifact or proposition has the required local supporting evidence. It does not constitute independent interoperability certification. The Lab distinguishes source/specification evidence, synthetic/calibration evidence, target-native runtime evidence and deployment/governance evidence.

A current implementation result can strengthen, fail or leave a proposition indeterminate; it cannot rewrite the upstream specification or the owning assurance/privacy model.

## Coordinated release context

v0.6.0 is the Interop Lab member of the September 2026 coordinated RAHP / DPIP / Trust Protocol Interop Lab release tranche. The repositories remain independently versioned and governed:

- **Lab:** produces bounded executable interoperability/implementation evidence;
- **DPIP:** evaluates composed privacy properties over admissible evidence;
- **RAHP:** owns the broader assurance lifecycle, residual ownership and terminal posture.

This separation lets evidence move without collapsing authority.

## Repository structure

```text
catalog/       Machine-readable component and Interop Case registries
cases/         Governed compositions, invariants, scenarios and vectors
analysis/      Versioned implementation-gap analysis
bindings/      Candidate protocol bindings
mappings/      Cross-protocol semantic mappings
experiments/   Executable experiment plans and harnesses
evidence/      Portable executed interoperability evidence
observatory/   Candidate signals from portfolio monitoring
reviews/       RAHP and other pressure-test reviews
schemas/       Machine-readable governance/evidence contracts
standards/     Governed external-standards discovery and mappings
proposals/     Upstream-oriented proposal material
docs/          Architecture, evidence, methods and release records
scripts/       Deterministic validation and readiness tooling
```

## Validation

```bash
python scripts/validate_catalog.py
python scripts/validate_cases.py
python scripts/validate_evidence.py
python scripts/validate_standards.py
python scripts/validate_standards_v2.py
python scripts/generate_standards.py
python scripts/generate_readiness.py
python scripts/check_links.py
```

The `Repository assurance` workflow additionally executes the bounded cross-specification, PDC, ARA, DPAC and evidence-producer tests represented in the current repository.

## Governance boundary

Upstream remains authoritative. The Lab owns only its experimental compositions, evidence, findings and maturity claims. See [GOVERNANCE.md](GOVERNANCE.md).

## Release status

**v0.6.0 — Current Implementation Evidence & Semantic Preservation** supersedes v0.5.0 as the latest stable Lab release. v0.5.0 remains the immutable Executable Governance Experiments baseline.

## License

Unless otherwise stated in an individual artifact, repository content is made available under the terms in [LICENSE](LICENSE).
