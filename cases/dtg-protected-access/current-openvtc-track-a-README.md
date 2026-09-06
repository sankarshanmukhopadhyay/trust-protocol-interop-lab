# Current OpenVTC Track A evidence tranche

This directory slice implements Interop Lab #153 from RAHP #439's current-baseline decision.

Start with `current-openvtc-track-a-evidence-index.yaml`. The executable pair is the current-target adapter plus `current-openvtc-track-a-evidence.yml`. The workflow runs a seeded positive control and a context-distinct pressure case against `OpenVTC/verifiable-trust-infrastructure@e393e38da4941202143e293b555413d8c86ef3b3`, exports DPIP bindings, and uploads the runtime artifact.

The tranche intentionally preserves unresolved status/policy and Trust Task evidence when the bounded current path does not execute those surfaces. Dogwood RC-1 is historical regression evidence only.
