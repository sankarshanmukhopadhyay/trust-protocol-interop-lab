# DTG hidden-subject binding — experimental composition evidence

This pre-admission case supports RAHP Discussion #371 and RAHP issue #376. It tests the composition proposition that independently valid hidden-subject credentials do **not** establish a joint predicate unless the proof also establishes the required same-subject or common-control relation.

The immediate upstream basis is the proposed VAC work in `trustoverip/dtgwg-cred-spec#29` @ `84650749afd48798e1c8919a95be359c0367a1c9`, which explicitly calls out VMC + VAC same-subject binding when subjects are hidden. Related delegation/common-control cases use the proposed VDC in PR #19 @ `ad5876f1b96e2149adec84d37d6595b4a212db9c`.

The semantic evaluator executes positive and negative credential-pooling/common-control cases. A composite predicate may pass only when every component is valid **and** the required binding relation is independently evidenced. Cryptographic validity remains separately attributable.

This is not a claim that a production ZKP construction has been demonstrated. Native cryptographic same-subject/common-control evidence remains a separate requirement; the experiment exists to ensure the composition layer cannot silently infer that relation from independently valid credentials.
