# Routing Signal Scorer v3 Semantic Readiness Canon

Version: 1.0
Status: active
Load type: on_request
Owner folder: 02_prompt_routing_and_indexing
Registered by: routing_signal_scorer_v3_semantic_readiness_canon_registration_v1

## Purpose

This canon is the on-request prompt-router guard for any KANDA Reasoner work involving machine learning, embeddings, semantic retrieval, vector indexes, vector databases, retrieval evaluation, semantic scorer work, Metadata Vector Manifest work, or `routing_signal_scorer` v3.

It must be requested before designing or implementing semantic retrieval, embedding providers, vector indexes, corpus generation, ML evaluation, or semantic evidence behavior.

This canon does not implement ML. It prevents premature ML implementation.

## Master rule

The semantic layer is an untrusted evidence witness.

It may provide evidence.

It may never provide authority.

```text
Semantic evidence may inform an advisory report.
The deterministic routing canon still decides final route.
The routing system canon still decides required context.
The human still confirms consequential actions.
The freeze system still records governed project memory.
```

## Required routing behavior

When the human asks for any of these, use Routed Work Path and request this canon:

```text
machine learning architecture
ML architecture
embeddings
semantic retrieval
semantic search
semantic scorer
semantic evidence layer
routing_signal_scorer v3
Metadata Vector Manifest
corpus generator
semantic corpus
vector index
vector database
FAISS
Qdrant
Chroma
sentence-transformers
all-MiniLM
retrieval evaluation
IR metrics
semantic candidate validation
semantic veto
model versioning
embedding drift
stale corpus
index poisoning
ML safety boundary
```

Minimum required companion context:

```text
1. kanda_routing_system_canon
2. kanda_box_shielding_canon
3. prompt_navigation_index
4. GROUP_ASSIMILATION_INDEX
5. active project freeze context, if frozen routing scorer behavior may be affected
6. routing_signal_scorer current design/freeze context, if implementation or design patch is requested
7. 05_patch_delivery_and_validation, if a patch ZIP or validation block is requested
```

May proceed now:

```text
PARTIAL for discussion or architecture planning.
NO for implementation until this canon, KBSC, current routing scorer shield context, patch boundary, validation plan, and freeze path are clear.
```

## Current frozen foundation

KANDA already has these required foundations:

```text
1. KANDA Box Shielding Canon registered and frozen.
2. KANDA Routing System Canon registered and frozen.
3. Freeze preview visibility repaired and frozen.
4. Routing Signal Scorer v2 Similarity Box Shield installed, validated, and frozen.
```

The current routing signal scorer is protected as:

```text
advisory-only
deterministic
standard-library-only
side-effect-free
bounded
candidate/display-only
non-authoritative
no router override
no May proceed now decision
no final prompt decision
no prompt auto-loading
no startup mutation
no freeze-memory mutation
no prompt-library mutation
no embeddings
no TF-IDF dependency
no vector store
no self-learning
no stronger ML
```

Any future semantic work must preserve these boundaries unless a separate governed patch explicitly changes the contract and is validated/frozen.

## Non-goals for the next phase

The next phase must not add:

```text
embeddings
sentence-transformers
ONNX
torch
FAISS
Qdrant
Chroma
vector database
vector index
corpus generator
provider implementation
runtime evidence aggregator
semantic scoring runtime logic
auto-rebuild at startup
self-learning
external API calls
telemetry that stores real user request text
GUI display of semantic candidates
dispatcher automation
prompt auto-loading
router override
May proceed now decision
final required prompt decision
```

The first semantic-readiness milestone should be design-only.

## Recommended next design feature

Preferred feature title:

```text
Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design
```

Preferred feature ID:

```text
routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1
```

Preferred design document path:

```text
kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md
```

## Design-only patch boundary

Allowed files for the design-only patch:

```text
CREATE:
- kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md
- tests/test_routing_signal_scorer_v3_structural_contract_semantic_readiness_design.py
- KANDA_FREEZE_HINT.json

UPDATE:
- kanda_reasoner_app/routing_signal_scorer/box_manifest.json
```

Forbidden files and boxes for that phase:

```text
- kanda_reasoner_app/routing_signal_scorer/contract.py
- kanda_reasoner_app/routing_signal_scorer/__init__.py
- runtime scorer logic
- provider implementation
- embedding implementation
- corpus generator implementation
- vector index implementation
- kanda_prompt_workspace/
- kanda_reasoner_app/freeze_hint_intake/
- kanda_reasoner_app/freeze_after_update/
- kanda_reasoner_app/freeze_after_update_gui/
- project_freeze_ledger/
- project_freeze_after_update/frozen_features_memory/
- startup delivery files
- prompt-library indexes
- GUI dispatcher code
```

If `contract.py` or `__init__.py` later needs an exported constant or typed structure, that must be a separate explicitly scoped patch with its own validation and freeze entry.

## Future architecture model

Use three strictly separated layers:

```text
Layer 1 — Canonical source layer
- prompt library
- routing canon
- KBSC
- freeze memory
- box manifests
- routing indexes

Layer 2 — Generated semantic corpus layer
- Metadata Vector Manifest
- generated corpus package
- generated corpus hash
- generated source structural hashes
- lifecycle state records

Layer 3 — Runtime scoring evidence layer
- lexical scorer
- future semantic provider, disabled by default
- metadata eligibility gate
- ambiguity gate
- advisory-only guard
- evidence report
```

Runtime scorer must not read canonical prompt-library or freeze-entry files directly for semantic retrieval.

Runtime scorer may only consume a generated, validated, human-reviewed Metadata Vector Manifest or generated corpus package.

## Metadata Vector Manifest

Future embeddings must not be generated from raw prompt files.

Future embeddings must not be generated from freeze entries.

Future embeddings must not be generated from past user requests.

Future embeddings should be generated only from a curated Metadata Vector Manifest.

Each manifest item should represent one routing context, prompt family, routing category, or recognized task type.

Every item should include at least:

```yaml
id: stable_candidate_id
label: Human-readable candidate label
route_family: governed_patch | freeze_workflow | prompt_registration | shield_work | etc
isolation_domain: routing_signal_scorer | prompt_library | freeze_workflow | startup | etc
lifecycle_status: active | deprecated | superseded | archived | experimental
source_path: canonical source path or manifest source reference
source_version: freeze ID, version ID, or manifest version
source_structural_hash: sha256 of source content at generation time
corpus_generation_run_id: stable generation run ID
embedding_model_id: model/provider ID used to generate future embedding
embedding_model_version: explicit version
embedding_dimensions: explicit dimension count
corpus_hash: sha256 of whole generated corpus
last_validated: UTC timestamp
valid_until: optional warning date, not sole invalidation source
allowed_use:
  - advisory_routing_hint
forbidden_use:
  - final_route_decision
  - required_prompt_decision
  - may_proceed_now_decision
  - prompt_auto_loading
  - freeze_write
summary: short curated embedding text
canonical_terms:
  - create patch
keywords:
  - patch
negative_examples:
  - explain a concept
min_score_threshold: item-specific score floor
```

## Corpus lifecycle state machine

Define a strict lifecycle:

```text
proposed -> validated -> active -> deprecated -> superseded -> archived
```

Rules:

```text
Only active items may be surfaced by the runtime scorer.
Deprecated, superseded, archived, experimental, or invalid items must be filtered out before semantic scoring.
Non-active items must not be scored lower; they must be excluded.
Lifecycle transitions require human-governed review.
Corpus changes require validation before use.
Corpus regeneration must be explicit, not automatic.
```

## Metadata eligibility gate

Metadata filtering must happen before semantic scoring or candidate promotion.

Future flow:

```text
candidate pool -> metadata eligibility gate -> semantic scoring -> ambiguity gate -> advisory-only guard
```

Candidate is eligible only if:

```text
lifecycle_status == active
allowed_use contains advisory_routing_hint
forbidden_use does not contain current use
source_structural_hash is valid
corpus_hash is valid
embedding_model_id matches index manifest
embedding_dimensions match provider/index manifest
isolation_domain is allowed for the request context
source is not stale
source is not deprecated
source is not superseded
```

A high vector score cannot rescue an ineligible candidate.

## Generated vector index policy

The vector index is disposable generated evidence.

It is not canonical memory.

It is not freeze memory.

It is not source of truth.

It must not be stored in `project_freeze_ledger`.

It must not be stored in `project_freeze_after_update/frozen_features_memory`.

It must not be manually edited.

It must not be consulted to override the routing canon.

Missing, stale, corrupt, or model-mismatched index must fall back to lexical scoring.

No crash.

No automatic rebuild.

No startup rebuild.

No hidden background generation in the design phase.

## Provider boundary

Future providers must be disabled by default.

Default provider:

```text
disabled_null_provider
```

Future provider categories:

```text
disabled_null_provider — default, no dependencies, no IO, no embeddings
offline_precomputed_provider — safest future path, reads precomputed vectors from generated artifacts
local_embedding_provider — possible later, explicit opt-in, dependency-reviewed, version-pinned, optional
external_api_provider — forbidden in v3; requires separate governance and audit
```

Provider must never return authority fields.

Forbidden provider output fields:

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
```

If a provider returns unexpected fields, the future runtime must reject the response and fall back to lexical scoring.

## Semantic evidence output shape

Approved future semantic candidate shape:

```yaml
semantic_candidates:
  - candidate_id: stable_id
    candidate_label: Human-readable advisory label
    route_family_hint: advisory route family
    score: 0.82
    confidence_band: WEAK | STRONG_ADVISORY | HIGH_SIGNAL_ADVISORY
    ambiguity_status: false
    evidence_summary: Short explanation
    source_context_id: manifest item id
    source_context_version: manifest/corpus version
    source_structural_hash: sha256
    corpus_hash: sha256
    embedding_model_id: model/provider id
    advisory_only_reason: Semantic evidence is not routing authority.
```

Approved state names:

```text
NO_SEMANTIC_PROVIDER
NO_MATCH
WEAK_SEMANTIC_MATCH
STRONG_SEMANTIC_ADVISORY
HIGH_SIGNAL_ADVISORY
AMBIGUOUS_SEMANTIC_MATCH
STALE_CORPUS_FALLBACK
INDEX_MISSING_FALLBACK
INDEX_CORRUPT_FALLBACK
PROVIDER_UNAVAILABLE_FALLBACK
ERROR_STATE_FALLBACK
```

## Ambiguity policy

If top candidates are too close, output must mark ambiguity and suppress candidate promotion.

Initial design placeholder:

```text
ambiguity_delta = 0.05
```

This value must be frozen before implementation.

Ambiguity threshold must not be runtime-adjustable.

Changing ambiguity thresholds requires a governed patch and freeze.

## Determinism-anchor discrepancy protocol

Disagreement cannot increase authority.

Disagreement can only increase caution.

Cases:

```text
Lexical low + semantic high for same family:
- allow advisory semantic candidate if metadata eligible
- mark discrepancy

Lexical high + semantic low:
- preserve lexical evidence
- mark semantic weak or unavailable

Lexical and semantic high but different families:
- mark disagreement
- trigger ambiguity/discrepancy warning
- no candidate promotion

Semantic high but canon rejects route:
- canon wins
- semantic disagreement remains advisory evidence only
```

## Human-in-the-loop validation gates

Future semantic candidate validation stages:

```text
1. Offline evaluation only
2. Hidden logging pilot with curated non-sensitive cases
3. Human review of disagreement cases
4. Advisory UI display only
5. Threshold calibration under governed freeze
```

No semantic candidate should become routing authority.

No semantic candidate should automatically update the corpus.

No semantic candidate should automatically change thresholds.

## Semantic veto as future governed correction

Allowed future concept:

```text
Human marks candidate as false positive.
The false positive is added to a review queue.
A future governed corpus update adds a negative example or suppression rule.
Validation runs.
Freeze occurs.
Only then behavior changes.
```

Forbidden concept:

```text
Human clicks veto.
Runtime silently updates corpus, index, model, thresholds, or weights.
```

## Privacy and no-query-persistence policy

The semantic scorer must not persist real user request text by default.

Forbidden:

```text
storing user queries for training
storing user queries in vector indexes
embedding user queries into persistent memory
uploading user queries to external APIs
silently logging full request text
```

Allowed future logging only if governed:

```text
non-sensitive curated evaluation cases
hashed request identifiers
aggregate metrics
explicitly opt-in debug logs
```

## External building block adoption policy

KANDA should not reinvent the wheel, but external code is a supply-chain risk.

Future candidates to study:

```text
sentence-transformers
all-MiniLM-L6-v2
FAISS
Qdrant
Chroma
```

This canon does not adopt them.

Adoption gate before any external dependency:

```text
1. license review
2. dependency review
3. Windows/PyCharm install review
4. disk/RAM/CPU footprint review
5. offline/local-first compatibility review
6. fallback behavior tests
7. no-authority-escalation tests
8. optional dependency boundary
9. disabled-by-default configuration
10. freeze approval
```

No external ML or vector dependency may become core runtime behavior without an explicit governed adapter boundary and freeze approval.

## Recommended future implementation order

Do not implement embeddings first.

Recommended order:

```text
Phase A — Design-only semantic readiness architecture
Phase B — Mock semantic provider and schema validation
Phase C — Metadata Vector Manifest generator design
Phase D — Offline evaluation corpus
Phase E — Offline precomputed embeddings
Phase F — Optional local embedding provider
Phase G — Optional vector index adapter
Phase H — Advisory UI display
Phase I — Calibration phase
```

## Retrieval evaluation plan

Before implementation, define a frozen evaluation corpus.

Evaluation categories:

```text
positive routing cases
near-miss cases
ambiguous cases
adversarial instruction cases
stale context cases
out-of-domain cases
freeze/shield boundary cases
Fast Path false-positive cases
```

Metrics:

```text
Precision@1
Precision@3
Recall@1
Recall@3
MRR
NDCG@10
false positive rate
stale candidate suppression rate
deprecated candidate suppression rate
ambiguity detection rate
authority leakage rate
latency p95
```

Design targets:

```text
0% authority leakage
0 deprecated candidates surfaced
0 superseded candidates surfaced
100% fallback on stale/corrupt/missing index
p95 semantic overhead target defined before implementation
```

## Latency, CPU, RAM, and local-first budget

This is a Windows/PyCharm local-first app.

Design constraints:

```text
default semantic provider disabled
no model load at startup
no startup index rebuild
no blocking UI thread
no required torch install
no required vector DB install
p95 advisory lookup overhead target defined before runtime implementation
memory footprint ceiling defined before runtime implementation
```

Initial conservative target:

```text
semantic disabled overhead: near zero
fallback path: existing lexical scorer speed preserved
future semantic lookup p95 target: under 100 ms if using precomputed vectors
```

If future local model loading exceeds this, it must remain optional and disabled by default.

## Threat model

Threats:

```text
authority creep
stale corpus contamination
deprecated prompt retrieval
superseded context retrieval
embedding drift
model version mismatch
index poisoning
manual index tampering
partial index generation
external dependency lock-in
external API data exposure
user-query persistence
ambiguity fatigue
high-score de facto authority
cross-box invasion
```

Required responses:

```text
Authority creep:
- advisory-only guard
- forbidden output fields
- canon decides final route

Stale corpus:
- source_structural_hash
- lifecycle_status
- corpus_hash
- explicit regeneration

Embedding drift:
- embedding_model_id
- embedding_model_version
- embedding_dimensions
- model/corpus hash mismatch fallback

Index poisoning:
- manifest hash check
- generated artifact policy
- fallback to lexical
- no automatic repair

Cross-box invasion:
- runtime consumes only generated manifest
- corpus generation is separate future governed box
```

## Fitness-function test matrix

Future tests must enforce the architecture law.

Tests should verify:

```text
advisory-only semantic evidence
lexical fallback
disabled-by-default provider
metadata eligibility gate
corpus lifecycle state machine
source_structural_hash
isolation_domain
corpus_hash
embedding_model_id
embedding_model_version
vector index disposable generated cache
no automatic rebuild at startup
no external API provider in v3
no user-query persistence
no authority output fields
retrieval evaluation metrics
latency/resource budget
external building block adoption policy
threat model
```

Tests should also verify no forbidden files are added in design-only phase.

## Explicit forbidden behavior

The design and future implementations must explicitly forbid:

```text
semantic output deciding final route
semantic output deciding required prompts
semantic output deciding May proceed now
semantic output auto-loading prompts
semantic output writing freeze memory
semantic output modifying startup
semantic output modifying prompt-library
semantic output modifying routing indexes
semantic output modifying corpus at runtime
semantic output modifying vector index at runtime
external API embeddings in v3
raw prompt files embedded directly
freeze entries embedded directly
user queries persisted for training
vector index used as canonical memory
automatic index rebuild at startup
automatic corpus update
self-learning loops
dependency installation in design phase
```

## Required design-only validation

The design-only patch must prove:

```text
1. Design document exists.
2. Manifest registers the design artifact.
3. No runtime behavior changed.
4. No ML dependency was added.
5. No provider implementation was added.
6. No vector index was added.
7. No corpus generator was added.
8. No prompt workspace files were touched in the design patch.
9. No freeze boxes were touched in the design patch.
10. No project_freeze_ledger files were touched.
11. Design document contains required architecture sections.
12. Design document contains explicit forbidden behavior.
13. Design document contains future evaluation metrics.
14. Design document contains future adoption gates for external libraries.
15. KANDA_FREEZE_HINT.json documents design-only scope.
```

## Final canon

```text
The semantic layer is an untrusted evidence witness.

It may compare a user request to a prevalidated, active, metadata-filtered manifest item.

It may never read canonical sources directly at runtime.

It may never retrieve deprecated or stale candidates.

It may never output authority fields.

It may never bypass lexical fallback.

It may never override the routing canon.

It may never mutate the corpus, vector index, startup, prompt library, freeze memory, or neighboring boxes.

Everything semantic remains advisory until a human-governed freeze explicitly says otherwise.
```
