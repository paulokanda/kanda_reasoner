# Routing Signal Scorer v3 Generator Candidate Human Decision Recording Candidate Design v1

This is a schema-only decision-recording-candidate milestone inside `kanda_reasoner_app/routing_signal_scorer`.

It follows `Routing Signal Scorer v3 Generator Candidate Human Decision Recording Boundary Design v1`.

## Scope

This milestone defines how a future human decision recording candidate could be described for review.

Current state: `decision_recording_candidate_not_created`.

Current recorded decision value: `not_recorded`.

No decision is recorded. No decision is written. No approval is inferred from the preparation chain, from validation output, from freeze output, or from the word `continue`.

## Explicit non-goals

- No real human decision recording.
- No decision write.
- No candidate patch approval.
- No generator candidate patch creation.
- No generator candidate patch authorization.
- No generator implementation.
- No dependency install or dependency authorization.
- No side-effect authorization.
- No artifact generation, writing, reading, loading, discovery, or overwrite.
- No prompt-library, freeze-entry, project-source, or runtime-query scanning.
- No raw text materialization.
- No embeddings, vectors, vector indexes, providers, model loading, credentials, or network access.
- No startup generation, runtime generation, background generation, or file-watcher generation.
- No deterministic router change.
- No public runtime export.

## Current effect

`no_effect_schema_only_not_created_not_recorded`

The output is review/schema material only and does not export public runtime behavior.

## Future work

A real human decision recording candidate, a candidate patch, or artifact generation each requires a separate governed, validated, and frozen patch.
