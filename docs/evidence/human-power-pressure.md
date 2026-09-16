# Human-power pressure evidence contract

The Trust Protocol Interop Lab uses this contract to make human-power-relevant runtime observations portable without taking over the judgment authority of RAHP, DPIP, governance bodies, deployers, or affected people.

## Contract boundary

The Lab may establish facts such as:

- what disclosure was minimally available, requested, and actually disclosed;
- what correlation scope was declared, requested, presented, retained, and effectively observable;
- whether refusal was available, what consequence followed, and whether a continuation/remediation path existed;
- whether authorization was presented and whether its validity was observed;
- whether authorization was bundled, preselected, repeatedly prompted, reversible, or purpose-specific;
- which decision features were declared and which were actually evaluated;
- what bounded outcome the fixture records.

The Lab does not infer from these facts that a system is harmful, fair, discriminatory, coercive, private, legitimate, consensual, conformant, or assurance-passing.

## Machine-readable schemas

Input fixtures use `interop-human-power-fixture/v1`.

Runner output uses `interop-human-power-observation-evidence/v1`, wrapped in `interop-human-power-evidence-package/v1`.

A result has `evidence_state: COMPLETE` only when all observation fields required by that pressure family are present. Missing runtime observation data yields `EVIDENCE_REQUIRED` and enumerates `missing_observations`.

## Pressure families

### Disclosure

Required observations: `available_minimal`, `requested`, `disclosed`, and `purpose_bound`. Derived signals report fields requested/disclosed beyond the available-minimal set. They are descriptive differences, not privacy judgments.

### Correlation

Required observations: declared, requested, presented, retained, and effective scopes plus explicit observer evidence. Identifier syntax alone is insufficient to assert cross-session or cross-context linkability.

### Refusal and interaction pressure

Required observations cover refusal availability, consequence, continuation path, bundling, default state, repeated prompts after refusal, reversibility, and purpose specificity. Formal ability to click “no” is therefore kept distinct from the observed consequence of refusal.

### Decision features

Required observations record both the declared feature set and the actually evaluated feature/value map. The runner exposes undeclared evaluated features as a machine-visible difference without deciding whether that use is justified.

## Counter-cases

Every family includes at least one bounded counter-case. This prevents simplistic rules such as “more disclosure is always wrong” or “stable identifiers are always unacceptable.” The evidence contract exists to preserve facts needed for later judgment, not to encode those judgments prematurely.

## Assurance and privacy handoff

RAHP may consume these observations when testing human-power harm propositions. DPIP may consume disclosure/correlation observations where privacy-depth analysis is warranted. Their resulting conclusions remain separate artifacts with separate authority and evidence requirements.

## Synthetic evidence limitation

Bundled fixtures are deterministic pressure-test evidence. They do not establish that a production deployment behaves the same way. Deployment claims require target-specific runtime evidence with appropriate provenance and observer coverage.
