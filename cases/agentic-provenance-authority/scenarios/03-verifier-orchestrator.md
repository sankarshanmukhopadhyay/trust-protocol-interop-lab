# Scenario 03 — Agentic verifier and orchestrator

## Purpose

Test an agent that orchestrates provenance checks, trust-registry queries, and policy evaluation.

## Flow

1. A relying party delegates a bounded `verify` task to an agent.
2. The agent verifies content provenance, resolves registry state, and assembles structured findings.
3. Findings distinguish identity, delegation, provenance, freshness, and policy inputs.
4. The agent returns verification evidence and an explicit confidence/indeterminacy state.
5. A separate decision authority decides whether a consequential effect is allowed.

## Expected boundary

The verifier-agent may state that verification checks passed. It may not silently turn `provenance_valid=true` into `claim_true=true`, or `authority_valid=true` into `approve_effect=true`, unless a separately evidenced decision mandate exists.

## Negative probe

The verifier is authorized only for verification but issues an approval/payment/certification command. The effect must be denied for absent decision authority.
