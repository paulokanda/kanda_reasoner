# P0 - Pilot/Copilot Scope Charter and Entry Gate Design v1

`pilot_copilot_scope_charter_entry_gate_design.py` defines the first governed
post-M35 P-series artifact after RG-PILOT-000 was frozen into router prompt
logic. It is an immutable design-only scope charter and entry-gate record.

P0 does not implement Pilot, Copilot, route projection, route comparison, prompt
loading, prompt library scanning, runtime integration, persistence, evidence
writing, review queue writing, report writing, human decision recording, gold or
registry mutation, training-data use, batch mode, limited shadow runtime,
provider/model calls, embeddings, candidate promotion, or runtime authority.

P0 preserves these governing rules:

- capability is not readiness;
- projection is not directive advice;
- human review is mandatory but non-approving;
- Pilot output is opt-in, ephemeral, in-memory, non-training, and non-batch by default;
- disagreement/divergence taxonomy must precede implementation;
- Pilot must reproduce frozen router/canon outcomes before divergence evidence is trusted;
- Copilot and runtime shadow mode are deferred to separately governed future scopes.

Next allowed milestone after P0 validation, freeze, startup freeze context refresh,
and `FREEZE_MEMORY_STATUS: OK`:

P1 - Routing Signal Scorer v3 Pilot Boundary Design v1.
