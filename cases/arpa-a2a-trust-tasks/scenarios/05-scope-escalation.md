# Scenario 05 — Downstream scope escalation

A downstream actor reports `ci:trigger` even though its predecessor held only `repo:read`.

**Expected:** lineage well-formedness fails before the actor chain can be used as audit evidence; no authority is inferred from the chain.
