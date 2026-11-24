#!/usr/bin/env python3
"""Collect pinned source and dependency observations, not build/test assurance."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time

PINS = {
    "OpenVTC/dtg-credentials": "cbae70f8b4d3686b982e1358bf5bb389ea08a599",
    "OpenVTC/verifiable-trust-infrastructure": "2316fbd2f64a5e33f7fff06df7efec2aec4f269c",
    "trustoverip/dtgwg-vti-spec": "83e88fcf8760f6bd159bbac09a27b002f5b656c2",
    "trustoverip/dtgwg-cred-spec": "634e0b0495abef9ca376901026074e4f20e5636e",
    "trustoverip/dtgwg-trust-tasks-spec": "bdf2cdd9256f9d7b98fe8b40c776124fc27a6084",
    "sankarshanmukhopadhyay/trust-protocol-interop-lab": "364d538977b790635fe250c36d16ed15a08f7556",
}
IMPLEMENTATIONS = {"dtg-credentials", "verifiable-trust-infrastructure"}
# Profiles observed in the pinned VTI .github/workflows/ci.yml. These are
# dependency-tree observations, not build or platform conformance results.
VTI_PROFILES = {
    "vta_tee_rest_didcomm": ["-p", "vta-service", "--no-default-features", "--features", "tee,rest,didcomm"],
    "vta_rest_didcomm": ["-p", "vta-service", "--no-default-features", "--features", "rest,didcomm"],
    "vta_rest": ["-p", "vta-service", "--no-default-features", "--features", "rest"],
    "vta_setup_tsp": ["-p", "vta-service", "--no-default-features", "--features", "setup,keyring,rest,tsp,cli-synthesis"],
    "vta_aws": ["-p", "vta-service", "--no-default-features", "--features", "aws-secrets,keyring,rest"],
    "vta_azure": ["-p", "vta-service", "--no-default-features", "--features", "azure-secrets,keyring,rest"],
    "vta_setup_didcomm": ["-p", "vta-service", "--no-default-features", "--features", "setup,keyring,rest,didcomm,cli-synthesis"],
    "vta_config_seed": ["-p", "vta-service", "--features", "config-seed"],
    "vta_config_seed_secrets": ["-p", "vta-service", "--features", "config-seed,vault-secrets,k8s-secrets"],
    "vta_tee_webs": ["-p", "vta-service", "--no-default-features", "--features", "tee,rest,didcomm,webs"],
    "vta_transport_harness": ["-p", "vta-service", "--features", "transport-harness"],
    "vtc_transport_harness": ["-p", "vtc-service", "--features", "transport-harness"],
    "vtc_vetting_voting": ["-p", "vtc-service", "--features", "vetting-pcs,voting"],
    "sdk_attest": ["-p", "vta-sdk", "--features", "attest-verify"],
    "sdk_transfer": ["-p", "vta-sdk", "--features", "client,sealed-transfer,provision-integration"],
    "sdk_vetting": ["-p", "vta-sdk", "--features", "client,vetting"],
    "sdk_all": ["-p", "vta-sdk", "--all-features"],
    "tee_overlay": ["-p", "vta-tee", "--features", "tenant-overlay"],
    "rooms_mls": ["-p", "vti-rooms", "--no-default-features", "--features", "mls"],
    "room_host_didcomm": ["-p", "room-host", "--features", "didcomm"],
    "workspace_all": ["--workspace", "--all-features"],
    "enclave_base": ["-p", "vta-enclave", "--no-default-features", "--features", "rest,didcomm,vsock-store,vsock-log"],
    "enclave_overlay": ["-p", "vta-enclave", "--no-default-features", "--features", "rest,didcomm,vsock-store,vsock-log,tenant-overlay"],
    "enclave_webs": ["-p", "vta-enclave", "--no-default-features", "--features", "rest,didcomm,vsock-store,vsock-log,webs"],
    "common_vsock": ["-p", "vti-common", "--features", "vsock-store,encryption"],
}
CREDENTIAL_PROFILES = {"all": ["--all-features"], "no_default": ["--no-default-features"]}
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def command(cwd, output, name, args, records, timeout=180):
    start = time.monotonic()
    with (output / (name + ".stdout")).open("wb") as out, (output / (name + ".stderr")).open("wb") as err:
        try:
            code = subprocess.run(args, cwd=cwd, stdout=out, stderr=err, timeout=timeout, check=False).returncode
        except (OSError, subprocess.TimeoutExpired) as exc:
            err.write(str(exc).encode())
            code = 125
    records.append({"id": name, "argv": args, "exit": code, "seconds": round(time.monotonic()-start, 3)})
    return code == 0

def collect(repo, pin, work, out, credential_lock=None, credential_lock_sha256=None):
    name = repo.split("/")[-1]
    dst = work / name
    dst.mkdir()
    out.mkdir()
    records = []
    def run(label, *args, timeout=180):
        return command(dst, out, label, list(args), records, timeout)
    result = {"repository": repo, "commit": pin, "commands": records, "state": "blocked"}
    if not (run("init", "git", "init", "-q") and
            run("fetch", "git", "-c", "credential.helper=", "fetch", "--no-tags", "--depth=1",
                "https://github.com/" + repo + ".git", pin, timeout=240) and
            run("checkout", "git", "checkout", "--detach", "FETCH_HEAD") and
            run("head", "git", "rev-parse", "HEAD")):
        return result
    if (out / "head.stdout").read_text().strip() != pin:
        result["state"] = "identity_mismatch"
        return result
    if not run("initial_status", "git", "status", "--porcelain", "--untracked-files=all") or (out / "initial_status.stdout").read_bytes():
        return result
    if not run("tree", "git", "ls-tree", "-r", "--full-tree", "HEAD"):
        return result
    result["state"] = "source_acquired"
    if name not in IMPLEMENTATIONS:
        return result
    lock = dst / "Cargo.lock"
    generated = not lock.exists()
    supplied = name == "dtg-credentials" and credential_lock is not None
    if supplied:
        if not generated or digest(credential_lock) != credential_lock_sha256:
            result["state"] = "dependency_blocked"
            result["blocker"] = "supplied lock conflicts with source or digest"
            return result
        lock.write_bytes(credential_lock.read_bytes())
    elif generated and (name != "dtg-credentials" or not run("generate_lock", "cargo", "+1.95.0", "generate-lockfile", timeout=300)):
        result["state"] = "dependency_blocked"
        return result
    if not lock.is_file():
        result["state"] = "dependency_blocked"
        return result
    result["lock_provenance"] = "supplied_verified" if supplied else ("generated" if generated else "tracked")
    result["lock_sha256_before"] = digest(lock)
    (out / "Cargo.lock").write_bytes(lock.read_bytes())
    ok = True
    for label, args in [
        ("metadata_default", ["metadata", "--locked", "--format-version", "1"]),
        ("metadata_no_default", ["metadata", "--locked", "--no-default-features", "--format-version", "1"]),
        ("features_default", ["tree", "--locked", "-e", "features"]),
        ("duplicates", ["tree", "--locked", "--duplicates"]),
    ]:
        ok = run(label, "cargo", "+1.95.0", *args, timeout=300) and ok
    profiles = CREDENTIAL_PROFILES if name == "dtg-credentials" else VTI_PROFILES
    result["profiles"] = {}
    for label, args in profiles.items():
        success = run("profile_" + label, "cargo", "+1.95.0", "tree", "--locked", "-e", "features", *args, timeout=90)
        result["profiles"][label] = "resolved" if success else "blocked"
        ok = success and ok
    result["lock_sha256_after"] = digest(lock) if lock.is_file() else None
    clean = run("tracked_diff", "git", "diff", "--exit-code", "HEAD")
    status_ok = run("final_status", "git", "status", "--porcelain", "--untracked-files=all")
    status = (out / "final_status.stdout").read_text().strip()
    expected_status = {"", "?? Cargo.lock"} if generated else {""}
    result["state"] = ("dependency_observed" if ok and clean and status_ok and status in expected_status
                       and result["lock_sha256_before"] == result["lock_sha256_after"] else "dependency_blocked")
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--credential-lock", type=Path)
    parser.add_argument("--credential-lock-sha256")
    args = parser.parse_args()
    if bool(args.credential_lock) != bool(args.credential_lock_sha256):
        parser.error("credential lock and expected SHA-256 must be supplied together")
    if args.credential_lock:
        args.credential_lock = args.credential_lock.resolve()
        if not args.credential_lock.is_file() or digest(args.credential_lock) != args.credential_lock_sha256:
            parser.error("credential lock missing or digest mismatch")
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    records = []
    for label, cmd in [("git", ["git", "--version"]), ("rustc", ["rustc", "+1.95.0", "--version", "--verbose"]), ("cargo", ["cargo", "+1.95.0", "--version"]), ("runner_head", ["git", "rev-parse", "HEAD"])]:
        command(Path.cwd(), out, label, cmd, records)
    results = []
    with tempfile.TemporaryDirectory(prefix="tpil-wp01-") as tmp:
        for repo, pin in PINS.items():
            results.append(collect(repo, pin, Path(tmp), out / repo.split("/")[-1], args.credential_lock, args.credential_lock_sha256))
    summary = {"scope": "source tree and cargo resolution only; no native build, test or conformance claim",
               "platform": platform.platform(), "run_id": os.environ.get("GITHUB_RUN_ID"),
               "runner_commands": records, "targets": results}
    (out / "observations.json").write_text(json.dumps(summary, indent=2) + "\n")
    files = sorted(p for p in out.rglob("*") if p.is_file())
    (out / "SHA256SUMS").write_text("".join(f"{digest(p)}  {p.relative_to(out)}\n" for p in files))
    good = all(r["exit"] == 0 for r in records) and all(
        r["state"] == ("dependency_observed" if r["repository"].split("/")[-1] in IMPLEMENTATIONS else "source_acquired")
        for r in results)
    return 0 if good else 1

if __name__ == "__main__":
    raise SystemExit(main())
