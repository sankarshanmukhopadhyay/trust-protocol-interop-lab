# DTG VAC attenuation — experimental evidence

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Test whether a child or derived authority credential can only narrow its parent and whether every link remains current at use time.
- **Current conclusion:** Every tested widening, stale-state, incomplete-chain, and revoked-authority condition is rejected.
- **Source basis:** proposed VAC rules in `trustoverip/dtgwg-cred-spec#29` at `84650749afd48798e1c8919a95be359c0367a1c9`.

## Why this matters
Derived authority creates an escalation risk. A child credential can remain cryptographically valid while being broader than the authority from which it was derived or while an upstream authority link has been revoked.

## Composition in plain language
The child VAC is compared with its parent across action set, governed scope, expiry, audience, chain depth and completeness, current root and intermediate state, and freshness. It is acceptable only if it is an attenuation, never an expansion.

## Concrete scenario
A parent permits `read` on one resource until Friday. A child may narrow that scope or duration. It must not add `write`, broaden scope, expire later, change audience, skip links, exceed depth, survive revocation, or rely on stale state.

## What was tested
One positive narrowed child and nine negative cases were executed. All expected outcomes match.

Run:
```bash
python experiments/dtg-vac-attenuation/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-vac-attenuation/run-results.json).

## Where it resolved
> **Derived authority must be monotonically narrower than its parent, and cryptographic validity must not substitute for current authority state.**

## What this status means
This is executable semantic evidence against a proposed upstream VAC model, not ratified DTG behavior or production cryptographic interoperability.

## What remains unresolved
Final upstream VAC semantics, production chain verification, authoritative revocation infrastructure, and cross-implementation evidence remain outside the claim.
