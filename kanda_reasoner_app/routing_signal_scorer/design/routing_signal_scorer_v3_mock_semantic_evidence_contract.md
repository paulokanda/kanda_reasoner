# Routing Signal Scorer v3 Mock Semantic Evidence Contract v1

Feature ID: `routing_signal_scorer_v3_mock_semantic_evidence_contract_v1`

Status: mock contract only. No embeddings, no vector index, no corpus generator, no external dependency, and no routing authority.

## Purpose

This milestone creates a standard-library-only mock semantic evidence contract so future ML or embedding providers must fit a narrow advisory shape before any real semantic implementation exists.

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

## Scope

This patch may add:

- `kanda_reasoner_app/routing_signal_scorer/semantic_evidence_contract.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_mock_semantic_evidence_contract.md`
- routing_signal_scorer manifest registration
- permanent contract tests

This patch must not add:

- embeddings
- sentence-transformers
- torch
- transformers
- ONNX
- FAISS
- Qdrant
- Chroma
- vector index
- vector database
- corpus generator
- runtime prompt loading
- semantic UI display
- external API provider
- user-query persistence
- self-learning
- router override
- May proceed now decision
- required prompt decision

## Frozen foundation

This mock contract is downstream of:

- `routing_signal_scorer_v2_similarity_box_shield_v1`
- `routing_signal_scorer_v3_semantic_readiness_canon_registration_v1`
- `routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1`

It must preserve design-only v3 law while introducing a testable evidence shape.

## Disabled provider report

The default semantic provider is `disabled_null_provider`.

The disabled report must emit:

```text
schema_version = 3.1-mock
feature_id = routing_signal_scorer_v3_mock_semantic_evidence_contract_v1
authority = advisory_only
semantic_enabled = false
provider_id = disabled_null_provider
semantic_state = NO_SEMANTIC_PROVIDER
semantic_candidates = []
metadata_eligibility_gate_applied = true
ambiguity_gate_applied = true
advisory_only_guard_applied = true
lexical_fallback_required = true
canon_decides_final_route = true
does_not_override_router = true
automatic_prompt_loading = false
self_learning_enabled = false
external_dependencies = []
input_text_persisted = false
```

The raw user request text must not be stored in the report.

## Mock candidate contract

A mock semantic candidate may contain only approved evidence fields:

```text
candidate_id
candidate_label
route_family_hint
score
confidence_band
ambiguity_status
evidence_summary
source_context_id
source_context_version
source_structural_hash
corpus_hash
embedding_model_id
embedding_model_version
embedding_dimensions
lifecycle_status
isolation_domain
allowed_use
forbidden_use
source_hash_status
corpus_hash_status
stale_status
metadata_eligible
metadata_eligibility_reasons
candidate_promotion_allowed
advisory_only_reason
```

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
required_prompt_files
load_prompts_now
freeze_write
startup_mutation
prompt_library_mutation
```

If a mock candidate contains forbidden or unexpected fields, it must be rejected and lexical fallback must remain primary.

## Metadata eligibility gate

Metadata eligibility must run before ambiguity scoring and before any advisory candidate appears.

A candidate is eligible only when:

```text
lifecycle_status == active
allowed_use contains advisory_routing_hint
forbidden_use does not block advisory_routing_hint
source_hash_status == valid
corpus_hash_status == valid
stale_status is fresh/current/valid
```

A high vector or mock score cannot rescue an ineligible candidate.

Non-active, deprecated, superseded, stale, corrupted, or hash-mismatched candidates must be rejected before scoring.

## Ambiguity gate

If the top two eligible mock candidates have scores within the frozen mock ambiguity delta, the report must return:

```text
semantic_state = AMBIGUOUS_SEMANTIC_MATCH
lexical_fallback_required = true
candidate_promotion_allowed = false
```

Ambiguity increases caution and cannot increase authority.

Initial mock delta:

```text
ambiguity_delta = 0.05
```

Changing the future production ambiguity threshold requires a separate governed patch and freeze.

## Advisory-only guard

Every report must preserve:

```text
authority = advisory_only
canon_decides_final_route = true
does_not_override_router = true
automatic_prompt_loading = false
self_learning_enabled = false
external_dependencies = []
input_text_persisted = false
```

Semantic candidates must never be promoted into final route, required prompts, prompt loading, May proceed now, freeze writes, startup mutation, or prompt-library mutation.

## Dependency and side-effect policy

The mock contract must be standard-library-only.

It must not import:

```text
numpy
pandas
sklearn
scipy
torch
tensorflow
sentence_transformers
transformers
faiss
chromadb
qdrant_client
langchain
llama_index
```

It must not import neighboring boxes:

```text
kanda_prompt_workspace
project_freeze_ledger
project_freeze_after_update
kanda_reasoner_app.freeze_hint_intake
kanda_reasoner_app.freeze_after_update
kanda_reasoner_app.freeze_after_update_gui
```

It must not write files.

It must not scan project directories.

It must not read prompt-library, freeze, or startup files.

## Validation requirements

Permanent tests must prove:

- disabled provider report has the correct advisory shape
- raw input text is not persisted
- metadata eligibility filters non-active/stale/hash-invalid candidates
- high score cannot rescue ineligible candidates
- ambiguity is detected when top scores converge
- forbidden authority fields are rejected
- output is deterministic
- rendered text is non-imperative and advisory-only
- no ML/vector dependencies are imported
- no neighbor boxes are imported
- no provider/index/corpus-generator artifact exists
- manifest registers the mock contract without enabling runtime ML

## Future path

The next safe phases after this mock contract are:

1. Metadata Vector Manifest Schema v1
2. Offline Corpus Governance Design v1
3. Retrieval Evaluation Corpus v1
4. Offline Precomputed Semantic Evidence Prototype v1

Real embeddings remain forbidden until a later governed patch explicitly authorizes them.
