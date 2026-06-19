# Routing Signal Scorer v3 Generator Candidate Proposal Schema Design v1

This milestone is design only, schema only, review evidence only.

It defines the future schema for a generator candidate proposal, but it does not create a generator candidate patch. It does not authorize a generator candidate, does not authorize generator candidate implementation, does not implement generation, and does not enable semantic runtime behavior.

Current state: `not_proposed`.

Current effect: `no_effect_schema_only_not_proposed`.

## Scope

The schema may describe what a future, separately governed generator-candidate
proposal would need to include after a separate recorded human decision permits
review-only candidate proposal work.

This milestone does not satisfy that prerequisite by itself.

## Required prior milestones

- Routing Signal Scorer v3 Closure Shield v1 frozen.
- Routing Signal Scorer v3 Disabled Generation Boundary Design v1 frozen.
- Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1 frozen.
- Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1 frozen.
- Routing Signal Scorer v3 Human Architectural Review Record Design v1 frozen.
- Routing Signal Scorer v3 Human Decision Intake Design v1 frozen.
- Routing Signal Scorer v3 Actual Human Decision Record Design v1 frozen.
- Routing Signal Scorer v3 Actual Human Decision Recording Boundary Design v1 frozen.
- Runtime-lite advisory-only regressions passing.
- Freeze-hint state-machine regressions passing.

## Non-goals

This milestone does not:

- record a real human decision;
- create a generator candidate patch;
- authorize generator candidate implementation;
- generate semantic artifacts;
- write semantic artifacts;
- read semantic artifacts;
- scan prompt libraries, freeze entries, project sources, or runtime user queries;
- materialize raw prompt text, user query text, freeze entry text, source text,
  embedding values, vector values, or vector indexes;
- add embeddings, TF-IDF dependencies, vector stores, providers, network access,
  credential loading, or model loading;
- add startup, runtime, background, or file-watcher generation;
- modify deterministic router behavior;
- decide routes, required prompts, missing context, missing behavior, or May
  proceed now;
- auto-load prompts;
- write freeze memory from proposal output.

## Future proposal requirements

A future generator candidate proposal must be a separate governed patch and must
include:

- traceability to a separate recorded human decision;
- scope statement;
- non-goal statement;
- privacy boundary review;
- authority boundary review;
- source selection policy;
- raw text handling policy;
- artifact lifecycle policy;
- dependency budget policy;
- resource budget policy;
- validation plan;
- rollback plan;
- KBSC shielding plan;
- stop conditions.

## Authority boundary

This schema is not router authority. It is not semantic evidence. It is not an
artifact generator. It is not an artifact writer. It is not an artifact reader.
It is not a provider boundary. It is not a runtime semantic scorer.

Any future generator candidate proposal requires another separately governed,
validated, and frozen patch.
