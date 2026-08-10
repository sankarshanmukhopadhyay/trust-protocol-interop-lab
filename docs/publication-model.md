# Publication Model

## Purpose

The repository is intended to preserve useful standards-adjacent work without turning exploratory analysis into an implied standard.

## Lifecycle

1. **Exploratory** — establish the problem and semantic boundaries.
2. **Experimental** — draft a coherent design and examples.
3. **Candidate** — stabilize normative language sufficiently for review.
4. **Interoperability Tested** — exercise the design through implementations and test vectors.
5. **Proposed Upstream** — open an upstream discussion, issue, or pull request.
6. **Upstreamed / Superseded** — record the authoritative outcome.

## Upstream engagement

When an artifact is ready for upstream discussion:

- link to the versioned artifact in this repository;
- identify the exact upstream baseline;
- summarize design goals and unresolved questions;
- avoid copying long-lived canonical text into a discussion when a stable versioned source exists;
- record upstream discussion/PR links in the artifact README and `STATUS.md`.

## Versioning

Version directories are immutable historical baselines once superseded.

For example:

```text
bindings/trust-tasks/mcp/0.2/
bindings/trust-tasks/mcp/0.3/
```

A new upstream baseline or a material semantic change should normally produce a new binding version.
