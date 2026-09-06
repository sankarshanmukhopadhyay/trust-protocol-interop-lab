# Current OpenVTC Track A runbook

CI performs the complete producer run:

1. check out this repository;
2. check out the immutable current OpenVTC revision;
3. verify its SHA and clean state;
4. execute the seeded positive control;
5. execute the context-distinct pressure case;
6. assert requirement classifications and producer boundaries;
7. verify the upstream checkout is clean;
8. export DPIP `provided_evidence` bindings;
9. upload the source-pinned evidence package.

No manual editing of generated evidence is part of the run.
