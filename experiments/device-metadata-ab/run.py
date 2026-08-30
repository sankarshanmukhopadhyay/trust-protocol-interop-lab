#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, pathlib, re, subprocess

OPENVTC_PROBE = r'''
use serde_json::json;
use openvtc_core::devices::display_name;
use vta_sdk::protocols::device_management::{DeviceHeartbeatBody, device_name_ext};
fn main() {
    let profile = std::env::args().nth(1).expect("profile");
    let name = display_name(&profile);
    let body = DeviceHeartbeatBody {
        platform: Some(std::env::consts::OS.to_string()),
        vault_seq: None,
        ext: Some(device_name_ext(&name)),
    };
    println!("{}", json!({"profile":profile,"display_name":name,"heartbeat_payload":serde_json::to_value(body).unwrap()}));
}
''';

VTI_PROBE = r'''
use serde_json::json;
use vta_service::acl::{AclEntry, Role, ConsumerKind, CompanionFormFactor, get_acl_entry, store_acl_entry};
use vta_service::auth::AuthClaims;
use vta_service::operations::device::{heartbeat_device, register_device};
use vta_service::store::Store;
use vti_common::config::StoreConfig;

fn auth(did: &str) -> AuthClaims {
    AuthClaims { did:did.into(), role:Role::Application, allowed_contexts:vec![],
        session_id:"rahp".into(), access_expires_at:0, issued_at:0, amr:Vec::new(), acr:String::new() }
}
#[tokio::main]
async fn main() {
    let did=std::env::args().nth(1).expect("did");
    let name=std::env::args().nth(2).expect("display name");
    let dir=tempfile::tempdir().unwrap();
    let store=Store::open(&StoreConfig{data_dir:dir.path().into()}).unwrap();
    let acl=store.keyspace(vta_service::keyspaces::ACL).unwrap();
    let audit:vta_audit::SharedAuditSink=std::sync::Arc::new(
        vta_audit::KeyspaceAuditSink::new(store.keyspace(vta_service::keyspaces::AUDIT).unwrap()));
    store_acl_entry(&acl,&AclEntry::new(&did,Role::Application,"did:key:zSetup")).await.unwrap();
    register_device(&acl,&audit,&auth(&did),
        ConsumerKind::Companion{form_factor:CompanionFormFactor::Desktop},
        "initial".into(),None,None,"rahp-probe").await.unwrap();
    let ext=serde_json::from_value(json!({"org.openvtc.device-name":{"displayName":name}})).unwrap();
    heartbeat_device(&acl,&auth(&did),None,Some(&ext)).await.unwrap();
    let entry=get_acl_entry(&acl,&did).await.unwrap().unwrap();
    let binding=entry.device.unwrap();
    println!("{}",json!({"consumer_did":did,"retained_display_name":binding.display_name,
        "device_id":binding.device_id,"last_seen_present":binding.last_seen_at.is_some()}));
}
''';

def run(cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,check=True)
    return json.loads([x for x in p.stdout.splitlines() if x.strip()][-1])

def install(root,rel,content):
    p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content); return p

def host_key(name):
    m=re.match(r"^OpenVTC on (.*) \([^)]*\)$",name)
    if not m: raise ValueError(name)
    return m.group(1)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--openvtc",type=pathlib.Path,required=True); p.add_argument("--vti",type=pathlib.Path,required=True)
    p.add_argument("--openvtc-revision",required=True); p.add_argument("--vti-revision",required=True)
    p.add_argument("--run-id",required=True); p.add_argument("--output",type=pathlib.Path,required=True)
    a=p.parse_args()
    for rev in (a.openvtc_revision,a.vti_revision):
        if not re.fullmatch(r"[0-9a-f]{40}",rev): raise SystemExit("immutable SHA40 required")
    op=install(a.openvtc,"openvtc-core/examples/rahp_device_metadata_probe.rs",OPENVTC_PROBE)
    vp=install(a.vti,"vta-service/examples/rahp_device_retention_probe.rs",VTI_PROBE)
    try:
        A=run(["cargo","run","--quiet","-p","openvtc-core","--example","rahp_device_metadata_probe","--","context-a"],a.openvtc)
        B=run(["cargo","run","--quiet","-p","openvtc-core","--example","rahp_device_metadata_probe","--","context-b"],a.openvtc)
        RA=run(["cargo","run","--quiet","-p","vta-service","--example","rahp_device_retention_probe","--","did:key:zContextA",A["display_name"]],a.vti)
        RB=run(["cargo","run","--quiet","-p","vta-service","--example","rahp_device_retention_probe","--","did:key:zContextB",B["display_name"]],a.vti)
        ka,kb=host_key(A["display_name"]),host_key(B["display_name"]); joined=ka==kb
        assert RA["retained_display_name"]==A["display_name"] and RB["retained_display_name"]==B["display_name"]
        P1=run(["cargo","run","--quiet","-p","openvtc-core","--example","rahp_device_metadata_probe","--","positive-control"],a.openvtc)
        P2=run(["cargo","run","--quiet","-p","openvtc-core","--example","rahp_device_metadata_probe","--","positive-control"],a.openvtc)
        assert P1["display_name"]==P2["display_name"]
        execution={"context_a":"executed","context_b":"executed"}
        cls="derivably-related" if joined else "fresh"
        surfaces={
          "device_or_install_display_metadata":{"classification":cls,"context_a":A["display_name"],"context_b":B["display_name"],
            "derived_join_key_a":ka,"derived_join_key_b":kb,"execution":execution,"producer_component":"OpenVTC/openvtc::devices::display_name"},
          "heartbeat_payloads":{"classification":cls,"context_a":A["heartbeat_payload"],"context_b":B["heartbeat_payload"],
            "execution":execution,"producer_component":"OpenVTC/openvtc + vta-sdk::DeviceHeartbeatBody"},
          "retained_presence_records":{"classification":cls,"context_a":RA["retained_display_name"],"context_b":RB["retained_display_name"],
            "execution":execution,"producer_component":"OpenVTC/verifiable-trust-infrastructure::heartbeat_device"}
        }
        ev={"schema":"interop-device-metadata-ab/v1","evidence_class":"runtime-upstream-observation",
          "experiment":{"kind":"unlinkability-pressure-case","expected_join":"must-not-emerge",
            "observed_join":"detected" if joined else "not-detected",
            "join_surfaces":list(surfaces) if joined else []},
          "positive_control":{"expected_join":"must-detect","observed_join":"detected","value":P1["display_name"]},
          "provenance":{"producer":"trust-protocol-interop-lab","run_id":a.run_id,
            "observed_at":dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00","Z"),
            "implementation_repository":"OpenVTC/openvtc","implementation_revision":a.openvtc_revision,
            "context_a_run":a.run_id+"-A","context_b_run":a.run_id+"-B"},
          "additional_source_pins":[{"repository":"OpenVTC/verifiable-trust-infrastructure","revision":a.vti_revision}],
          "requirement_id":"ER-DEVICE-METADATA-AB",
          "observation_summary":"Pinned OpenVTC runtime generated heartbeat metadata in two unrelated contexts; pinned VTI runtime persisted each value on the authenticated device binding.",
          "surfaces":surfaces}
        ev["sha256"]=hashlib.sha256(json.dumps(ev,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(ev,indent=2,sort_keys=True)+"\n")
        print(json.dumps({"observed_join":ev["experiment"]["observed_join"],"sha256":ev["sha256"],"join_key":ka}))
    finally:
        op.unlink(missing_ok=True); vp.unlink(missing_ok=True)
if __name__=="__main__": main()
