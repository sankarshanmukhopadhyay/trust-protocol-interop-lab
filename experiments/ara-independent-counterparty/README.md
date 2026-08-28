# ARA Phase 6 — independent counterparty verification

This experiment is executable evidence for `IC-ARA-REL-001` issue #38.

It moves the ARA walking skeleton across a real runtime boundary. `sender.py` and `receiver.py` execute as separate Python processes. Their only relationship-action exchange is a serialized JSON wire artifact.

## Proposition

Can the receiving Agent Role decide independently using transported evidence plus its own relationship/policy state, without trusting the sender's private model reasoning or treating the sender's `allow` decision as the receiver's authorization?

## Run

```bash
python experiments/ara-independent-counterparty/run.py --check
```

## Independence boundary

The receiver has its own configuration for:

- expected sender Role;
- receiver Role;
- relationship identifier;
- currently accepted sender Role Record head;
- exact Agreement reference;
- allowed purpose/resource/action;
- receiver-local instance policy;
- receiver-local replay state.

The receiver receives sender decision/admission receipts for correlation and attribution, but it independently checks relationship state, agreement, authority, task scope/version, recipient, freshness, replay, cryptographic-use evidence, signature, and its own policy.

## Falsification

The executable suite covers:

- sender says allow while receiver policy denies;
- invalid/revoked sender authority despite transported sender evidence;
- stale sender relationship state;
- recipient/context substitution;
- replayed serialized request;
- missing required evidence => `indeterminate`;
- materially inconsistent receiver relationship/agreement state;
- transport success with receiver task-policy denial;
- invalid signature.

## Claim boundary

The file transport is deliberately a replaceable Lab adapter. HMAC verification is a local stand-in inherited from Phase 5. This proves a process and independent-verification boundary only; it does not claim TSP, public-key identity/control proof, VTA, remote attestation, confidential transport, or production counterparty security.
