# ARA Phase 10 — RAHP-style adversarial pressure review

Issue: #42  
Case: `IC-ARA-REL-001`

## Review question

Which ARA claims remain defensible when valid-looking artifacts are manipulated, stale, correlated, semantically inflated, or used outside the authority/state boundary that gave them meaning?

## Material pressure propositions

| Proposition | Failure mode | Counter-case / legitimate condition | Disposition |
|---|---|---|---|
| Identity/authentication is not authority | Authenticated Live Agent or signer is treated as entitled to act | Authenticated identity is one input to a current policy decision with authority, agreement, state and task bindings | Executably defended |
| Signature is not legitimate action | Valid cryptographic evidence is used after revocation, substitution or stale state | Signature is accepted only when protected use and receiver verification bind current admitted context | Executably defended |
| Evidence is not authority | Assurance or receipts are used to create permission | Evidence can support a claim but has no authority effect | Executably defended |
| Assurance is not retroactive authorization | Later review makes an originally refused action appear legitimate | Historical legitimacy follows the original authorization/admission state | Executably defended |
| Multiplicity is not independence | Several credentials/witnesses controlled by one lineage are counted as independent corroboration | Independence is counted by source/control lineage, not artifact count | Executably defended for Lab model |
| Local state is not collective state | One party's annotation is represented as mutual relationship state | Collective state requires all required party dispositions; disagreement remains visible | Executably defended |
| Delivery/inspection/acceptance remain distinct | Transport or decryption is inflated into acceptance | Each stage/disposition remains separately evidenced | Executably defended |
| Recovery must not outrun defensible state | Resumption begins from a later but unreviewed head | Recovery is bounded to the last defensible checkpoint until suspect interval review | Executably defended |
| Link is not traversal authority | Relationship pointer causes graph aggregation/disclosure | Link existence may be reported while traversal stays separately authorized | Executably defended |
| Successful effect requires correlation | Low-level effect is accepted without decision/task/capability lineage | Effect receipt must correlate to exact admission context | Executably defended |

## False-independence finding

The assurance layer explicitly groups attestations by issuer/control/source lineage. Three witness artifacts under one controller count as one independent support group. Four attestations from two issuer lineages count as two independent support groups.

This is deliberately conservative. It does **not** claim that different lineages are necessarily truly independent; it only prevents the simpler false inference that artifact count itself proves independence. More sophisticated organizational, economic, infrastructure, or governance correlation remains a residual assurance problem.

## Residual uncertainty

- local lineage identifiers are supplied to the test harness rather than discovered cryptographically;
- production compromise detection and recovery are not demonstrated;
- standards-native TSP/VTA/RCard/VRC implementations have not yet replaced the relevant Lab adapters;
- no external certification or independent third-party assessment has been performed;
- arbitrary multi-party/quorum relationship semantics remain out of scope;
- standards-native false-independence evidence may require richer provenance than current candidate components expose.

## Maturity recommendation

Treat the ARA slice as an **adapter-backed executable relationship with adversarial evidence**.

Do not yet label it standards-native or production-secure. Missing standards-native integration is a visible partial gate, not a PASS.
