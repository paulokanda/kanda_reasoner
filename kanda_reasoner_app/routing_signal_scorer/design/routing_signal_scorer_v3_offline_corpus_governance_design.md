# Routing Signal Scorer v3 Offline Corpus Governance Design v1

Feature ID: `routing_signal_scorer_v3_offline_corpus_governance_design_v1`

## Purpose

This milestone defines the offline governance contract for a future Metadata Vector Manifest generation process.

It is intentionally a governance design and validation contract only. It does not generate a corpus, does not read prompt-library files, does not read freeze entries, does not create embeddings, does not create vector values, does not build a vector index, does not implement a provider, and does not change runtime scorer behavior.

The semantic layer remains an untrusted evidence witness. It may provide evidence. It may never provide authority.

## Relationship to frozen v3 phases

This milestone comes after:

1. Routing Signal Scorer v3 Semantic Readiness Canon Registration v1.
2. Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design v1.
3. Routing Signal Scorer v3 Mock Semantic Evidence Contract v1.
4. Routing Signal Scorer v3 Metadata Vector Manifest Schema v1.

It preserves the v2 similarity shield and all v3 no-authority rules.

## Core rule

Corpus generation must be offline, human-governed, diff-reviewed, schema-validated, and frozen before runtime use.

Runtime scorer code must not generate, regenerate, repair, rebuild, or silently update the corpus.

## Non-goals

This phase must not implement:

- corpus generator logic
- prompt-library scanning
- freeze-entry scanning
- embedding generation
- vector values
- vector index
- provider implementation
- external API calls
- semantic UI display
- runtime routing behavior
- prompt-router mutation
- freeze-memory writing

## Allowed output of this milestone

This milestone may define:

- an offline corpus governance plan shape
- human-governed trigger vocabulary
- forbidden automatic triggers
- source-layer rules
- output-artifact rules
- validation gates
- audit-trail requirements
- a disabled default governance status

## Human-governed triggers

Allowed governance-review triggers are explicit human-governed events only:

- `manual_human_governed_rebuild_request`
- `schema_version_change_human_reviewed`
- `source_hash_mismatch_human_reviewed`
- `lifecycle_status_change_human_reviewed`
- `model_version_change_human_reviewed`
- `evaluation_failure_human_reviewed`

These triggers may start a future review process. They do not authorize automatic generation.

## Forbidden automatic triggers

The following must remain forbidden:

- `startup`
- `runtime_request`
- `file_watcher`
- `background_thread`
- `scheduled_job`
- `automatic_prompt_library_change`
- `automatic_freeze_write`
- `semantic_score_disagreement`

No startup rebuild. No runtime rebuild. No background rebuild. No file-watcher rebuild.

## Source layer policy

Future source layers must use curated metadata records only.

Allowed source types:

- `prompt_metadata_record`
- `routing_index_metadata_record`
- `box_manifest_metadata_record`
- `semantic_readiness_canon_metadata_record`
- `metadata_vector_manifest_item`

Forbidden source types:

- `raw_prompt_text`
- `freeze_entry_text`
- `user_query_text`
- `chat_history`
- `terminal_log_text`
- `runtime_memory`
- `vector_values`
- `embedding_values`
- `external_network_content`

Every source layer must require source structural hashes, human review, and raw-text exclusion.

## Output artifact policy

Future output artifacts are generated evidence, not canonical memory.

Allowed artifact types:

- `metadata_vector_manifest_draft`
- `metadata_vector_manifest_candidate`
- `governance_diff_report`
- `validation_report`

Forbidden artifact types:

- `embedding_vector_file`
- `vector_index`
- `provider_cache`
- `runtime_cache`
- `freeze_memory_entry`
- `prompt_library_mutation`
- `startup_delivery_mutation`

Output artifacts must not contain raw text or vector values. They must require freeze before any runtime use.

## Required validation gates

A future corpus-generation process must pass all gates before use:

- metadata vector manifest schema validation
- active-only eligibility check
- no authority fields check
- no raw prompt text check
- no user query text check
- no freeze entry text check
- no vector values check
- source structural hash check
- human review required
- diff review required
- freeze required before runtime use

## Required audit trail

Future governance must record:

- generation run ID policy
- source hashes required
- diff review required
- human reviewer required
- freeze before runtime use required

## Forbidden actions

The governance contract must forbid:

- auto-generate corpus at startup
- auto-generate corpus at runtime
- auto-rebuild vector index
- read raw prompt files at runtime
- read freeze entries at runtime for semantic search
- persist user queries
- write freeze memory
- modify prompt library
- modify startup delivery
- install ML dependency
- call external embedding API
- create vector index
- produce final route
- produce required prompts
- produce May proceed now

## Authority boundary

The offline corpus governance process may only prepare future candidate evidence under human review.

It must never decide:

- final route
- required prompts
- May proceed now
- prompt auto-loading
- freeze memory writes
- startup modification
- prompt-library modification

## Runtime boundary

The runtime scorer must remain side-effect-free.

If a future manifest is missing, stale, invalid, unfrozen, or not explicitly enabled, the scorer must fall back to lexical evidence.

Missing corpus is normal. Stale corpus is normal. Invalid corpus is normal. None of these states authorize automatic repair.

## External dependency boundary

This phase adds no external dependency.

Future use of sentence-transformers, all-MiniLM-L6-v2, FAISS, Qdrant, Chroma, ONNX, torch, or any external API requires a separate governed adapter patch with license review, dependency review, Windows/PyCharm review, fallback tests, optional disabled-by-default configuration, and freeze approval.

## Design-only implementation note

`offline_corpus_governance.py` is a standard-library-only validator for governance plan shape. It does not perform IO. It does not generate files. It does not read neighboring boxes. It does not import ML/vector libraries. It does not authorize generation.

## Future next step

After this milestone is frozen, the next safe phase is an offline evaluation corpus design or a schema-only manifest example. Real embeddings remain forbidden until later governed phases.
