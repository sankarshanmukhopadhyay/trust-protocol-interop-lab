# ARA Phase 5 — protected signing and cryptographic-use receipts

This experiment is executable evidence for `IC-ARA-REL-001` issue #37.

## Proposition

Can cryptographic use occur only through an authenticated deterministic Workflow for the exact Agent Role, current Role Record head, Trust Task, relationship, Agreement Object, authority decision, capability, recipient, purpose, payload, freshness window, signing identity, and already-admitted Phase 4 execution context?

The experiment deliberately treats signing as a **consequential actuator**, not as proof that authorization existed.

## Run

```bash
python experiments/ara-protected-signing/run.py --check
```

## Boundary

`ProtectedSigner` exposes one context-bound `use(...)` operation and no unrestricted `sign(bytes)` API. The request is derived from the Phase 4 task, decision, capability, authority, and admission receipt. Every accepted or refused attempt emits a deterministic cryptographic-use receipt.

The local HMAC operation is only an executable stand-in for protected key use. This phase does **not** claim OpenVTC VTA, HSM, TEE, DID, TSP, VID, hardware isolation, non-exportability, remote attestation, or production key-management conformance.

## Required bindings

Accepted use binds:

- persistent Agent Role;
- current Role Record head;
- authenticated Workflow identifier/version;
- exact Trust Task identifier/version and instance;
- relationship and exact Agreement Object;
- authority and authorization decision;
- capability;
- Phase 4 admission receipt;
- recipient and purpose;
- payload digest;
- nonce;
- expiry;
- requested signing identity;
- expected cryptographic-use receipt class.

## Falsification suite

The runner executes the positive path plus denial vectors for direct Live Agent access, arbitrary bytes, unauthenticated/replaced Workflow, stale task version, recipient/payload substitution, wrong relationship/agreement, stale Role Record head, expired/revoked authority, replay, suspension/closure, and missing decision/admission evidence.

The claim being tested is therefore stronger than “the key produced a valid MAC”:

> possession or reachability of cryptographic key material is insufficient; the cryptographic-use boundary must independently re-check the exact admitted relationship context before exercising technical power.
