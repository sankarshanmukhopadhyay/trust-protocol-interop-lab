# ARA Phase 4 — Agreement, Policy Gate, Trust Task, Capability, Execution

This experiment is executable evidence for `IC-ARA-REL-001` issue #36.

It tests the proposition that a consequential relationship operation is admitted only when **all** of the relevant evidence and state align: authenticated identity, active and in-scope authority, exact active Agreement Object, current Role Record head, relationship state, deterministic instance policy, exact Trust Task identifier/version, least-privilege capability, freshness, recipient, purpose, resource, action, and effect-correlation requirements.

## Run

```bash
python experiments/ara-policy-spine/run.py --check
```

Optional evidence file:

```bash
python experiments/ara-policy-spine/run.py --output /tmp/ara-phase4.json
```

The CI `Repository assurance` workflow executes the `--check` form.

## Components

`authorization.py` implements five deliberately separate Lab-local boundaries:

1. **AgreementLedger** — immutable agreement terms plus append-only proposal/acceptance/activation/suspension/closure events.
2. **PolicyGate** — deterministic `allow`, `deny`, `escalate`, or `indeterminate` decision over explicit evidence inputs.
3. **CapabilityService** — technical capability minted only after `allow`, bound to exact relationship/agreement/recipient/purpose/resource/action/expiry, with attenuation/suspension/revocation.
4. **TrustTaskBuilder** — exact task binding to relationship, agreement, Role Record head, authority, decision, capability, recipient, purpose, payload digest, nonce, timestamps, expiry, and evidence requirements.
5. **ExecutionAdmitter** — independent final admission that rechecks decision, capability, authority, agreement, task version, current Role Record head, freshness, replay, and exact scope before emitting a process/effect receipt.

The experiment imports the Phase 3 Role Record engine and binds policy to its current head. This means Phase 4 is built on the previously evidenced persistent-state boundary rather than recreating a second state model.

## Non-implication rules made executable

The vector suite demonstrates at least:

- identity != authority;
- valid authority/delegation != policy authorization;
- accepted agreement != active agreement;
- active agreement != capability;
- capability != current legitimate authority;
- capability for one agreement != capability for another;
- valid task shape/version mismatch != admitted action;
- evidence insufficiency != PASS;
- successful-looking effect != attributable admitted effect;
- assurance != retroactive authorization;
- historical/stale Role Record head != current defensible head.

## Decision vocabulary

The Policy Gate has a closed vocabulary:

- `allow` — all required conditions evaluated by the bounded gate are satisfied;
- `deny` — sufficient evidence exists to determine the requested operation is not permitted;
- `escalate` — policy requires an external/human decision before proceeding;
- `indeterminate` — required evidence is missing, so the implementation refuses to invent a PASS.

No later stage may reinterpret `deny`, `escalate`, or `indeterminate` as an `allow` merely because a signature, capability-shaped object, execution effect, or assurance result exists.

## Evidence and refusal codes

The runner emits deterministic JSON with per-vector expected/observed codes and the decision/execution artifacts used as evidence. Negative cases have distinct codes, including:

- `authority_inactive_or_missing`
- `authority_purpose_out_of_scope`
- `agreement_not_active`
- `capability_missing`
- `authority_revoked_or_inactive`
- `capability_wrong_agreement`
- `unsupported_task_version`
- `instance_policy_denied`
- `missing_required_evidence`
- `effect_not_correlated_to_admission`
- `capability_requires_allow_decision`
- `attenuation_cannot_expand_expiry`
- `capability_not_active`
- `capability_expired`
- `stale_role_record_head`

## Claim boundary

This is a **Lab-local executable composition**, not a claim of:

- normative ARA Agreement Object semantics;
- a registered ARA Trust Task profile;
- TSP or TEA wire conformance;
- OpenVTC VTA protected-signing conformance;
- ARPA authority conformance for this exact execution path;
- production capability-security guarantees;
- jurisdiction-specific authority or fiduciary validity;
- production policy-engine security;
- external certification.

The point of this phase is narrower: preserve and falsify the ARA authorization distinctions before the protected-signing and independent-counterparty phases add more infrastructure.
