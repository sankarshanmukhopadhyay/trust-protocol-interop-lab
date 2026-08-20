# Scenario 07 — Evidence-state separation

Test otherwise identical chains with (a) no evidence reference, (b) an unresolvable reference, (c) bytes that resolve but fail integrity/signature validation, (d) valid but revoked/expired authority, and (e) valid evidence with an explicit policy denial.

**Expected:** the five states remain machine-distinguishable and are not collapsed into `not_authorized`.
