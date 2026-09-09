# Portable evidence producer migration

The current OpenVTC Data Room runtime experiment is the first Interop Lab producer used to pressure-test RAHP's `rahp-evidence-producer-result/v1` boundary.

The existing `interop-evidence-package/v1` result remains authoritative for the current workflow while migration is characterized. The adapter preserves proposition observations and the source pin while making the ownership boundary explicit:

- the Lab owns target-specific execution and raw/bounded observations;
- a specialist such as DPIP owns domain-specific interpretation;
- RAHP owns generic provenance/freshness validation and terminal reconciliation.

The portable envelope explicitly does not support terminal assurance PASS or deployment-wide inference. Migration must not retire the legacy result until a real workflow artifact is emitted with non-placeholder obligation keys, execution identity/time, producer revision and artifact digest and is validated by RAHP.

This tranche is therefore an adapter/characterization step, not a claim that the producer migration is complete.
