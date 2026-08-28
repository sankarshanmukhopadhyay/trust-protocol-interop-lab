# ARA Phase 7 — distributed Verifiable Relationship Record semantics

This experiment is executable evidence for `IC-ARA-REL-001` issue #39.

## Proposition

Can independently controlled parties preserve local Role Records while later proving the exact relationship-bearing objects, receipts, dispositions, disagreements, and corrections that constitute the defensible shared relationship intersection?

## Model

The experiment keeps four evidence classes distinct:

- `shared_object`: exact content is relationship-shareable;
- `source_pointer`: attributable pointer without automatic disclosure or traversal;
- `opaque_commitment`: commitment exists but hidden content is not collectively known;
- `private_role_evidence`: local evidence that is explicitly excluded from shared exports/checkpoints.

It also separates procedural receipt stages from semantic dispositions. Delivery, resolution, decryption and inspection never automatically mean acceptance.

## Checkpoint

A relationship checkpoint compactly cross-anchors:

- persistent relationship identifier;
- party-set epoch;
- both independent Role Record heads;
- shared object references;
- receipt references;
- disposition references;
- correction references.

It is a summary of evidence, not a jointly writable master record.

## Run

```bash
python experiments/ara-distributed-vrr/run.py --check
```

## Claim boundary

This is a Lab-local semantic/executable model. It does not claim normative VRC, RCard, VRR, ToIP, consensus, replicated-log, CRDT, distributed-ledger, or production storage conformance.
