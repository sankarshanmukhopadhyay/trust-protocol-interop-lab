#!/usr/bin/env python3
"""Observer-bound device metadata A/B evidence.

This probe instruments the pinned VTI test module only to expose observations from
real ACL storage and list_devices calls. It does not assert the target privacy
outcome. The Python detector consumes the returned runtime observations and runs
positive/negative controls through the same comparison function.
"""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, re, subprocess
from datetime import datetime, timezone

OPENVTC_PIN = "2aa7ce3f8d1397048f13b85dffc3da6e10667a15"
VTI_PIN = "8b8e1adeb97572b979f8a1e57e6bc37d1ee27129"

def capture_display_name(openvtc: pathlib.Path) -> str:
    ex = openvtc / "openvtc-core" / "examples"
    ex.mkdir(exist_ok=True)
    p = ex / "rahp_device_name_observation_v2.rs"
    p.write_text('fn main() { println!("{}", openvtc_core::devices::display_name("default")); }\n', encoding="utf-8")
    try:
        return subprocess.check_output(
            ["cargo", "run", "-q", "-p", "openvtc-core", "--example", p.stem],
            cwd=openvtc, text=True
        ).strip()
    finally:
        p.unlink(missing_ok=True)

def inject_probe(vti: pathlib.Path) -> pathlib.Path:
    path = vti / "vta-service" / "src" / "operations" / "device.rs"
    text = path.read_text(encoding="utf-8")
    anchor = '    #[tokio::test]\n    async fn list_filters_then_disable_hides_device() {'
    if anchor not in text:
        raise SystemExit("pinned VTI test anchor not found")
    probe = r'''
    fn rahp_scoped_manage_auth(did: &str, role: Role, contexts: &[&str]) -> AuthClaims {
        AuthClaims {
            did: did.into(),
            role,
            allowed_contexts: contexts.iter().map(|s| (*s).to_string()).collect(),
            session_id: "rahp".into(),
            access_expires_at: 0,
            issued_at: 0,
            amr: Vec::new(),
            acr: String::new(),
        }
    }

    #[tokio::test]
    async fn rahp_observer_bound_device_scope_probe() {
        let (acl_ks, audit, _dir) = fresh().await;
        let target_name = std::env::var("RAHP_TARGET_NAME")
            .unwrap_or_else(|_| "OpenVTC on target-host (default)".into());

        seed_and_register(
            &acl_ks, &audit, "did:key:zContextADevice",
            CompanionFormFactor::Desktop, &target_name
        ).await;
        seed_and_register(
            &acl_ks, &audit, "did:key:zContextBDevice",
            CompanionFormFactor::Mobile, "Context B Device"
        ).await;

        let mut entry_a = get_acl_entry(&acl_ks, "did:key:zContextADevice")
            .await.unwrap().unwrap();
        entry_a.allowed_contexts = vec!["community-A".into()];
        store_acl_entry(&acl_ks, &entry_a).await.unwrap();

        let mut entry_b = get_acl_entry(&acl_ks, "did:key:zContextBDevice")
            .await.unwrap().unwrap();
        entry_b.allowed_contexts = vec!["community-B".into()];
        store_acl_entry(&acl_ks, &entry_b).await.unwrap();

        let observer_a = rahp_scoped_manage_auth(
            "did:key:zAdminA", Role::Admin, &["community-A"]
        );
        let observer_b = rahp_scoped_manage_auth(
            "did:key:zAdminB", Role::Admin, &["community-B"]
        );
        let super_admin = rahp_scoped_manage_auth(
            "did:key:zSuperAdmin", Role::Admin, &[]
        );
        let nowhere = rahp_scoped_manage_auth(
            "did:key:zNowhere", Role::Initiator, &[]
        );

        let payload = list_payload(json!({}));
        let a = list_devices(&acl_ks, &observer_a, &payload).await.unwrap();
        let b = list_devices(&acl_ks, &observer_b, &payload).await.unwrap();
        let operator = list_devices(&acl_ks, &super_admin, &payload).await.unwrap();
        let none = list_devices(&acl_ks, &nowhere, &payload).await.unwrap();

        println!("RAHP_OBSERVATION_JSON={}", json!({
            "context_a": {
                "observer": observer_a.did,
                "scope": observer_a.allowed_contexts,
                "devices": a["devices"]
            },
            "context_b": {
                "observer": observer_b.did,
                "scope": observer_b.allowed_contexts,
                "devices": b["devices"]
            },
            "operator": {
                "observer": super_admin.did,
                "scope": "unrestricted",
                "devices": operator["devices"]
            },
            "authorized_nowhere": {
                "observer": nowhere.did,
                "scope": "none",
                "devices": none["devices"]
            }
        }));
    }

'''
    path.write_text(text.replace(anchor, probe + anchor), encoding="utf-8")
    return path

def run_probe(vti: pathlib.Path, target_name: str) -> dict:
    inject_probe(vti)
    env = os.environ.copy()
    env["RAHP_TARGET_NAME"] = target_name
    proc = subprocess.run(
        ["cargo", "test", "-q", "-p", "vta-service", "rahp_observer_bound_device_scope_probe", "--", "--nocapture"],
        cwd=vti, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True
    )
    match = re.search(r"RAHP_OBSERVATION_JSON=(\{.*\})", proc.stdout)
    if not match:
        raise SystemExit("runtime observation marker missing")
    return json.loads(match.group(1))

def digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()

def normalized(devices: list[dict]) -> list[str]:
    return sorted(digest(str(d.get("displayName", ""))) for d in devices if d.get("displayName"))

def detector(a: list[str], b: list[str]) -> tuple[bool, list[str]]:
    common = sorted(set(a) & set(b))
    return bool(common), common

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--openvtc", type=pathlib.Path, required=True)
    ap.add_argument("--vti", type=pathlib.Path, required=True)
    ap.add_argument("--output", type=pathlib.Path, required=True)
    ap.add_argument("--run-id", default=os.getenv("GITHUB_RUN_ID", "local"))
    args = ap.parse_args()

    for repo, pin in ((args.openvtc, OPENVTC_PIN), (args.vti, VTI_PIN)):
        subprocess.run(["git", "rev-parse", "--verify", pin + "^{commit}"], cwd=repo, check=True)

    target_name = capture_display_name(args.openvtc)
    observation = run_probe(args.vti, target_name)

    a_vals = normalized(observation["context_a"]["devices"])
    b_vals = normalized(observation["context_b"]["devices"])
    joined, common = detector(a_vals, b_vals)
    positive, _ = detector(["sha256:known-correlator"], ["sha256:known-correlator"])
    negative, _ = detector(["sha256:known-a"], ["sha256:known-b"])
    if not positive or negative:
        raise SystemExit("detector controls failed")

    dids_a = {d.get("consumerDid") for d in observation["context_a"]["devices"]}
    dids_b = {d.get("consumerDid") for d in observation["context_b"]["devices"]}
    nowhere_count = len(observation["authorized_nowhere"]["devices"])
    scope_leak = "did:key:zContextBDevice" in dids_a or "did:key:zContextADevice" in dids_b or nowhere_count != 0
    operator_names = [d.get("displayName") for d in observation["operator"]["devices"]]
    operator_disclosure = target_name in operator_names

    observed_at = datetime.now(timezone.utc).isoformat()
    evidence = {
        "requirement_id": "ER-DEVICE-METADATA-AB",
        "evidence_class": "runtime-upstream-observation",
        "experiment": {
            "kind": "unlinkability-pressure-case",
            "expected_join": "must-not-emerge",
            "observed_join": "detected" if joined else "not-detected",
            "join_surfaces": ["retained_presence_record"],
        },
        "experimental_design": {
            "contexts": [
                {"id": "community-A", "instantiated": True, "observer_id": observation["context_a"]["observer"], "auth_principal": observation["context_a"]["observer"]},
                {"id": "community-B", "instantiated": True, "observer_id": observation["context_b"]["observer"], "auth_principal": observation["context_b"]["observer"]},
            ],
            "controls": {
                "positive": {"uses_same_detector": True, "can_fail": True, "result": "detected" if positive else "not-detected"},
                "negative": {"uses_same_detector": True, "can_fail": True, "result": "detected" if negative else "not-detected"},
            },
            "target_outcome_asserted": False,
            "observed_join_derivation": "computed-from-recorded-observations",
        },
        "provenance": {
            "producer": "trust-protocol-interop-lab",
            "run_id": str(args.run_id),
            "observed_at": observed_at,
            "implementation_repository": "OpenVTC/verifiable-trust-infrastructure",
            "implementation_revision": VTI_PIN,
            "context_a_run": f"{args.run_id}:community-A",
            "context_b_run": f"{args.run_id}:community-B",
        },
        "observation_summary": (
            "Distinct context-scoped administrative principals executed the pinned VTI device/list path "
            "against persisted bindings. The join result is derived only from display-name digests each "
            "observer actually received. OpenVTC display_name was executed once to characterize the producer; "
            "no heartbeat transport observation is claimed."
        ),
        "surfaces": {
            "retained_presence_record": {
                "classification": "identical" if joined else "fresh",
                "context_a": a_vals,
                "context_b": b_vals,
                "execution_source": "runtime-read",
                "observer": f"{observation['context_a']['observer']}/{observation['context_b']['observer']}",
                "common_value_digests": common,
            },
            "device_install_display_metadata": {
                "classification": "single-observation",
                "context_a": digest(target_name),
                "execution_source": "runtime-read",
                "observer": "OpenVTC local producer",
                "correlator_origin": "target-derived",
            },
            "heartbeat_payload": {
                "classification": "not-evidenced",
                "note": "No cross-context heartbeat transport was executed; the pinned implementation addresses the install's own VTA."
            },
        },
        "bounded_findings": {
            "context_scope_leak_observed": scope_leak,
            "operator_host_metadata_disclosure_observed": operator_disclosure,
            "authorized_nowhere_device_count": nowhere_count,
            "context_a_returned_consumer_dids": sorted(x for x in dids_a if x),
            "context_b_returned_consumer_dids": sorted(x for x in dids_b if x),
        },
        "source_pins": [
            {"repository": "OpenVTC/openvtc", "revision": OPENVTC_PIN},
            {"repository": "OpenVTC/verifiable-trust-infrastructure", "revision": VTI_PIN},
        ],
        "boundary": (
            "This experiment does not infer cross-context correlation from deterministic hostname generation. "
            "It records only what distinct scoped observers actually read. A detected join is therefore attributable "
            "to the observer-visible VTI path exercised here, not to an assumed heartbeat egress."
        ),
    }

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "er-device-metadata-observer-ab.json").write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
    (args.output / "summary.json").write_text(json.dumps({
        "outcome": "join-detected" if joined else "join-not-detected",
        "scope_leak_observed": scope_leak,
        "operator_disclosure_observed": operator_disclosure,
        "requirement": "ER-DEVICE-METADATA-AB",
        "openvtc_revision": OPENVTC_PIN,
        "vti_revision": VTI_PIN,
    }, indent=2, sort_keys=True) + "\n")
    print(json.dumps(evidence["bounded_findings"], sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
