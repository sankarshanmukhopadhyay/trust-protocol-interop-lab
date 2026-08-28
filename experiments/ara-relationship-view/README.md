# ARA Phase 9 — Authorized Relationship Views

This experiment is executable evidence for `IC-ARA-REL-001` issue #41.

## Proposition

Can an authorized reviewer understand why a consequential relationship action was admitted, denied, disputed, remediated, or uncertain without access to model reasoning or unrestricted private records?

## View model

The view is a deterministic **derived explanation**, not a new source of authority. Every material assertion carries:

- an assertion key;
- an epistemic/status class;
- the value if authorized;
- source/evidence references;
- an explicit restriction marker where access is withheld.

Status classes include `verified`, `historical`, `disputed`, `restricted`, `indeterminate`, and `reported`.

The generator exposes material dependency existence without granting traversal. It excludes unrelated private Role Record content by construction and keeps missing evidence visible as `indeterminate`.

## Run

```bash
python experiments/ara-relationship-view/run.py --check
```

## Non-collapse rules

The executable suite preserves:

- redacted != verified;
- restricted dependency != nonexistent dependency;
- link existence != traversal authority;
- historical admitted action != currently active capability;
- dispute/remediation != clean undisputed history;
- missing evidence != resolved evidence;
- view != authority.

## Claim boundary

This is a Lab-local explanation format. It does not claim normative ARA view semantics, legal disclosure sufficiency, human-factors validation, accessibility conformance, or that the view itself authorizes any action.
