#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TOKEN_FILE = Path(os.environ.get("ACTUATOR_TOKEN_FILE", "/run/secrets/actuator-token"))
JOURNAL = Path("/journal/effects.jsonl")


def token() -> str:
    return TOKEN_FILE.read_text(encoding="utf-8").strip()


def effects() -> list[dict]:
    if not JOURNAL.exists():
        return []
    return [json.loads(line) for line in JOURNAL.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_effect(payload: dict) -> tuple[bool, dict]:
    nonce = payload.get("nonce")
    request_digest = payload.get("request_digest")
    if not nonce or not request_digest:
        return False, {"reason": "missing_actuator_binding"}
    existing = effects()
    if any(item.get("nonce") == nonce for item in existing):
        return False, {"reason": "duplicate_effect", "effect_count": len(existing)}
    effect_id = "effect:" + hashlib.sha256(f"{nonce}:{request_digest}".encode()).hexdigest()[:16]
    record = {
        "effect_id": effect_id,
        "nonce": nonce,
        "request_digest": request_digest,
        "action": payload.get("action"),
        "loan_id": payload.get("loan_id"),
        "amount_inr": payload.get("amount_inr"),
    }
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return True, {"reason": "effect_recorded", "effect": record, "effect_count": len(existing) + 1}


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, body: dict) -> None:
        data = json.dumps(body, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json(200, {"ok": True})
            return
        self._json(404, {"reason": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/effect":
            self._json(404, {"reason": "not_found"})
            return
        if self.headers.get("Authorization") != f"Bearer {token()}":
            self._json(403, {"reason": "workspace_auth_required"})
            return
        length = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(length).decode() or "{}")
        created, body = append_effect(payload)
        self._json(201 if created else 409, body)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "serve"
    if command == "count":
        print(len(effects()))
        return 0
    if command == "dump":
        print(json.dumps(effects(), sort_keys=True))
        return 0
    if command == "serve":
        ThreadingHTTPServer(("0.0.0.0", 8081), Handler).serve_forever()
        return 0
    raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    raise SystemExit(main())
