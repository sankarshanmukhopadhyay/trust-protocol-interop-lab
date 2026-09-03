# Known limitations — IC-DPAC-ACTUATION-001

This experiment is intentionally bounded.

- The reference evaluators are semantic/composition models, not production agent harnesses, policy engines, authorization servers, capability systems, or actuators.
- The initial DPAC model represents authority as observable boolean state sufficient to exercise the invariant. The GovOps delegated-loan pressure test adds monetary scope, exact target/amount binding, revocation-at-actuation, policy enforcement, capability revision, and single-use actuation state, but still does not prescribe an authority token, credential format, issuer, transport, or cryptographic mechanism.
- Capability is represented as an independently administered state surface. The GovOps pressure test requires `capability_controller_separate` and rechecks capability revision at actuation, but does not demonstrate OS-, container-, cloud-, hardware-, or network-enforced isolation.
- `DPAC-005` models direct/transitive capability-controller capture as an explicit graph-derived condition; this wave does not implement a general static or runtime dependency-graph analyser.
- The composed GovOps pressure test now covers authority and capability scope divergence, revocation between authorization and actuation, capability-state TOCTOU, target substitution, amount widening, and duplicate/retry execution. It still does not claim coverage of all prompt injection, confused-deputy, concurrency, credential theft, side-channel, compromise, or supply-chain attacks.
- The evidence is self-authored and deterministically reproduced within the Lab. It is not independent implementation evidence, external review, certification, or an interoperability-tested claim.
- No normative change is made to TEA, GAAM, GovOps, TSMM, TIS, Trust Tasks, or any other upstream project. If later implementation pressure exposes a reusable semantic gap, that gap must be raised to the owning layer separately.
- External adversarial harness integration is deliberately deferred. The Agent Security Harness or another upstream tool may later be consumed as an independent pressure-test input without becoming authoritative over Lab maturity claims.

Accordingly, passing runs establish only that the repository-owned reference models preserve their declared DPAC boundaries for the recorded scenarios at the tested revision.
