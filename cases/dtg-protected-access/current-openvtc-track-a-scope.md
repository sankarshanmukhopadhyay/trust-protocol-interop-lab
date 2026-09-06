# Scope of the current OpenVTC Track A run

The purpose of this run is not to prove that the whole current VTI stack is unlinkable. It answers a smaller implementation question: when two context-distinct executions use the current pinned VTI DIDComm/E2E path, which correlation-relevant surfaces are actually observable, and can the evidence producer distinguish a deliberately seeded join from a context-distinct pressure case?

The producer therefore runs both a positive control and a pressure case. The positive control reuses the same deterministic client identity and must be detected. The pressure case uses distinct client identities and distinct verifier context. The same capture/classification machinery processes both.

This execution materially observes the relationship-equivalent client binder and verifier transcript family. It also establishes bounded absence of named relationship-DID and edge-ID fields on this executed path. It does not execute status/policy-discovery or Trust Task operations; those requirements remain explicitly `not-evidenced`.

That distinction is the assurance result we want from the producer. A missing observation is not silently converted into a favourable privacy conclusion, and a historical Dogwood result is not used to fill a current evidence gap.
