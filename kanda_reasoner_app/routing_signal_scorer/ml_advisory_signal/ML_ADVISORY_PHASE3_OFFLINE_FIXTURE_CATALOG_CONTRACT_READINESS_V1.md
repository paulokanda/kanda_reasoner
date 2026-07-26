# ML Advisory Signal Phase 3 Offline Fixture Catalog Contract Readiness v1

This readiness note does not implement Phase 3. It records the minimum safe
shape for a future fixture catalog contract after the Phase 2 result review gate
is validated and frozen.

Future Phase 3 may only define a governed offline fixture catalog contract for
caller-supplied, in-memory advisory evaluation fixtures. The catalog must be a
contract and validation surface, not a prompt library reader, not freeze-memory reader, not router-canon reader, not persistence, and not runtime ML.

## Required Phase 3 preconditions

- Phase 1a boundary contract frozen.
- Phase 1a result review gate frozen.
- Phase 1b non-runtime design audit contract frozen.
- Phase 1b result review gate frozen.
- Phase 2 offline evaluation harness contract frozen.
- Phase 2 result review gate frozen.
- MLRT remains closed and paused.
- Patch install delivery guard remains active for every patch output.

## Future Phase 3 allowed surface

A future Phase 3 fixture catalog contract may define in-memory fixture schema,
fixture names, synthetic or caller-supplied cases, expected abstention behavior,
expected firewall rejection behavior, and route-invariance assertions.

## Future Phase 3 forbidden surface

A future Phase 3 patch must not add real ML, provider calls, embeddings, vector
stores, persistence, report persistence, prompt loading, prompt registry
mutation, prompt library reads, freeze-memory reads or writes, router-canon
reads, runtime shadow mode, router prompt logic modification, router final
selection modification, route authority, advisory rankings, free-text advisory
explanations, training, calibration, model improvement, runtime Pilot behavior,
runtime Copilot behavior, or MLRT-113.

## Next planned feature

Routing Signal Scorer ML Advisory-Signal Phase 3 Offline Fixture Catalog Contract v1
