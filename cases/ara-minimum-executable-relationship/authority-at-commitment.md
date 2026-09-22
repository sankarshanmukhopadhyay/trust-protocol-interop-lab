# Authority at Material Commitment — IC-ARA-REL-001 extension

This tranche extends the existing Minimum Executable Agent Relationship case without changing its admitted claim. The existing case already requires current authority for a consequential bounded action; this fixture sharpens that proposition at the **exact material commitment** boundary.

## Proposition

An authenticated actor or valid signature does not establish that the actor had authority for the exact action another party is asked to rely upon. The action is admitted only when current authority, scope constraints and any required exact-action approval concur.

## Executable outcomes

The fixture intentionally distinguishes:

- `permit` — current active authority, exact action binding, scope satisfied, approval satisfied when required;
- `deny` — revoked/expired/suspended authority, scope violation, wrong-action approval, or stale approval;
- `indeterminate` — authority state cannot be established, exact action binding is absent, or a required approval has not yet arrived.

The fixture does not implement a negotiation protocol. Runtime admission, transport, settlement and reputation remain separate concerns.

## Run

```bash
python experiments/ara-authority-at-commitment/run.py --check
```

To produce inspectable evidence:

```bash
python experiments/ara-authority-at-commitment/run.py \
  --output evidence/ara-minimum-executable-relationship/authority-at-commitment-results.json
```

## Claim boundary

This is deterministic Lab evidence for the modeled authority decision boundary. It is not legal advice, a claim of contractual enforceability, A2A conformance, ARPA certification, production authorization assurance or evidence that a particular cryptographic mandate format is universally sufficient.
