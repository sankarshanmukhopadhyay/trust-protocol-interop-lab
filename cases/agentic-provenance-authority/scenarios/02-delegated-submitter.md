# Scenario 02 — Delegated agent submission

## Purpose

Test an agent submitting authentic evidence on behalf of a principal.

## Flow

1. The principal delegates `evidence.submit` for a named proceeding/resource and validity window.
2. The agent packages provenance-bearing evidence and submits it through an interaction protocol.
3. The receiver resolves agent identity and authority state.
4. TRQP/registry verification establishes relevant trust state.
5. The receiving institution records a decision receipt separately from the submitted evidence.

## Expected boundary

Authentic evidence submitted by an authenticated agent is not automatically an authorized submission. The action, resource, recipient/purpose, and temporal scope must be satisfied.

## Negative probe

A valid agent submits the same evidence to a proceeding not included in the delegation. The system must reject or route to review rather than broaden scope.
