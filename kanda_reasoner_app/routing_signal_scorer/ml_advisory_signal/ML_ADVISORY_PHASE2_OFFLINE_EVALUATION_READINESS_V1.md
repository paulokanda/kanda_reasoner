# ML Advisory Signal Phase 2 Offline Evaluation Readiness v1

This readiness note is not an implementation plan and does not authorize Phase
2. It records what must be true before a future Phase 2 patch can be proposed.

A future Phase 2 offline evaluation harness may be considered only after Phase
1b is validated, frozen, and reviewed.

## Required preconditions

- Phase 1a boundary contract is frozen.
- Phase 1a result-review gate is frozen.
- Phase 1b non-runtime design audit contract is frozen.
- Phase 1b result-review gate is frozen.
- NullAdvisor and MockAdvisor remain deterministic and non-authoritative.
- Output firewall remains enforced.
- Prompt Intake remains the only safe door for future prompts.
- Manual Prompt Code Hint remains classification help only.
- MLRT remains closed and paused.

## Future Phase 2 allowed shape

The future Phase 2 patch may only create an offline, in-memory, caller-supplied
comparison harness. It may compare NullAdvisor and MockAdvisor outputs against
provided test fixtures, but the final governed route must remain unchanged.

## Future Phase 2 forbidden shape

A future Phase 2 patch must not add real ML, provider calls, embeddings, vector
stores, persistence, report persistence, prompt loading, prompt registry
mutation, freeze-memory read or write, router-canon direct access, runtime
shadow mode, router prompt logic modification, router final selection
modification, route authority, runtime Pilot behavior, or runtime Copilot
behavior.

Phase 2 must not create MLRT-113 unless a separate governed risk reopens MLRT.
