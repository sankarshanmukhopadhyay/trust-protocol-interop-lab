# Security Policy

## Reporting a vulnerability

Do **not** disclose security-sensitive details in a public issue, discussion, pull request, or commit message.

Use GitHub's private vulnerability-reporting / Security Advisory channel for this repository when it is available. If the private-report control is not available in the repository UI, contact the repository maintainer through their GitHub profile to arrange a private channel before sending technical details.

A useful report includes:

- affected file, workflow, experiment, evidence package, or release;
- reproduction steps and required preconditions;
- expected and observed behaviour;
- security impact, including any authority, delegation, privacy, evidence-integrity, or supply-chain boundary affected; and
- a proof of concept where it can be shared safely.

## Supported versions

This repository is an experimental interoperability laboratory rather than a long-lived product distribution. Security fixes apply to the current default branch and to any explicitly identified current release. Historical case baselines and superseded evidence remain available for audit but are not independently maintained as supported software versions.

## Disclosure and remediation

The maintainer will acknowledge, triage, and remediate reports on a best-effort basis proportionate to impact. A security correction MUST preserve the repository's evidence trail: affected claims, cases, evidence, and generated views are corrected or superseded rather than silently rewritten.

## Security boundary

A passing repository workflow, maturity gate, or interoperability experiment is not a security certification. Upstream projects remain authoritative for their own security statements and supported versions.
