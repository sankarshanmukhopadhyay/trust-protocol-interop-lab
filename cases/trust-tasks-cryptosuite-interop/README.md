# Trust Tasks Cryptosuite Interoperability Pressure Test

## Purpose

This downstream fixture makes one interoperability proposition executable:

> Permitting several cryptosuites without a mandatory common floor does not, by
> itself, guarantee that two otherwise conforming implementations can verify
> each other's documents.

The matrix exercises implementations supporting only `eddsa-jcs-2022`, only
`eddsa-rdfc-2022`, or both.

## Results represented by the fixture

- shared supported suite -> `verify-capable`;
- disjoint supported-suite sets -> `unsupported-cryptosuite`;
- malformed/invalid proof under a supported suite -> `invalid-proof`;
- producer claiming a suite it does not support -> `producer-capability-mismatch`;
- no suite fallback or canonicalization substitution is permitted.

These result classes are intentionally distinct. An implementation that does
not support a suite has not established that the proof is cryptographically
invalid; it lacks the capability to evaluate it.

## Evidence boundary

This fixture tests **capability-set interoperability**, not EdDSA, JCS, or RDF
canonicalization implementations. It therefore cannot by itself establish that
either cryptosuite is correctly implemented, nor does it select a mandatory
suite for Trust Tasks.

Its purpose is to provide falsification evidence for the narrower architectural
claim that optional cryptosuite choice alone is sufficient for independent
implementation interoperability. A later upstream decision can use this evidence
without treating the lab as normative authority.
