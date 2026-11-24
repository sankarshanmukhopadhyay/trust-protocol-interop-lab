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

def collect(repo, pin, work, out):
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
    if generated and (name != "dtg-credentials" or not run("generate_lock", "cargo", "+1.95.0", "generate-lockfile", timeout=300)):
        result["state"] = "dependency_blocked"
        return result
    if not lock.is_file():
        result["state"] = "dependency_blocked"
        return result
    result["lock_provenance"] = "generated" if generated else "tracked"
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
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    records = []
    for label, cmd in [("git", ["git", "--version"]), ("rustc", ["rustc", "+1.95.0", "--version", "--verbose"]), ("cargo", ["cargo", "+1.95.0", "--version"]), ("runner_head", ["git", "rev-parse", "HEAD"])]:
        command(Path.cwd(), out, label, cmd, records)
    results = []
    with tempfile.TemporaryDirectory(prefix="tpil-wp01-") as tmp:
        for repo, pin in PINS.items():
            results.append(collect(repo, pin, Path(tmp), out / repo.split("/")[-1]))
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
