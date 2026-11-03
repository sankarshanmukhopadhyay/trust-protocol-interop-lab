# Post-fix VTI Trust Task consuming-path evidence

This experiment follows upstream [VTI #2404](https://github.com/OpenVTC/verifiable-trust-infrastructure/issues/2404) and [VTI #2402](https://github.com/OpenVTC/verifiable-trust-infrastructure/issues/2402), to inform [RAHP #691](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/691) and [RAHP #966](https://github.com/sankarshanmukhopadhyay/rahp-toolkit/issues/966).

**Authority and source:** VTI owns implementation, Trust Tasks owns the declared error vocabulary, this Lab owns reproducible target-native execution records, and RAHP owns downstream assurance judgment. The source is pinned to `OpenVTC/verifiable-trust-infrastructure@2fc769fddbe2ee6f87a5b8a8ce048d8f5ffeef84`, which includes both correction commits. No upstream source is patched.

**Historical independence:** This is **not** Eucalyptus. The frozen Eucalyptus revision `49f5f1beb61adc34bdf7cf0bd3eb10f594415b80` and its original Lab tests, feasibility record and evidence remain unchanged. A native test observed on the post-fix tree is not evidence about Eucalyptus.

## Executable cases

The runner uses eight existing upstream Rust tests. Six address #691's positive and negative error/outcome interpretation: valid host-cleanup details, absent/empty/malformed details, generic wrong-code refusal, and `deleted: false` not being reported as completed deletion. Two address #966's source-native retry behavior: the same persisted effect and identity across reconstructed VTA lifetimes, and a synthetic interrupted in-flight claim after a committed effect, with no duplicate effect on retry.

Every cargo command is recorded with its exact test name and upstream source revision. A returned status of zero without exactly one counted passing native test does **not** count as successful execution. Failure and timeout are retained. Source files are hashed and checked for required test/function anchors before execution; the target commit and tracked-source cleanliness are checked again after each case. Output includes raw native stdout/stderr with SHA-256 integrity, a contract, attempts, and a result. An integrity manifest detects missing/modified packet files but does not constitute an external signature or independent attestation.

## Run

Use an isolated Linux environment with Rust 1.95.0, `libdbus-1-dev`, `libpcsclite-dev`, `pkg-config`, `clang`, `cmake` and adequate disk capacity. Clone the **exact commit** into a clean separate checkout. Run from the root of the Interop Lab checkout:

```bash
python3 -m unittest tests.test_vti_postfix_consumption -v
python3 experiments/vti-postfix-consumption/run.py \
  --target /tmp/vti-postfix \
  --output /tmp/vti-postfix-evidence \
  --timeout-seconds 900
python3 experiments/vti-postfix-consumption/run.py \
  --verify /tmp/vti-postfix-evidence \
  --require-native-pass
```

The target checkout must be `2fc769fddbe2ee6f87a5b8a8ce048d8f5ffeef84`. The output directory must not already exist. No test is skipped or substituted for a missing upstream test. The GitHub Actions workflow is manually dispatchable and triggered by changes to this experiment.

## Evidence limits

A completely passing run establishes **bounded target-native upstream regression execution** only, not deployment-wide or composed-consumer assurance. Specifically:

- The SDK tests instantiate structured rejection errors; they do not send a signed refusal from a real VTA into an interactive CLI terminal. An external host and operator decision are not exercised.
- The CLI test verifies the `deleted: false` helper outcome, not the interactive confirmation loop.
- The restart tests exercise an actual second service lifetime and persisted key counts, but the interruption case simulates the state left after an effect commits by modifying an idempotency record. It is not a process kill at a machine-injected commit point.
- No independent organizations, live governance decisions, deployed topology, revocation freshness, or wider Eucalyptus properties are established.

Consequently, the result always records `assurance_state=INDETERMINATE`, `composition_pass=0`, and no discharged RAHP propositions, including after all native tests pass. RAHP must independently qualify whether the additional operationally composed evidence it needs is obtainable. Do not update frozen Eucalyptus historical claims or reinterpret successful native tests as an independent assurance verdict.

The runner and calibration unit tests are maintained in this Lab; upstream implementation corrections are reported to VTI, not contributed to that repository by this experiment.
