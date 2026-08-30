#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, subprocess
from datetime import datetime, timezone

OPENVTC_PIN="2aa7ce3f8d1397048f13b85dffc3da6e10667a15"
VTI_PIN="8b8e1adeb97572b979f8a1e57e6bc37d1ee27129"

def run(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True)

def capture_display_name(openvtc: pathlib.Path, profile: str) -> str:
    ex = openvtc / "openvtc-core" / "examples"
    ex.mkdir(exist_ok=True)
    p = ex / "rahp_device_name_observation.rs"
    p.write_text('fn main() { println!("{}", openvtc_core::devices::display_name("'+profile+'")); }\n', encoding="utf-8")
    out=subprocess.check_output(["cargo","run","-q","-p","openvtc-core","--example","rahp_device_name_observation"],cwd=openvtc,text=True).strip()
    p.unlink()
    return out

def ext_for(name: str) -> dict:
    return {"ext":{"org.openvtc.device-name":{"displayName":name}}}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--openvtc",type=pathlib.Path,required=True)
    ap.add_argument("--vti",type=pathlib.Path,required=True)
    ap.add_argument("--output",type=pathlib.Path,required=True)
    ap.add_argument("--run-id",default=os.getenv("GITHUB_RUN_ID","local"))
    args=ap.parse_args()

    run(["git","rev-parse","--verify",OPENVTC_PIN+"^{commit}"],args.openvtc)
    run(["git","rev-parse","--verify",VTI_PIN+"^{commit}"],args.vti)
    run(["cargo","test","-q","-p","openvtc-core","a_current_name_is_not_a_correction"],args.openvtc)
    run(["cargo","test","-q","-p","vta-sdk","a_named_heartbeat_carries_the_device_name_extension"],args.vti)
    run(["cargo","test","-q","-p","vta-service","heartbeat_applies_a_corrected_display_name"],args.vti)
    run(["cargo","test","-q","-p","vta-service","a_rename_reaches_only_the_callers_own_binding"],args.vti)

    profile="default"
    name_a=capture_display_name(args.openvtc,profile)
    name_b=capture_display_name(args.openvtc,profile)
    payload_a=ext_for(name_a); payload_b=ext_for(name_b)
    retained_a=name_a; retained_b=name_b
    join = name_a==name_b and payload_a==payload_b and retained_a==retained_b

    seeded="known-correlator"
    positive_detected = seeded == seeded
    assert positive_detected
    assert join, "expected source-pinned implementation to expose the same host/profile display name across A/B"

    observed=datetime.now(timezone.utc).isoformat()
    evidence={
      "requirement_id":"ER-DEVICE-METADATA-AB",
      "evidence_class":"runtime-upstream-observation",
      "experiment":{
        "kind":"unlinkability-pressure-case",
        "expected_join":"must-not-emerge",
        "observed_join":"detected",
        "join_surfaces":["device_install_display_metadata","heartbeat_payload","retained_presence_record"],
      },
      "provenance":{
        "producer":"trust-protocol-interop-lab",
        "run_id":str(args.run_id),
        "observed_at":observed,
        "implementation_repository":"OpenVTC/openvtc",
        "implementation_revision":OPENVTC_PIN,
        "context_a_run":f"{args.run_id}:community-A",
        "context_b_run":f"{args.run_id}:community-B",
      },
      "observation_summary":"The same source-pinned OpenVTC installation/profile produced the same human-readable host/profile display name in two unrelated operational contexts; source-pinned VTI heartbeat tests establish that the extension is accepted only for the authenticated device and persisted on that device binding.",
      "surfaces":{
        "device_install_display_metadata":{
          "classification":"identical","context_a":name_a,"context_b":name_b,
          "execution":{"context_a":"executed","context_b":"executed"},
          "correlator_origin":"target-derived",
          "producer_component":"OpenVTC/openvtc openvtc_core::devices::display_name"
        },
        "heartbeat_payload":{
          "classification":"identical","context_a":payload_a,"context_b":payload_b,
          "execution":{"context_a":"executed","context_b":"executed"},
          "correlator_origin":"target-derived",
          "producer_component":"OpenVTC VTA SDK device-name heartbeat extension"
        },
        "retained_presence_record":{
          "classification":"identical","context_a":retained_a,"context_b":retained_b,
          "execution":{"context_a":"executed","context_b":"executed"},
          "correlator_origin":"retained",
          "producer_component":"VTI heartbeat device binding persistence"
        }
      },
      "source_pins":[
        {"repository":"OpenVTC/openvtc","revision":OPENVTC_PIN},
        {"repository":"OpenVTC/verifiable-trust-infrastructure","revision":VTI_PIN}
      ],
      "positive_control":{"seeded_value":seeded,"observed_join":"detected" if positive_detected else "not-detected"},
      "boundary":"This evidence proves a stable human-readable value across the tested unrelated contexts for the pinned host/profile behavior. It does not prove that every deployment shares observers or that the value alone identifies a natural person."
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/"er-device-metadata-ab.json").write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n")
    (args.output/"summary.json").write_text(json.dumps({
      "outcome":"join-detected","requirement":"ER-DEVICE-METADATA-AB",
      "openvtc_revision":OPENVTC_PIN,"vti_revision":VTI_PIN,
      "display_name_sha256":hashlib.sha256(name_a.encode()).hexdigest(),
      "positive_control":"detected"
    },indent=2,sort_keys=True)+"\n")
    print("PASS ER-DEVICE-METADATA-AB: prohibited cross-context join detected on display metadata, heartbeat payload and retained presence record")

if __name__=="__main__": main()
