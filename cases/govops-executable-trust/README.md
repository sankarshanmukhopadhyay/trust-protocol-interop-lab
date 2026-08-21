# IC-GOVOPS-EXEC-TRUST-001 — GovOps capability governance and executable trust composition

**Status:** Experimental

**Admission anchor:** [Discussion #6](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/discussions/6)

Tests whether a GovOps authorization capability can be projected through portable semantic, authority, delegation, decision, and evidence artifacts without changing GovOps capability semantics, transferring runtime authorization authority, or collapsing capability, authority, entitlement, evidence, and assurance boundaries.

## Admission and maturity decision

The study was admitted at **Exploratory** maturity through PR #7. This tranche promotes it to **Experimental** by adding a repository-owned mapping and machine-readable scenarios that make the admitted invariants testable without requiring an upstream GovOps change.

Experimental status means the semantic composition is now specified well enough to construct vectors. It does not establish GovOps conformance, endorsement, production integration, normative alignment, successful execution, or any obligation on GovOpsWG, TSMM, GAAM, or TIS.

## Components and authority boundaries

- **GovOpsWG/GovOps** remains authoritative for GovOps capability and operational-governance architecture.
- **TSMM** remains authoritative for canonical trust-system semantics.
- **GAAM** remains authoritative for authority, delegation, revocation, accountability, and assurance semantics.
- **TIS** remains authoritative for portable machine-readable artifact contracts.
- **Trust Protocol Interop Lab** owns only this experimental composition, local mappings, scenarios, vectors, executed evidence, findings, limitations, and maturity claims.

The core semantic boundary is:

```text
Capability
    ≠
Authority
    ≠
Entitlement
    ≠
Authorization decision
    ≠
Evidence
    ≠
Assurance conclusion
```

## Experimental mapping

The executable mapping is defined in [`mappings/govops-executable-trust.md`](../../mappings/govops-executable-trust.md). It defines a one-way governance pipeline:

```text
capability
  -> request context
  -> authority/delegation evaluation
  -> GovOps/PDP policy input
  -> Allow | Deny | Challenge
  -> execution admission
  -> observed effect
  -> portable evidence
  -> later assurance
```

No later stage can create authority or rewrite an earlier runtime decision. `capability_id` remains the GovOps capability identifier. The lab introduces separate `request_id`, `decision_id`, `effect_id`, `evidence_bundle_id`, and `assurance_result_id` correlation fields so the experiment does not assume that GovOps intends `capability_id` to serve every lifecycle correlation purpose.

## Initial use case

The first experiment uses the capability:

```yaml
action: approve
resource: loan
```

The capability identifies an exposed operation. Authority, entitlement, policy evaluation, runtime authorization, execution, evidence, and later assurance remain separate governance states.

## Scenario estate

[`scenarios/scenarios.yaml`](scenarios/scenarios.yaml) defines seven scenario contracts covering:

1. valid authority plus GovOps/PDP `Allow` and a correctly correlated effect;
2. valid authority with policy `Deny`;
3. delegated authority that exceeds its source limit;
4. authority revoked before the runtime decision;
5. authority revoked after an authorized effect, preserving historical evidence;
6. an unrelated runtime effect that fails decision correlation; and
7. complete evidence plus later positive assurance that cannot retroactively authorize a denied action.

Each scenario references the invariants it exercises and declares expected independent states for authorization, execution, evidence, and assurance.

## Experimental constraints

The case remains subject to the ten invariants in `invariants.yaml` and the scope/failure conditions recorded in Discussion #6. In particular:

- `capability_id` remains a GovOps identifier and is not replaced by a TSMM, GAAM, TIS, or lab identifier;
- valid authority evidence does not itself produce `Allow`;
- delegated authority cannot exceed its source;
- the GovOps/PDP policy layer remains authoritative for runtime `Allow`, `Deny`, or `Challenge` decisions;
- executed effects must correlate to the admitting decision and capability;
- evidence and assurance never confer or retroactively create authority; and
- historical execution evidence remains distinct from current authority validity after revocation.

## Open architectural dependency

The experiment still does **not** resolve whether GovOps intends `capability_id` to be the durable correlation key across authorization, execution, observation, and externally represented governance evidence. That remains an attributable upstream clarification item. Until authoritative upstream guidance exists, the lab profile preserves `capability_id` as the capability reference and uses separate lifecycle correlation identifiers.

## Next maturity gate

Promotion to **Candidate** requires positive and negative executable vectors, explicit expected behavior, and known limitations. Those vectors should be derived directly from the seven scenario contracts rather than introducing a second semantic model.

A subsequent **Interoperability Tested** claim requires a deterministic evaluator, executed results, reproduction command, and hash-bound evidence manifest.

## Explicit exclusions

The current iteration excludes PolicyMesh, Agent Registry Protocol, Agent Name Assurance Baseline, TRQP, RAHP, DTG conformance/assurance, agent-specific workflows, credential protocols, portfolio-monitor integration, changes to GovOps/Gemara/AuthZEN/PARC, and new policy or entitlement languages.
