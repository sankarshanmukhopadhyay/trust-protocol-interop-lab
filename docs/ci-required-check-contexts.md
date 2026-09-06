# Required CI check context

The repository `protect-main` ruleset requires the GitHub Actions check context `validate`.

That context is intentionally reserved for the repository-wide assurance job in `.github/workflows/ci.yml`.

Specialist evidence workflows MUST use unique job/check names rather than `validate`. Reusing the required context across multiple workflows makes branch-protection evaluation ambiguous and can leave a pull request blocked with `Required status check "validate" is expected` even when the repository-wide assurance job has succeeded.

Current specialist contexts renamed as part of this fix:

- `action-vocabulary`
- `data-room-actuation`
- `hidden-subject-binding`
- `vac-attenuation`

When adding future workflows, do not introduce another job/check named `validate` unless the repository ruleset is deliberately changed at the same time.
