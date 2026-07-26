# ML Advisory Signal Phase 4 Offline Advisor Comparison Contract Readiness v1

This readiness note does not implement Phase 4. It records the minimum safe
shape for a future offline advisor comparison contract after the Phase 3 result
review gate is validated and frozen.

Future Phase 4 may only define an offline in-memory comparison contract that
uses already-safe advisory interfaces, the offline evaluation harness, and the
synthetic fixture catalog. It may compare NullAdvisor and MockAdvisor-style
behavior for abstention, firewall, and route-invariance evidence only.

## Required Phase 4 preconditions

- Phase 1a boundary contract frozen.
- Phase 1a result review gate frozen.
- Phase 1b non-runtime design audit contract frozen.
- Phase 1b result review gate frozen.
- Phase 2 offline evaluation harness contract frozen.
- Phase 2 result review gate frozen.
- Phase 3 offline synthetic fixture catalog contract frozen.
- Phase 3 result review gate frozen.
- Patch install delivery guard remains active for every patch output.
- MLRT remains closed and paused.

## Future Phase 4 allowed surface

A future Phase 4 patch may define an offline comparison contract for safe local
advisor stubs. It may produce in-memory comparison summaries and explicit
abstention/route-invariance evidence for tests. It may not persist reports.

## Future Phase 4 forbidden surface

A future Phase 4 patch must not add real ML, provider calls, embeddings, vector
stores, persistence, report persistence, prompt loading, prompt registry
mutation, prompt library reads, freeze-memory reads or writes, router-canon
reads, runtime shadow mode, router prompt logic modification, router final
selection modification, route authority, advisory rankings, free-text advisory
explanations, training, calibration, model improvement, runtime Pilot behavior,
runtime Copilot behavior, or MLRT-113.

## Next planned feature

Routing Signal Scorer ML Advisory-Signal Phase 4 Offline Advisor Comparison Contract v1
