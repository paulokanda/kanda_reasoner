# Routing Signal Scorer v3 Metadata Vector Manifest Schema v1

Feature ID: `routing_signal_scorer_v3_metadata_vector_manifest_schema_v1`

Status: schema and validation contract only.

This milestone adds a standard-library-only schema contract for the future Metadata Vector Manifest. It does not implement embeddings, vector search, a corpus generator, provider logic, prompt loading, runtime routing authority, or a vector index.

## Purpose

The Metadata Vector Manifest is the only future embeddable source for semantic routing evidence. It is a curated, generated, human-reviewed metadata artifact that abstracts canonical routing contexts into safe semantic-evidence items.

The manifest exists to prevent raw prompt files, freeze entries, user queries, terminal logs, or chat history from becoming the embedding source.

## Relationship to frozen v3 design

This schema implements the next narrow step after the frozen structural design and mock semantic evidence contract:

1. Semantic-readiness canon: on-request router canon.
2. Structural Contract and Semantic Readiness Design: architecture and safety boundary.
3. Mock Semantic Evidence Contract: disabled/null provider and candidate evidence shape.
4. Metadata Vector Manifest Schema: curated manifest schema and validation contract.

This is still before real ML.

## Master rule

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

The Metadata Vector Manifest may describe candidate evidence items. It may never decide final route, required prompts, May proceed now, prompt loading, freeze writing, or startup mutation.

## What this phase adds

- `metadata_vector_manifest_schema.py`
- `build_empty_metadata_vector_manifest`
- `validate_metadata_vector_manifest`
- `validate_metadata_vector_manifest_item`
- `metadata_manifest_item_eligibility_reasons`
- `render_metadata_vector_manifest_validation_text`
- Permanent regression tests
- Manifest registration in `box_manifest.json`

## What this phase forbids

This phase explicitly forbids:

- Real embeddings
- Actual vector values
- Vector indexes
- Corpus generator implementation
- Provider implementation
- Runtime scorer behavior changes
- External ML libraries
- sentence-transformers
- torch
- FAISS
- Qdrant
- Chroma
- User query persistence
- Raw prompt text in manifest items
- Freeze entry text in manifest items
- Terminal log text in manifest items
- Chat history text in manifest items
- Prompt auto-loading
- Routing authority
- Self-learning loops
- Runtime rebuilds
- Startup rebuilds
- External API providers

## Manifest-level required fields

A valid Metadata Vector Manifest must include:

```yaml
schema_version: "3.2-metadata-vector-manifest"
manifest_id: "stable manifest id"
manifest_version: "human reviewed manifest version"
generated_at: "UTC timestamp"
generation_mode: "schema_only_no_embeddings_no_vectors | offline_human_governed_manifest"
authority: "advisory_schema_only"
source_layer: "generated_metadata_vector_manifest | offline_human_governed_manifest"
corpus_hash: "sha256:..."
items: []
```

Recommended manifest flags:

```yaml
contains_embeddings: false
contains_vectors: false
contains_raw_prompt_text: false
contains_user_queries: false
contains_freeze_entries: false
runtime_rebuild_allowed: false
startup_rebuild_allowed: false
external_api_allowed: false
```

## Item-level required fields

Each manifest item must include:

```yaml
id: "stable_candidate_id"
label: "Human-readable label"
route_family: "advisory route family hint"
isolation_domain: "routing_signal_scorer | prompt_library | freeze_workflow | startup | etc"
lifecycle_status: "proposed | validated | active | deprecated | superseded | archived | experimental"
source_path: "canonical source reference"
source_version: "freeze id or source version"
source_structural_hash: "sha256:..."
corpus_generation_run_id: "generation run id"
embedding_model_id: "schema_only_no_model | future pinned model id"
embedding_model_version: "schema-only | future pinned version"
embedding_dimensions: 0
corpus_hash: "sha256:..."
last_validated: "UTC timestamp"
allowed_use:
  - "advisory_routing_hint"
forbidden_use:
  - "final_route_decision"
  - "required_prompt_decision"
  - "may_proceed_now_decision"
  - "prompt_auto_loading"
  - "freeze_write"
semantic_summary: "Curated short text for future embedding."
canonical_terms:
  - "create patch"
keywords:
  - "patch"
negative_examples:
  - "explain concept"
min_score_threshold: 0.72
```

## Forbidden fields

A manifest or item must be invalid if it contains any field that encodes authority, raw source material, vectors, runtime provider objects, external APIs, or rebuild behavior.

Forbidden authority fields include:

```text
final_route
required_prompts
may_proceed_now
route_override
auto_load_prompts
write_freeze_memory
modify_startup
modify_prompt_library
self_update_corpus
router_override
```

Forbidden raw content fields include:

```text
raw_prompt_text
prompt_file_text
freeze_entry_text
freeze_memory_text
user_query_text
user_request_text
conversation_text
chat_history_text
terminal_log_text
raw_source_text
raw_file_text
```

Forbidden vector/runtime fields include:

```text
embedding
embeddings
vector
vectors
dense_vector
sparse_vector
vector_index_path
faiss_index_path
qdrant_collection
chroma_collection
provider_instance
model_object
external_api_key
network_endpoint
runtime_rebuild_enabled
startup_rebuild_enabled
auto_regenerate
```

## Lifecycle rule

Only `active` manifest items may be eligible for future semantic evidence.

Non-active items are not scored lower. They are excluded.

Lifecycle statuses are:

```text
proposed
validated
active
deprecated
superseded
archived
experimental
```

## Eligibility gate

A manifest item is eligible for future semantic evidence only if:

- item schema is valid
- `lifecycle_status == active`
- `allowed_use` includes `advisory_routing_hint`
- `forbidden_use` explicitly forbids `final_route_decision`
- `source_structural_hash` is present and SHA-256-prefixed
- `corpus_hash` is present and SHA-256-prefixed
- no forbidden raw text, vector, provider, runtime, or authority fields are present

A high vector or mock score cannot rescue an ineligible manifest item.

## No raw prompt embedding

The future embedding source is the curated `semantic_summary`, `canonical_terms`, `keywords`, and `negative_examples` inside the manifest item.

The future embedding source is not raw prompt text, freeze memory text, user query text, chat history, terminal logs, or project memory as a whole.

## No vector values in this phase

This schema phase must not store actual vectors.

Vector data belongs to a future disposable generated artifact after separate governance.

The manifest may record model identifiers, dimensions, and hashes, but it must not contain `embedding`, `vector`, `dense_vector`, `sparse_vector`, or vector index paths.

## No automatic rebuild

The manifest schema must preserve the no-auto-rebuild rule.

If a future manifest or vector artifact is missing, stale, corrupt, or mismatched, the future runtime must fall back to lexical scoring.

It must not rebuild the manifest or index at startup.

## External building block adoption boundary

This schema does not authorize any external library.

External building blocks such as sentence-transformers, all-MiniLM-L6-v2, FAISS, Qdrant, or Chroma require a future governed adapter boundary, license review, dependency review, Windows/PyCharm install review, fallback tests, no-authority tests, and freeze approval.

## Validation text rule

Validation output must use advisory language only. It must not use imperative routing language such as final route, required prompts, May proceed now, load prompts now, or Confirm and Write.

## Future next step

After this schema is frozen, the next safe phase is Offline Corpus Governance Design v1 or a schema-only validation corpus example. Real embeddings remain forbidden until the corpus lifecycle and evaluation set are frozen.
