# ARA documentation-foundation check

This check keeps the completed ARA experiment usable as an executable companion to the architecture document.

It verifies that:

- the machine-readable architecture-to-code crosswalk covers the required architecture concepts;
- every mapped implementation, runner and evidence path exists;
- the case landing page reports the final admitted status rather than the historical pre-admission status;
- the follow-along guide, final claim boundary, admission README and evidence manifest exist.

Run:

```bash
python experiments/ara-documentation-foundation/run.py --check
```

This is a documentation/code-coherence test. It does not substitute for the ARA semantic or adversarial test suites.
