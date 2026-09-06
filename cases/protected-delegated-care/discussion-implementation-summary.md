# Medical-prescription Discussion — implementation summary

The Protected Delegated Care workstream took the original medical-prescription / medication-assistance Discussion and translated it into an executable assurance programme rather than a single application prototype.

## What was built

The base case, `IC-PDC-MED-001`, now includes a deterministic delegated-care core, Trust Task-shaped consequential requests, explicit disclosure controls, negative/replay/stale-state scenarios, runtime privacy evidence and a fail-closed current-authority actuation boundary. The bounded refill extension, `IC-PDC-REFILL-001`, adds selective-disclosure comparison and a synthetic prescription/order-to-refill lifecycle.

## What the implementation pressure test found

The strongest positive result is architectural: identity, relationship, delegation, task authorization, execution and evidence can remain separate application concerns. Missing upstream authority evidence can also be represented without manufacturing a `PERMIT`: the current VTI/OpenVTC surface inspection found no exact generic delegated-action evaluator for the PDC action/resource, so the actuation boundary correctly remains `INDETERMINATE/BLOCKED`.

Runtime privacy evidence supports minimum disclosure at the application boundary. It does not justify claims about provider/network/device confidentiality or universal unlinkability. At the refill boundary, selective disclosure currently improves attribute minimisation without requiring an unexercised ZKP construction. The stronger ZKP candidate remains deliberately `INDETERMINATE` until real proof generation/verification is exercised and measured residual linkability warrants it.

The prescription/refill lifecycle further separates prescription existence, holder possession, refill eligibility and any later dispensing authority. Expired, revoked, superseded or exhausted orders fail closed; context/challenge mismatch fails closed; replay cannot create a second synthetic refill effect.

## Assurance outcome

`IC-PDC-MED-001` remains **Experimental**. CI and executable evidence are reproducible, but the assurance result is not green because material boundaries remain unresolved or `INDETERMINATE`:

- exact current delegated-action authority at actuation;
- provider/network/device confidentiality and broader correlation;
- generic Trust Task proof versus authenticated-transport semantics;
- explicit mapping between relationship/current-membership state and delegated consequential-action authority.

This is a useful outcome of the Discussion. The work did not merely show that a medication-assistance flow can be coded; it exposed which trust properties are application-owned, which can be exercised against existing DTG/VTC/OpenVTC surfaces, and which still require specification/profile or implementation work.

## Claim boundary

Nothing in this work establishes prescribing, clinical decision support, medication ingestion, legal dispensing authority, production pharmacy interoperability, healthcare certification, provider confidentiality or universal unlinkability.

The full implementation chain is documented in the case README and the machine-readable maturity decision is in `assurance-decision.yaml`.
