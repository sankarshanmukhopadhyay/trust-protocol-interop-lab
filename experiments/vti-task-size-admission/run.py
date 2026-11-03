#!/usr/bin/env python3
"""Source-pinned VTI task-size admission evidence for RAHP #1174.

Native source tests do not establish signed end-to-end consumer admission.
No RAHP PASS is issued from component-only evidence.
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
TARGET_SHA = "9d781a7333a198ef24ec229f59ff8fbcae3b1346"
CASE_ID = "IC-VTI-SIZE-ADMISSION-1174"
# Each filter identifies an existing upstream target-native test. No synthetic PASS.
SCENARIOS = (
    ("declared-limit-mapping", "RAHP-1174", "vtc-service", "a_declared_limit_is_the_specifications_own", "lib"),
    ("at-limit-admission", "RAHP-1174", "vtc-service", "a_document_at_its_types_limit_is_admitted", "lib"),
    ("over-raised-limit", "RAHP-1174", "vtc-service", "a_document_over_its_raised_limit_is_refused", "lib"),
    ("undeclared-default-limit", "RAHP-1174", "vtc-service", "a_document_over_the_default_is_refused_for_a_type_that_declares_nothing", "lib"),
    ("standing-and-budget-boundary", "RAHP-1174", "vtc-service", "a_raised_limit_needs_an_issuer_with_standing", "lib"),
)
SOURCE_ANCHORS = {
    "vtc-service/src/trust_tasks/size.rs": (
        "a_declared_limit_is_the_specifications_own",
        "a_document_at_its_types_limit_is_admitted",
        "a_document_over_its_raised_limit_is_refused",
        "a_document_over_the_default_is_refused_for_a_type_that_declares_nothing",
        "a_raised_limit_needs_an_issuer_with_standing",
        "LARGE_DOCUMENT_GLOBAL_BUDGET_PER_WINDOW",
    ),
    "vti-specs-vtc/trust-tasks/vtc/website/upload/chunk/0.1.bundle.json": (
        '"maxDocumentBytes":{"request":360448,"response":null}',
    ),
    "vti-specs-vtc/trust-tasks/vtc/website/upload/begin/0.1.bundle.json": (
        '"maxDocumentBytes":{"request":262144,"response":null}',
    ),
    "vti-specs-vtc/trust-tasks/vtc/members/update/0.1.bundle.json": (
        '"maxDocumentBytes":{"request":null,"response":null}',
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
        "schema": "vti-size-admission-native-evidence/v1", "case_id": CASE_ID,
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
        "evidence_class": "target-native-size-gate-regression",
        "status": ("partial" if all(x == "EXECUTED_PASS" for x in states) else
                   "fail" if "EXECUTED_FAIL" in states else "not-run"),
        "attempts": attempts, "assurance_state": "INDETERMINATE",
        "composition_pass": 0, "discharged_propositions": [],
        "limitations": [
            "The existing target-native tests exercise the size-gate and source policy mapping, not a complete signed/authorized request through the actual consumer endpoint.",
            "The fixture does not execute separate 262144-byte and 360448-byte signed tasks at every exact boundary.",
            "A signed in-bound request may still fail another independent authorization or policy check; success is not required to establish admission-only behavior.",
            "The presence of maxDocumentBytes in a bundle or binding is not alone evidence of enforced transport admission.",
            "No cross-transport, deployment, denial-of-service, or composed assurance PASS is inferred.",
        
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
        print(f"VTI task-size evidence unavailable: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
