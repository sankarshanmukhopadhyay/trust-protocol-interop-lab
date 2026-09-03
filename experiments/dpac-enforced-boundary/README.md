# DPAC enforced Workspace boundary experiment

This experiment strengthens `IC-DPAC-ACTUATION-001` from logical/state separation to a bounded runtime-enforcement proposition.

## Proposition

The Workflow security principal cannot directly or transitively enlarge, replace, disable, or bypass the Workspace capability policy, and every route to the consequential loan-approval effect passes through Workspace enforcement.

The topology is intentionally small:

```text
workflow/helper -- request_net --> workspace -- actuator_net --> actuator
                                      |
                                      +-- read-only capability policy
                                      +-- actuator credential
                                      +-- replay state
```

`workflow` and `actuator` share no Docker network. Only `workspace` joins both. The actuator credential is mounted only into Workspace and actuator containers. The capability policy is mounted read-only into Workspace and is not mounted into Workflow/helper containers. All containers run read-only root filesystems, drop Linux capabilities, use `no-new-privileges`, and run as distinct numeric UIDs.

The actuator owns the effect journal. A denial response is therefore not treated as proof of no actuation: every negative scenario checks that the actuator-owned effect count remains unchanged.

## Run

Requires Docker with the Compose v2 plugin:

```bash
python experiments/dpac-enforced-boundary/run.py --check
```

To retain the evidence document:

```bash
python experiments/dpac-enforced-boundary/run.py --check \
  --output /tmp/dpac-enforced-boundary.json
```

The runner creates ephemeral runtime policy/credential material, builds the three security-domain images, executes ten positive/negative scenarios, records topology/effect evidence, and always tears down containers, networks, tmpfs state, and runtime material.

## Falsification coverage

The runner exercises valid concurrence; direct actuator bypass; capability-policy mutation/admin attempts; capability overreach; authority revocation; request target substitution; capability-revision TOCTOU; replay; a Workflow-controlled helper as a bounded transitive path; and indeterminate capability state.

## Claim boundary

A passing run demonstrates a concrete container-enforced realization in which the tested Workflow/helper principals cannot reach the actuator network or runtime capability-policy mount and cannot cause a second effect through replay. It does **not** establish production isolation, host/daemon compromise resistance, independent implementation, external certification, or exhaustive transitive-control analysis. The Docker daemon/host remains outside the modeled adversary boundary, and authority authenticity remains abstracted as supplied evidence rather than a cryptographically verified upstream authority artifact.
