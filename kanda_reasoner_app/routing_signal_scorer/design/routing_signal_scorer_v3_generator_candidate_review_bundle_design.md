# Routing Signal Scorer v3 Generator Candidate Review Bundle Design v1

This file documents a design only, schema only review bundle for a future generator candidate patch.

## Boundary

This milestone bundles the frozen preparation gates for review only. It does not create a generator candidate patch, does not authorize a generator candidate, does not implement generation, does not install dependencies, does not authorize side effects, does not write/read/load/discover semantic artifacts, does not scan source or prompt/freeze text, does not materialize raw text, does not generate embeddings or vectors, does not execute providers, does not enable runtime semantic scoring, and does not change router authority.

## Current state

`not_review_bundle_defined`

The current effect is `no_effect_schema_only_not_review_bundle_defined`.

## Required frozen inputs

- proposal schema
- proposal review
- candidate patch preflight
- candidate patch envelope
- candidate patch skeleton
- candidate patch file-set
- dependency boundary
- side-effect boundary
- runtime-lite and freeze-hint regressions

## Allowed output

The only allowed output is review readiness metadata such as a checklist, required inputs, required boundaries, required validation summary, and stop conditions.

## Explicit non-goals

- no candidate patch
- no generator authorization
- no artifact generation
- no artifact writing or reading
- no source scanning
- no raw text materialization
- no embeddings
- no vectors
- no providers
- no runtime behavior change
- no public runtime export
- no router authority

Any future candidate patch still requires another separately governed patch with explicit validation evidence and freeze.
