# Scenario 01 — Authorized agent content production

## Purpose

Test an AI agent producing or transforming media under a bounded principal mandate.

## Flow

1. ANAB-compatible evidence identifies the named agent at the required assurance tier.
2. ARPA authority state binds the agent to a principal and permits `content.transform` for a specified asset set and purpose.
3. The agent transforms the asset and emits CAWG/C2PA-compatible provenance.
4. A verifier checks provenance and current delegation state.
5. TIS-compatible evidence binds the authority and provenance checks into a portable bundle.
6. Local policy decides whether publication is permitted.

## Expected boundary

Successful provenance proves the recorded provenance assertions were verifiable. It does not prove that the transformed content is truthful or that publication is permitted. Publication authority must be independently established.

## Negative probe

The agent has authority to enhance lighting but removes structural damage. The resulting action is outside transformation scope and must not be admitted merely because provenance is valid.
