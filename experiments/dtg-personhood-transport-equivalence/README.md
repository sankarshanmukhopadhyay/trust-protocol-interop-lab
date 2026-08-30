# DTG personhood transport equivalence evidence

This experiment answers RAHP #263 against an immutable VTI revision.

It deliberately does not create a second implementation of the personhood ceremony. Instead it executes the upstream VTI test surfaces that own the relevant invariants and verifies the three transport adapters converge on the same core implementation.

The evidence boundary is:

- REST: executable personhood integration suite, including nonce/challenge and replay-adjacent negative cases.
- DIDComm: executable shared-dispatcher tests for membership and subject binding.
- TSP: executable verified-sender and request-demultiplexing tests, plus source-pinned verification that TSP feeds the same `dispatch_trust_task_core`.
- Shared semantics: both challenge and assertion dispatch into the same `challenge_inner` / `assert_inner` implementation used by REST.

A green workflow is evidence for the named transport-equivalence proposition only. It is not a whole-VTI assurance conclusion.
