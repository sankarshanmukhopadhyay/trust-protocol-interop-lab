# ER-DEVICE-METADATA-AB

Executable source-pinned A/B privacy pressure case for RAHP #273 / Interop Lab #75.

Two unrelated operational contexts execute the same pinned OpenVTC installation/profile behavior. The harness executes the upstream OpenVTC display-name producer and the pinned VTI heartbeat extension/persistence tests, then records whether display metadata, heartbeat payload and retained presence state expose a reusable join.

The test intentionally preserves the implementation's actual host/profile naming behavior. It does not manufacture context-specific aliases to force an unlinkable result.

A seeded positive control proves the join detector is capable of detecting an identical value.

DPIP owns the privacy conclusion; this experiment produces attributable runtime evidence only.
