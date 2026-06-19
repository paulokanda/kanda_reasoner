# Routing Signal Scorer v3 Generator Candidate Human Decision Recording Boundary Design v1

This is a schema-only recording-boundary milestone for `kanda_reasoner_app/routing_signal_scorer`.

It follows `Routing Signal Scorer v3 Generator Candidate Human Decision Record Design v1` and defines the boundary that any future explicit human decision recording patch must pass through.

## Current state

`decision_recording_boundary_not_open`

The current recorded decision value remains:

`not_recorded`

No decision is written by this milestone.

## What this design allows

- A schema-only human decision recording boundary contract.
- A future recording evidence checklist.
- Future allowed recording actions vocabulary.
- Current `not_recorded` notice.
- Stop conditions before any future decision recording.

## What this design forbids

- Real human decision recording.
- Human decision writing.
- Inferring approval from preparation closure, validation success, freeze success, or user `continue` messages.
- Candidate patch approval.
- Generator candidate patch creation or authorization.
- Generator implementation.
- Dependency installation or authorization.
- Side-effect authorization.
- Artifact generation, writing, reading, loading, or discovery.
- Source scanning or raw text materialization.
- Embeddings, vectors, providers, network access, credentials, or model loading.
- Runtime semantic scoring, router authority, startup generation, background generation, or public runtime export.
- Freeze memory writing or prompt auto-loading from this boundary output.

## Required future evidence before any decision recording patch

A later governed patch must provide explicit human confirmation to record a decision, decision scope, referenced freeze IDs, and acknowledgements that generator implementation, artifact IO, source scanning, dependencies, side effects, runtime behavior, and router authority remain non-goals unless separately governed.

## KBSC boundary

This milestone preserves the authority boundary, dependency direction, truth-source priority, public contract, side-effect boundary, regression-critical outputs, and do-not-invade-other-box rules. It does not modify deterministic routing behavior and does not export public runtime behavior.
