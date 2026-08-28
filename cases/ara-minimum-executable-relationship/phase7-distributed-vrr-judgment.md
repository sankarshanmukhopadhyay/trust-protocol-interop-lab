# IC-ARA-REL-001 Phase 7 — visible distributed-VRR judgment

Issue: #39  
Parent: #32  
Depends on completed independent-counterparty phase: #38

## Proposition under test

Can two independently controlled parties prove the externally meaningful relationship intersection without collapsing their private Role Records into a jointly writable master dossier?

## Alternatives genuinely considered

### One shared relationship database

Rejected. A master database obscures provenance and control boundaries, makes one storage state appear authoritative by construction, and risks turning private local evidence into collectively visible state.

### Treat everything exchanged as shared relationship knowledge

Rejected. Copy, delivery, resolution, decryption, inspection, acknowledgement, semantic acceptance, and evidentiary acceptance are different claims.

### Treat pointers and commitments as equivalent to disclosed content

Rejected. A pointer does not authorize traversal or prove inspection. A commitment proves binding to hidden content without proving that the counterparty knew that content.

### Cross-anchored evidence intersection over independent Role Records

Selected. Each Role remains locally controlled. Relationship evidence is reconstructed from canonical objects, attributable receipts, semantic dispositions, immutable disagreement/correction history, and checkpoints anchored to each party's current Role Record head.

## Core judgment

> Shared relationship state is not whatever either party stores locally or whatever bytes crossed transport. It is the subset whose exact evidence class, handling stage, attribution, and semantic disposition can be proved.

The implementation preserves:

```text
sent != delivered
delivered != inspected
decrypted != accepted
inspected != accepted
one-party annotation != mutual state
pointer != traversal authority
commitment != knowledge of hidden content
private evidence != shared relationship state
correction != historical erasure
```

## Falsification evidence

The executable suite pressures:

- false inspection claims for a different digest;
- delivery/copy being confused with inspection;
- decryption being confused with acceptance;
- unilateral annotation being presented as mutual;
- dispute being silently converted into agreement;
- corrections erasing earlier disagreement;
- private evidence leaking into shared export;
- opaque commitment being treated as disclosed knowledge;
- relationship pointer being treated as traversal authority;
- checkpoint formation with a missing party head.

## Claim boundary

The checkpoint is evidence composition, not distributed consensus. No normative VRC/RCard/VRR format, CRDT, blockchain, replicated database, or authoritative collective-state protocol is claimed.

## Residual uncertainty

Deferred intentionally:

- lifecycle replacement, challenge, correction, remediation, revocation, continuation and closure (#40);
- human-verifiable Relationship Views (#41);
- adversarial RAHP assurance and false-independence pressure (#42);
- standards-native substitution (#43).

## Human acceptance boundary

Green CI can satisfy only the bounded proposition that the Lab can reconstruct shared relationship evidence from independent state while preserving private/shared, receipt/disposition, disagreement, commitment, and pointer boundaries.

The overall ARA case remains pre-admission.

The judgment to preserve is:

> The relationship record is an evidence intersection, not a master dossier and not an inference that whatever one party knows, the other party knows too.
