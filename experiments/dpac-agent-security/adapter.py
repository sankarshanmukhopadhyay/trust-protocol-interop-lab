#!/usr/bin/env python3
"""Test-only HTTP translation boundary for the pinned Agent Security Harness.

This adapter does not implement DPAC policy. It translates two narrow external
harness surfaces into calls to the existing Workspace enforcement point:

* delegation replay: maps the upstream request identifier to a DPAC nonce and
  otherwise constructs a valid bounded loan-approval request. Only replay
  semantics are claimed from this mapping; delegation attenuation semantics are
  deliberately not inferred from the external chain.
* governance mutation: forwards mutation attempts to Workspace's admin-policy
  surface unchanged. Workspace owns the refusal; the adapter does not synthesize
  a denial.

Every forwarded call is exposed through /audit so the Lab runner can establish
that a harness verdict came from a request that actually reached the intended
Workspace surface.
"""
from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

WORKSPACE_URL = os.environ.get("WORKSPACE_URL", "http://workspace:8080").rstrip("/")
AUDIT: list[dict[str, Any]] = []


def http_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw or "{}")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            body = json.loads(raw or "{}")
        except json.JSONDecodeError:
            body = {"raw": raw[:500]}
        return exc.code, body
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return 0, {"reason": "workspace_unavailable", "error": type(exc).__name__}


def replay_translation(payload: dict[str, Any]) -> tuple[int, dict]:
    request = payload.get("request")
    if not isinstance(request, dict) or not isinstance(request.get("request_id"), str):
        return 400, {"allowed": False, "adapter_error": "missing request.request_id"}

    request_id = request["request_id"]
    resource = str(request.get("resource", "external-harness-resource"))
    loan_id = "ASH-" + hashlib.sha256(resource.encode("utf-8")).hexdigest()[:12].upper()
    amount = 100000
    dpac_request = {
        "action": "approve",
        "loan_id": loan_id,
        "amount_inr": amount,
        "nonce": f"ash:{request_id}",
        "expected_capability_revision": "policy-v1",
        "authority": {
            "current": True,
            "limit_inr": 5000000,
            "bound_loan_id": loan_id,
            "bound_amount_inr": amount,
        },
    }

    status, body = http_json("POST", f"{WORKSPACE_URL}/actuate", dpac_request)
    allowed = status == 200 and body.get("actuated") is True
    receipt = None
    if allowed and isinstance(body.get("effect"), dict):
        receipt = body["effect"].get("effect_id")

    AUDIT.append({
        "surface": "delegation-replay",
        "external_request_id": request_id,
        "dpac_nonce": dpac_request["nonce"],
        "workspace_status": status,
        "workspace_reason": body.get("reason"),
        "actuated": body.get("actuated"),
        "receipt": receipt,
    })
    response: dict[str, Any] = {
        "allowed": allowed,
        "dpac_reason": body.get("reason"),
        "adapter_mapping": "delegation-request-id-to-dpac-nonce-v1",
    }
    if receipt:
        response["receipt"] = receipt
    return 200, response


def governance_forward(payload: dict[str, Any]) -> tuple[int, dict]:
    status, body = http_json("POST", f"{WORKSPACE_URL}/admin/policy", payload)
    AUDIT.append({
        "surface": "governance-mutation",
        "workspace_status": status,
        "workspace_reason": body.get("reason"),
        "method": payload.get("method"),
    })
    # Preserve the Workspace status. An explicit 404/405 is therefore a refusal
    # by the target surface, not a denial invented by this adapter.
    return status or 503, body


class Handler(BaseHTTPRequestHandler):
    def _json(self, status: int, body: Any) -> None:
        data = json.dumps(body, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _payload(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length).decode("utf-8")
        parsed = json.loads(raw or "{}")
        if not isinstance(parsed, dict):
            raise ValueError("request body must be an object")
        return parsed

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            status, body = http_json("GET", f"{WORKSPACE_URL}/status")
            self._json(200 if status == 200 else 503, {"ok": status == 200, "workspace": body})
            return
        if self.path == "/audit":
            self._json(200, {"events": AUDIT})
            return
        self._json(404, {"reason": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            payload = self._payload()
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"reason": "malformed_request"})
            return
        if self.path == "/delegation":
            status, body = replay_translation(payload)
            self._json(status, body)
            return
        if self.path == "/governance":
            status, body = governance_forward(payload)
            self._json(status, body)
            return
        self._json(404, {"reason": "not_found"})

    def log_message(self, format: str, *args: object) -> None:
        return


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
