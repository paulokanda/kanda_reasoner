# M29 - Routing Signal Scorer v3 Auxiliar/Assistant Assistance Skeleton Design v1

M29 is design-only. It defines immutable skeleton slots for possible later Auxiliar/Assistant human-review support.

It does not implement a live assistance builder, callable Assistant helper, live contract validation, input processing, output generation, observation transformation, route comparison, route selection, prompt selection, prompt loading, runtime integration, router authority, file IO, persistence, report writing, review queue writing, human decision recording, gold mutation, registry mutation, provider/model calls, embeddings, candidate promotion, shadow-mode activation, Auxiliar/Assistant behavior, Pilot behavior, or Copilot behavior. It does not activate shadow mode or Assistant behavior.

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

## Future skeleton limits

A future assistance skeleton may only reserve non-authoritative in-memory human-review support slots. It must carry no routing effect, no prompt-loading effect, no persistence effect, no human-decision effect, no candidate-promotion effect, no shadow-mode activation effect, and no Assistant activation effect.

## Next allowed milestone

After M29 is validated and frozen, proceed only to M30: Routing Signal Scorer v3 Auxiliar/Assistant Implementation Gate Design v1, after separate governed scope review.
