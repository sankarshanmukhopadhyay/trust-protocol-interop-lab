# Agentic provenance and authority semantic mapping

This mapping supports `IC-AGENT-PROVENANCE-AUTH-001`. It is an interoperability artifact, not a normative amendment to any referenced specification.

| Concern | Semantic owner in this composition | Must not be inferred from |
|---|---|---|
| Governance/authority/accountability meaning | GAAM | transport success or content provenance |
| Trust-system entity, delegation, decision, effect grammar | TSMM | local field names alone |
| Portable authority/evidence/decision artifacts | TIS | narrative documentation alone |
| Named-agent identity strength | ANAB | capability advertisement or registry presence |
| Agent authority, delegation, lifecycle, historical state | ARPA | Agent Card/capability metadata |
| Discovery and interaction | A2A | authorization or institutional acceptance |
| Content provenance/authenticity assertions | CAWG/C2PA | truth, legality, safety, admissibility, or decision authority |
| Read-only trust-registry query result | TRQP | authority to mutate a registry or authorize an effect |
| Evidence sufficiency evaluation | DCAS | creation of missing source authority |
| Consequential decision | Local relying-party/institutional policy | verifier success alone |
| Operational effect | Application/institutional control plane | decision receipt without effect evidence |
| Risk/harm analysis | RAHP review used by the lab | protocol conformance alone |

## Canonical separation

```text
identity evidence
  + delegation evidence
  + provenance evidence
  + registry verification
  + policy context
      ↓
structured verification finding
      ↓
separately authorized decision
      ↓
separately evidenced effect
```

### Prohibited semantic collapses

1. `agent_identity_valid` → `delegation_valid`
2. `capability_advertised` → `action_authorized`
3. `provenance_valid` → `claim_true`
4. `TRQP_query_success` → `decision_authorized`
5. `verification_pass` → `effect_permitted`
6. `historically_authorized` → `currently_authorized`
7. `decision_allow` → `effect_occurred`
8. `assurance_evaluation_pass` → `independent certification`

## Evidence handoff

The composition should produce references sufficient to bind:

- acting agent identifier and identity-assurance evidence;
- originating principal;
- delegation chain and effective scope;
- lifecycle/revocation state and freshness;
- provenance object/manifest and verification result;
- TRQP query inputs, selected state, and result;
- policy or decision-authority reference;
- final decision receipt;
- effect evidence where an effect occurs;
- replay, correction/supersession, and redress references.
