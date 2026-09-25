# Trust Protocol Interop Lab

**Current stable release: v0.7.0 — Portable Evidence, Authority Composition & Current-Epoch Revalidation**

Experimental compositions, bindings, profiles, mappings, negative tests and interoperability evidence connecting independently governed trust infrastructure, agent and application protocols.

> **Status:** Independent experimental work. Nothing in this repository is an approved specification of the Trust over IP Foundation, DTGWG, Trust Tasks Task Force, OpenVTC, MCP, GovOpsWG or any other referenced standards body unless explicitly stated.

## Mission

The Lab is the **experimental integration and interoperability-assurance layer**. It asks a stronger question than “can these systems exchange messages?”:

> **Can these components compose without losing authority, delegation, lifecycle, evidence, provenance, privacy, correlation or accountability semantics?**

The working model is:

**upstream specifications → bounded Interop Case → semantic ownership + invariants → positive/negative scenarios → executable evidence → bounded findings → candidate upstream/downstream feedback**

## What v0.7.0 adds

v0.7.0 packages the post-v0.6 tranche around **portable evidence obligations, authority-at-commitment composition, interoperability preconditions and current-epoch evidence refresh**:

- a deterministic human-power pressure evidence program with portable machine-verifiable observation packages and explicit counter-cases;
- admission/execution support for DPIP evidence obligations without allowing the Lab to issue privacy or broader assurance conclusions;
- task-citation convergence machinery separating exact citation binding, completion evidence, action authority and correlation observations;
- authority-at-material-commitment vectors for current authority, revocation, scope, approval binding and unavailable status;
- collective-authority composition evidence covering threshold satisfaction, stale membership/rules and duplicate participation;
- cryptosuite capability-floor evidence showing why optional suite choice without a shared floor does not guarantee independent implementation interoperability;
- current proof-required-route evidence that distinguishes remediated dispatcher controls from still-reachable bearer-route divergence;
- a 2026-09-24 source-pinned refresh of the evidence surfaces consumed by the DTG/VTC clean-room assurance epoch.

## Start here

- [Rendered documentation home](docs/index.md)
- [Assessments](docs/assessments.md)
- [Standards Intelligence](docs/standards-intelligence.md)
- [Evidence & Assurance](docs/evidence-and-assurance.md)
- [Methods & Architecture](docs/methods.md)
- [Repository and artifact status](STATUS.md)
- [Roadmap](ROADMAP.md)
- [v0.7.0 release notes](docs/releases/v0.7.0.md)

## Current evidence families

### Portable evidence and specialist handoff

The Lab can now accept bounded evidence obligations from DPIP, preserve their target revision, observer scope, required maturity, observations and claim boundaries, and report whether the requested observation can actually be produced. Targetless or unavailable runtime obligations are blocked rather than replaced by synthetic substitutes.

Human-power pressure evidence is likewise emitted as neutral observations and derived signals. DPIP and RAHP remain the owners of privacy and broader assurance judgment.

### Authority at material commitment

The ARA evidence surface now exercises whether authority is current at the point a material act is committed. Single-actor and collective-authority cases distinguish current authority, revocation, scope, approval binding, threshold satisfaction, stale membership/rules, duplicate participation and unavailable status.

Identity/signature evidence remains necessary input, not independent authority.

### Task citation, proof and correlation

The Lab separately evaluates exact task citation, completion evidence, action authority and correlation. Current source characterization is not silently promoted into runtime conformance. Missing implementation or observation surfaces remain explicit `not-implemented` / `not-observable` evidence states.

### Cryptosuite capability floor

A dedicated interoperability fixture demonstrates that a shared supported cryptosuite is a necessary verification precondition. Unsupported suite, invalid proof and producer capability mismatch remain distinct outcomes. The fixture does not choose an MTI suite or claim cryptographic implementation conformance.

### Current DTG / VTI evidence epoch

The September 24 evidence refresh re-pins the Trust Task → credential path, keyed replay convergence, VAC use-time authority/binding, and selected A/B privacy observer surfaces to the current VTI/DPIP/RAHP source epoch. Historical evidence remains lineage rather than a substitute for current execution.

## Interop cases

The authoritative registry is [`catalog/interoperability-cases.yaml`](catalog/interoperability-cases.yaml). Current notable cases include Trust Tasks ↔ MCP, TEA/TSP ↔ MCP ↔ Trust Tasks, ARPA/A2A/Trust Tasks, cross-spec VC/DID cases, GovOps executable trust, minimum executable agent relationships, protected delegated care and DPAC actuation.

Maturity labels such as **Interoperability Tested (bounded semantic scope)** describe only the evidence and semantics named by the case. They are not certification or blanket wire-level interoperability claims.

## Evidence discipline

A passing validation or experiment demonstrates that the named repository artifact or proposition has the required local supporting evidence. It does not constitute independent interoperability certification. The Lab distinguishes source/specification evidence, synthetic/calibration evidence, target-native runtime evidence and deployment/governance evidence.

A current implementation result can strengthen, fail or leave a proposition indeterminate; it cannot rewrite the upstream specification or the owning assurance/privacy model.

## Release context

v0.7.0 is independently versioned from RAHP and DPIP. The Lab produces bounded executable observations and evidence packages; DPIP evaluates privacy propositions over admissible evidence; RAHP owns the broader assurance lifecycle and residual reconciliation. This separation lets evidence move without collapsing authority.

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

The `Repository assurance` workflow additionally executes the bounded cross-specification, PDC, ARA, DPAC, human-power, task-citation and evidence-producer tests represented in the current repository.

## Governance boundary

Upstream remains authoritative. The Lab owns only its experimental compositions, evidence, findings and maturity claims. See [GOVERNANCE.md](GOVERNANCE.md).

## Release status

**v0.7.0 — Portable Evidence, Authority Composition & Current-Epoch Revalidation** supersedes v0.6.0 as the latest stable Lab release. v0.6.0 remains the immutable Current Implementation Evidence & Semantic Preservation baseline.

## License

Unless otherwise stated in an individual artifact, repository content is made available under the terms in [LICENSE](LICENSE).
