# XSP-001 source basis

The assessment is bounded to the canonical publisher baselines recorded in `standards/register.yaml`. The following source semantics are the basis for the composition rules.

| Source | Material semantic used by this assessment | Canonical baseline |
|---|---|---|
| W3C VC Data Model v2.0 | `credentialStatus` supports lifecycle/status discovery; verifier trust in issuers and purposes is outside the data model and remains a verifier decision | https://www.w3.org/TR/2025/REC-vc-data-model-2.0-20250515/ |
| W3C VC Data Integrity 1.0 | proof verification uses verification methods/cryptosuites and proof-purpose semantics; successful cryptographic verification is a proof-layer result | https://www.w3.org/TR/2025/REC-vc-data-integrity-20250515/ |
| OpenID4VCI 1.0 | OAuth protects the issuance API; issuance authorization controls receiving credentials and proof-of-possession binds request freshness/audience where configured | https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html |
| OpenID4VP 1.0 | presentations are bound to the intended verifier and transaction using `client_id`/audience and `nonce`; the verifier must validate that binding | https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html |

## Interpretation boundary

These sources establish the semantics owned by their respective layers. The Interop Lab adds only the composition requirement that those semantics remain separately observable and must not be substituted for the relying party's authority and effect decision.
