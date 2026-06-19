# Routing Signal Scorer v3 — M24 Shadow Observation Review Evidence Design v1

M24 is a design-only post-Adviser milestone. It defines the future review-evidence envelope that may later summarize M23 non-runtime shadow observations for human review.

## Status

- Adviser phase remains closed through M16.
- M17 remains post-Adviser transition design only.
- M18 remains immutable shadow-mode boundary design only.
- M19 remains input/output contract design only.
- M20 remains contract validator design only.
- M21 remains observation skeleton design only.
- M22 remains implementation gate design only.
- M23 remains the first non-runtime in-memory observation implementation.
- M24 remains review evidence design only.
- Shadow mode is not active.
- Auxiliar/Assistant has not started.
- Candidate promotion remains blocked.
- Runtime router authority remains not granted.

## What M24 defines

M24 defines future review-evidence fields for a later governed builder:

- review evidence record kind
- routing case id
- source observation schema version
- review reason summary
- constraint flags for review
- authority notice
- review storage design status
- explicit human-review requirement
- no routing effect
- no prompt-loading effect
- no candidate-promotion effect

## What M24 does not do

M24 does not:

- build review evidence from a live observation
- transform M23 outputs
- validate live inputs
- compare routes
- execute observations
- persist observations
- write reports
- write review queues
- write registries
- mutate gold sets
- record human approval, rejection, or override decisions
- read or write files
- load prompts
- integrate with runtime routing
- grant router authority
- activate shadow mode
- start Auxiliar/Assistant behavior
- promote candidates
- call providers or models
- use embeddings or vector indexes

## Boundary rule

M24 is only a static field-and-boundary design. Any executable evidence builder, persistence target, review queue writer, or human decision record belongs to a later separately governed milestone.

## Next milestone

After M24 is installed, validated, and frozen with startup freeze context refreshed, the next safe milestone is:

M25 - Routing Signal Scorer v3 Shadow Mode Readiness Gate for Assistant Boundary Review v1

M24 does not persist observations, does not write reports, and does not record human approval, rejection, or override decisions.
