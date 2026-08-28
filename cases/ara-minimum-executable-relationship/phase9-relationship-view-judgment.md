# IC-ARA-REL-001 Phase 9 — visible Authorized Relationship View judgment

Issue: #41  
Parent: #32  
Depends on completed lifecycle-continuity phase: #40

## Proposition under test

Can an authorized human or machine reviewer understand the basis, limits, evidence, disagreement, uncertainty, dependencies, and remedies of a consequential relationship action without model reasoning or unrestricted private-record access?

## Alternatives genuinely considered

### Render one overall green/red legitimacy badge

Rejected. A single badge collapses current authority, historical validity, disagreement, evidence sufficiency, privacy restriction, and remediation into an opaque conclusion.

### Dump all supporting records into the view

Rejected. This defeats privacy boundaries, encourages unrestricted traversal, and turns explanation into a parallel dossier.

### Hide restricted dependencies entirely

Rejected. A reviewer can be materially misled if an important dependency vanishes merely because its content is access-controlled.

### Generate source-traceable, scope-aware assertions with explicit epistemic status

Selected. The view is derived deterministically from attributable relationship evidence. Restricted content remains restricted, but material dependency existence, uncertainty, dispute, and historical/current distinctions stay visible.

## Core judgment

> Explainability is not simplification into a verdict. A defensible Relationship View must preserve the distinctions that made the underlying authorization defensible.

The implementation preserves:

```text
view != authority
redacted != verified
restricted != nonexistent
historical validity != current authority
dispute != resolved fact
evidence gap != PASS
link visibility != traversal permission
```

## Falsification evidence

The executable suite tests:

- authorized view explaining the last admitted action with traceable evidence;
- unrelated private evidence remaining absent;
- material dependency remaining visible without traversal;
- restricted dependency not being silently concealed;
- differently scoped views remaining consistent about shared historical facts;
- redaction not converting authority into apparent verification;
- missing evidence remaining explicitly `indeterminate`;
- dispute/remediation remaining visible;
- revoked capability not appearing active;
- missing capability not disappearing as though resolved;
- every material assertion carrying evidence references;
- view having no authority effect;
- deterministic regeneration.

## Claim boundary

This phase establishes only a Lab-local explanation artifact. It does not establish normative ARA view schema ownership, legal disclosure sufficiency, human comprehension metrics, accessibility/usability certification, or any authority conferred by the view itself.

## Residual uncertainty

Deferred:

- adversarial RAHP pressure review and false-independence analysis (#42);
- standards-native substitution and conformance boundaries (#43);
- final admission/disposition of IC-ARA-REL-001 (#32).

## Human acceptance boundary

Green CI can satisfy only the bounded proposition that a deterministic, privacy-scoped explanation can preserve material legitimacy distinctions and evidence traceability.

The overall case remains pre-admission.

The judgment to preserve is:

> A reviewer should be able to see not only what the system concluded, but which evidence supports it, which facts are historical, which powers are current, what is disputed, what is restricted, and what remains unknown.
