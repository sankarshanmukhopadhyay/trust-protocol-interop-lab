#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

POLICY = Path(os.environ.get("CAPABILITY_POLICY", "/policy/policy.json"))
TOKEN_FILE = Path(os.environ.get("ACTUATOR_TOKEN_FILE", "/run/secrets/actuator-token"))
STATE = Path("/state/consumed.json")
ACTUATOR_URL = os.environ.get("ACTUATOR_URL", "http://actuator:8081/effect")


def load_policy() -> tuple[dict[str, Any], str]:
    raw = POLICY.read_bytes()
    parsed = json.loads(raw.decode())
    if not isinstance(parsed.get("revision"), str) or not isinstance(parsed.get("capabilities"), dict):
        raise ValueError("capability policy missing required fields")
    return parsed, hashlib.sha256(raw).hexdigest()


def consumed() -> set[str]:
    if not STATE.exists():
        return set()
    return set(json.loads(STATE.read_text(encoding="utf-8")))


def mark_consumed(nonce: str) -> None:
    values = consumed()
    values.add(nonce)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(sorted(values)), encoding="utf-8")


def canonical_digest(payload: dict[str, Any]) -> str:
    bound = {
        "action": payload["action"],
        "loan_id": payload["loan_id"],
        "amount_inr": payload["amount_inr"],
        "nonce": payload["nonce"],
    }
    return hashlib.sha256(json.dumps(bound, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def deny(reason: str, *, evidence_state: str = "complete", policy_revision: str | None = None, policy_digest: str | None = None) -> tuple[int, dict]:
    body: dict[str, Any] = {
        "actuated": False,
        "reason": reason,
        "evidence_state": evidence_state,
        "workspace_uid": os.getuid(),
    }
    if policy_revision is not None:
        body["policy_revision"] = policy_revision
    if policy_digest is not None:
        body["policy_digest"] = policy_digest
    return 409, body


def evaluate(payload: dict[str, Any]) -> tuple[int, dict]:
    required = {"action", "loan_id", "amount_inr", "nonce", "expected_capability_revision", "authority"}
    if required - payload.keys():
        return deny("indeterminate_request", evidence_state="indeterminate")
    authority = payload.get("authority")
    if not isinstance(authority, dict):
        return deny("indeterminate_authority", evidence_state="indeterminate")
    authority_required = {"current", "limit_inr", "bound_loan_id", "bound_amount_inr"}
    if authority_required - authority.keys():
        return deny("indeterminate_authority", evidence_state="indeterminate")

    try:
        policy, policy_digest = load_policy()
        revision = policy["revision"]
        capability = policy["capabilities"].get("loan-approve")
        if not isinstance(capability, dict):
            raise ValueError("loan-approve capability unavailable")
    except (OSError, ValueError, json.JSONDecodeError, TypeError):
        return deny("indeterminate_capability", evidence_state="indeterminate")

    if payload["expected_capability_revision"] != revision:
        return deny("capability_state_changed", policy_revision=revision, policy_digest=policy_digest)
    if payload["nonce"] in consumed():
        return deny("replay", policy_revision=revision, policy_digest=policy_digest)
    if authority["current"] is not True:
        return deny("authority_not_current", policy_revision=revision, policy_digest=policy_digest)
    if payload["amount_inr"] > authority["limit_inr"]:
        return deny("authority_scope_exceeded", policy_revision=revision, policy_digest=policy_digest)
    if payload["loan_id"] != authority["bound_loan_id"] or payload["amount_inr"] != authority["bound_amount_inr"]:
        return deny("authority_binding_mismatch", policy_revision=revision, policy_digest=policy_digest)
    if payload["action"] != capability.get("action") or payload["amount_inr"] > capability.get("max_amount_inr", -1):
        return deny("capability_scope_exceeded", policy_revision=revision, policy_digest=policy_digest)

    request_digest = canonical_digest(payload)
    actuator_payload = {
        "action": payload["action"],
        "loan_id": payload["loan_id"],
        "amount_inr": payload["amount_inr"],
        "nonce": payload["nonce"],
        "request_digest": request_digest,
    }
    request = urllib.request.Request(
        ACTUATOR_URL,
        data=json.dumps(actuator_payload).encode(),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TOKEN_FILE.read_text(encoding='utf-8').strip()}",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            actuator = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        actuator = json.loads(exc.read().decode() or "{}")
        return deny(f"actuator_rejected:{actuator.get('reason', exc.code)}", policy_revision=revision, policy_digest=policy_digest)
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return deny("actuator_unavailable", evidence_state="indeterminate", policy_revision=revision, policy_digest=policy_digest)

    mark_consumed(payload["nonce"])
    return 200, {
        "actuated": True,
        "reason": "concurrence",
        "evidence_state": "complete",
        "workspace_uid": os.getuid(),
        "policy_revision": revision,
        "policy_digest": policy_digest,
        "request_digest": request_digest,
        "effect": actuator.get("effect"),
    }


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, body: dict) -> None:
        data = json.dumps(body, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/status":
            try:
                policy, digest = load_policy()
                self._json(200, {"workspace_uid": os.getuid(), "policy_revision": policy["revision"], "policy_digest": digest})
            except (OSError, ValueError, json.JSONDecodeError, TypeError):
                self._json(503, {"reason": "indeterminate_capability", "workspace_uid": os.getuid()})
            return
        self._json(404, {"reason": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/actuate":
            self._json(404, {"reason": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode() or "{}")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"actuated": False, "reason": "malformed_request", "evidence_state": "indeterminate"})
            return
        status, body = evaluate(payload)
        self._json(status, body)

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
