#!/usr/bin/env python3
"""Execute one context-distinct Dogwood RC-1 pressure observation.

This target-specific adapter deliberately varies the deterministic client key seed
between A and B while reusing the established Dogwood runtime observation adapter.
It changes no generic capture/classification/export semantics and makes no privacy
judgment itself.
"""
from __future__ import annotations

import argparse
import json
import sys
import textwrap
from pathlib import Path

import dogwood_rc1_context as base


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout",
        type=Path,
        default=Path(base.os.environ.get("DOGWOOD_CHECKOUT", "build/dogwood-rc1")),
    )
    parser.add_argument("--context", choices=["A", "B"], required=True)
    parser.add_argument("--verifier", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--challenge", required=True)
    parser.add_argument("--client-seed", type=lambda value: int(value, 0), required=True)
    args = parser.parse_args()

    if not 0 <= args.client_seed <= 255:
        raise ValueError("--client-seed must fit in one byte")

    needle = "did_key_from_seed(0x11)"
    replacement = f"did_key_from_seed(0x{args.client_seed:02x})"
    if base.PROBE.count(needle) != 1:
        raise RuntimeError("Dogwood positive-control probe shape changed; pressure adapter must be reviewed")

    # The base adapter remains the positive-control implementation. This wrapper
    # changes only the target fixture's deterministic client key for this invocation.
    base.PROBE = base.PROBE.replace(needle, replacement)
    result = base.execute_context(
        args.checkout.resolve(),
        args.context,
        args.verifier,
        args.purpose,
        args.challenge,
    )
    result["pressure_fixture"] = {
        "client_seed": f"0x{args.client_seed:02x}",
        "relationship_seed_shared_across_contexts": False,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(textwrap.fill(f"ERROR: {exc}", width=120), file=sys.stderr)
        raise SystemExit(2)
