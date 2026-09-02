# DTG VDC × VAC composition — experimental evidence

This pre-admission case supports RAHP Discussion #371 and RAHP issue #374. It pressure-tests the proposed separation between **delegation/representation** (VDC) and **authority** (VAC) without representing either proposal as adopted DTG semantics.

## Source pins

- VDC: `trustoverip/dtgwg-cred-spec#19` @ `ad5876f1b96e2149adec84d37d6595b4a212db9c` — `proposed-upstream`.
- VAC: `trustoverip/dtgwg-cred-spec#29` @ `84650749afd48798e1c8919a95be359c0367a1c9` — `proposed-upstream`.
- RAHP proposition matrix: `DTG-371-P06`, `P07`, `P09`, `P14`.

## Working boundary

The evaluator treats four facts independently:

1. **delegation valid** — the actor is appointed to act in the principal's name for the requested action;
2. **principal authority current** — the represented principal is currently allowed to perform the requested action;
3. **delegate eligibility satisfied** — any independently required governance condition on the delegate holds;
4. **task/invocation binding valid** — the presented appointment and authority evidence are bound to the requested action/context.

The operation is admitted only when every required fact is true. In particular:

- VDC does not create authority;
- VAC does not create representation;
- revocation or withdrawal of either relevant current state fails closed;
- component validity does not by itself create an actuation PASS.

This is a semantic composition experiment. It does not claim production cryptographic interoperability, final credential schemas, or ratified DTG behavior.

## Vectors

The scenario includes a positive control and the seven pressure cases required by RAHP #374: missing principal authority, missing delegation, narrower delegate authority, principal-authority withdrawal, VDC revocation, delegate-eligibility failure, and task/invocation mismatch.

Run:

```bash
python experiments/dtg-vdc-vac-composition/run.py --check
```

The committed result is deterministic and exists to establish the semantic non-substitution boundary ahead of upstream ratification. Any material change to PR #19 or #29 makes this evidence stale and requires a rerun against new immutable pins.
