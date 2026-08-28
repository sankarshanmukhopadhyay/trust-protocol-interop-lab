# IC-ARA-REL-001 Phase 6 — visible independent-counterparty judgment

Issue: #38  
Parent: #32  
Depends on completed protected-signing phase: #37

## Proposition under test

Can a receiving Agent Role verify and independently admit a relationship action using only transported attributable artifacts and its own relationship/policy state, without trusting sender-private reasoning or adopting the sender's authorization conclusion?

## Alternatives genuinely considered

### Keep both Roles in one process and pass Python objects

Rejected. That would preserve hidden shared memory and make it impossible to distinguish protocol evidence from implementation convenience.

### Put both Roles behind one shared policy/state service

Rejected. This would demonstrate orchestration, not independent control. A counterparty could appear independent while silently inheriting sender-local conclusions.

### Serialize the sender's final `allow` result and let the receiver honor it

Rejected. Sender authorization is evidence of what the sender decided, not authority for the receiver. Receiver policy and relationship state may legitimately differ.

### Separate sender and receiver processes with serialized wire evidence and receiver-local state

Selected. The sender constructs the Phase 3–5 evidence chain, serializes the bounded relationship action, and terminates its control at the transport boundary. The receiver independently validates the artifact using only wire evidence plus its own state/configuration.

## Core judgment

> A counterparty must be able to reject a sender-authorized action for its own defensible reasons. Sender-local authorization, transport delivery, and signature validity are evidence inputs, not receiver acceptance.

The executable boundary therefore preserves:

```text
sender allow
!= receiver allow

transport success
!= relationship recognition
!= evidence sufficiency
!= receiver policy acceptance
!= execution admission
```

## Required falsification

The receiver must safely distinguish:

- sender allow / receiver deny;
- signature evidence / inactive authority;
- sender historical head / receiver-current inconsistent state;
- intended recipient / substituted recipient;
- first delivery / replay;
- complete evidence / unresolved required evidence;
- sender agreement / receiver-known different agreement;
- successful transport / receiver-disallowed task;
- valid wire shape / invalid cryptographic evidence.

## Claim boundary

The selected process boundary is real but local: separate subprocesses and serialized files. The transport adapter is intentionally replaceable.

The inherited HMAC mechanism is still only a Lab verification stand-in. Phase 6 does not establish TSP conformance, public-key sender identity/control, remote attestation, secure transport, non-repudiation, hardware key protection, or distributed VRR semantics.

## Residual uncertainty

Still deliberately deferred:

- distributed/shared Verifiable Relationship Record semantics (#39);
- lifecycle replacement, challenge, remediation, continuation and closure (#40);
- human-verifiable Relationship Views (#41);
- adversarial RAHP pressure review (#42);
- standards-native TSP/VTA/RCard/VRC substitution (#43).

## Human acceptance boundary

Green CI can satisfy only the bounded claim that two independent local processes can exchange a complete serialized ARA action and the receiver can reach its own accept/deny/indeterminate result without consuming sender-private state.

It does not yet prove distributed relationship consensus or admit the overall case.

The judgment to preserve is:

> Independent control becomes meaningful only when disagreement is executable: the receiver can verify the sender's evidence, reject the sender's conclusion, and record why.
