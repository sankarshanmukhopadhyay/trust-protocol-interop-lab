# `(test) Produce current OpenVTC Track A A/B evidence`

Closes the executable producer obligation in #153 once CI evidence is successful and inspected.

This PR introduces a bounded target-specific adapter for the current source-pinned VTI revision, reuses the existing A/B capture/export machinery, runs a seeded positive control plus a context-distinct pressure case, and uploads a DPIP-consumable evidence package. Dogwood RC-1 remains historical/regression evidence only.

The selected current path exercises relationship-equivalent and verifier surfaces. Status/policy-discovery and Trust Task surfaces remain `not-evidenced` where unexecuted. No privacy PASS or RAHP GREEN is manufactured.
