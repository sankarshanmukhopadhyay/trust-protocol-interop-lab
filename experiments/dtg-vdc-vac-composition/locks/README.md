# Immutable dependency graph for the action-time credential target

This folder holds a **Lab-owned test-build lockfile**, not an amendment to the authoritative credential repository.

| Boundary | Pinned value |
|---|---|
| Source repository | [OpenVTC/dtg-credentials](https://github.com/OpenVTC/dtg-credentials) |
| Source commit | [`66376c01c1f56033cd9ba0775eb8ce0030ff038c`](https://github.com/OpenVTC/dtg-credentials/commit/66376c01c1f56033cd9ba0775eb8ce0030ff038c) |
| Evidence-build lock | [`dtg-credentials-66376c01.Cargo.lock`](dtg-credentials-66376c01.Cargo.lock) |
| Lock SHA-256 | `0ab883de1791d1941ea256489cf718a72be73570f285d606450954d09c3588eb` |
| Toolchain | Rust `1.95.0` |

## Rationale

The immutable credential source does not commit a `Cargo.lock`. A fresh resolve in [action-time run #41639975002](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/actions/runs/41639975002) selected `affinidi-messaging-sdk 0.22.0` with `affinidi-messaging-core 0.1.11`; compiling that graph failed with Rust E0639 because the SDK constructed the core's non-exhaustive `Inbound` type. Version `0.1.10` reproduced the failure; `0.1.6` was rejected by the dependent crate's `^0.1.7` requirement. Version `0.1.7` satisfied resolution and passed the full native workflow in [run #41642039816](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/actions/runs/41642039816).

The corresponding exact resolved `Cargo.lock` is retained here. Its hash is checked in the workflow before `cargo test --locked --all-targets`. This prevents a future dependency-index change from silently altering the tested build. The checkout's tracked source and Git revision remain immutable.

## Reproduce

On Linux with Rust 1.95.0, required native libraries, and a clean checkout of the exact credential commit:

```bash
cp experiments/dtg-vdc-vac-composition/locks/dtg-credentials-66376c01.Cargo.lock /path/to/dtg-credentials/Cargo.lock
printf '%s  %s\n' \
  0ab883de1791d1941ea256489cf718a72be73570f285d606450954d09c3588eb \
  /path/to/dtg-credentials/Cargo.lock | sha256sum --check -
cargo test --manifest-path /path/to/dtg-credentials/Cargo.toml --locked --all-targets
```

See [the workflow](../../../.github/workflows/dtg-vdc-vac-action-time.yml) for the CI environment, target pin, evidence adapter, and artifact retention.

## Evidence and change control

The lockfile establishes **reproducible build inputs**, not independent certification of credential semantics or action-time authority. The workflow's component test success is qualified separately from downstream composition evidence.

If the credential source revision or dependency set changes, create a new separately named lockfile and require a native test run before updating the evidence baseline. Do not overwrite historical source pins or retain a green assurance conclusion after tests become unavailable.
