# DTG/VTI engineering assessment — WP01 inventory (2026-11-24)

Status: executed source and dependency inventory; not native build or runtime evidence. Parent #259; WP01 #260. Source retrieval via GitHub at immutable refs; Initial local acquisition was blocked; hosted acquisition and dependency resolution subsequently succeeded. No upstream writes.

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

Paths below were recovered from merge records and selected current pinned files; historical artifact acquisition and attribution disposition are recorded below. All cited prior issues are closed; no historical result is asserted current.

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

## Manual acquisition reference (superseded by executed collector)

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

- Pinned trees and selected Linux feature profiles acquired and verified in hosted execution; native builds remain WP03.
- Historical artifacts reconciled below; mismatched target attribution quarantined for WP03.
- Root upstream SECURITY.md lookup returned 404 for both implementations; alternate locations and org channel remain unverified.
- Source-level entry points, actual call graph, known divergences and supported deployment configurations remain incomplete.
- WP02 may derive scoped oracles after inventory review; WP03 owns native baseline and evidence binding; no G1 admission or maturity promotion.
- First vertical slices: credential parsing/verification/authority; VTA/VTC task dispatch and durable mutation; state recovery. Client/forge/mobile/TEE deployment only when required by an admitted proposition.

The collector and workflow added by PR #272 are restricted to source/dependency observations. See execution reconciliation below.


## Executed inventory reconciliation

- Initial run 45321875470 / artifact 14887244178, archive SHA-256 34ef77231261d213d2a3ed4eccf663ddccbafd5933909aa32dede8b4c84bc359.
- Expanded run 45322471460 / artifact 14888097752, archive SHA-256 771c2a7801934a1498835a2a82a96b19b8013efbea360287308663ff33217e55. Downloaded archive and all 161 manifest-listed file hashes independently checked. Runner checkout recorded as 1e581f1d8abababc59143b68f8192305978385c4 (PR merge checkout, not branch head).
- All six pinned source trees acquired; both implementations resolved locked default/no-default metadata and 27 feature profiles (2 credential, 25 VTI). No compilation or target tests implied.
- Exact generated credential lock SHA-256 005ac82537244c460d47450bacdcdb553c6526d8595f64ff6320cc37daf41572 now retained at experiments/dtg-engineering-inventory/locks/dtg-credentials-cbae70f8.Cargo.lock. VTI tracked lock SHA-256 29790be4507f147f9c0cf39d96d767a7b527421978b3a2ebb3a2cbf5f3f463fb. Final workflow replays the versioned lock without downloading an older artifact.
- Reproduce from PR checkout using Python 3.13, Git and Rust 1.95.0: `python experiments/dtg-engineering-inventory/collect.py --output /tmp/wp01-observations --credential-lock experiments/dtg-engineering-inventory/locks/dtg-credentials-cbae70f8.Cargo.lock --credential-lock-sha256 005ac82537244c460d47450bacdcdb553c6526d8595f64ff6320cc37daf41572`; then from the output directory run `sha256sum --check SHA256SUMS`. Output directory must not exist. The workflow is network-enabled and read-only, with bounded command/job timeouts.

- Repository-owned lock replay: run 45323289062 succeeded. Consolidated inventory head 26a9c009b733a9db8f8323294208f83cefa977d9 passed inventory run 45323389741 and Repository assurance run 45323388109. Artifact 14887719417, reported archive SHA-256 83afed6551ad13b40661b0956b347973bd2b91c2c0b018933a28ba56e18ca0bf.

## Historical attribution disposition

Historical artifacts independently downloaded and archive digests verified: 10379865808 (#163), 10087128733 (#174), 10088370973 (#203), 10192669229 (#208), 10193079490 (#210), and 10795450058, 10794948383, 10794849165, 10795520707, 10794499174, 10795083200 (#243). Historical run IDs: 34924700795, 34307256014, 34310631415, 34583222186, 34584195587 and 35968025734, 35968025970, 35968025726, 35968025742, 35968025746, 35968025958 respectively. #235 runner experiments/ara-authority-at-commitment/run.py and #238 experiments/trust-tasks-cryptosuite-interop/run.py are semantic fixtures (runs 35736285386, 35748900915; no retained artifact returned). #241 source report analysis/rahp-767-proof-required-bearer-evidence.md, PR #242, is historical source characterization. #163 runner experiments/dtg-credential-task-actuation/run.py. #243 reused the existing VTI credential/replay/VAC and A/B workflow families; no new independent native test claim inferred.

For #243 Track B task and status, historical job logs show checkout of 3551ceda3431707b2364eae6d30d50d94cec29dc, but exported evidence declares 76eae3f8093cc09fc6d47428833a158e326a981f. Policy export matches the intended pin. **Quarantine task/status exports for current-epoch attribution**; preserve original bytes. Current producer source at Lab baseline reveals split target identity: reusable workflow checks checkout against input, while scripts/run_current_openvtc_ab_member.py validates against characterization/manifest; both current case manifests and shared characterization declare 76eae3f. Capture derives provenance from manifest. Workflow substitutes only an older adapter pin, not characterization or manifests. This establishes missing cross-boundary binding, not historical runtime behavior or exact historical root cause without inspecting historical producer tree. WP03 owns fail-closed regression and explicit target binding before future reuse; no retrospective relabeling. DPIP/RAHP interpretation remains with owners.

## WP02/03 admission inputs

Pinned VTI WD0.2.0, Credentials WD0.6.0, Trust Tasks WD0.7.0 are working drafts. VTI Appendix F is informative, not a waiver. F.1 authority encoding; F.2 replay, freshness and versioning; F.3 delivery/session/resolution; F.4 audit and identifiers; F.5 community authority; F.6 custody; F.7 closed; F.5a administrative authority. Map actual clauses in WP02. Upstream #1641 and #1684 closed; treat bearer retirement as regression hypothesis, not open defect. Existing VTI CI includes nextest, separate VTC tests, feature matrix, locked MSRV, cargo-deny, scheduled advisories, fuzz build/run, transport harnesses, enclave and mobile builds. Credentials CI includes clippy, default/all/no-default tests, package and MSRV checks. WP03 must reuse those paths and distinguish upstream results from independent reruns. Mobile/WASM/platform-specific build and standalone enclave proxy are conditional, outside this Linux dependency inventory; explicitly admit if required. Security policy alternate locations remain unverified; no sensitive publication authorized. Full call-path verification belongs to WP02/03, not inferred from module inventory.
