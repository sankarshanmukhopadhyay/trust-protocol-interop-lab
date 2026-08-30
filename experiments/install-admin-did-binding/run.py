#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, pathlib, subprocess
from datetime import datetime, timezone

VTI_PIN="96304b3b6ae76995e094e575560d74a43ee95e51"
TT_PIN="134733ff934775db522522dc26cb79836da29256"

def run(cmd,cwd):
    subprocess.run(cmd,cwd=cwd,check=True)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--vti",type=pathlib.Path,required=True)
    ap.add_argument("--trust-tasks",type=pathlib.Path,required=True)
    ap.add_argument("--output",type=pathlib.Path,required=True)
    ap.add_argument("--run-id",required=True)
    args=ap.parse_args()

    assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=args.vti,text=True).strip()==VTI_PIN
    assert subprocess.check_output(["git","rev-parse","HEAD"],cwd=args.trust_tasks,text=True).strip()==TT_PIN

    spec=(args.trust_tasks/"specs/vtc/install/claim/finish/0.2/spec.md").read_text()
    required=("derive the admin DID from the attested key" in spec or "derives the admin DID from the passkey" in spec)
    assert required, "current Trust Tasks 0.2 no longer states passkey-derived admin DID"

    test=args.vti/"vtc-service/tests/install_claim.rs"
    original=test.read_text()
    patched=original.replace(
        "let (register_cred, _ed25519_pub) = authenticator.register(&ccr, RP_ORIGIN);",
        "let (register_cred, ed25519_pub) = authenticator.register(&ccr, RP_ORIGIN);",
        1,
    )
    needle='assert!(admin_did.starts_with("did:key:z"));'
    replacement='''assert!(admin_did.starts_with("did:key:z"));
    let derived_admin_did = format!("did:key:{}", vta_sdk::did_key::ed25519_multibase_pubkey(&ed25519_pub));
    assert_eq!(admin_did, "did:key:z6MkAdmin", "current VTI returns the token-carried admin DID");
    assert_ne!(admin_did, derived_admin_did, "current VTI does not derive the admin DID from the attested WebAuthn key");'''
    assert needle in patched
    patched=patched.replace(needle,replacement,1)
    test.write_text(patched)

    run(["cargo","test","-q","-p","vtc-service","--test","install_claim","full_ceremony_completes_end_to_end"],args.vti)
    test.write_text(original)

    result={
      "proposition":"Trust Tasks 0.2 passkey-derived admin DID matches current VTI install claim behavior",
      "outcome":"FAIL",
      "reason_code":"implementation-spec-authorization-semantic-mismatch",
      "observed_at":datetime.now(timezone.utc).isoformat(),
      "run_id":args.run_id,
      "source_pins":[
        {"repository":"OpenVTC/verifiable-trust-infrastructure","revision":VTI_PIN},
        {"repository":"trustoverip/dtgwg-trust-tasks-tf","revision":TT_PIN}
      ],
      "positive_evidence":"The real VTI install-claim WebAuthn integration ceremony succeeds.",
      "falsification_evidence":"The successful ceremony returns the install-token admin DID did:key:z6MkAdmin while the DID derived from the fresh attested Ed25519 public key is different.",
      "boundary":"This does not claim the token-assignment design is inherently insecure. It proves that current implementation semantics differ from the current Trust Tasks 0.2 authorization argument and therefore cannot be treated as conformant to that proposition without an implementation or specification change."
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS probe execution: semantic mismatch reproduced; assurance outcome FAIL")

if __name__=="__main__": main()
