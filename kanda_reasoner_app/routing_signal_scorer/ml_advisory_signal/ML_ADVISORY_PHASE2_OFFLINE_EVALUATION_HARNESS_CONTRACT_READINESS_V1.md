# ML Advisory Signal Phase 2 Offline Evaluation Harness Contract Readiness v1

This readiness note does not implement Phase 2. It records the minimum contract
shape for a future Phase 2 patch after the Phase 1b result review gate is
validated and frozen.

Future Phase 2 may only create an offline, in-memory, caller-supplied evaluation
harness that compares NullAdvisor and MockAdvisor telemetry against explicit
fixtures. Final governed route selection must remain unchanged.

## Required Phase 2 preconditions

- Phase 1a boundary contract frozen.
- Phase 1a result review gate frozen.
- Phase 1b non-runtime design audit contract frozen.
- Phase 1b result review gate frozen.
- MLRT remains closed and paused.
- Output firewall remains enforced.
- NullAdvisor and MockAdvisor remain deterministic and non-authoritative.
- Prompt Intake remains the only safe door for future prompts.
- Manual Prompt Code Hint remains classification help only.

## Future Phase 2 allowed surface

A future Phase 2 harness may use only caller-supplied, in-memory fixtures and
bounded telemetry. It may run contract checks that prove advisory output does
not change deterministic final route decisions.

## Future Phase 2 forbidden surface

A future Phase 2 patch must not add real ML, provider calls, embeddings, vector
stores, persistence, report persistence, prompt loading, prompt registry
mutation, prompt library reads, freeze-memory reads or writes, router-canon
reads, runtime shadow mode, router prompt logic modification, router final
selection modification, route authority, advisory rankings, free-text advisory
explanations, training, calibration, model improvement, runtime Pilot behavior,
or runtime Copilot behavior.

Next planned feature after this review gate, if frozen:

Routing Signal Scorer ML Advisory-Signal Phase 2 Offline Evaluation Harness Contract v1
