# Eucalyptus frozen VTI consuming-path evidence

**Status:** Source-compatible experimental native consumer. No deployment-wide or RAHP proposition PASS is claimed.

**Authority:** This Lab owns executable evidence production only. OpenVTC owns its implementation and test assertions; RAHP [#966](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/966) owns the downstream Eucalyptus assurance residuals. The historical [RAHP #960](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/960) and its source pins are not changed.

## Why this is a separate versioned path

The existing Lab current-VTI and Dogwood programs test *different immutable sources*. Their accepted source guards and historical evidence cannot be repurposed by changing a revision string. This runner accepts only `OpenVTC/verifiable-trust-infrastructure@49f5f1beb61adc34bdf7cf0bd3eb10f594415b80` from the Eucalyptus coordinated release. A wrong checkout or changed tracked source fails before evidence collection.

## Exact target-native consuming-fixture experiments

| Vector | Actual upstream fixture and effect observer | Assurance boundary |
|---|---|---|
| `positive-sealed-tsp` | `tests/e2e/tests/tsp_vta_trust_task.rs`: a sealed secret is unsealed by a running VTA through the embedded TSP/mediator path | In-process native integration, not independent operating parties |
| `negative-unauthorized-tsp` | Same test binary: sender without authority is refused through TSP rather than silently accepted or lost | Fixture's asserted denial, not every transport or authorization entry point |
| `replay-same-key-effect` | `vta-service/tests/it/idempotency_trust_task.rs`: identical key retry checks the **stored key count**, not merely successful HTTP response | In-process state/effect comparison before a service restart |
| `replay-changed-payload` | Same file: same key with changed payload must be rejected and leave expected key count unchanged | One keyed-task class; not universal replay protection |

The runner executes the real target test binaries, captures unmodified stdout/stderr, test counts, exit code, tool invocation, duration, immutable source and Lab producer revisions, and a SHA-256 integrity manifest. It does **not** synthesize application receipts, patch upstream test assertions or call this an independent deployment. Unit tests in this Lab use mocked process outputs solely to falsify the evidence collector; they produce no target-native assurance evidence.

## Reproduce on an isolated Linux runner

Prerequisites: Rust 1.95.0, `libdbus-1-dev`, `libpcsclite-dev`, `pkg-config`, `clang`, `cmake`, a clean checkout of the **exact** source pin, and sufficient disk and time for the Rust workspace. Use an isolated `CARGO_TARGET_DIR` and nonproduction test fixtures.

```bash
python3 -m unittest tests.test_eucalyptus_native_consumption -v
python3 experiments/eucalyptus-vti-consumption/run.py \
  --target /tmp/vti-eucalyptus \
  --output /tmp/eucalyptus-lab-evidence \
  --timeout-seconds 900
python3 experiments/eucalyptus-vti-consumption/run.py \
  --verify /tmp/eucalyptus-lab-evidence \
  --require-native-pass
```

The output directory must be new. Verification detects missing, additional or changed files. `--require-native-pass` returns nonzero when any required vector was not verified as a passing native test. This is an **engineering gate**, not an assurance certification. The full integrity-verified packet still uses `assurance_state=INDETERMINATE`, `composition_pass=0` and `discharged_euc_propositions=[]`.

## What remains before #966 can close

These in-process observations are a first usable consumer execution surface. They do not yet satisfy the full #966 proposal:

- Capture attributable deployed topology, live identities and policy/status configuration independently of the upstream fixture.
- Induce a genuinely lost acknowledgement and inspect durable effects **across a service restart**, which the current native suite does not establish.
- Exercise stale or revoked authority *at action time*, not just unauthorized sender identity.
- Produce a portable producer-result bound to an actual RAHP obligation identifier and accepted contract, rather than assigning a fictional or placeholder obligation key.
- Obtain the relevant specialist/privacy/participant evidence if making claims about those surfaces.

The current machine result is intentionally an **Interop Lab observation**, not a fabricated `rahp-evidence-producer-result/v1`. RAHP can consume the evidence with its original limitation and should only close propositions supported by attributable external execution. A successful collection workflow proves packet integrity and bounded fixture execution, not target-wide interoperability.
