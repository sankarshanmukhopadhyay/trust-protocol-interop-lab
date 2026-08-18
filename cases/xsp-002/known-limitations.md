# XSP-002 known limitations

- The evaluator does not execute a DID method, resolver network request, JWT signature, Federation Entity Discovery, or metadata-policy operator.
- DID Resolution is pinned to the 2026-08-06 Candidate Recommendation Snapshot; its Candidate Recommendation status means later changes are possible.
- Organizational/legal authority is necessarily deployment-specific and is represented as an explicit external evidence input.
- The model does not assume a DID controller is a legal person, organization, registrar, or authorized agent.
- The model does not treat a federation trust anchor as universally authoritative outside its federation or application profile.
- Production assurance should add DID-method-specific conformance, OpenID Federation implementation tests, freshness/cache behavior, and governance-authority fixtures.
