---
layout: default
title: Repository Baseline
parent: Methods & Architecture
nav_order: 95
---
# Repository Security, Supply-Chain, and Release Baseline

This page records the repository-local controls that make changes auditable and consumable without overstating what GitHub settings or local CI can prove.

## Change-control authority

`main` is governed by the active `protect-main` ruleset. Repository changes must use the protected pull-request path and satisfy the required `validate` status. The ruleset prohibits deletion and non-fast-forward updates, requires review-thread resolution, and has no bypass actors.

A merge records acceptance of a bounded repository change. It does not create upstream authority, external certification, or broader interoperability meaning than the associated evidence supports.

## Workflow trust boundary

Repository assurance workflows use least-privilege token permissions unless a workflow documents a narrower write requirement. The primary repository-assurance workflow uses `contents: read` and does not use `pull_request_target` to execute contributor-controlled code with elevated repository authority.

Workflow changes that add write permissions, secrets, external deployment authority, or execution of untrusted contributor-controlled inputs are consequential governance changes and require explicit review of that new trust boundary.

### Action dependencies

- GitHub-maintained Actions may use stable major release references and are monitored through Dependabot.
- Non-GitHub Actions that execute repository code SHOULD be pinned to an immutable commit SHA when practical.
- Dependabot is configured for GitHub Actions so action updates remain visible as reviewable pull requests rather than silent dependency drift.

## Dependency policy

The repository is primarily source, fixtures, deterministic validators, and documentation rather than a packaged runtime distribution.

- **Python:** CI installs the small validation dependency set explicitly. There is no published Python package and therefore no package lockfile contract for consumers.
- **Ruby/Jekyll:** `Gemfile` defines the GitHub Pages documentation toolchain. CI uses Bundler and Dependabot monitors the Bundler ecosystem.
- **Node/BBS evidence:** the BBS construction experiment declares its npm dependency in `experiments/dtg-protected-access-bbs/package.json`; experiment dependencies should remain exact-version pinned unless a deliberate range is justified. Dependabot monitors that directory.
- Transient build/install products are not evidence artifacts and MUST NOT be committed unless a governed evidence contract explicitly requires them.

## Release and provenance policy

This laboratory's primary consumable surface is the version-controlled repository and GitHub Pages documentation, not a continuously supported binary or library release train.

Repository releases are therefore **optional publication checkpoints**, not a required delivery mechanism. When a release is created, its authority is limited to the tagged repository revision and any explicitly enumerated artifacts. A release MUST NOT broaden an Interop Case maturity or conformance claim beyond the catalog and evidence present at that revision.

Generated readiness and standards views are deterministic repository artifacts. CI regenerates them and fails if the checked-in tree differs. Executed interoperability evidence is governed separately by case-specific evidence manifests and integrity identifiers.

No separate reproducible-binary guarantee is claimed because this repository does not publish a production binary distribution. If such an artifact is introduced later, reproducibility and provenance become mandatory release controls before it is treated as supported output.

## Security-setting evidence boundary

Repository files can define security reporting and supply-chain policy but cannot, by themselves, prove account-side GitHub settings such as Dependabot alerts, secret scanning, or private vulnerability reporting are enabled. Those settings should be verified in GitHub when available to the maintainer.

Absence of machine-readable settings evidence MUST NOT be converted into a false PASS claim. Repository-local controls remain valid independently: [SECURITY.md](../SECURITY.md) prohibits public vulnerability disclosure and directs reporters to a private channel; Dependabot configuration establishes update monitoring once GitHub processes the configuration.

## Discoverability

The repository has a public description and GitHub Pages homepage. The README is the authoritative adoption entry point and links to rendered documentation, assessments, standards intelligence, evidence/assurance, methods, and current status.

Repository topics are helpful discovery metadata but are not part of the assurance or authority model and do not affect the validity of an Interop Case.
