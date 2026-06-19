# Routing Signal Scorer v3 Generator Candidate Side-Effect Boundary Design v1

This milestone is design only, schema only, and side-effect boundary evidence only. It
creates the metadata side-effect boundary that a possible future generator-candidate patch
would have to provide. It does not create a generator candidate patch, does not authorize a generator candidate, and does not implement a generator.

## Scope

The scope is `generator_candidate_patch_side-effect boundary_only`.

The current side-effect boundary state is `not_side-effect boundary_defined`, with effect
`no_effect_schema_only_not_side-effect boundary_defined`.

## Required prior milestones

A future side-effect boundary can only be considered after the v3 closure shield, disabled
generation boundary, dry-run plan, local generator candidate review gate, human
review record, human decision intake, actual human decision record design,
actual decision recording boundary, generator candidate proposal schema,
generator candidate proposal review, and generator candidate patch preflight
have been frozen and their relevant tests are still passing.

## Non-goals

This milestone does not:

- create a generator candidate patch
- authorize a generator candidate
- implement artifact generation
- write, overwrite, read, load, or discover semantic artifacts
- scan prompt libraries, freeze entries, project sources, or runtime user queries
- materialize raw prompt text, user query text, freeze entry text, source text,
  embedding values, vector values, or vector indexes
- add embeddings, TF-IDF side-effect operations, vector stores, providers, network access,
  credential loading, or model loading
- add startup, runtime, background, or file-watcher generation
- modify deterministic router behavior
- decide routes, required prompts, missing context, missing behavior, or May
  proceed now
- auto-load prompts
- write freeze memory

## Future work boundary

Any future candidate patch requires another separately governed patch with its
own validation evidence and KBSC shielding. Any future artifact generation work
requires another separately governed and frozen patch after that.

- Current side-effect boundary state: `not_side-effect boundary_defined`.

- Current side-effect boundary state: `not_side-effect boundary_defined`.

- This design only declares future allowed and forbidden side-effect boundary expectations.

- This design is a side-effect boundary schema only.

- Current side-effect boundary state: `not_side-effect boundary_defined`.

- It installs no side-effect operations and adds no side-effect imports.

- Standard library only remains the default until a separate governed patch says otherwise.

- Third-party, embedding, vector-store, provider, network, credential, model-loading, startup, runtime, and file-watcher side-effect operations remain forbidden here.

- Current side-effect boundary state: `not_side_effect_boundary_defined`.

- It performs no artifact writes, artifact reads, source scans, raw text materialization, vector index writes, provider execution, startup generation, or runtime generation.

- Any future side-effect requires a separate governed, validated, and frozen patch.
