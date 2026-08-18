# XSP-001 known limitations

- The executed evaluator is a semantic reference model. It does not send OpenID4VCI/OpenID4VP messages or run W3C cryptosuites.
- No claim is made about implementation conformance, cryptographic algorithm correctness, wallet security, transport security, status-method availability, or privacy properties beyond the modeled invariants.
- The test uses pinned specification baselines. Later errata or revisions require reassessment rather than silently changing the result.
- Issuer-authority policy is intentionally deployment-owned because VC Data Model v2.0 leaves the verifier's issuer-trust decision out of scope.
- A production profile should add protocol-native conformance suites and deployment-specific trust-policy fixtures before treating this result as operational assurance.
