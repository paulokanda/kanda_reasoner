# Routing Signal Scorer v3 Human Decision Intake Design v1

## Status

Design only. Schema only. Review evidence only.

This milestone defines the shape of a future human decision intake record. It does not record a real human decision and does not authorize a generator candidate.

## Purpose

The previous milestone created a human architectural review record schema. This milestone adds the next boundary: how a future human decision could be represented before any generator candidate is even proposed.

The boundary is intentionally inert. It exists to prevent a vague approval such as "go next" from becoming generator authorization.

## Non-authority guarantees

This milestone must not:

- record an actual human decision;
- authorize a generator candidate patch;
- generate artifacts;
- write, overwrite, read, load, or discover artifacts;
- scan prompt libraries, freeze entries, project sources, or runtime user queries;
- materialize raw prompt text, user query text, freeze entry text, source text, embedding values, vector values, or vector indexes;
- add embeddings, TF-IDF dependencies, vector stores, providers, network access, credential loading, or model loading;
- add startup, runtime, background, or file-watcher generation;
- modify deterministic router behavior;
- decide routes, required prompts, missing context, missing behavior, or May proceed now;
- auto-load prompts;
- write freeze memory.

## Required prior milestones

- Routing Signal Scorer v3 Closure Shield v1
- Routing Signal Scorer v3 Disabled Generation Boundary Design v1
- Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1
- Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1
- Routing Signal Scorer v3 Human Architectural Review Record Design v1
- v2 similarity runtime-lite advisory-only regressions
- freeze-hint state-machine regressions

## Allowed future decision values

The schema names future decision values only. This milestone does not record any of them as real project state.

- `not_recorded`
- `defer_generator_candidate_proposal`
- `reject_generator_candidate_proposal`
- `permit_separate_generator_candidate_proposal_review_only`

Even a future `permit_separate_generator_candidate_proposal_review_only` value would not authorize generation. It would only allow a separately governed generator-candidate proposal to be reviewed.

## Current decision value

The current schema-only decision value is always:

```text
not_recorded
```

## Future work boundary

A future actual decision record requires a separate governed, validated, and frozen patch.

A future generator candidate requires another separate governed, validated, and frozen patch after that. It still must not implement real generation unless explicitly governed and shielded.
