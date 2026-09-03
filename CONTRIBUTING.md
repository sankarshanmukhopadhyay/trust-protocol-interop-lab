# Contributing

Contributions are welcome where they improve interoperability analysis, implementation evidence, test coverage, or specification clarity.

## Contribution types

Useful contributions include:

- corrections to protocol mappings;
- implementation observations;
- test vectors and scenarios;
- security or corrigibility analysis;
- proposed binding language;
- compatibility notes against newer upstream releases.

## Issue → PR → evidence → merge

Substantive changes follow an auditable judgment trail:

1. **Issue** — state the bounded problem, affected authority/scope, and intended evidence or acceptance criteria.
2. **Branch / implementation** — make the smallest coherent change against the declared baseline.
3. **Pull request** — link the issue and state authority boundaries, validation evidence, and rollback/supersession behaviour.
4. **Automated evidence** — the required `validate` status must pass, including claim/evidence validation and generated-tree/link/Pages checks where applicable.
5. **Review judgment** — resolve review conversations and preserve any material limitation or dissent in the repository record.
6. **Merge** — merge only through the protected default-branch path. A merge records repository acceptance of the bounded change; it does not create upstream authority, certification, or broader interoperability meaning.
7. **Correction / revocation** — if later evidence invalidates a claim, correct or supersede it through a new auditable change rather than rewriting history.

## Expectations

Please:

1. identify the upstream specification/version used;
2. distinguish observed behavior from proposed behavior;
3. avoid implying endorsement by an upstream standards body;
4. preserve semantic boundaries between transport, execution, identity, authorization, and governance;
5. add or update tests/examples when changing a candidate binding materially; and
6. keep generated artifacts synchronized with their canonical inputs.

## Dependencies and workflow changes

Dependency changes should remain explicit and reproducible. Exact package versions are preferred for experiment-only dependencies. GitHub Actions dependencies are monitored by Dependabot; non-GitHub Actions that execute repository code should be pinned to an immutable commit when practical. Changes to workflow permissions or contributor-code execution boundaries require explicit review in the pull request.

## Security-sensitive contributions

Do not open a public issue or pull request containing vulnerability details. Follow [SECURITY.md](SECURITY.md).

## AI-assisted contributions

AI tools may be used for analysis, drafting, editing, or code generation. Contributors are encouraged to disclose material AI assistance when it would help reviewers understand provenance or validation expectations. Human contributors remain responsible for the accuracy and appropriateness of submitted material.
