# XSP-002 source basis

The assessment is bounded to the canonical publisher baselines recorded in `standards/register.yaml`.

| Source | Material semantic used by this assessment | Canonical baseline |
|---|---|---|
| W3C DID Core v1.0 | DIDs identify subjects and DID documents expose verification relationships/service information; control of a DID does not itself create every external organizational or legal authority | https://www.w3.org/TR/2022/REC-did-core-20220719/ |
| W3C DID Resolution v1 | resolution obtains a DID document and accompanying metadata; the document enables cryptographically verifiable interactions and may expose current/deactivated state | https://www.w3.org/TR/2026/CR-did-resolution-1.0-20260806/ |
| OpenID Federation 1.0 | a validated trust chain proves federation membership rooted at a selected trust anchor; federation policy derives/constrains metadata for the subject | https://openid.net/specs/openid-federation-1_0-final.html |

## Interpretation boundary

The assessment treats DID resolution and federation membership as evidence layers. Organizational role, delegated action scope, and permission to produce a consequential effect remain separately governed unless an application profile explicitly and validly binds those semantics.
