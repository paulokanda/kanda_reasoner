# M30 - Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1

M30 is design-only. It defines immutable implementation-gate criteria for a possible later non-runtime Auxiliar/Assistant assistance implementation.

It does not implement a live gate, callable gate entrypoint, implementation permission grant, runtime state inspection, freeze-memory reading, source scanning, case discovery, live assistance builder, live contract validation, input processing, output generation, observation transformation, route comparison, route selection, prompt selection, prompt loading, runtime integration, router authority, file IO, persistence, report writing, review queue writing, human decision recording, gold mutation, registry mutation, provider/model calls, embeddings, candidate promotion, shadow-mode activation, Auxiliar/Assistant behavior, Pilot behavior, or Copilot behavior. It does not activate shadow mode or Assistant behavior.

## Required prior frozen milestones

- M18 Shadow Mode Boundary Design v1
- M19 Shadow Mode Input Output Contract Design v1
- M20 Shadow Mode Contract Validator Design v1
- M21 Shadow Mode Observation Skeleton Design v1
- M22 Shadow Mode Implementation Gate Design v1
- M23 Non Runtime Shadow Observation Implementation v1
- M24 Shadow Observation Review Evidence Design v1
- M25 Shadow Mode Readiness Gate for Assistant Boundary Review v1
- M26 Auxiliar/Assistant Boundary Design v1
- M27 Auxiliar/Assistant Input Output Contract Design v1
- M28 Auxiliar/Assistant Contract Validator Design v1
- M29 Auxiliar/Assistant Assistance Skeleton Design v1

## Future gate limits

A future implementation gate may only decide whether a later M31 scope discussion is blocked or not blocked for separate human review. It must not grant implementation permission, activate Assistant behavior, activate shadow mode, route, load prompts, persist, write reports, record human decisions, or promote candidates.

## Future M31 limits

A future M31 implementation, if separately governed and confirmed, may only be non-runtime, in-memory, caller-supplied primitive-data based, non-authoritative human-review support. It must not carry routing effect, prompt-loading effect, persistence effect, human-decision effect, candidate-promotion effect, shadow-mode activation effect, Assistant activation effect, or runtime authority.

## Next allowed milestone

After M30 is validated and frozen, proceed only to M31: Routing Signal Scorer v3 Non Runtime Auxiliar/Assistant Assistance Implementation v1, after separate governed scope review.
