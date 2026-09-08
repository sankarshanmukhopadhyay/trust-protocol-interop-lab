# DTG VDC × VAC composition — experimental evidence

## At a glance
- **Status:** Pre-admission experimental evidence against adopted Credential Spec WD02 semantics.
- **Purpose:** Test the separation between **representation/delegation (VDC)** and **authority (VAC)**.
- **Current conclusion:** Appointment to act for a principal and the principal's current authority are independent predicates; both must hold.
- **WD02 pin:** `trustoverip/dtgwg-cred-spec@67149716032318f7f29770e5d3e6f0d35e52b8c3`.
- **Component merge pins:** VDC #19 → `37074bdcd861c51f3e5b7868ce700832b17b73ce`; VAC #29 → `4f7e66b6dfcd8eddc212c8002351a6ad814c60e1`.

## Why this matters
"May act for someone" and "that someone is allowed to perform this action" are different governance statements. Collapsing them lets delegation create authority the principal never had, or lets authority imply an appointment that never existed.

## Composition in plain language
**VDC** is the adopted representation/delegation artifact. **VAC** is the adopted authority artifact. The decision additionally preserves any independent delegate-eligibility requirement and exact task/invocation binding.

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

The semantic non-substitution and current-authority vectors remain valid against the adopted WD02 source pin.

## What this status means
The experiment is deliberately pre-admission composition evidence. It pressure-tests adopted specification semantics but is not production implementation or deployment assurance.

## What remains unresolved
Production cryptographic interoperability, target-implementation lifecycle behavior, and future upstream changes remain outside the claim.
