# IC-GOVOPS-EXEC-TRUST-001 — GovOps capability governance and executable trust composition

**Status:** Exploratory

**Admission anchor:** [Discussion #6](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/discussions/6)

Tests whether a GovOps authorization capability can be projected through portable semantic, authority, delegation, decision, and evidence artifacts without changing GovOps capability semantics, transferring runtime authorization authority, or collapsing capability, authority, entitlement, evidence, and assurance boundaries.

## Admission decision

The study is admitted as a bounded experimental Interop Case at **Exploratory** maturity. Admission establishes a repository-owned experiment scope and governance lineage only. It does not establish GovOps conformance, endorsement, integration, normative alignment, or any obligation on GovOpsWG, TSMM, GAAM, or TIS.

## Components and authority boundaries

- **GovOpsWG/GovOps** remains authoritative for GovOps capability and operational-governance architecture.
- **TSMM** remains authoritative for canonical trust-system semantics.
- **GAAM** remains authoritative for authority, delegation, revocation, accountability, and assurance semantics.
- **TIS** remains authoritative for portable machine-readable artifact contracts.
- **Trust Protocol Interop Lab** owns only this experimental composition, local mappings, vectors, executed evidence, findings, limitations, and maturity claims.

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

## Initial use case

The first experiment will use the capability:

```yaml
action: approve
resource: loan
```

The capability identifies an exposed operation. Authority, entitlement, policy evaluation, runtime authorization, execution, evidence, and later assurance remain separate governance states.

## Admission constraints

The case is admitted subject to the ten invariants in `invariants.yaml` and the scope/failure conditions recorded in Discussion #6. In particular:

- `capability_id` remains a GovOps identifier and is not replaced by a TSMM, GAAM, or TIS identifier;
- valid authority evidence does not itself produce `Allow`;
- the GovOps/PDP policy layer remains authoritative for runtime `Allow`, `Deny`, or `Challenge` decisions;
- evidence and assurance never confer or retroactively create authority; and
- historical execution evidence remains distinct from current authority validity after revocation.

## Open architectural dependency

Admission does **not** resolve whether GovOps intends `capability_id` to be the durable correlation key across authorization, execution, observation, and externally represented governance evidence. That question remains an attributable upstream clarification item. The experimental mapping MUST preserve the current GovOps identifier semantics unless and until authoritative upstream guidance says otherwise.

## Next maturity gate

Promotion to **Experimental** requires repository-owned mappings and scenarios that make the admitted invariants executable without requiring upstream GovOps changes. Positive and negative vectors, execution evidence, and findings are subsequent maturity gates.

## Explicit exclusions

The first iteration excludes PolicyMesh, Agent Registry Protocol, Agent Name Assurance Baseline, TRQP, RAHP, DTG conformance/assurance, agent-specific workflows, credential protocols, portfolio-monitor integration, changes to GovOps/Gemara/AuthZEN/PARC, and new policy or entitlement languages.
