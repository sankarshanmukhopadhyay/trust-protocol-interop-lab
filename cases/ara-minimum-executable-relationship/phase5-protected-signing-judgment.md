# IC-ARA-REL-001 Phase 5 — visible protected-signing judgment

Issue: #37  
Parent: #32  
Depends on completed authorization spine: #36

## Proposition under test

Can protected signing be exercised only by an authenticated deterministic Workflow for the exact Agent Role, relationship state, task type/version and instance, recipient, payload, authority context, capability, prior admission, and expiry already established by the bounded ARA authorization path?

## Alternatives genuinely considered

### Expose a normal signing API and rely on callers to use it correctly

Rejected. This would make possession or API reachability of key material equivalent to practical authority and leave the Phase 4 authorization spine bypassable.

### Validate only caller identity before signing

Rejected. Authenticated caller identity does not establish authority, active agreement, current relationship state, exact task semantics, recipient, payload, freshness, or policy admission.

### Treat a valid Trust Task or signature as sufficient

Rejected. Both may be structurally and cryptographically valid while still being stale, revoked, out of scope, substituted, replayed, or disconnected from the current relationship decision.

### Require the exact Phase 4 admission receipt and re-check current context

Selected. The protected signer is the next constrained actuator after execution admission. It accepts only a canonical request derived from the admitted task/decision/capability context and independently re-checks current authority, agreement, Role Record head, workflow authentication, task version, recipient, purpose, payload digest, expiry, and replay.

## Decision

Implement a Lab-local `ProtectedSigner` with no unrestricted raw-byte signing operation. Every attempt, including refusal, produces an attributable cryptographic-use receipt.

For the walking skeleton, HMAC-SHA256 is used only to make cryptographic use executable and context-sensitive. The key is a process-local test secret. That is **not** a production protection guarantee.

## Core judgment

> Cryptographic possession is not authority. A signature or MAC becomes legitimate ARA action evidence only when cryptographic use itself is gated by the exact current authorization and relationship context.

Phase 5 therefore preserves:

```text
key possession
!= permission to use key
!= relationship authority
!= policy authorization
!= admitted task
!= legitimate effect
```

## Falsification evidence required

The executable suite must refuse at least:

- direct Live Agent call;
- arbitrary-byte signing;
- unauthenticated Workflow;
- substituted/replaced Workflow identity or version;
- unsupported/stale Trust Task version;
- recipient substitution;
- payload substitution;
- wrong relationship;
- wrong agreement;
- stale Role Record head;
- revoked authority;
- expired authority;
- replayed nonce/task;
- signing after agreement suspension;
- signing after agreement closure;
- missing decision binding;
- missing Phase 4 admission evidence.

A positive vector must show an accepted cryptographic-use receipt whose signed-context reference binds the complete admitted context rather than caller-provided arbitrary bytes.

## Rejected inferences

This phase must not be read to establish:

- OpenVTC VTA conformance;
- HSM, TEE, secure enclave, or hardware-backed signing;
- DID or TSP conformance;
- normative VID semantics;
- key non-exportability;
- resistance to local process compromise;
- remote attestation;
- production cryptographic policy enforcement;
- overall ARA case admission.

## Residual uncertainty

Still unresolved by design:

- standards-native protected-signing realization;
- independent counterparty/process boundary (#38);
- distributed relationship record semantics (#39);
- replacement, challenge, correction, remediation, revocation and closure lifecycle (#40);
- human-verifiable Relationship Views (#41);
- adversarial RAHP assurance (#42);
- standards-native substitution (#43).

## Human acceptance boundary

Green CI may satisfy the bounded Phase 5 executable proposition only after human review and merge. It does not promote `IC-ARA-REL-001` to the authoritative catalog.

The judgment to preserve is:

> The ARA walking skeleton is defensible only if the cryptographic side effect is no easier to exercise than the authorization decision it is supposed to embody.
