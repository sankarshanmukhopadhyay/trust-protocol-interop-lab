# Known limitations — IC-DPAC-ACTUATION-001

This experiment is intentionally bounded.

- The reference evaluator is a semantic model, not a production agent harness, policy engine, authorization server, capability system, or actuator.
- Authority is represented as observable boolean state sufficient to exercise the invariant. The experiment does not prescribe an authority token, credential format, issuer, transport, or cryptographic mechanism.
- Capability is represented as an independently administered decision input. The experiment does not yet demonstrate OS-, container-, cloud-, hardware-, or network-enforced isolation.
- `DPAC-005` models direct/transitive capability-controller capture as an explicit graph-derived condition; this wave does not implement a general static or runtime dependency-graph analyser.
- The scenario set covers the five falsification cases agreed for the initial experiment. It does not claim coverage of all prompt injection, confused-deputy, race, TOCTOU, credential theft, side-channel, concurrency, compromise, or supply-chain attacks.
- The evidence is self-authored and deterministically reproduced within the Lab. It is not independent implementation evidence, external review, certification, or an interoperability-tested claim.
- No normative change is made to TEA, GAAM, GovOps, TSMM, TIS, Trust Tasks, or any other upstream project. If later implementation pressure exposes a reusable semantic gap, that gap must be raised to the owning layer separately.
- External adversarial harness integration is deliberately deferred. The Agent Security Harness or another upstream tool may later be consumed as an independent pressure-test input without becoming authoritative over Lab maturity claims.

Accordingly, a passing run establishes only that the repository-owned reference model preserves its declared DPAC invariants for the recorded scenarios at the tested revision.
