# IC-ARA-REL-001 — known limitations and deliberate deferrals

This file is normative only for the **claim boundary of this Lab experiment**. It does not define the limits of the ARA proposal or any upstream specification.

## Current maturity

The case is a **pre-admission executable-ready design**. No runtime implementation evidence has yet been produced by this case. The following limitations therefore remain material.

## Identity and key-control limitations

The foundation does not yet implement or prove:

- stable Agent Role identity across real cryptographic key rotation;
- precommitted rotation authority;
- threshold/recovery control;
- compromise-interval reconstruction;
- algorithm migration;
- KERI, BetterSign, DID, VLAD, or other identity-control conformance;
- external witness/gossip/transparency-log fork detection.

Phase 3 may model local state-head/fork semantics, but production-strength identity/control claims require later pinned implementations and evidence.

## TSP / TEA limitations

No TSP transport or conformant TSP-Enabled Agent is implemented by the foundation.

A later independent-process experiment may initially use a Lab transport adapter. Successful byte exchange over that adapter cannot be reported as TSP interoperability or TEA conformance.

## Trust Tasks limitations

The foundation uses the architectural concept of an exact versioned task/action binding. It does not yet pin the current Trust Tasks baseline or prove that every proposed ARA ceremony operation already exists as a generic Trust Task.

Phase 2 must classify each mapping as direct, composition-dependent, adapter-only, candidate, or not-yet-evidenced.

## VTA / protected signing limitations

No OpenVTC VTA, TEE, HSM, non-exportable key store, remote attestation, or production anti-rollback mechanism is integrated yet.

The first protected signer will be a Lab adapter used to prove the **decision and non-bypass semantics**. It must not be described as providing hardware-backed or VTA-conformant guarantees.

## RCard and VRC limitations

The foundation preserves separate semantic slots for participant description and relationship recognition, but does not yet integrate or validate concrete RCard/VRC profiles.

In particular:

- participant self-assertion is not independently verified standing;
- relationship recognition is not delegation;
- VRC possession/issuance is not Agreement Object activation;
- VRC/RCard evidence is not automatic record-access permission.

## Role Record limitations

The Role Record engine does not yet exist.

The foundation specifies intended properties only. A later Lab implementation may demonstrate append-only/equivalently end-verifiable local state, but that does not automatically establish production durability, anti-rollback, availability, disaster recovery, confidentiality, or cross-implementation portability.

## Distributed Verifiable Relationship Record limitations

The distributed VRR is not yet executable.

The foundation intentionally rejects a central-master-record shortcut, but it has not yet proven:

- canonical byte representation;
- exact content identifier profile;
- party-set epoch mechanics beyond the planned two-party slice;
- collective-knowledge certificates;
- cross-anchored relationship checkpoints;
- evidence availability/recovery under independent failure;
- selective disclosure/ZK proofs of hidden relationship context;
- scalable multi-party/fork reconciliation.

## Agreement limitations

The initial Agreement Object is a synthetic machine-test fixture. It does not establish legal enforceability, jurisdictional validity, fiduciary status, informed consent, or domain-specific legal sufficiency.

The experiment tests exact-version binding and state/effect semantics, not legal drafting quality.

## Fiduciary and duty limitations

The case does not attempt to implement a universal fiduciary ontology or determine jurisdiction-specific duties.

The initial Policy Gate may use explicit local policy/duty rules only to exercise the architecture. Any mapping to fiduciary law, community governance, or owner preferences requires separate semantic authority and evidence.

## Workspace / model-security limitations

The foundation does not yet prove:

- sandbox escape resistance;
- secure boot;
- model isolation;
- prompt/context injection resistance in a real model runtime;
- protected secret handling;
- administrative separation;
- secure tool broker implementation.

The adversarial phase should test architectural bypass propositions, but passing those Lab tests is not a production penetration-test result.

## Privacy limitations

The minimum slice does not yet make broad privacy claims.

In particular it does not establish:

- unlinkability;
- non-discoverability;
- metadata minimization across real TSP/network infrastructure;
- resistance to traffic analysis;
- pairwise/relationship-specific identifier privacy;
- safe aggregation across Relationship Views;
- ZK selective proof of linked context.

If privacy claims are introduced, they require explicit observable surfaces and may need DPIP evaluation.

## VTC / governance limitations

The initial slice does not implement multi-community recognition, VTC certification, peer-community federation, arbitration networks, or community trust registries.

Any later VTC evidence remains evidence subject to local evaluation; community membership/certification must not become universal action authority.

## Multi-party limitations

The first executable slice is two-party.

It does not yet prove quorum, constituting-role semantics, affected-party representation, party-set changes, nested delegation, collective action, or multi-party checkpoint rules.

## Reputation limitations

The case does not implement a reputation system. Process/performance evidence may be retained, but no scalar or portable reputation conclusion is inferred.

## Human comprehension limitations

The eventual Relationship View will be a bounded proof package, not a usability-validated production interface. Human comprehension, cognitive load, accessibility, and informed authorization require separate testing.

## Assurance limitations

Repository Assurance, RAHP review, or any later Lab result is evidence about the bounded experiment. It is not external certification, ToIP approval, legal assurance, or proof of production safety.

Missing evidence must remain `indeterminate`, `not-started`, or explicitly out of scope.

## False independence limitation

Where later stages introduce multiple issuers, credentials, witnesses, attestations, communities, votes, or evidence paths, their multiplicity must not be treated as independent support without dependency/common-control analysis.

The initial two-party slice does not yet prove a generalized independence-detection mechanism.

## Deliberately deferred work

Unless required to falsify the minimum relationship proposition, defer:

- arbitrary multi-party relationships;
- full KERI/BetterSign control profile;
- generalized zero-knowledge relationship proofs;
- broad VTC federation;
- reputation markets;
- production-grade UI;
- every ARA ceremony profile;
- every proposed Trust Task;
- legal/fiduciary domain conformance;
- cross-jurisdiction policy resolution;
- production deployment certification;
- creation of a new repository.

## Claim boundary rule

A later PR may narrow or resolve a limitation only when it cites concrete executable or source evidence. A design intention, passing unrelated test, or adjacent component capability is not sufficient to remove a limitation.
