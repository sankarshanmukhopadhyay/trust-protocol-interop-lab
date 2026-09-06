# Runtime acceptance criteria for #153

The current-target workflow is acceptable evidence only when all of the following hold:

1. the exact OpenVTC revision is verified before execution;
2. the positive control detects the deliberately seeded relationship-equivalent binder;
3. the context-distinct pressure run executes the same current target with distinct client identities and verifier contexts;
4. the upstream checkout is clean after the temporary observer probe is removed;
5. the artifact preserves `not-evidenced` for status/policy and Trust Task surfaces that this path does not execute;
6. the DPIP export binds to the exact runtime artifact and target revision;
7. no workflow result is interpreted as privacy PASS or RAHP GREEN.

This tranche intentionally stops rather than inventing observations for implementation surfaces that the bounded current target path does not exercise.
