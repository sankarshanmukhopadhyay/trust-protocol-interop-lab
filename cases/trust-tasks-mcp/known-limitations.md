# Known limitations

- No multi-implementation interoperability run has yet been recorded for binding v0.3.
- The 23-scenario test plan defines evidence requirements but does not yet ship a reference runner for every vector.
- The case does not define production credential/key custody, JSON Schema engine choice, cryptosuite choice, or an MCP principal-to-VID profile.
- Authorization remains a consumer-policy decision; the binding defines when it must be evaluated and re-evaluated, not a universal authorization model.
- `trust-task-control` ↔ MCP `tasks/cancel` automation is intentionally profile-defined rather than implicit.
- The Trust Tasks baseline is an editor's draft pinned by commit because upstream document version `0.3` continues to evolve.
