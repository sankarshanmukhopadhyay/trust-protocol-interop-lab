# DTG VAC attenuation — experimental evidence

This pre-admission case supports RAHP Discussion #371 and RAHP issue #375. It tests the proposed VAC attenuation rules at `trustoverip/dtgwg-cred-spec#29` head `84650749afd48798e1c8919a95be359c0367a1c9` (`proposed-upstream`).

The experiment treats a child VAC as valid only when it is no broader than its parent across action set, governed scope, expiry, audience and chain depth, and when every required parent/current-state predicate remains valid. Signature validity is deliberately not treated as current authority.

The vectors cover action widening, scope widening, later expiry, audience substitution, incomplete chain, excessive depth, revoked root, revoked intermediate, and stale cached current-state. A positive control demonstrates a strictly narrowed child.

This is semantic executable evidence, not ratified DTG behavior or production cryptographic interoperability. Track C consumes canonical proposition `DTG-371-P08` and the current-state boundary in `DTG-371-P09`.
