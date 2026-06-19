# Routing Signal Scorer v3 Generator Candidate Human Decision Recording Implementation Design v1

This is a schema-only decision-recording-implementation design for `kanda_reasoner_app/routing_signal_scorer`.

It follows the frozen human decision recording candidate design and defines the shape of a future
human decision recording implementation review. It does not implement the decision write and does
not record approval.

## Current state

- Feature ID: `routing_signal_scorer_v3_generator_candidate_human_decision_recording_implementation_design_v1`
- Schema version: `3.33-generator-candidate-human-decision-recording-implementation-design`
- Current implementation state: `decision_recording_implementation_not_implemented`
- Current recorded decision value: `not_recorded`

## Non-authority rules

- No real human decision is recorded.
- No decision is written.
- No recording implementation is created.
- No write function is enabled.
- No approval is inferred from the preparation chain, freeze chain, validation output, or the word `continue`.
- No generator candidate patch is created or authorized.
- No generator implementation is authorized.
- No dependencies are installed, added, or authorized.
- No side effects are authorized.
- No semantic artifact is generated, written, read, loaded, discovered, or overwritten.
- No source scanning or raw text materialization is authorized.
- No embeddings, vectors, providers, runtime semantic scoring, router authority, startup generation,
  background generation, or public runtime export are added.

## Future-governed requirements

A future patch that actually records a human decision must be separate, governed, validated, and frozen.
It must provide explicit human decision text, actor/source, scope, timestamp/session reference, relevant
freeze IDs, and rollback/stop conditions. This design only prepares the review schema and stop rules.

## Public/runtime export

This module is intentionally not exported by `contract.py` or `__init__.py` and does not export public runtime behavior.
