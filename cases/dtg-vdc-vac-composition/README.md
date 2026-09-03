# DTG VDC × VAC composition — experimental evidence

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Test the proposed separation between **representation/delegation (VDC)** and **authority (VAC)**.
- **Current conclusion:** Appointment to act for a principal and the principal's current authority are independent predicates; both must hold.
- **Source pins:** VDC PR #19 @ `ad5876f1b96e2149adec84d37d6595b4a212db9c`; VAC PR #29 @ `84650749afd48798e1c8919a95be359c0367a1c9`.

## Why this matters
"May act for someone" and "that someone is allowed to perform this action" are different governance statements. Collapsing them lets delegation create authority the principal never had, or lets authority imply an appointment that never existed.

## Composition in plain language
**VDC** is treated as the proposed representation/delegation artifact. **VAC** is treated as the proposed authority artifact. The decision additionally preserves any independent delegate-eligibility requirement and exact task/invocation binding.

```text
valid representation
AND current principal authority
AND required delegate eligibility
AND exact invocation binding
= eligible represented action
```

## Concrete scenario
A company is authorized to read a governed record and appoints an employee to act for it. The request is rejected if appointment is absent, revoked, or narrower; principal authority is withdrawn; delegate eligibility fails; or the evidence is bound to another task.

## What was tested
One positive control and seven negative cases were executed: missing authority, missing delegation, narrower delegation, authority withdrawal, VDC revocation, delegate-eligibility failure, and invocation mismatch.

Run:
```bash
python experiments/dtg-vdc-vac-composition/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-vdc-vac-composition/run-results.json).

## Where it resolved
```text
delegation/representation != authority
authority != delegation/representation
component validity != actuation permission
```

## What this status means
The experiment is deliberately pre-admission and does not represent VDC or VAC proposals as adopted DTG behavior.

## What remains unresolved
Final schemas, production cryptographic interoperability, authoritative lifecycle resolution, and future upstream changes remain outside the claim.
