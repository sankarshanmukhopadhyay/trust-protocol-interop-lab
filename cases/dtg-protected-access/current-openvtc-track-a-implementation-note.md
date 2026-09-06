# Current adapter design note

The current adapter deliberately does not refactor or rename the Dogwood adapter. Historical producer code remains readable as historical code, while the new adapter has its own current-target revision constant and checkout path.

The adapter uses the target repository's E2E crate and existing test responder support. It temporarily adds a test-only probe to the checked-out target, executes that probe against the pinned target crates, captures a structured observation marker, and removes the probe. The workflow rejects a dirty checkout after execution.

The explicit `executed_surfaces` field is important. The generic A/B capture layer can now distinguish a field that was materially checked and absent from one that simply was not exercised. For this bounded run, relationship DID, edge identifier, relationship-equivalent binder and verifier surfaces are executed; status/policy and Trust Task surfaces are not.

No production source in OpenVTC is changed and nothing is committed upstream.
