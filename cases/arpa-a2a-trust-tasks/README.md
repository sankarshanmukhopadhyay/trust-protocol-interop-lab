# IC-ARPA-A2A-TT-001 — Governed agent discovery to Trust Task execution

**Status:** `interoperability-tested`  
**Admitted claim:** bounded executed semantic composition of ARPA v0.9.5, ANAB v0.10.0 assurance inputs, A2A v1.0 interaction metadata, and Trust Tasks.  
**Evidence scope:** local semantic evaluator only; excludes live-network interoperability, cryptographic interoperability, upstream conformance, certification, or any claim that attribution metadata creates authority.

## Question

Can ARPA authority state, ANAB name/operator assurance, A2A discovery and interaction metadata, and Trust Task work semantics compose without treating identity, assurance, registry state, or reported actor lineage as delegated authority—and without losing revocation, scope, or evidence boundaries before a consequential effect?

## Composition boundary

The case keeps four control surfaces independently evaluable:

- **ARPA** — registry and authority state, including current scope and revocation state;
- **ANAB** — integrity-bound name/operator assurance inputs;
- **A2A** — discovery, interaction, and attribution metadata;
- **Trust Tasks** — semantics of the requested work and the pre-effect authorization checkpoint.

The governing invariant is that discovery, name assurance, identity/proof validation, actor-chain attribution, authority, task semantics, and effect admission are related but non-substitutable. A successful check in one layer cannot enlarge authority owned by another.

A2A issue #2028 is treated as an informative pressure-test input only. A syntactically consistent actor chain can still contain fabricated grants, scope escalation, stale authority, or rewritten history.

## Admitted claim

The executed reference model demonstrates that the declared composition can fail closed when name assurance, authority, scope, revocation, or task/effect conditions are invalid. It also demonstrates that attribution lineage can be evaluated separately from independently resolved authority evidence.

`Interoperability Tested` here means **bounded semantic composition in this repository-owned evaluator**. It does not establish production protocol interoperability or confer normative status on case-local actor-chain fields.

## Scenarios and vectors

The deterministic evidence package currently records **7/7 passing vectors**, including:

- governed execution;
- ANAB name mismatch;
- revoked ANAB assurance;
- stale ANAB assurance;
- unbound ANAB evidence;
- revoked authority;
- scope expansion.

The actor-chain extension adds pressure tests for fabricated-but-monotone lineage, scope escalation, prior-hop mutation, evidence-state separation, cross-context replay, and privacy-minimized lineage.

Browse the [scenario set](scenarios/) and [vectors](vectors/). The actor-chain/authority separation is documented in [the mapping](../../mappings/a2a-actor-chain-authority.md).

## Evidence

The evidence package is hash-bound in [`evidence/arpa-a2a-anab/evidence-manifest.json`](../../evidence/arpa-a2a-anab/evidence-manifest.json). It records the executed result, run log, test vectors, invariant set, semantic-ownership model, known limitations, and reference evaluator with SHA-256 hashes.

The manifest's admitted claim scope explicitly excludes live-network, cryptographic, upstream-conformance, and certification claims.

## Reproduce

From the repository root:

```bash
python3 experiments/arpa-a2a-anab/run.py
```

Inspect the resulting evidence under [`evidence/arpa-a2a-anab/`](../../evidence/arpa-a2a-anab/), especially the manifest, `result.json`, and `run-log.json`.

A green exit code is not sufficient on its own: compare the result against [`ownership.yaml`](ownership.yaml), [`invariants.yaml`](invariants.yaml), the vectors, and the limitations before relying on the local maturity claim.

## Limitations

The authoritative limitation set is [`known-limitations.md`](known-limitations.md). Material boundaries include:

- A2A issue #2028 remains an open proposal and may change;
- `actorChain`, `proof_ref`, `credentialRef`, and `originAnchor` are not claimed as normative A2A v1.0 fields;
- payload-level monotonic narrowing cannot prove that an underlying grant actually existed;
- the lab does not standardize a universal delegation credential;
- no single privacy-preserving lineage construction is selected;
- ANAB retrieval, digest, key, signature, and revocation checks are modeled semantically rather than through live network/cryptographic execution.

## Upstream / next disposition

The immediate upstream pressure point is A2A issue #2028: actor-chain attribution should remain distinguishable from independently resolved authority and effect admission. The lab should not promote the proposal into adopted A2A semantics unless and until upstream does so.

The next evidence boundary is therefore not more local metadata. It is stronger substitution/equivalence evidence: live authority/evidence resolution, cryptographic verification, and—if upstream actor-chain semantics stabilize—an updated pressure test pinned to the adopted specification text.
