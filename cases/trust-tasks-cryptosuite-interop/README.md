# Trust Tasks Cryptosuite Interoperability Pressure Test

> **Current status: Experimental downstream interoperability evidence**
>
> **Admitted claim:** a common supported cryptosuite is a necessary capability precondition for two implementations to verify a document using that suite. This case does not perform cryptographic verification and is not an upstream Trust Tasks conformance claim.

Issue context: [#238](https://github.com/sankarshanmukhopadhyay/trust-protocol-interop-lab/issues/238)  
Machine-readable matrix: [matrix.json](matrix.json)  
Executable evaluator: [../../experiments/trust-tasks-cryptosuite-interop/run.py](../../experiments/trust-tasks-cryptosuite-interop/run.py)  
Negative fixture tests: [../../tests/test_trust_tasks_cryptosuite_interop.py](../../tests/test_trust_tasks_cryptosuite_interop.py)

## At a glance

| Item | Current state |
|---|---|
| **Status** | Experimental downstream interoperability evidence |
| **Purpose** | Test whether optional cryptosuite choice, without a common implementation floor, is sufficient to guarantee interoperability. |
| **Suites exercised** | `eddsa-jcs-2022` and `eddsa-rdfc-2022` as capability labels drawn from the implementer feedback under review. |
| **Positive control** | Producer and consumer share the declared suite, so the pair is `verify-capable` at the capability-set layer. |
| **Negative control** | Producer and consumer have disjoint supported-suite sets, yielding `unsupported-cryptosuite`. |
| **Claim boundary** | Capability-set interoperability only; no independent EdDSA, JCS, RDF canonicalization, or signature-correctness claim. |

## Why this matters

A framework can permit several cryptosuites and still leave two conforming
implementations unable to verify each other's documents if no common suite is
required. That is an interoperability failure even when neither implementation
is defective in isolation.

The distinction also matters diagnostically. A verifier that does not implement
the declared suite has not proved the signature invalid. It has established a
different result: it lacks the capability required to evaluate that proof. The
fixture therefore keeps `unsupported-cryptosuite`, `invalid-proof`, and
`producer-capability-mismatch` separate.

This is useful evidence for deciding whether a mandatory-to-implement floor is
needed, but the evidence does not choose which suite should occupy that role.

## Concrete scenario

Three synthetic implementations are represented:

- **impl-jcs-only** supports only `eddsa-jcs-2022`;
- **impl-rdfc-only** supports only `eddsa-rdfc-2022`;
- **impl-dual** supports both labels.

The matrix asks what happens when each implementation produces or consumes a
document declaring one of those suites. Shared capability produces
`verify-capable`; disjoint capability produces `unsupported-cryptosuite`.
An invalid proof under a mutually supported suite remains `invalid-proof`.
A producer claiming a known suite it does not support is classified separately
as `producer-capability-mismatch`. An unknown suite is explicitly unsupported.

No test silently substitutes one suite for another, and no canonicalization
fallback is allowed.

## Where it resolved

The downstream engineering question is resolved at the capability-set level:
**optional support alone does not guarantee interoperability**. The executable
matrix contains both shared-suite positive controls and disjoint-suite negative
controls, and the dedicated workflow runs the matrix plus regression tests.

The resolution is deliberately narrow. It establishes the need for some common
verification capability if the project expects arbitrary conforming
implementations to interoperate. It does not establish that a particular suite
is superior, mandatory, secure, or correctly implemented.

## What remains unresolved

The upstream normative decision remains open. This case does not decide:

- whether Trust Tasks should define a mandatory-to-implement cryptosuite;
- which cryptosuite, if any, should be that floor;
- whether the floor belongs in the framework, a profile, or a binding;
- whether multiple mandatory suites are justified;
- how algorithm agility and future cryptosuite migration should work;
- whether the examples observed in the implementer feedback are intentional
  long-term interoperability signals or merely draft examples.

A real cross-implementation cryptographic test would also need independent
implementations that produce and verify actual Data Integrity proofs and compare
canonicalization outputs and failure classes.

## Evidence and execution

The authoritative fixture for this case is [matrix.json](matrix.json). The
evaluator at
[run.py](../../experiments/trust-tasks-cryptosuite-interop/run.py) computes
capability intersections deterministically. The negative regression tests at
[test_trust_tasks_cryptosuite_interop.py](../../tests/test_trust_tasks_cryptosuite_interop.py)
lock the distinctions into CI.

Run locally with:

```bash
python experiments/trust-tasks-cryptosuite-interop/run.py --check
python -m pytest -q tests/test_trust_tasks_cryptosuite_interop.py
```

The dedicated GitHub Actions workflow executes the same checks for changes to
this case.

## Evidence boundary

This case tests **capability-set interoperability**, not EdDSA, JCS, or RDF
canonicalization implementations. `verify-capable` means only that the
producer and consumer both claim support for the declared suite and the fixture
marks the proof state valid. It does not independently establish signature
correctness.

The Interop Lab remains a downstream evidence producer. Trust Tasks and its
maintainers remain authoritative for any normative cryptosuite requirement.
