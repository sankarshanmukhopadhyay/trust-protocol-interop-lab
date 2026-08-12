# Scenario 04 — Revocation between creation and reliance

## Purpose

Test the distinction between historical authority and current reliance.

## Flow

1. At `T1`, an agent has valid authority and produces provenance-bearing content.
2. At `T2`, the delegation is revoked.
3. At `T3`, a relying party verifies the artifact and asks both what was authoritative at `T1` and whether current authority exists at `T3`.

## Expected boundary

The system may truthfully report `authorized_at_T1=true` and `current_authority=false`. It must not rewrite historical state because the agent is now revoked, nor infer that historical validity authorizes a new action at `T3`.

## Negative probe

A verifier replaces requested-time state with current state and reports that the action was unauthorized at `T1` solely because the mandate is revoked at `T3`. This is historical-state collapse.
