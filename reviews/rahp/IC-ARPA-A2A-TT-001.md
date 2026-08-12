# RAHP pressure test — IC-ARPA-A2A-TT-001

## Affected parties

Principals delegating to agents, relying parties admitting actions, operators publishing Agent Cards or registry state, and people affected by consequential automated actions.

## Priority harms

1. **Authority laundering through discovery:** an advertised capability is mistaken for delegated authority.
2. **Stale-authority execution:** revocation or suspension is not observed before a consequential action.
3. **Scope expansion:** an agent executes outside attenuated delegation because transport/execution accepts a broader capability.
4. **Evidence discontinuity:** a later reviewer cannot connect the action to the authority and Trust Task that justified it.

## Test implications

The case therefore includes negative vectors for revoked authority and scope expansion, requires explicit local authorization, and targets portable result evidence linking authority, task, action, and outcome.
