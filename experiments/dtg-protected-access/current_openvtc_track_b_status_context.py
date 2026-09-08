#!/usr/bin/env python3
"""Observe current OpenVTC status-list surfaces through its own integration test.

The Interop Lab only orchestrates the run. The executed behavior belongs to the
immutable OpenVTC checkout supplied via OPENVTC_CHECKOUT. This adapter deliberately
records no policy or Trust Task surface because this target test does not exercise them.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

OPENVTC_REPOSITORY = "OpenVTC/verifiable-trust-infrastructure"
OPENVTC_REVISION = "72bf5794071971da506eb7a5af8e4765c35c137c"
STATUS_HANDLE = "revocation"
STATUS_ENDPOINT = "https://vtc.example.com/v1/status-lists/revocation"


def run(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=cwd, text=True, capture_output=True, check=False)


def verify_checkout(checkout: Path) -> None:
    head = run("git", "rev-parse", "HEAD", cwd=checkout)
    if head.returncode != 0:
        raise RuntimeError(head.stderr.strip() or "cannot resolve OpenVTC checkout HEAD")
    if head.stdout.strip() != OPENVTC_REVISION:
        raise ValueError(
            f"OpenVTC checkout must be pinned to {OPENVTC_REVISION}; observed {head.stdout.strip()}"
        )


def observe(checkout: Path, context: str) -> dict[str, object]:
    verify_checkout(checkout)
    completed = run(
        "cargo",
        "test",
        "-p",
        "vtc-service",
        "--test",
        "status_lists",
        "show_returns_signed_vc_without_trust_task_header",
        "--",
        "--exact",
        "--nocapture",
        cwd=checkout,
    )
    if completed.returncode != 0:
        detail = "\n".join(x for x in (completed.stdout.strip(), completed.stderr.strip()) if x)
        raise RuntimeError(f"OpenVTC status-list integration test failed:\n{detail[-12000:]}")

    return {
        "run_id": f"current-openvtc-track-b-status-{context.lower()}-{uuid.uuid4()}",
        "implementation_repository": OPENVTC_REPOSITORY,
        "implementation_revision": OPENVTC_REVISION,
        "executed_surfaces": ["status_handle", "status_endpoint"],
        "observations": {
            "status_handle": STATUS_HANDLE,
            "status_endpoint": STATUS_ENDPOINT,
            "policy_discovery_handle": None,
            "policy_endpoint": None,
            "task_identifier": None,
            "thread_identifier": None,
            "retained_relationship_evidence": None,
            "retained_outcome_evidence": None,
        },
        "producer_component": OPENVTC_REPOSITORY,
        "assurance_boundary": (
            "The target's own status-list integration test executed and verified a signed "
            "revocation status-list response. Policy-discovery and Trust Task surfaces were "
            "not executed and therefore remain not-evidenced."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        type=Path,
        default=Path(os.environ.get("OPENVTC_CHECKOUT", "build/current-openvtc")),
    )
    parser.add_argument("--context", choices=["A", "B"], required=True)
    args = parser.parse_args()
    print(json.dumps(observe(args.checkout.resolve(), args.context), sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
