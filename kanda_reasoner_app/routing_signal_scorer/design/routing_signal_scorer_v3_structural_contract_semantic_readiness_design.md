# Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design

Feature title: `Routing Signal Scorer v3 Structural Contract and Semantic Readiness Design v1`

Feature ID: `routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1`

Owning bounded context: `kanda_reasoner_app/routing_signal_scorer`

Status: design-only architecture contract. No runtime behavior change.

---

## 1. Purpose

This design freezes the structural contract for future semantic retrieval, embeddings, vector indexes, and machine-learning evidence inside `routing_signal_scorer`.

It is not an embedding implementation. It is not a vector index implementation. It is not a provider implementation. It is not a corpus generator implementation. It is not dispatcher automation.

The semantic layer is an untrusted evidence witness.

It may provide evidence. It may never provide authority.

This design exists so future machine-learning work cannot accidentally become the routing canon, mutate neighboring boxes, auto-load prompts, or hide authority inside a high semantic score.

---

## 2. Frozen v2 shield preservation

The previous `routing_signal_scorer_v2_similarity_box_shield_v1` remains the active shield for the current runtime-lite similarity chain.

This v3 design preserves all v2 shield laws:

- advisory-only
- deterministic fallback
- standard-library-only current runtime-lite path
- side-effect-free scoring
- bounded execution
- no authority escalation
- no cross-box mutation
- no router override
- no `May proceed now` decision
- no final required prompt decision
- no prompt auto-loading
- no startup mutation
- no freeze-memory mutation
- no prompt-library mutation
- no embeddings in current runtime
- no TF-IDF dependency in current runtime
- no vector store in current runtime
- no self-learning
- no stronger ML implementation in this phase

Any future ML work must pass through KBSC and a new governed patch/freeze cycle.

---

## 3. Core semantic rule

The semantic layer is an untrusted evidence witness.

It may compare a user request to a prevalidated, active, metadata-filtered manifest item.

It may never read canonical sources directly at runtime.

It may never retrieve deprecated or stale candidates.

It may never output authority fields.

It may never bypass lexical fallback.

It may never override the routing canon.

It may never mutate corpus, vector index, startup, prompt library, freeze memory, router state, or neighboring boxes.

Everything semantic remains advisory unless a human-governed freeze explicitly says otherwise.

---

## 4. Non-goals for this phase

This phase does not add:

- embeddings
- sentence-transformers
- ONNX
- torch
- TensorFlow
- FAISS
- Qdrant
- Chroma
- vector database
- vector index
- corpus generator
- provider implementation
- runtime evidence aggregator
- semantic scoring runtime logic
- semantic UI display
- startup rebuild behavior
- self-learning
- external API calls
- telemetry that stores real user request text
- prompt auto-loading
- router override
- `May proceed now` decisions
- final required prompt decisions

This phase changes documentation and manifest registration only.

---

## 5. Three-layer architecture

Future semantic retrieval must use three strictly separated layers.

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
- corpus hash
- source structural hashes
- lifecycle state records
- optional generated vector cache

Layer 3 — Runtime scoring evidence layer
- lexical scorer
- future semantic provider, disabled by default
- metadata eligibility gate
- ambiguity gate
- advisory-only guard
- evidence report
```

Layer 3 must not read Layer 1 directly for semantic retrieval. It may consume only a generated, reviewed, versioned Layer 2 manifest/corpus artifact.

Canonical sources produce corpus offline. Corpus produces disposable vector evidence. Runtime scorer consumes only generated evidence. Canon still decides final routing.

---

## 6. Data-flow law

Allowed future flow:

```text
Canonical sources
    -> offline human-governed corpus generation
    -> Metadata Vector Manifest
    -> optional generated vector/cache artifact
    -> runtime evidence layer
    -> advisory report only
    -> canon decides final route
```

Forbidden future flow:

```text
User request
    -> runtime embedding model reads prompt library or freeze entries directly
    -> vector candidate becomes route or required prompt
```

---

## 7. Metadata Vector Manifest

Future embeddings must not be generated from raw prompt files.

Raw prompt files contain operational instructions, governance text, examples, warnings, and historical context. That content creates semantic noise and increases the chance that a high vector score surfaces the wrong routing context.

Future embeddings should be generated only from a curated `Metadata Vector Manifest`.

The manifest is a generated, reviewed, versioned artifact that abstracts canonical sources into safe routing-evidence items.

A manifest item should represent exactly one well-defined routing context, prompt family, routing category, or recognized task type.

It should not represent:

- raw prompt file content
- full freeze entries
- user request logs
- historical chat turns
- private user text
- generated terminal logs
- project memory as a whole

Freeze entries are law/history. They may be referenced for governance but should not be embedded as routing candidates.

---

## 8. Future corpus item schema

A future manifest/corpus item should include at least:

```yaml
id: "stable_candidate_id"
label: "Human-readable candidate label"
route_family: "governed_patch | freeze_workflow | prompt_registration | shield_work | etc"
isolation_domain: "routing_signal_scorer | prompt_library | freeze_workflow | startup | etc"
lifecycle_status: "active | deprecated | superseded | archived | experimental"
source_path: "canonical source path or manifest source reference"
source_version: "freeze ID, version ID, or manifest version"
source_structural_hash: "sha256 of source content at generation time"
corpus_generation_run_id: "stable generation run ID"
embedding_model_id: "model/provider ID used to generate future embedding"
embedding_model_version: "explicit version"
embedding_dimensions: 384
corpus_hash: "sha256 of whole generated corpus"
last_validated: "UTC timestamp"
valid_until: "optional warning date, not sole invalidation source"
allowed_use:
  - "advisory_routing_hint"
forbidden_use:
  - "final_route_decision"
  - "required_prompt_decision"
  - "may_proceed_now_decision"
  - "prompt_auto_loading"
  - "freeze_write"
summary: "Short curated embedding text"
canonical_terms:
  - "create patch"
  - "install block"
keywords:
  - "patch"
  - "zip"
negative_examples:
  - "explain a concept"
min_score_threshold: 0.72
```

`valid_until` may warn about aging, but TTL alone must not be the primary invalidation mechanism. The decisive invalidation mechanisms are hash mismatch, corpus version mismatch, embedding model mismatch, lifecycle status, generation run mismatch, and human-governed invalidation.

---

## 9. Corpus lifecycle state machine

The corpus lifecycle is explicit:

```text
proposed -> validated -> active -> deprecated -> superseded -> archived
```

Rules:

- Only `active` items may be surfaced by runtime semantic evidence.
- Deprecated, superseded, archived, experimental, or invalid items must be excluded before scoring.
- Non-active items must not be scored lower; they must be filtered out.
- Lifecycle transitions require human-governed review.
- Corpus regeneration must be explicit and validated before use.
- Corpus generation is a future separate governance box or explicitly governed tool, not current runtime scorer behavior.

---

## 10. Metadata eligibility gate

Metadata filtering must happen before semantic scoring or candidate promotion.

Future flow:

```text
candidate pool
    -> metadata eligibility gate
    -> semantic scoring
    -> ambiguity gate
    -> advisory-only guard
```

A candidate is eligible only if:

- `lifecycle_status == active`
- `allowed_use` contains `advisory_routing_hint`
- `forbidden_use` does not contain the current intended use
- `source_structural_hash` is valid
- `corpus_hash` is valid
- `embedding_model_id` matches the index manifest
- `embedding_dimensions` match the provider/index manifest
- `isolation_domain` is allowed for the request context
- source is not stale
- source is not deprecated
- source is not superseded

A high vector score cannot rescue an ineligible candidate.

---

## 11. Generated vector index policy

The vector index is disposable generated evidence.

It is not canonical memory. It is not freeze memory. It is not source of truth. It must not be stored in `project_freeze_ledger`. It must not be stored in `project_freeze_after_update/frozen_features_memory`. It must not be manually edited. It must not be consulted to override the routing canon.

Normal fallback states:

- missing index
- stale index
- corrupt index
- embedding model mismatch
- corpus hash mismatch
- source structural hash mismatch

All of these must fall back to lexical scoring in a future implementation.

No crash. No automatic rebuild. No startup rebuild. No hidden background generation in this phase.

---

## 12. No automatic rebuild at startup

The design explicitly forbids automatic index regeneration at startup.

If a future index is missing, stale, corrupted, mismatched, or poisoned:

- mark semantic provider unavailable
- fall back to lexical scorer
- emit advisory warning
- require explicit human-governed rebuild in a future phase

Automatic rebuild creates hidden side effects. Hidden side effects violate the shield boundary. Generated vector artifacts must not become silent project memory.

---

## 13. Provider boundary

Future providers must be disabled by default.

Default provider:

```text
disabled_null_provider
```

Provider classes are future concepts only:

```text
1. disabled_null_provider
   - default
   - no dependencies
   - no IO
   - no embeddings

2. offline_precomputed_provider
   - safest future implementation path
   - reads precomputed vectors from generated artifacts
   - no runtime model loading

3. local_embedding_provider
   - possible later
   - explicitly enabled only
   - dependency-reviewed
   - version-pinned
   - optional

4. external_api_provider
   - forbidden in v3
   - requires separate governance and audit
```

The provider interface must be constrained at both ends. A future provider may return only an approved candidate shape. Unexpected fields should cause rejection and lexical fallback.

Forbidden provider output fields:

- `final_route`
- `required_prompts`
- `may_proceed_now`
- `route_override`
- `auto_load_prompts`
- `write_freeze_memory`
- `modify_startup`
- `modify_prompt_library`
- `self_update_corpus`

---

## 14. Future semantic evidence output shape

Approved future shape:

```yaml
semantic_candidates:
  - candidate_id: "stable_id"
    candidate_label: "Human-readable advisory label"
    route_family_hint: "advisory route family"
    score: 0.82
    confidence_band: "WEAK | STRONG_ADVISORY | HIGH_SIGNAL_ADVISORY"
    ambiguity_status: false
    evidence_summary: "Short explanation"
    source_context_id: "manifest item id"
    source_context_version: "manifest/corpus version"
    source_structural_hash: "sha256"
    corpus_hash: "sha256"
    embedding_model_id: "model/provider id"
    advisory_only_reason: "Semantic evidence is not routing authority."
```

Approved future state names:

- `NO_SEMANTIC_PROVIDER`
- `NO_MATCH`
- `WEAK_SEMANTIC_MATCH`
- `STRONG_SEMANTIC_ADVISORY`
- `HIGH_SIGNAL_ADVISORY`
- `AMBIGUOUS_SEMANTIC_MATCH`
- `STALE_CORPUS_FALLBACK`
- `INDEX_MISSING_FALLBACK`
- `INDEX_CORRUPT_FALLBACK`
- `PROVIDER_UNAVAILABLE_FALLBACK`
- `ERROR_STATE_FALLBACK`

---

## 15. Ambiguity policy

Ambiguity must be explicit and durable.

Design rule:

```text
If top score and second score differ by <= frozen ambiguity_delta, mark AMBIGUOUS_SEMANTIC_MATCH.
```

Suggested future placeholder:

```text
ambiguity_delta = 0.05
```

This is a design placeholder, not implementation behavior.

If ambiguity occurs:

- do not promote any candidate
- do not auto-load prompts
- do not decide route
- do not decide `May proceed now`
- output ambiguity status
- preserve human/canon decision boundary

Ambiguity threshold must not be runtime-adjustable. Changing ambiguity thresholds requires a governed patch and freeze.

---

## 16. Determinism-anchor discrepancy protocol

Semantic output may disagree with lexical evidence. Disagreement must be visible.

Cases:

```text
Lexical low + semantic high for same family:
- allow advisory semantic candidate only if metadata eligible
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
- semantic disagreement logged only as advisory evidence
```

Core rule:

```text
Disagreement cannot increase authority.
Disagreement can only increase caution.
```

---

## 17. Human-in-the-loop validation gates

Semantic candidates must go through human-governed validation before display or operational use.

Stages:

1. Offline evaluation only
2. Hidden pilot on curated non-sensitive cases
3. Human review of disagreement cases
4. Advisory UI display only
5. Threshold calibration under governed freeze

No semantic candidate should become routing authority. No semantic candidate should automatically update corpus, index, model, or thresholds.

---

## 18. Semantic veto as governed corpus correction

A human semantic veto is useful only as a governed correction process.

Allowed future concept:

```text
Human marks candidate as false positive
    -> false positive enters review queue
    -> future governed corpus update adds negative example or suppression rule
    -> validation runs
    -> freeze occurs
    -> behavior changes only after freeze
```

Forbidden concept:

```text
Human clicks veto
    -> runtime silently updates corpus, index, model, thresholds, or weights
```

---

## 19. Privacy and no-query-persistence policy

The semantic scorer must not persist real user request text by default.

Forbidden:

- storing user queries for training
- storing user queries in vector indexes
- embedding user queries into persistent memory
- uploading user queries to external APIs
- silently logging full request text

Allowed only under future governed opt-in:

- non-sensitive curated evaluation cases
- aggregate metrics
- hashed request identifiers
- explicit debug logs with human awareness

---

## 20. External building block adoption policy

KANDA should not reinvent the wheel, but external code is a supply-chain risk.

Future candidates to study:

- `sentence-transformers`
- `all-MiniLM-L6-v2`
- `FAISS`
- `Qdrant`
- `Chroma`

This phase does not adopt them.

Adoption gate before any external dependency:

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

Rule:

```text
No external ML or vector dependency may become core runtime behavior without explicit governed adapter boundary and freeze approval.
```

External API providers are forbidden in v3.

---

## 21. Retrieval evaluation plan

Before implementation, define and freeze an evaluation corpus.

Categories:

1. positive routing cases
2. near-miss cases
3. ambiguous cases
4. adversarial instruction cases
5. stale context cases
6. out-of-domain cases
7. freeze/shield boundary cases
8. Fast Path false-positive cases

Metrics:

- Precision@1
- Precision@3
- Recall@1
- Recall@3
- MRR
- NDCG@10
- false positive rate
- stale candidate suppression rate
- deprecated candidate suppression rate
- ambiguity detection rate
- authority leakage rate
- latency p95

Design targets:

- 0% authority leakage
- 0 deprecated candidates surfaced
- 0 superseded candidates surfaced
- 100% fallback on stale/corrupt/missing index
- p95 semantic overhead target defined before implementation

Evaluation corpus must be separate from runtime corpus. Acceptance thresholds must be defined before evaluation, not after seeing results.

---

## 22. Latency, CPU, RAM, and local-first budget

This is a Windows/PyCharm local-first project.

Design constraints:

- semantic provider disabled by default
- no model load at startup
- no startup index rebuild
- no blocking GUI/UI thread
- no required torch install
- no required vector DB install
- p95 advisory lookup target defined before runtime implementation
- memory footprint ceiling defined before runtime implementation

Initial conservative target:

- semantic disabled overhead: near zero
- fallback path: existing lexical scorer speed preserved
- future precomputed-vector lookup target: under 100 ms p95

If future local model loading exceeds local-first budget, it must remain optional and disabled by default.

---

## 23. Threat model

Threats:

1. authority creep
2. stale corpus contamination
3. deprecated prompt retrieval
4. superseded context retrieval
5. embedding drift
6. model version mismatch
7. index poisoning
8. manual index tampering
9. partial index generation
10. external dependency lock-in
11. external API data exposure
12. user-query persistence
13. ambiguity fatigue
14. high-score de facto authority
15. cross-box invasion

Design responses:

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
- corpus generation is a separate future governed box/tool
```

---

## 24. Recommended future implementation order

Do not implement embeddings first.

Recommended sequence:

```text
Phase A — Design-only semantic readiness architecture
Phase B — Mock semantic provider and schema validation
Phase C — Metadata Vector Manifest generator design
Phase D — Offline evaluation corpus
Phase E — Offline precomputed semantic evidence
Phase F — Optional local embedding provider
Phase G — Optional vector index adapter
Phase H — Advisory UI display
Phase I — Calibration phase
```

The next implementation after this design should likely be:

```text
Routing Signal Scorer v3 Mock Semantic Evidence Contract v1
```

not real embeddings.

---

## 25. Fitness-function test matrix

Future tests must enforce architecture law.

Required future test themes:

- semantic disabled by default
- lexical fallback works when provider missing/error/empty
- forbidden output fields absent
- non-active corpus items excluded
- stale index fallback
- ambiguity detection fires
- adversarial instructions ignored
- cross-box mutation absent
- latency bounded
- authority escalation absent
- metadata eligibility before scoring
- no user-query persistence
- external API provider forbidden until separate governance
- vector index disposable generated cache

Design-only validation must verify this document contains these laws and that no runtime ML behavior was added in this phase.

---

## 26. Explicit forbidden behavior

The design forbids:

- semantic output deciding final route
- semantic output deciding required prompts
- semantic output deciding `May proceed now`
- semantic output auto-loading prompts
- semantic output writing freeze memory
- semantic output modifying startup
- semantic output modifying prompt library
- semantic output modifying routing indexes
- semantic output modifying corpus at runtime
- semantic output modifying vector index at runtime
- external API embeddings in v3
- raw prompt files embedded directly
- freeze entries embedded directly
- user queries persisted for training
- vector index used as canonical memory
- automatic index rebuild at startup
- automatic corpus update
- self-learning loops
- dependency installation in design phase

---

## 27. Future implementation gate

No future ML implementation may begin until this design is:

- installed
- validated
- frozen

Every future ML step requires a separate feature ID, patch boundary, tests, validation evidence, and freeze entry.

This design does not authorize implementation. It defines the law implementation must obey.

---

## 28. Final canon for this phase

The semantic layer is an untrusted evidence witness.

It may compare a user request to a prevalidated, active, metadata-filtered manifest item.

It may never read canonical sources directly at runtime.

It may never retrieve deprecated or stale candidates.

It may never output authority fields.

It may never bypass lexical fallback.

It may never override the routing canon.

It may never mutate the corpus, vector index, startup, prompt library, freeze memory, or neighboring boxes.

Everything semantic remains advisory until a human-governed freeze explicitly says otherwise.
