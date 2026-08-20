# Known limitations — IC-ARPA-A2A-TT-001

- A2A issue #2028 is an open proposal and may change shape, naming, or governance disposition.
- The lab does not claim that `actorChain`, `proof_ref`, `credentialRef`, or `originAnchor` are normative A2A v1.0 fields.
- Payload-only monotonic narrowing cannot prove that a grant existed and cannot detect historical-hop rewriting if the receiver did not retain the received representation or digest.
- Evidence resolution semantics depend on the referenced authority/evidence system; the lab tests state separation but does not standardize a universal delegation credential.
- Privacy-preserving lineage is identified as an interoperability requirement but no single cryptographic construction is selected here.
- ANAB declaration retrieval, digest verification, key resolution, signature verification, and revocation fetching are modeled as semantic inputs; the runner does not perform live cryptography or network resolution.
