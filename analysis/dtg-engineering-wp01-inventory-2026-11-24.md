# DTG/VTI engineering assessment — WP01 inventory (2026-11-24)

Status: partial source inventory, not runtime evidence. Parent #259; WP01 #260. Source retrieval via GitHub at immutable refs; full checkout and dependency resolution blocked in current execution environment (DNS resolution for github.com failed; cargo and gh absent). No upstream writes.

## Source baseline

| Repository | Immutable commit | Role |
|---|---|---|
| OpenVTC/dtg-credentials | cbae70f8b4d3686b982e1358bf5bb389ea08a599 | credential implementation |
| OpenVTC/verifiable-trust-infrastructure | 2316fbd2f64a5e33f7fff06df7efec2aec4f269c | VTI implementation |
| trustoverip/dtgwg-vti-spec | 83e88fcf8760f6bd159bbac09a27b002f5b656c2 | VTI specification |
| trustoverip/dtgwg-cred-spec | 634e0b0495abef9ca376901026074e4f20e5636e | credential specification |
| trustoverip/dtgwg-trust-tasks-spec | bdf2cdd9256f9d7b98fe8b40c776124fc27a6084 | Trust Tasks framework |
| sankarshanmukhopadhyay/trust-protocol-interop-lab | 364d538977b790635fe250c36d16ed15a08f7556 | evidence source baseline |

VTI README acknowledges specification precedence and Appendix F divergence register. Specification draft status, actual clauses and companion dependencies must be verified before WP02 assigns normative oracles. VTI spec paths are enumerated in specs.json and STRUCTURE.md; credential and Trust Tasks use spec/body.md. Do not substitute design commentary for normative requirements.

## Observed source inventory

Credentials Cargo.toml Git blob 04b541ce16cecc0c0b5862dbd9277b938906cd18; src/lib.rs blob 9c4deb4306cf4ef8747c08d960cd25a632184e17. Package 0.14.0, Rust 1.95.0, edition 2024; default affinidi-signing, optional secrets resolver; examples sign_and_verify and data_room require signing. Modules accept, authority, create, delegation, purposes, statement. Direct dependencies include affinidi-data-integrity 0.9, affinidi-did-common 0.5, serde, canonicalizer, sha2, chrono, unicode-normalization. Example cipher is dev-only.

VTI Cargo.toml blob 7330845b9c663a123fcc854a290ad35494cc8f30; Cargo.lock blob 47a30a62ca87fe83421cd13f97a0d87fd9e62b08 (Git blob identity, not SHA-256). Rust 1.95.0, edition 2024. Declares dtg-credentials 0.14, affinidi-tdk 0.45, affinidi-data-integrity 0.8.7 with ml-dsa, messaging SDK 0.47.2, Tokio 1.49, Fjall 3. These are manifest requirements, not resolved versions. Standalone credential source pin is not necessarily the registry package consumed by VTI; identify actual resolved graph and package checksum before comparison.

| Component group | Members observed in workspace | Initial assessment |
|---|---|---|
| Service and clients | vta-service, vtc-service, vta-sdk, vtc-client, vta-cli-common, cnm-cli, pnm-cli, didcomm-test, vta-mobile-core | request/response and enforcement |
| VTA subsystems | vta-config, vta-keyspaces, vta-audit, vta-backup, vta-keys, vta-policy, vta-signing, vta-support, vta-tee, vta-sweepers, vta-vault, vta-external, vta-webvh, vta-persona, vta-enclave | authority, state, keys, recovery |
| VTC and shared | vtc-audit, vti-common, vti-trust-task-server, vti-oob-server, vti-secrets, vti-webauthn, vti-vtn | governance, dispatch, transport |
| MCP | vta-mcp, vtc-mcp, vti-mcp-common | tool boundary |
| Generated contracts | vti-specs, vti-specs-core, vti-specs-rooms, vti-specs-vta, vti-specs-vtc, vti-specs-vtn | contract drift |
| Rooms | room-host, vti-rooms, vti-rooms-dtg, vti-rooms-host, vti-rooms-wasm | lifecycle and isolation |
| Specialist | vti-witness, vti-vetting-pcs, vti-voting, vti-voting-service | conditional coverage |
| Tests | tests/e2e, vta-test-support | actual consumer paths |

Default-members differs from workspace; mobile and specialist components require explicit assessment admission. deploy/nitro/enclave-proxy excluded from workspace. VTA owns key/DID/access-policy functions; VTC owns community membership and policy functions and depends on VTA. This is architectural source characterization, not a verified call graph.

## Dependency resolution constraint

Root Cargo.lock not found for credential pin. TPIL already has an explicit historical dependency lock solution: .github/workflows/dtg-vdc-vac-action-time.yml at Lab pin uses target 66376c01c1f56033cd9ba0775eb8ce0030ff038c and experiments/dtg-vdc-vac-composition/locks/dtg-credentials-66376c01.Cargo.lock with declared SHA-256 0ab883de1791d1941ea256489cf718a72be73570f285d606450954d09c3588eb. Workflow documents an earlier incompatible resolver selection and enforces messaging-core 0.1.7. Digest and historical execution not independently verified in this session. Reuse mechanism, not old lock bytes or constraints, for current credential pin. Capture a fresh resolved lock, toolchain, registry checksums, feature matrix and locked rerun; if resolution fails, preserve failure rather than patch upstream to obtain green.

## Reuse reconciliation

Paths below were recovered from merge records and selected current pinned files; retained historical CI artifact bytes and hashes have not been independently acquired. All cited prior issues are closed; no historical result is asserted current.

| Issue | Exact runner/workflow or provenance | Output/claim and action |
|---|---|---|
| #163 | issue record; successor #203/#233 | historical vectors; locate original artifacts |
| #174 | .github/workflows/dtg-vdc-vac-action-time.yml; experiments/dtg-vdc-vac-composition/run_action_time.py | wd02-dtg-credentials-target.json, wd02-action-time.json; component native plus composition; re-pin lock |
| #191 | docs/workflow-rationalisation.md; scripts/run_current_openvtc_ab_member.py; .github/workflows/reusable-current-openvtc-ab-evidence.yml | reuse admission and equivalence rules; do not add bespoke workflow without distinct need |
| #203 | .github/workflows/vti-trust-task-credential-path.yml; experiments/vti-trust-task-credential-path/evaluate.py | vti-trust-task-credential-path.json and drift; source wiring plus package tests, not dedicated effect test |
| #208 | .github/workflows/vti-resolved-effect-binding.yml; experiments/vti-resolved-effect-binding/evaluate.py | vti-resolved-effect-binding.json and drift; approval/effect identity residual |
| #210 | .github/workflows/vti-credential-replay-convergence.yml; experiments/vti-credential-replay-convergence/evaluate.py | vti-credential-replay-convergence.json and drift; no deployment-wide retry claim |
| #230 | experiments/dpip-evidence-obligation/admit.py; tests/test_dpip_evidence_obligation.py; scripts/validate_evidence.py | admission contract; NO_TARGET is not acquired evidence |
| #233 | experiments/dtg-task-citation-convergence/evaluate.py; openvtc-source-characterization.json in same directory; tests/test_dtg_task_citation_source_characterization.py | historical source characterization plus fixture; target 1099d7b24366b9d390f24201dc6db308fda70e21; recheck newer path |
| #235 | issue record IC-ARA-AUTHORITY-COMMIT-001 | semantic vectors; locate exact runner |
| #238 | issue record | capability floor fixture; locate exact runner |
| #241 | issue record | proof-required route census; locate exact runner |
| #243 | issue record; previous VTI 3551ceda3431707b2364eae6d30d50d94cec29dc | six refreshed evidence surfaces; locate exact manifest and artifacts |

The three VTI historical workflows above invoke cargo test -p vta-service --lib without --locked in inspected source. That observation does not establish actual historical dependency drift; current WP03 must explicitly check lock integrity before and after execution.

## Clean-checkout execution packet (not executed here)

Use a disposable network-enabled Linux environment with Git, Rust 1.95.0, Python and native dependencies (existing credential workflow installs libdbus-1-dev and pkg-config; verify VTI requirements). For each source row:

```sh
git clone "https://github.com/$owner/$repo.git" "$checkout"
git -C "$checkout" checkout --detach "$pin"
test "$(git -C "$checkout" rev-parse HEAD)" = "$pin"
test -z "$(git -C "$checkout" status --porcelain)"
git -C "$checkout" ls-tree -r HEAD > "$out/source-tree.txt"
```

Use a separate output directory per repository outside its checkout. Record git/rustc/cargo versions and OS. For credential only, generate a lock if absent, retain it separately with SHA-256 and explicit generated provenance; do not replace tracked files. For VTI require existing lock and record hash. In each implementation checkout run:

```sh
cargo +1.95.0 metadata --locked --format-version 1 > "$out/metadata-default.json"
cargo +1.95.0 metadata --locked --no-default-features --format-version 1 > "$out/metadata-no-default.json"
cargo +1.95.0 tree --locked -e features > "$out/features-default.txt"
cargo +1.95.0 tree --locked --duplicates > "$out/duplicates.txt"
sha256sum Cargo.lock > "$out/lock.sha256"
git status --porcelain --untracked-files=all > "$out/post-resolution-status.txt"
```

Record exit status and stderr per command; unsupported configurations are explicit blockers, not successful empty artifacts. VTI workspace/target-specific feature combinations must be enumerated from manifests and CI, not inferred from the root no-default-features run. Retain full source-tree listing, package/source/checksum graph, feature sets and observed source drift; hash outputs and verify against pinned source. No compilation or test PASS is claimed by metadata resolution.

## Residuals and gate

- Full pinned checkout, full tree inventory, complete dependency/feature resolution and SHA-256 manifests: blocked by local network/toolchain.
- Historical runner/manifest/CI artifact reconciliation: partial; exact paths above are observed, historical uploaded bytes not retrieved.
- Root upstream SECURITY.md lookup returned 404 for both implementations; alternate locations and org channel remain unverified.
- Source-level entry points, actual call graph, known divergences and supported deployment configurations remain incomplete.
- WP02/03 readiness remains conditional; no G1 admission or maturity promotion.
- First vertical slices: credential parsing/verification/authority; VTA/VTC task dispatch and durable mutation; state recovery. Client/forge/mobile/TEE deployment only when required by an admitted proposition.

No new workflow or dependency introduced by this document. This is a reviewable partial inventory, not an evidence manifest or completion of #260.
