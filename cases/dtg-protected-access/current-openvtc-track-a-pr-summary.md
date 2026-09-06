# PR summary

Implements the executable portion of #153 against the current source-pinned OpenVTC target selected by RAHP #439.

The change adds a target-specific current VTI adapter, a seeded positive control, a context-distinct A/B pressure case, CI execution, evidence-boundary assertions, DPIP export and explicit Dogwood historical quarantine. Existing generic A/B capture semantics are reused unchanged.

The selected current path materially exercises relationship-equivalent and verifier surfaces. Status/policy-discovery and Trust Task surfaces are intentionally retained as `not-evidenced` where they are not executed. The producer does not manufacture a privacy PASS or assurance promotion.
