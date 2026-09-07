#!/usr/bin/env python3
"""Local application demonstrator for IC-PDC-MED-001.

Synthetic data only. The HTTP/UI layer never grants authority: consequential caregiver
requests are delegated to CareCore.execute_exception_response(), which re-evaluates
current authority immediately before effect.
"""
from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from core import Task, build_active_exception_core

MAX_BODY_BYTES = 16_384


class PDCApplication:
    """Small application-facing boundary around the deterministic PDC core."""

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> dict[str, Any]:
        self.core = build_active_exception_core()
        self.request_sequence = 0
        return self.view()

    def view(self) -> dict[str, Any]:
        payload = self.core.safe_exception_payload()
        validation = self.core.validate_exception_payload(payload)
        return {
            "case": "IC-PDC-MED-001",
            "maturity": "Experimental",
            "synthetic": True,
            "authoritative_state": self.core.snapshot(),
            "caregiver_exception": payload
            if validation["authorization"] == "permit"
            else None,
            "evidence": list(self.core.evidence),
            "assurance_boundary": (
                "Application-owned demonstrator; unresolved upstream/runtime "
                "assurance boundaries remain unresolved."
            ),
        }

    def request_re_reminder(self) -> dict[str, Any]:
        """Create a fresh bounded task and execute it through the current-authority gate."""
        self.request_sequence += 1
        self.core.task = Task(
            id=f"task:demo-{self.request_sequence:03d}",
            resource=self.core.reminder.id,
        )
        result = self.core.execute_exception_response()
        return {"result": result, "view": self.view()}

    def revoke(self) -> dict[str, Any]:
        """Revoke the synthetic delegation and retain append-only lifecycle evidence."""
        changed = self.core.delegation.status != "revoked"
        self.core.delegation.status = "revoked"
        if changed:
            self.core.evidence.append(
                {
                    "event": "delegation_revoked",
                    "delegation": self.core.delegation.id,
                    "policy_version": "pdc-policy-v1",
                    "observed_at": "2026-09-05T08:00:00Z",
                }
            )
        return {
            "result": {
                "authorization": "permit",
                "changed": changed,
                "delegation_status": self.core.delegation.status,
            },
            "view": self.view(),
        }

    def remove_authority_evidence(self) -> dict[str, Any]:
        """Pressure-test the fail-closed missing-evidence boundary."""
        self.core.delegation.evidence_present = False
        return {
            "result": {
                "authorization": "permit",
                "changed": True,
                "evidence_present": False,
            },
            "view": self.view(),
        }


def parse_json_body(raw: bytes) -> dict[str, Any]:
    """Accept only bounded UTF-8 JSON objects at the local HTTP boundary."""
    if len(raw) > MAX_BODY_BYTES:
        raise ValueError("request body too large")
    if not raw:
        return {}
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("request body must be valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise ValueError("request body must be a JSON object")
    return value


HTML = r'''<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Protected Delegated Care</title>
<style>
body{font:16px system-ui,sans-serif;max-width:1100px;margin:0 auto;padding:24px;background:#f6f7f8;color:#17191c}
h1{margin-bottom:4px}.sub{color:#5a626c}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:22px}
.card{background:#fff;border:1px solid #dfe3e7;border-radius:10px;padding:18px}button{padding:9px 13px;margin:4px 4px 4px 0;border:1px solid #777;border-radius:7px;background:white;cursor:pointer}
button.primary{background:#17191c;color:white}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f3f4;padding:12px;border-radius:7px;font-size:13px}.badge{display:inline-block;padding:3px 8px;border-radius:12px;background:#eceff1;font-size:12px}.warning{border-left:4px solid #777;padding-left:12px}
</style></head><body>
<h1>Protected Delegated Care</h1><div class="sub">IC-PDC-MED-001 · synthetic application demonstrator · <span class="badge">Experimental</span></div>
<p class="warning">This demonstrates bounded delegation and evidence semantics. It is not a medical, prescribing, pharmacy, messaging-provider, or production identity system.</p>
<div class="grid">
<section class="card"><h2>Principal</h2><p>Controls the bounded caregiver delegation.</p><div id="delegation"></div><button onclick="post('/api/delegation/revoke')">Revoke delegation</button><button onclick="post('/api/reset')">Reset demo</button><button onclick="post('/api/authority-evidence/remove')">Remove authority evidence</button></section>
<section class="card"><h2>Caregiver</h2><p>Receives only the declared exception payload, not the medication plan.</p><pre id="exception"></pre><button class="primary" onclick="post('/api/caregiver/re-reminder')">Request re-reminder</button><div id="decision"></div></section>
<section class="card"><h2>Evidence</h2><p>Authorization and effect records generated by the deterministic core.</p><pre id="evidence"></pre></section>
</div><section class="card" style="margin-top:16px"><h2>Authoritative state</h2><pre id="state"></pre></section>
<script>
let last=null;
async function load(){const r=await fetch('/api/state');render(await r.json())}
async function post(path){const r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json'},body:'{}'});const x=await r.json();if(x.error){document.getElementById('decision').textContent=x.error;return}last=x.result||null;render(x.view||x)}
function render(v){document.getElementById('delegation').innerHTML='<p>Status: <b>'+v.authoritative_state.delegation.status+'</b><br>Evidence present: <b>'+v.authoritative_state.delegation.evidence_present+'</b></p>';document.getElementById('exception').textContent=JSON.stringify(v.caregiver_exception,null,2);document.getElementById('evidence').textContent=JSON.stringify(v.evidence,null,2);document.getElementById('state').textContent=JSON.stringify(v.authoritative_state,null,2);document.getElementById('decision').innerHTML=last?'<p>Latest decision: <b>'+String(last.authorization).toUpperCase()+'</b>'+(last.reason?' · '+last.reason:'')+'</p>':''}
load();
</script></body></html>'''


def make_handler(application: PDCApplication):
    class Handler(BaseHTTPRequestHandler):
        def _send(
            self,
            status: int,
            body: bytes,
            content_type: str = "application/json; charset=utf-8",
        ) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            self._send(
                status,
                json.dumps(payload, sort_keys=True).encode("utf-8"),
                "application/json; charset=utf-8",
            )

        def do_GET(self) -> None:
            if self.path == "/":
                self._send(200, HTML.encode("utf-8"), "text/html; charset=utf-8")
                return
            if self.path == "/api/state":
                self._json(200, application.view())
                return
            self._json(404, {"error": "not found"})

        def do_POST(self) -> None:
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > MAX_BODY_BYTES:
                    raise ValueError("invalid request body length")
                parse_json_body(self.rfile.read(length))
                routes = {
                    "/api/reset": application.reset,
                    "/api/caregiver/re-reminder": application.request_re_reminder,
                    "/api/delegation/revoke": application.revoke,
                    "/api/authority-evidence/remove": application.remove_authority_evidence,
                }
                operation = routes.get(self.path)
                if operation is None:
                    self._json(404, {"error": "not found"})
                    return
                result = operation()
                self._json(
                    200,
                    result
                    if "view" in result
                    else {"result": {"authorization": "permit"}, "view": result},
                )
            except ValueError as exc:
                self._json(400, {"error": str(exc)})

        def log_message(self, format: str, *args: Any) -> None:
            return

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the synthetic Protected Delegated Care demonstrator"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    application = PDCApplication()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(application))
    print(f"PDC demo: http://{args.host}:{args.port}")
    print("Synthetic data only. Ctrl-C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
