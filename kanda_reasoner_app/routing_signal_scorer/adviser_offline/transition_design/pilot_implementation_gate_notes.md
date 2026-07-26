# P7 - Pilot Implementation Gate Design v1

This note records the design-only implementation gate for the Pilot P-series.
P7 defines static conditions that must remain closed unless a later, separately
governed milestone satisfies them. P7 does not evaluate a gate and does not
authorize implementation.

P7 is the final design-only gate before any future non-runtime Pilot candidate
implementation may be considered. It preserves the post-P6 chain and keeps the
next milestone limited to a non-runtime, opt-in, case-local, in-memory-only
Pilot candidate. Copilot, runtime authority, prompt loading, persistence,
training-data use, batch execution, provider calls, embeddings, and Limited
Shadow Runtime remain outside the allowed scope.

## Design-only gate stages

1. Freeze chain and installer canon.
2. Scope boundary.
3. Safety invariants.

These are stage designs only. P7 does not run them.

## Required safety invariants

- previous M35/RG-PILOT-000/P0-P6 freezes complete
- KANDA root-drive ZIP staging installer canon preserved
- next implementation scope limited to non-runtime Pilot candidate only
- match-before-disagree preserved
- critical boundary error budget remains zero
- human review mandatory but not approval
- opt-in per invocation and in-memory-only design constraints preserved

## Forbidden in P7

- no gate evaluation
- no implementation approval
- no Pilot candidate creation
- no callable Pilot
- no live validation
- no input processing
- no output generation
- no evidence collection
- no evidence packet generation
- no simulation execution
- no reproduction harness execution
- no gold loading
- no freeze-memory reading
- no prompt-library reading
- no route comparison execution
- no metric calculation
- no disagreement trust
- no Pilot implementation
- no Copilot implementation
- no projection implementation
- no prompt loading
- no persistence
- no human decision recording
- no approval recording
- no training-data use
- no batch mode
- no Limited Shadow Runtime
- no runtime authority

Next allowed milestone after P7 validation, freeze, startup refresh, and
`FREEZE_MEMORY_STATUS: OK`: P8 - Routing Signal Scorer v3 Non-Runtime Pilot
Candidate Implementation v1.
