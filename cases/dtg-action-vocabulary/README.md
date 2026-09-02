# DTG cross-governance action vocabulary — experimental evidence

This pre-admission case supports RAHP Discussion #371 and RAHP issue #377. It pressure-tests the proposed VAC rule that action strings are scope-local and must not acquire semantics merely because another governance domain uses the same token.

Source: `trustoverip/dtgwg-cred-spec#29` @ `84650749afd48798e1c8919a95be359c0367a1c9` (`proposed-upstream`).

The experiment distinguishes lexical equality from semantic authority. A foreign verifier may rely on an action only when an explicit governance/profile mapping binds the issuer's action semantic to the verifier's required operation. It rejects same-token/different-meaning, implicit hierarchy (`admin` ⇒ `write`) and unmapped foreign action cases. It also demonstrates that an explicit namespaced/profile mapping can make a cross-domain action interpretable without changing VAC Core semantics.

This experiment does not select a normative federation mechanism. It exists to identify the boundary between local VAC semantics and the profile/governance artifact required for federated reliance.
