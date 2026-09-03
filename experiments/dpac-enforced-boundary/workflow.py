#!/usr/bin/env python3
from __future__ import annotations

import json
import socket
import sys
import time
import urllib.error
import urllib.request

WORKSPACE = "http://workspace:8080"


def http_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict]:
    data = None if payload is None else json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            body = json.loads(response.read().decode() or "{}")
            return response.status, body
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "idle"
    if command == "idle":
        while True:
            time.sleep(3600)
    if command == "status":
        code, body = http_json("GET", f"{WORKSPACE}/status")
        print(json.dumps({"status": code, "body": body}, sort_keys=True))
        return 0 if code == 200 else 1
    if command == "request":
        payload = json.loads(sys.argv[2])
        code, body = http_json("POST", f"{WORKSPACE}/actuate", payload)
        print(json.dumps({"status": code, "body": body}, sort_keys=True))
        return 0
    if command == "direct-actuator":
        try:
            socket.getaddrinfo("actuator", 8081)
            print(json.dumps({"reachable": True, "reason": "dns_resolved"}))
            return 1
        except socket.gaierror:
            print(json.dumps({"reachable": False, "reason": "network_isolation"}))
            return 0
    if command == "policy-access":
        path = "/policy/policy.json"
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("{}")
            print(json.dumps({"mutation_denied": False, "path": path}))
            return 1
        except OSError as exc:
            print(json.dumps({"mutation_denied": True, "path": path, "error": type(exc).__name__}))
            return 0
    if command == "admin-policy":
        code, body = http_json("POST", f"{WORKSPACE}/admin/policy", {"revision": "workflow-owned"})
        print(json.dumps({"status": code, "body": body}, sort_keys=True))
        return 0 if code in {404, 405} else 1
    raise SystemExit(f"unknown command: {command}")


if __name__ == "__main__":
    raise SystemExit(main())
