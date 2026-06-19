# Routing Signal Scorer v3 Generator Candidate Proposal Review Design v1

This milestone is design only, schema only, and review evidence only.

It defines an inert review schema for checking a future generator candidate
proposal. It does not create a generator candidate patch, does not authorize a generator candidate, does not authorize a generator implementation, and does
not generate, write, read, load, or discover semantic artifacts.

Current state: `not_reviewed`.

Current effect: `no_effect_schema_only_not_reviewed`.

## hard boundary

This milestone must not:

- record a real human decision;
- create a generator candidate patch;
- authorize a generator candidate patch;
- implement artifact generation;
- write, overwrite, read, load, or discover semantic artifacts;
- scan prompt libraries, freeze entries, project sources, or runtime user queries;
- materialize raw prompt text, user query text, freeze entry text, source text, embedding values, vector values, or vector indexes;
- add embeddings, TF-IDF dependencies, vector stores, providers, network access, credential loading, or model loading;
- add startup, runtime, background, or file-watcher generation;
- modify deterministic router behavior;
- decide routes, required prompts, missing context, missing behavior, or May proceed now;
- auto-load prompts;
- write freeze memory from proposal-review output.

## allowed output

The only allowed output is review evidence:

- proposal review schema;
- proposal input checklist;
- proposal review questions;
- proposal rejection reasons;
- future review outcome vocabulary;
- review effect policy summary;
- stop conditions list.

## next step policy

A future proposal review outcome such as
`permit_separate_governed_generator_candidate_patch_review_only` still does not
authorize generation. It only means another separately governed patch may be
proposed for review. Real artifact generation remains out of scope until later
separate approval, validation, shielding, and freeze.
