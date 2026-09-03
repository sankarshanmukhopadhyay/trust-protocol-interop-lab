# DTG cross-governance action vocabulary — experimental evidence

## At a glance
- **Status:** Pre-admission experimental evidence
- **Purpose:** Test whether the same action word used in two governance domains can be treated as equivalent authority.
- **Current conclusion:** No. Lexical equality is not semantic authority; cross-domain reliance requires an explicit governance/profile mapping.
- **Source basis:** proposed VAC work in `trustoverip/dtgwg-cred-spec#29` pinned at `84650749afd48798e1c8919a95be359c0367a1c9`.

## Why this matters
Words such as `read`, `write`, or `admin` look universal but are governance-local. A verifier that accepts an action because the token text matches can silently widen authority across domains.

## Composition in plain language
The proposed **VAC (Verifiable Authority Credential)** carries an action meaning in the issuer's governance context. The verifier has its own operation vocabulary. The bridge between them must be an explicit mapping artifact; the token alone is insufficient.

## Concrete scenario
An issuer presents `write`; a verifier needs `write-object`. The evaluator accepts only when an explicit mapping binds those meanings. It rejects same-token reliance without a mapping, implicit `admin -> write` hierarchy, and unrelated foreign actions.

## What was tested
The deterministic evaluator executes six positive/negative vectors. All expected outcomes match.

Run:
```bash
python experiments/dtg-action-vocabulary/run.py --check
```

Inspect [scenario.yaml](scenario.yaml) and [run-results.json](../../results/dtg-action-vocabulary/run-results.json).

## Where it resolved
> **Cross-governance action semantics require an explicit mapping artifact; token equality does not create authority.**

The experiment intentionally does not select the eventual federation/profile mechanism.

## What this status means
This is not an admitted catalog case and does not represent ratified DTG behavior. It pressure-tests proposed upstream semantics.

## What remains unresolved
The normative mapping/federation mechanism remains open. A material upstream VAC change makes this evidence stale and requires re-evaluation.
