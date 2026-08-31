# ER-DEVICE-METADATA-AB — observer-bound rerun

This experiment supersedes the methodology used in PR #76 without rewriting that historical artifact.

It separates three propositions:

1. **Producer observation** — OpenVTC's pinned `display_name` is executed once to characterize the human-readable host/profile value.
2. **Operator disclosure** — a VTA super-admin reads persisted device metadata through the actual pinned `device/list` implementation.
3. **Cross-context isolation/join** — two distinct Admin principals with different `allowed_contexts` execute `device/list`; the detector compares only values actually returned to each observer.

The target result is not asserted. Positive and negative controls use the same detector and can fail. Heartbeat transport is explicitly marked **not evidenced** because the implementation-side review established that the device flow addresses the installation's own VTA; this probe does not manufacture a second heartbeat recipient.

The VTI test module is instrumented at runtime in the source-pinned checkout to seed real ACL entries and call the real storage/list functions. The instrumentation is test-only and is not presented as upstream remediation.
