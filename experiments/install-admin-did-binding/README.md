# Install admin-DID binding alignment

Source-pinned executable falsifier for RAHP #282.

It runs the current VTI WebAuthn install-claim integration ceremony and derives the DID from the actual attested Ed25519 public key. The probe then compares that value with the admin DID returned by VTI.

The current Trust Tasks 0.2 text is pinned separately and requires the admin DID to be derived from the attested key.

A successful probe means the test machinery executed correctly. Its assurance result can still be FAIL when the two semantics differ.
