# Routing Signal Scorer v3 Generator Candidate Human Decision Record Design v1

Feature ID: `routing_signal_scorer_v3_generator_candidate_human_decision_record_design_v1`

Schema version: `3.30-generator-candidate-human-decision-record-design`

This milestone is **schema only**. It follows `Routing Signal Scorer v3 Generator Candidate Human Decision Gate Design v1` and defines the inert shape of a future human decision record.

## Current state

`human_decision_record_not_recorded`

The current recorded decision value is `not_recorded`.

The current effect is `no_effect_schema_only_not_recorded`.

## Purpose

This design defines how a future explicit human decision record could be represented, including required prior milestones, required future recording inputs, allowed future recorded decision values, no-authority assertions, record-effect policy, and stop conditions.

## Non-goals

This milestone does not record a human decision.

This milestone does not infer approval from the preparation chain.

This milestone does not approve a generator candidate patch.

This milestone does not create or authorize a generator candidate patch.

This milestone does not authorize generation.

This milestone does not install dependencies.

This milestone does not authorize side effects.

This milestone does not write, read, overwrite, load, or discover semantic artifacts.

This milestone does not scan prompt libraries, freeze entries, project sources, or runtime user queries.

This milestone does not materialize raw prompt text, raw user query text, freeze entry text, source text, embedding values, vector values, or vector indexes.

This milestone does not add providers, model loading, network access, credentials, runtime semantic scoring, startup generation, background generation, file-watcher generation, router authority, or public runtime exports.

## Future only

Any real decision recording requires a separate governed, validated, and frozen patch.

Any generator candidate patch requires a separate governed, validated, and frozen patch after the decision recording boundary is satisfied.

Any artifact generation requires another separate governed, validated, and frozen patch.
