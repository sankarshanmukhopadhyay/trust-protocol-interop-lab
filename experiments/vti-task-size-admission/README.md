# VTI task-size admission: bounded native consumer evidence

**Owner:** Interop Lab produces evidence; [RAHP #1174](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/1174) owns assurance reconciliation. **No composition PASS is claimed.**

## Source contract

- Exact implementing source: [OpenVTC/VTI `9d781a7333a198ef24ec229f59ff8fbcae3b1346`](https://github.com/OpenVTC/verifiable-trust-infrastructure/tree/9d781a7333a198ef24ec229f59ff8fbcae3b1346).
- Whole-document **request** maxima: `vtc/website/upload/begin/0.1` = 262,144 bytes; `vtc/website/upload/chunk/0.1` = 360,448 bytes (from exact source bundle `policy.maxDocumentBytes.request`).
- `vtc/members/update/0.1` declares no request/response bound; the VTC consumer uses a 65,536-byte default.
- The concrete VTC size gate is `vtc-service/src/trust_tasks/size.rs`, delegating lower-level preparse checks to `vti-trust-task-server/src/size.rs`. It also imposes recognized-issuer standing and a bounded preverification large-document budget, and the HTTPS door sets a maximum buffered size across served types.

**Normative interpretation:** A declared limit is an admission ceiling for whole serialized documents. An at/below-limit, valid authorized document must not be rejected *solely because of document size*. Other independent authorization, proof, policy, and rate-budget requirements still apply. An above-limit request is a negative scenario; do not upgrade specification `SHOULD` language to `MUST`.

## Executed by this evidence producer

The source-pinned runner selects five existing VTC **native Rust unit/integration-fixture tests**: policy lookup, exact-limit acceptance by the size checker, refusal above the raised limit, default refusal for an undeclared task, and issuer-standing enforcement. It records immutable target pin, source SHA-256 inventory, native commands, full logs, one counted test per scenario, return code, duration, and packet integrity. Collector mock outputs are **only calibration inputs**.

```bash
python3 -m unittest tests.test_vti_task_size_admission -v
python3 experiments/vti-task-size-admission/run.py \
  --target /path/to/clean-vti-at-exact-pin \
  --output /tmp/vti-size-admission-evidence \
  --timeout-seconds 900
python3 experiments/vti-task-size-admission/run.py \
  --verify /tmp/vti-size-admission-evidence \
  --require-native-pass
```

Requires Rust 1.95, the system prerequisites declared by [the workflow](../../.github/workflows/vti-task-size-admission.yml), and a clean checkout of the stated commit. Output destination must be new. Each command uses `cargo test --locked`; success without **exactly one native test counted** is not a PASS.

## Explicit residuals and negative pressure

The five source-native tests **do not** establish RAHP #1174's full acceptance contract: the relevant size tests use padded JSON, not independently verified signed/authorized documents through the deployed consumer endpoint. The two independently declared maxima have not been exercised at their exact boundaries with valid signed documents in this package. HTTP body buffering, DIDComm/TSP equivalence, no-effect proofs for rejected operations, configured budgets, and external deployment are also not established. Complete the missing consumer-level matrix under RAHP #1174 before any end-to-end assertion.

The runner must continue to report `INDETERMINATE`, `composition_pass=0`, and no discharged RAHP propositions even when all selected native tests pass. For a future qualified matrix, record request bytes **including proof**, source/consumer revisions, issuer standing and authorization, precisely attributable rejection stage, actual response and effects, transport configuration, and packet integrity. Include the second declared task type plus the undeclared negative control.

No upstream code, canonical spec, historical Eucalyptus artifact, or release is changed.
