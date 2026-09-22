# DTG task-citation convergence experiment

This experiment implements the evidence work for issue #233 and is coordinated by RAHP #690.

## Purpose

The experiment prevents six distinct propositions from collapsing into one "credential verified" result:

1. credential validity;
2. citation identity;
3. exact initiating-document binding;
4. Trust Task completion;
5. action authorization;
6. cross-presentation correlation.

That separation is the central assurance property. A verifier can correctly validate a credential while still lacking evidence that the cited exchange completed, or while exposing a durable correlator across presentations.

## Authority boundary

Only the merged Trust Tasks #17 semantics are treated as adopted in the current experiment. Credential #56, VTI #33, ZKP #11, and Credential #58 are tracked as candidate sources. Their modeled behavior is useful for pressure testing but is not promoted into target-runtime evidence.

The merged Trust Tasks source is pinned at:

2bdc08bc55e48fd3bd4e03cd665b26d266f75c11

## Evidence classifications

Each vector terminates as one of:

- supported: observations match the explicitly stated expectation;
- divergent: observations contradict the stated expectation;
- not-implemented: the target runtime does not expose the required path;
- not-observable: the path exists but the required observation surface is unavailable.

The last two are legitimate evidence outcomes. They must not be rewritten as PASS.

## Running

The evaluator is importable for tests and downstream producers:

experiments/dtg-task-citation-convergence/evaluate.py

The regression tests exercise positive, negative, reused-context, authority non-inference, correlation, and unavailable-runtime cases.

## Downstream use

RAHP should consume this package as bounded composition evidence. DPIP should use the correlation observations to decide whether visible or committed citation material expands effective correlation scope. Neither consumer should infer target implementation behavior from a fixture-only vector.
