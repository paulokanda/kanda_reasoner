# Routing Signal Scorer v3 Local Generator Candidate Review Gate Design v1

Feature ID: `routing_signal_scorer_v3_local_generator_candidate_review_gate_design_v1`

## Purpose

This milestone adds a review-only gate for deciding whether a future local
artifact generator candidate may even be proposed. It is not a generator. It is
a human-reviewed design boundary that sits after the dry-run artifact generation
plan and before any separately governed generator-candidate patch.

## Scope

This milestone is review-only and standard-library-only. It defines static
contract data and validation rules for future architectural review. It does not
scan sources, generate artifacts, write artifacts, read artifacts, generate
embeddings, materialize vectors, instantiate providers, or enable semantic
runtime behavior.

## Required prior milestones

- Routing Signal Scorer v3 Closure Shield v1 must remain frozen.
- Routing Signal Scorer v3 Disabled Generation Boundary Design v1 must remain frozen.
- Routing Signal Scorer v3 Dry-Run Artifact Generation Plan Design v1 must remain frozen.
- Freeze-hint state-machine regressions must remain passing.
- Routing Signal Scorer v2 runtime-lite must remain advisory-only.

## Review-gate behavior

The review gate may produce only review evidence:

- candidate readiness summary
- candidate risk register
- input manifest requirements
- privacy review requirements
- dependency review requirements
- resource budget requirements
- validation matrix requirements
- permanent blocker list
- recommended candidate patch boundary

The review gate cannot authorize generation. It cannot create a generator
candidate patch by itself. It cannot create files, scan project materials, or
turn on runtime behavior. Future generator work still requires a separate
governed, validated, and frozen patch.

## Permanent blockers

The following conditions block future generator-candidate work until corrected:

- no explicit human request for generator-candidate review
- missing privacy review
- missing dependency review
- missing resource budget review
- missing redaction review
- missing authority-leakage review
- missing input-manifest review
- request to generate artifacts immediately
- request to write artifacts immediately
- request to scan sources immediately
- request to materialize raw text immediately
- request to generate embeddings immediately
- request to enable provider execution immediately
- request to enable runtime semantic scoring immediately
- request to modify router authority immediately
- request to bypass a future governed patch

## Forbidden behavior

This milestone must not:

- Do not implement artifact generation
- implement artifact generation
- write, overwrite, read, load, or discover semantic artifacts
- scan prompt libraries, freeze entries, project sources, or runtime user queries
- materialize raw prompt text, user query text, source text, freeze entry text,
  embedding values, vector values, or vector indexes
- add embeddings, TF-IDF dependencies, vector stores, providers, network access,
  credential loading, or model loading
- add startup, runtime, background, or file-watcher generation
- modify deterministic router behavior
- let review output decide routes, required prompts, missing context, missing
  behavior, or May proceed now
- auto-load prompts from review output
- write freeze memory from review output

## Next allowed step

After this review gate is installed, validated, and frozen, the next safe action
is not automatic generation. The next safe action is a human architectural review
of whether a local generator candidate should be proposed at all.
