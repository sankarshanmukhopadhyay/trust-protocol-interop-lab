#!/usr/bin/env python3
"""Source-pinned VTI native regression observations after upstream #2402/#2404.

Does not rewrite frozen Eucalyptus, prove independent deployment, or issue RAHP PASS.
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
REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
TARGET_SHA = "2fc769fddbe2ee6f87a5b8a8ce048d8f5ffeef84"
CASE_ID = "IC-VTI-POSTFIX-CONSUMING-001"
# Each filter identifies an existing upstream target-native test. No synthetic PASS.
SCENARIOS = (
    ("error-evidenced", "RAHP-691", "vta-sdk", "well_formed_details_are_evidence", "lib"),
    ("error-missing-details", "RAHP-691", "vta-sdk", "absent_details_are_not_evidence", "lib"),
    ("error-empty-details", "RAHP-691", "vta-sdk", "an_empty_list_is_not_evidence", "lib"),
    ("error-malformed-details", "RAHP-691", "vta-sdk", "malformed_entries_are_not_an_empty_list", "lib"),
    ("error-wrong-code", "RAHP-691", "vta-sdk", "another_refusal_is_not_this_one_whatever_it_says", "lib"),
    ("deleted-false-not-success", "RAHP-691", "vta-cli-common", "a_declined_deletion_is_not_reported_as_done", "lib"),
    ("keyed-effect-survives-restart", "RAHP-966", "vta-service", "vti_ops_061_a_keyed_effect_survives_a_restart_once", "it"),
    ("post-effect-interruption-not-reexecuted", "RAHP-966", "vta-service", "vti_ops_061_an_attempt_interrupted_after_its_effect_is_never_rerun", "it"),
)
SOURCE_ANCHORS = {
    "vta-sdk/src/protocols/context_management/delete.rs": (
        "pub fn host_cleanup_refusal", "enum HostCleanupRefusal", "Unreadable", "well_formed_details_are_evidence",
        "absent_details_are_not_evidence", "an_empty_list_is_not_evidence",
        "malformed_entries_are_not_an_empty_list", "another_refusal_is_not_this_one_whatever_it_says",
    ),
    "vta-cli-common/src/commands/contexts.rs": (
        "HostCleanupRefusal::Evidenced", "HostCleanupRefusal::Unreadable",
        "fn deletion_outcome", "a_declined_deletion_is_not_reported_as_done",
    ),
    "vta-service/tests/it/idempotency_trust_task.rs": (
        "vti_ops_061_a_keyed_effect_survives_a_restart_once",
        "vti_ops_061_an_attempt_interrupted_after_its_effect_is_never_rerun",
    ),
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(path), *args], text=True,
                                   stderr=subprocess.PIPE, timeout=30).strip()


def admit(target: Path) -> list[dict]:
    if git(target, "rev-parse", "HEAD") != TARGET_SHA:
        raise ValueError("target is not the exact qualified post-fix revision")
    if git(target, "diff", "HEAD", "--"):
        raise ValueError("tracked VTI source differs from the admitted revision")
    sources = []
    for relative, anchors in SOURCE_ANCHORS.items():
        raw = (target / relative).read_bytes()
        source = raw.decode("utf-8")
        if any(anchor not in source for anchor in anchors):
            raise ValueError("source regression fixture missing: " + relative)
        sources.append({"path": relative, "sha256": digest(raw)})
    return sources


def command(package: str, test_name: str, kind: str) -> tuple[str, ...]:
    selector = ("--lib",) if kind == "lib" else ("--test", "it")
    return ("cargo", "test", "--locked", "-p", package, *selector, test_name)


def classify(code: int | None, stdout: str, timed_out: bool) -> tuple[str, dict]:
    counts = {"passed": 0, "failed": 0, "ignored": 0}
    for p, f, s in re.findall(r"test result: \w+\. (\d+) passed; (\d+) failed; (\d+) ignored;", stdout):
        counts["passed"] += int(p)
        counts["failed"] += int(f)
        counts["ignored"] += int(s)
    if timed_out or code is None:
        return "ATTEMPTED_UNAVAILABLE", counts
    if code == 0 and counts == {"passed": 1, "failed": 0, "ignored": 0}:
        return "EXECUTED_PASS", counts
    if code != 0 or counts["failed"]:
        return "EXECUTED_FAIL", counts
    return "ATTEMPTED_UNAVAILABLE", counts


def execute(target: Path, cmd: tuple[str, ...], timeout: int) -> tuple[int | None, str, str, bool]:
    p = subprocess.Popen(cmd, cwd=target, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return p.returncode, out, err, False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
        return p.returncode, out, err, True


def manifest(folder: Path) -> dict[str, str]:
    return {str(p.relative_to(folder)): digest(p.read_bytes()) for p in sorted(folder.rglob("*"))
            if p.is_file() and p.name != "integrity.json"}


def verify(folder: Path) -> dict:
    expected = json.loads((folder / "integrity.json").read_text())
    if expected != {"schema": "lab-evidence-integrity/v1", "sha256": manifest(folder)}:
        raise ValueError("evidence integrity mismatch")
    result = json.loads((folder / "result.json").read_text())
    if (result.get("target", {}).get("revision") != TARGET_SHA
            or result.get("assurance_state") != "INDETERMINATE"
            or result.get("composition_pass") != 0
            or result.get("discharged_propositions") != []
            or len(result.get("attempts", [])) != len(SCENARIOS)):
        raise ValueError("evidence qualification boundary mismatch")
    return result


def collect(target: Path, output: Path, timeout: int = 900) -> dict:
    if not 30 <= timeout <= 3600:
        raise ValueError("timeout outside 30..3600")
    if output.exists():
        raise ValueError("new output directory required")
    sources = admit(target)
    output.mkdir(parents=True)
    write(output / "contract.json", {
        "schema": "vti-postfix-native-evidence/v1", "case_id": CASE_ID,
        "target": {"repository": REPOSITORY, "revision": TARGET_SHA},
        "producer": {"repository": "sankarshanmukhopadhyay/trust-protocol-interop-lab",
                     "revision": git(ROOT, "rev-parse", "HEAD")},
        "source_inventory": sources, "created_at": datetime.now(timezone.utc).isoformat(),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "scenario_filters": [{"id": n, "proposition": p, "command": list(command(pkg, test, kind))}
                             for n, p, pkg, test, kind in SCENARIOS],
        "boundary": "Native upstream tests at a post-fix pin, not deployed cross-component assurance.",
    })
    attempts = []
    for name, proposition, package, test, kind in SCENARIOS:
        cmd = command(package, test, kind)
        start = time.monotonic()
        code, stdout, stderr, timed_out = execute(target, cmd, timeout)
        state, counts = classify(code, stdout, timed_out)
        logs = {}
        for stream, value in (("stdout", stdout), ("stderr", stderr)):
            path = output / f"{name}.{stream}.txt"
            path.write_text(value, encoding="utf-8")
            logs[stream] = {"path": path.name, "sha256": digest(path.read_bytes())}
        attempts.append({"id": name, "proposition": proposition,
                         "command": list(cmd), "state": state, "returncode": code,
                         "timed_out": timed_out, "counts": counts,
                         "duration_seconds": round(time.monotonic() - start, 3), "logs": logs})
        write(output / "attempts.json", attempts)
        admit(target)
    states = [a["state"] for a in attempts]
    result = {
        "case_id": CASE_ID, "target": {"repository": REPOSITORY, "revision": TARGET_SHA},
        "evidence_class": "target-native-postfix-regression",
        "status": ("partial" if all(x == "EXECUTED_PASS" for x in states) else
                   "fail" if "EXECUTED_FAIL" in states else "not-run"),
        "attempts": attempts, "assurance_state": "INDETERMINATE",
        "composition_pass": 0, "discharged_propositions": [],
        "limitations": [
            "Does not rerun or amend the frozen Eucalyptus source or historical observations.",
            "Rust integration fixtures are source-native but not independent deployed actors.",
            "Interrupted claim test injects the persisted post-effect state; it does not kill a live process mid-commit.",
            "No interactive CLI prompt or external host is exercised by the SDK/CLI unit vectors.",
        ],
    }
    write(output / "result.json", result)
    write(output / "integrity.json", {"schema": "lab-evidence-integrity/v1", "sha256": manifest(output)})
    verify(output)
    return result


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--target", type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--verify", type=Path)
    p.add_argument("--require-native-pass", action="store_true")
    p.add_argument("--timeout-seconds", type=int, default=900)
    args = p.parse_args()
    try:
        result = (verify(args.verify) if args.verify else
                  collect(args.target.resolve(), args.output.resolve(), args.timeout_seconds)
                  if args.target and args.output else None)
        if result is None:
            p.error("provide --verify or both --target and --output")
        print(json.dumps({"status": result["status"],
                          "assurance_state": result["assurance_state"],
                          "vectors": [(a["id"], a["state"]) for a in result["attempts"]]}, indent=2))
        return 0 if not args.require_native_pass or result["status"] == "partial" else 2
    except (OSError, ValueError, subprocess.SubprocessError, UnicodeError) as e:
        print(f"VTI post-fix evidence unavailable: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
