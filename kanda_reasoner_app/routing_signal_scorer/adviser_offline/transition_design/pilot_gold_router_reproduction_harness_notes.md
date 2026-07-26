# P4 - Pilot Gold/Frozen Router Reproduction Harness Design v1

This note records the design-only boundary for a future Pilot reproduction harness.
P4 exists because the Pilot must **match-before-disagree**: no Pilot disagreement
label from P3 may be trusted until a later governed harness first proves that the
candidate can reproduce frozen router/canon outcomes on governed reference cases.

P4 does not implement the harness. It does not load gold sets, read freeze memory,
read prompt libraries, inspect runtime router state, compare routes, calculate
scores, rank candidates, certify readiness, write reports, persist records, train
models, run batch mode, activate Limited Shadow Runtime, or grant Pilot/Copilot
authority.

## Design-only reference classes

- Frozen router/canon reference: future caller-supplied immutable reference summary
  with freeze ID, feature ID, validation marker, and human-reviewed source summary.
- Governed case reference: future caller-supplied JSON-safe case summary approved
  under a later governed harness scope.
- Expected output reference: future human-reviewed frozen output summary. It must
  not become route selection, prompt selection, or prompt loading.

## Future harness phase designs

1. Preflight provenance check design.
2. Frozen outcome alignment design.
3. Critical failure blocker design.

These are vocabulary and boundary records only. P4 adds no callable harness phase.

## Required future metric concepts

- Exact frozen outcome match is required before any disagreement trust.
- Critical boundary error count must remain zero.
- Human review remains mandatory and non-approving.
- Effect fields must remain fixed to none.

## Forbidden in P4

- no reproduction harness execution
- no gold loading
- no freeze-memory reading
- no prompt-library reading
- no route comparison execution
- no score calculation
- no disagreement trust
- no Pilot implementation
- no Copilot implementation
- no projection implementation
- no runtime authority
- no persistence
- no training-data use
- no batch mode
- no Limited Shadow Runtime

Next allowed milestone after P4 validation, freeze, startup refresh, and
`FREEZE_MEMORY_STATUS: OK`: P5 - Routing Signal Scorer v3 Pilot Simulation
Skeleton Design v1.
