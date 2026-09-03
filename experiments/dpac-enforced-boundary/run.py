#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
COMPOSE = ROOT / "compose.yaml"
RUNTIME = ROOT / "runtime"
DEFAULT_POLICY = ROOT / "policy.default.json"
PROJECT = "dpac-enforced-boundary"


def run_cmd(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=check)


def compose(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_cmd(["docker", "compose", "-p", PROJECT, "-f", str(COMPOSE), *args], check=check)


def exec_json(service: str, *args: str, check: bool = True) -> dict[str, Any]:
    result = compose("exec", "-T", service, "python", "/app/workflow.py", *args, check=check)
    return json.loads(result.stdout.strip())


def effect_count() -> int:
    result = compose("exec", "-T", "actuator", "python", "/app/actuator.py", "count")
    return int(result.stdout.strip())


def workspace_status() -> dict[str, Any]:
    return exec_json("workflow", "status")["body"]


def request(payload: dict[str, Any]) -> dict[str, Any]:
    return exec_json("workflow", "request", json.dumps(payload, separators=(",", ":")))["body"]


def base_request(nonce: str, *, amount: int = 3500000, loan_id: str = "LN-2026-004217") -> dict[str, Any]:
    return {
        "action": "approve",
        "loan_id": loan_id,
        "amount_inr": amount,
        "nonce": nonce,
        "expected_capability_revision": "policy-v1",
        "authority": {
            "current": True,
            "limit_inr": 5000000,
            "bound_loan_id": loan_id,
            "bound_amount_inr": amount,
        },
    }


def record(results: list[dict[str, Any]], scenario: str, passed: bool, evidence: dict[str, Any]) -> None:
    results.append({"scenario": scenario, "pass": passed, "evidence": evidence})


def no_effect(before: int) -> tuple[bool, int]:
    after = effect_count()
    return after == before, after


def prepare_runtime() -> None:
    RUNTIME.mkdir(exist_ok=True)
    shutil.copyfile(DEFAULT_POLICY, RUNTIME / "policy.json")
    (RUNTIME / "actuator-token.txt").write_text("workspace-only-demo-token\n", encoding="utf-8")


def wait_ready() -> None:
    deadline = time.time() + 45
    last = ""
    while time.time() < deadline:
        result = compose("exec", "-T", "workflow", "python", "/app/workflow.py", "status", check=False)
        if result.returncode == 0:
            return
        last = result.stderr or result.stdout
        time.sleep(1)
    raise RuntimeError(f"workspace did not become ready: {last}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    failures: list[str] = []
    prepare_runtime()
    compose("down", "-v", "--remove-orphans", check=False)

    try:
        compose("up", "-d", "--build")
        wait_ready()

        # 1. Valid concurrence produces exactly one actuator-owned effect.
        before = effect_count()
        valid_payload = base_request("nonce-valid-001")
        valid = request(valid_payload)
        after = effect_count()
        passed = valid.get("actuated") is True and after == before + 1 and valid.get("effect", {}).get("effect_id")
        record(results, "DPAC-ENF-001-valid-concurrence", bool(passed), {"workspace": valid, "effect_count_before": before, "effect_count_after": after})

        # 2. Workflow cannot address actuator because there is no shared network.
        before = effect_count()
        attack = exec_json("workflow", "direct-actuator")
        unchanged, after = no_effect(before)
        passed = attack.get("reachable") is False and unchanged
        record(results, "DPAC-ENF-002-direct-actuator-denied", passed, {"attack": attack, "effect_count_before": before, "effect_count_after": after})

        # 3. Workflow cannot mutate or administratively replace capability policy.
        before = effect_count()
        status_before = workspace_status()
        file_attack = exec_json("workflow", "policy-access")
        admin_attack = exec_json("workflow", "admin-policy")
        status_after = workspace_status()
        unchanged_effect, after = no_effect(before)
        passed = (
            file_attack.get("mutation_denied") is True
            and admin_attack.get("status") in {404, 405}
            and status_before.get("policy_digest") == status_after.get("policy_digest")
            and unchanged_effect
        )
        record(results, "DPAC-ENF-003-policy-mutation-denied", passed, {"file_attack": file_attack, "admin_attack": admin_attack, "policy_before": status_before, "policy_after": status_after, "effect_count_after": after})

        # 4. Authority may permit more than Workspace capability; capability still bounds actuation.
        before = effect_count()
        payload = base_request("nonce-capability-overreach", amount=6000000)
        payload["authority"]["limit_inr"] = 10000000
        denied = request(payload)
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "capability_scope_exceeded" and unchanged
        record(results, "DPAC-ENF-004-capability-overreach", passed, {"workspace": denied, "effect_count_after": after})

        # 5. Revocation/currentness is re-evaluated at actuation.
        before = effect_count()
        payload = base_request("nonce-revoked")
        payload["authority"]["current"] = False
        denied = request(payload)
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "authority_not_current" and unchanged
        record(results, "DPAC-ENF-005-revoked-authority", passed, {"workspace": denied, "effect_count_after": after})

        # 6. Target or parameter substitution breaks the authority binding.
        before = effect_count()
        payload = base_request("nonce-substitution")
        payload["loan_id"] = "LN-SUBSTITUTED"
        denied = request(payload)
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "authority_binding_mismatch" and unchanged
        record(results, "DPAC-ENF-006-request-substitution", passed, {"workspace": denied, "effect_count_after": after})

        # 7. Independently administered capability revision change invalidates stale concurrence.
        before = effect_count()
        changed_policy = json.loads(DEFAULT_POLICY.read_text(encoding="utf-8"))
        changed_policy["revision"] = "policy-v2"
        changed_policy["capabilities"]["loan-approve"]["max_amount_inr"] = 4000000
        (RUNTIME / "policy.json").write_text(json.dumps(changed_policy, indent=2) + "\n", encoding="utf-8")
        denied = request(base_request("nonce-stale-capability"))
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "capability_state_changed" and denied.get("policy_revision") == "policy-v2" and unchanged
        record(results, "DPAC-ENF-007-capability-revision-race", passed, {"workspace": denied, "effect_count_after": after})
        shutil.copyfile(DEFAULT_POLICY, RUNTIME / "policy.json")

        # 8. A consumed actuation nonce cannot create a second effect.
        before = effect_count()
        denied = request(valid_payload)
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "replay" and unchanged
        record(results, "DPAC-ENF-008-replay-single-effect", passed, {"workspace": denied, "effect_count_after": after})

        # 9. A Workflow-controlled helper inherits no path to policy administration or actuator.
        before = effect_count()
        helper_direct = exec_json("helper", "direct-actuator")
        helper_policy = exec_json("helper", "policy-access")
        unchanged, after = no_effect(before)
        passed = helper_direct.get("reachable") is False and helper_policy.get("mutation_denied") is True and unchanged
        record(results, "DPAC-ENF-009-transitive-helper-denied", passed, {"direct_attack": helper_direct, "policy_attack": helper_policy, "effect_count_after": after})

        # 10. Unresolvable capability state fails closed.
        before = effect_count()
        (RUNTIME / "policy.json").write_text("{\"revision\":\"broken\",\"capabilities\":{}}\n", encoding="utf-8")
        denied = request(base_request("nonce-indeterminate-capability"))
        unchanged, after = no_effect(before)
        passed = denied.get("reason") == "indeterminate_capability" and denied.get("evidence_state") == "indeterminate" and unchanged
        record(results, "DPAC-ENF-010-indeterminate-fails-closed", passed, {"workspace": denied, "effect_count_after": after})
        shutil.copyfile(DEFAULT_POLICY, RUNTIME / "policy.json")

        # Topology evidence: distinct container UIDs and policy digest are observable.
        status = workspace_status()
        workflow_uid = int(compose("exec", "-T", "workflow", "id", "-u").stdout.strip())
        helper_uid = int(compose("exec", "-T", "helper", "id", "-u").stdout.strip())
        actuator_uid = int(compose("exec", "-T", "actuator", "id", "-u").stdout.strip())
        topology = {
            "workflow_uid": workflow_uid,
            "helper_uid": helper_uid,
            "workspace_uid": status.get("workspace_uid"),
            "actuator_uid": actuator_uid,
            "policy_revision": status.get("policy_revision"),
            "policy_digest": status.get("policy_digest"),
            "policy_file_sha256_host": hashlib.sha256((RUNTIME / "policy.json").read_bytes()).hexdigest(),
        }

    except Exception as exc:
        failures.append(f"runner_error: {type(exc).__name__}: {exc}")
        topology = {}
    finally:
        logs = compose("logs", "--no-color", check=False)
        compose("down", "-v", "--remove-orphans", check=False)
        shutil.rmtree(RUNTIME, ignore_errors=True)

    failed_scenarios = [item["scenario"] for item in results if not item["pass"]]
    failures.extend(failed_scenarios)
    payload = {
        "case_id": "IC-DPAC-ACTUATION-001",
        "experiment": "dpac-enforced-boundary",
        "claim": "bounded container-enforced separation evidence; not production certification",
        "topology": topology,
        "results": results,
        "summary": {"total": len(results), "passed": sum(1 for item in results if item["pass"]), "failed": len(failures)},
        "failures": failures,
        "container_logs": logs.stdout[-12000:] if 'logs' in locals() else "",
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 1 if args.check and failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
