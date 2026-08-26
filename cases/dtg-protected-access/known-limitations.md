# Known limitations — IC-DTG-PROTECTED-ACCESS-001

This construction is deliberately pre-admission and abstract.

## Not yet established

- No concrete upstream DTG baselines are pinned for Credentials/VRC, Trust Tasks, ZKP, directory/registry or DPIP surfaces.
- `provider_class_authorised` is an abstract predicate; the authoritative source and proof path remain to be mapped.
- The fixtures describe observable privacy properties but do not yet instantiate a concrete ZKP construction, selective-disclosure format, status mechanism or verifier protocol.
- Correlation resistance is tested only against explicitly modelled observable artifacts. Network-layer, timing, transport, endpoint and side-channel correlation are outside this first slice.
- Non-discoverability is represented as an evaluator expectation; no concrete enumeration attack surface has yet been bound to an implementation.
- The replay vector models verifier/challenge/purpose mismatch but does not yet model state revocation, provider reassignment or entitlement expiry.
- No DPIP interaction fixture or conformance-result evidence has yet been generated.
- No RAHP finding is created by this construction.

## Questions required before admission

1. Which current DTG artifact owns the entitlement/provable-fact semantics used by this slice?
2. Which artifact establishes provider-class authority without requiring disclosure of the specific protected provider?
3. What concrete proof construction can demonstrate the predicates with the required disclosure boundary?
4. Which observable fields, metadata, status calls or registry interactions must the evaluator inspect for correlation and relationship discovery?
5. How should the slice bind into DPIP so the privacy failure is evaluated over the composed interaction rather than proof validity alone?
6. Which current upstream baselines should be pinned and what semantic ownership statements are attributable to them?

An inability to answer one of these questions is not automatically an upstream defect. It should first be classified against the portfolio capability matrix and tested with stronger evidence.