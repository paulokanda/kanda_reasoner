# Routing Signal Scorer v3 Generator Candidate Patch Envelope Design v1

This milestone is design only, schema only, and envelope evidence only. It
creates the metadata envelope that a possible future generator-candidate patch
would have to provide. It does not create a generator candidate patch, does not authorize a generator candidate, and does not implement a generator.

## Scope

The scope is `generator_candidate_patch_envelope_only`.

The current envelope state is `not_enveloped`, with effect
`no_effect_schema_only_not_enveloped`.

## Required prior milestones

A future envelope can only be considered after the v3 closure shield, disabled
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
- add embeddings, TF-IDF dependencies, vector stores, providers, network access,
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
