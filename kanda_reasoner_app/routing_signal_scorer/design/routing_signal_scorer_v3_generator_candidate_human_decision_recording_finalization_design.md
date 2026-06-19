# Routing Signal Scorer v3 Generator Candidate Human Decision Recording Finalization Design v1

This document defines a schema-only decision-recording-finalization boundary for the routing signal scorer v3 generator-candidate chain.

## Current state

- `current_human_decision_recording_finalization_state`: `decision_recording_finalization_not_finalized`
- `current_recorded_decision_value`: `not_recorded`
- No decision is written.
- No decision is committed or finalized.
- No human approval is recorded.
- No approval is inferred from the preparation chain, validation success, freeze success, or the word `continue`.

## Allowed outputs

- Human decision recording finalization schema.
- Future finalization evidence checklist.
- Current `not_recorded` notice.
- Current finalization-not-finalized notice.
- Stop conditions.

## Prohibited outputs

This design must not produce a recorded human decision, a decision write, a decision recording patch, a write function, a candidate patch approval, a generator candidate patch, generator authorization, dependency installation, side-effect authorization, artifact generation, artifact reading, artifact writing, source scanning, raw text materialization, embeddings, vectors, provider execution, runtime scoring, router authority, prompt auto-loading, or freeze-memory writes.

## Boundary

This schema does not export public runtime behavior and must not be imported by `contract.py` or `__init__.py`.

Future real human decision recording requires a separate governed, validated, and frozen patch.
Future generator candidate patch work requires another separate governed, validated, and frozen patch.
Future artifact generation requires another separate governed, validated, and frozen patch.
