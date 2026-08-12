# Scenario 05 — Multi-agent sub-delegation

## Purpose

Test principal continuity and scope attenuation when Agent A invokes Agent B or a specialized tool-agent.

## Flow

1. Principal P delegates `verify.provenance` and `verify.registry` to Agent A with sub-delegation permitted only for `verify.provenance`.
2. Agent A delegates `verify.provenance` to Agent B.
3. Agent B returns provenance findings to Agent A.
4. Agent A performs registry verification itself and assembles the evidence bundle.

## Expected boundary

The resulting evidence must retain P → A → B delegation lineage. B cannot acquire `verify.registry` or downstream decision authority through the sub-delegation.

## Negative probe

Agent B attempts a registry mutation or consequential decision using Agent A's broader capabilities. The action must be denied because effective sub-delegated scope is narrower.
