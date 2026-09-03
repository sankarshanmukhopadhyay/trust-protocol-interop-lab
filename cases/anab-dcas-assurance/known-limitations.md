# Known limitations — IC-ANAB-DCAS-001

This case demonstrates a bounded semantic/evaluation composition. It does **not** establish production certification, upstream conformance, live-network interoperability, cryptographic verification, or independent implementation equivalence.

The current evaluator is authored inside the Interop Lab and uses explicit relying-party policy encoded in each normalized input. Its successful execution proves reproducibility of the declared fixture semantics, not universality of those policy choices.

Evidence URIs are synthetic fixture identifiers. The experiment tests treatment of evidence state (`available`, `missing`, `stale`, `revoked`) rather than retrieval from live systems.

The ANAB `INDETERMINATE-AUTHORITY` vector deliberately tests a boundary, not a claim that ANAB itself is an authority protocol. A successful identity/name binding remains insufficient for consequential action when the relying decision requires separately sourced action-specific authority.

Promotion beyond Experimental should require at least one separately implemented evaluator consuming the same normalized inputs and producing materially equivalent decisions and source-requirement findings.
