# Scenario 06 — Prior-hop rewrite

A delegating actor forwards a chain after modifying an earlier hop so the forwarded representation narrows cleanly. The receiver retained the received-chain digest.

**Expected:** forwarded-vs-received comparison detects mutation. A downstream party that possesses only the forwarded representation cannot recover the prior bytes; that limitation is recorded rather than hidden.
