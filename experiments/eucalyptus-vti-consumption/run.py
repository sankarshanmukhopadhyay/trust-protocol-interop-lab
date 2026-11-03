#!/usr/bin/env python3
"""Collect genuine frozen Eucalyptus native consuming-fixture observations.

This does not simulate runtime traces, mint authority or issue RAHP/DPIP assurance.
External deployment, restart persistence and independently operated parties remain out of scope.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
TARGET_REPO = "OpenVTC/verifiable-trust-infrastructure"
TARGET_SHA = "49f5f1beb61adc34bdf7cf0bd3eb10f594415b80"
CASE_ID = "IC-VTI-EUCALYPTUS-CONSUMING-001"
# Test functions are verified from the pinned upstream tree, not a new Lab fixture.
SCENARIOS = (
    ("positive-sealed-tsp", "EUC-06", ("cargo", "test", "--locked", "-p", "vti-e2e-tests",
       "--test", "tsp_vta_trust_task", "a_tsp_sealed_secret_is_unsealed_by_a_running_vta")),
    ("negative-unauthorized-tsp", "EUC-01", ("cargo", "test", "--locked", "-p", "vti-e2e-tests",
       "--test", "tsp_vta_trust_task", "an_unauthorized_sender_is_refused_over_tsp_not_met_with_silence")),
    ("replay-same-key-effect", "EUC-05", ("cargo", "test", "--locked", "-p", "vta-service",
       "--test", "it", "a_retry_under_the_same_key_converges_to_one_effect")),
    ("replay-changed-payload", "EUC-05", ("cargo", "test", "--locked", "-p", "vta-service",
       "--test", "it", "the_same_key_with_a_different_payload_is_refused")),
)
MISSING = (
    "post-restart durable effect comparison is not exercised",
    "deployment-level policy/status/revocation freshness is not observed",
    "independent real participants and external observer evidence are not established",
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git(target: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(target), *args], text=True,
                                   stderr=subprocess.PIPE, timeout=30).strip()


def verify_target(target: Path) -> None:
    if git(target, "rev-parse", "HEAD") != TARGET_SHA:
        raise ValueError("target revision does not equal immutable Eucalyptus revision")
    if git(target, "diff", "HEAD", "--"):
        raise ValueError("target tracked source changed since pinned commit")
    for relative, needle in (
        ("tests/e2e/tests/tsp_vta_trust_task.rs", "an_unauthorized_sender_is_refused_over_tsp_not_met_with_silence"),
        ("vta-service/tests/it/idempotency_trust_task.rs", "a_retry_under_the_same_key_converges_to_one_effect"),
    ):
        if needle not in (target / relative).read_text(encoding="utf-8"):
            raise ValueError("pinned target test evidence anchor missing: " + relative)


def classify(command: tuple[str, ...], code: int | None, stdout: str, timed_out: bool) -> tuple[str, dict]:
    counts = {"passed": 0, "failed": 0, "skipped": 0}
    for p, f, s in re.findall(r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored;", stdout):
        counts["passed"] += int(p); counts["failed"] += int(f); counts["skipped"] += int(s)
    if timed_out or code is None:
        return "ATTEMPTED_UNAVAILABLE", counts
    if code == 0 and counts["passed"] == 1 and counts["failed"] == 0:
        return "EXECUTED_PASS", counts
    if counts["failed"] > 0:
        return "EXECUTED_NONZERO", counts
    return "ATTEMPTED_UNAVAILABLE", counts


def execute(target: Path, command: tuple[str, ...], timeout: int) -> tuple[int | None, str, str, bool]:
    proc = subprocess.Popen(command, cwd=target, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
        return proc.returncode, out, err, False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        out, err = proc.communicate()
        return proc.returncode, out, err, True


def seal(folder: Path) -> None:
    entries = {str(p.relative_to(folder)): sha(p.read_bytes()) for p in sorted(folder.rglob("*"))
               if p.is_file() and p.name != "integrity.json"}
    write(folder / "integrity.json", {"schema": "lab-evidence-integrity/v1", "sha256": entries})


def verify_packet(folder: Path) -> dict:
    manifest = json.loads((folder / "integrity.json").read_text(encoding="utf-8"))
    actual = {str(p.relative_to(folder)): sha(p.read_bytes()) for p in sorted(folder.rglob("*"))
              if p.is_file() and p.name != "integrity.json"}
    if manifest.get("schema") != "lab-evidence-integrity/v1" or manifest.get("sha256") != actual:
        raise ValueError("Eucalyptus evidence integrity mismatch (missing, extra or altered files)")
    result = json.loads((folder / "result.json").read_text(encoding="utf-8"))
    if result.get("target", {}).get("revision") != TARGET_SHA:
        raise ValueError("Eucalyptus target pin mismatch in result")
    if result.get("assurance_state") != "INDETERMINATE" or result.get("composition_pass") != 0:
        raise ValueError("consuming-fixture observations must not become composition PASS")
    return result


def collect(target: Path, output: Path, timeout: int = 900) -> dict:
    if not 30 <= timeout <= 3600:
        raise ValueError("timeout out of 30..3600 bound")
    if output.exists():
        raise ValueError("fresh output directory required; do not overwrite evidence")
    verify_target(target)
    output.mkdir(parents=True)
    write(output / "run-contract.json", {
        "schema": "interop-eucalyptus-native-contract/v1",
        "target": {"repository": TARGET_REPO, "revision": TARGET_SHA},
        "producer": {"repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab",
                     "revision": git(ROOT, "rev-parse", "HEAD")},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "runner_sha256": sha(Path(__file__).read_bytes()),
        "scenarios": [{"id": name, "proposition": prop, "command": list(cmd)} for name, prop, cmd in SCENARIOS],
        "timeout_seconds": timeout,
        "boundary": "Pinned in-process consuming fixtures; no independent real-party, restart or deployed-system inference.",
    })
    results = []
    for name, proposition, command in SCENARIOS:
        begun = time.monotonic()
        code, stdout, stderr, timed_out = execute(target, command, timeout)
        state, counts = classify(command, code, stdout, timed_out)
        logs = {}
        for stream, content in (("stdout", stdout), ("stderr", stderr)):
            dest = output / f"{name}.{stream}.txt"
            dest.write_text(content, encoding="utf-8")
            logs[stream] = {"path": dest.name, "sha256": sha(dest.read_bytes())}
        results.append({"id": name, "proposition": proposition, "command": list(command),
                        "state": state, "returncode": code, "timed_out": timed_out,
                        "duration_seconds": round(time.monotonic() - begun, 3),
                        "native_test_counts": counts, "logs": logs,
                        "evidence_class": "target-native-consuming-fixture"})
        write(output / "attempts.json", results)
        verify_target(target)
    statuses = [r["state"] for r in results]
    result = {
        "case_id": CASE_ID,
        "result_id": "eucalyptus-native-consuming:" + TARGET_SHA,
        "status": "partial" if all(s == "EXECUTED_PASS" for s in statuses) else (
            "fail" if "EXECUTED_NONZERO" in statuses else "not-run"),
        "observations": [
            f"{r['id']}: {r['state']} ({r['native_test_counts']['passed']} passing native tests)"
            for r in results],
        "vectors": [name for name, _, _ in SCENARIOS],
        "evidence_manifest": "integrity.json",
        "target": {"repository": TARGET_REPO, "revision": TARGET_SHA},
        "evidence_class": "target-native-consuming-fixture",
        "attempts": results,
        "assurance_state": "INDETERMINATE",
        "composition_pass": 0,
        "discharged_euc_propositions": [],
        "limitations": list(MISSING),
    }
    write(output / "result.json", result)
    seal(output)
    verify_packet(output)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--target", type=Path)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--timeout-seconds", type=int, default=900)
    ap.add_argument("--verify", type=Path)
    ap.add_argument("--require-native-pass", action="store_true")
    args = ap.parse_args()
    try:
        if args.verify:
            result = verify_packet(args.verify)
        else:
            if not args.target or not args.output:
                ap.error("--target and --output are required for collection")
            result = collect(args.target.resolve(), args.output.resolve(), args.timeout_seconds)
        print(json.dumps({"status": result["status"], "observations": result["observations"],
                          "assurance_state": result["assurance_state"]}, indent=2))
        if args.require_native_pass and result["status"] != "partial":
            return 2
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f"Eucalyptus consuming evidence unavailable: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
