# Scenario 04 — Fabricated but monotone actor lineage

A caller supplies a syntactically correct actor chain in which every downstream scope is a subset of its predecessor, but no independently resolvable grant evidence exists.

**Expected:** lineage well-formedness passes; authority remains indeterminate/denied according to relying policy; consequential effect admission fails closed.
