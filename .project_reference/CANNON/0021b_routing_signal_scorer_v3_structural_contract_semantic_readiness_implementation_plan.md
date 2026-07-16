# Routing Signal Scorer v3 — Structural Contract and Semantic Readiness Implementation Plan

Feature title:

```text
Routing Signal Scorer v3 — Structural Contract and Semantic Readiness Design
```

Feature ID:

```text
routing_signal_scorer_v3_structural_contract_semantic_readiness_design_v1
```

Recommended document filename:

```text
routing_signal_scorer_v3_structural_contract_semantic_readiness_implementation_plan.md
```

---

# 1. Purpose

This document defines the implementation plan for the next KANDA Reasoner phase before any real machine-learning, embedding, vector-index, or semantic-retrieval implementation is added.

This phase exists to prevent premature ML integration.

The purpose is to freeze the architecture, safety boundaries, data contracts, evaluation plan, and future implementation gates for a semantic evidence layer inside `routing_signal_scorer`.

This is not an embedding implementation.

This is not a vector-store implementation.

This is not a corpus generator implementation.

This is not a provider implementation.

This is not a routing automation patch.

This phase creates the contract that future semantic or embedding implementations must obey.

---

# 2. Current frozen foundation

The project already has the required governance foundation:

```text
1. KANDA Box Shielding Canon registered and frozen.
2. KANDA Routing System Canon registered and frozen.
3. Freeze preview visibility repaired and frozen.
4. Routing Signal Scorer v2 Similarity Box Shield installed, validated, and frozen.
```

The current routing signal scorer is protected as:

```text
- advisory-only
- deterministic
- standard-library-only
- side-effect-free
- bounded
- candidate/display-only
- non-authoritative
- no router override
- no May proceed now decision
- no final prompt decision
- no prompt auto-loading
- no startup mutation
- no freeze-memory mutation
- no prompt-library mutation
- no embeddings
- no TF-IDF dependency
- no vector store
- no self-learning
- no stronger ML
```

This v3 design must preserve all of that.

---

# 3. Master rule

The semantic layer must behave like an untrusted evidence witness.

It may provide evidence.

It may never provide authority.

```text
Semantic evidence may inform a human or a future advisory report.
The deterministic routing canon still decides final route.
The routing system canon still decides required context.
The human still confirms consequential actions.
The freeze system still records governed project memory.
```

---

# 4. Non-goals

This phase must not implement or add:

```text
- embeddings
- sentence-transformers
- ONNX
- torch
- FAISS
- Qdrant
- Chroma
- vector database
- vector index
- corpus generator
- provider implementation
- runtime evidence aggregator
- semantic scoring runtime logic
- auto-rebuild at startup
- self-learning
- external API calls
- telemetry that stores real user request text
- GUI display of semantic candidates
- dispatcher automation
- prompt auto-loading
- router override
- May proceed now decision
- final required prompt decision
```

This phase must not change runtime behavior.

---

# 5. Recommended patch boundary

Allowed files for the design-only patch:

```text
CREATE:
- kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_structural_contract_semantic_readiness_design.md
- tests/test_routing_signal_scorer_v3_structural_contract_semantic_readiness_design.py
- KANDA_FREEZE_HINT.json

UPDATE:
- kanda_reasoner_app/routing_signal_scorer/box_manifest.json
```

Forbidden files and boxes:

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

If `contract.py` or `__init__.py` later needs an exported constant or typed structure, that must be a separate explicitly scoped patch with its own freeze entry.

---

# 6. Proposed architecture

The future architecture should have three strictly separated layers.

```text
Layer 1 — Canonical source layer
- prompt library
- routing canon
- KBSC
- freeze memory
- box manifests
- routing indexes

Layer 2 — Generated semantic corpus layer
- metadata vector manifest
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

Important boundary:

```text
Runtime scorer must not read canonical prompt-library or freeze-entry files directly for semantic retrieval.

Runtime scorer may only consume a generated, validated, human-reviewed metadata vector manifest or generated corpus package.
```

---

# 7. Data flow

Future safe data flow:

```text
Canonical sources
    |
    v
Offline human-governed corpus generation
    |
    v
Metadata Vector Manifest
    |
    v
Generated vector/cache artifacts, optional and disposable
    |
    v
Runtime evidence layer
    |
    v
Advisory report only
    |
    v
Canon decides final route
```

Forbidden data flow:

```text
User request
    |
    v
Embedding model directly reads prompt library or freeze entries at runtime
    |
    v
Vector candidate becomes final routing decision
```

---

# 8. Metadata Vector Manifest

Future embeddings must not be generated from raw prompt files.

Raw prompt files contain operational instructions, routing rules, governance rules, examples, warnings, and historical context. That creates semantic noise and increases the risk of misleading retrieval.

Instead, future embeddings should be generated only from a curated Metadata Vector Manifest.

The Metadata Vector Manifest is a generated, reviewed, versioned artifact that abstracts canonical sources into safe routing-evidence items.

Each item should represent one well-defined routing context, prompt family, routing category, or recognized task type.

It should not represent:

```text
- raw prompt file content
- full freeze entries
- historical chat turns
- user request logs
- private user text
- generated terminal logs
- project memory as a whole
```

---

# 9. Proposed corpus item shape

Each future corpus item should include:

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

---

# 10. Corpus lifecycle state machine

The design must define a strict lifecycle.

```text
proposed
  -> validated
  -> active
  -> deprecated
  -> superseded
  -> archived
```

Rules:

```text
- Only active items may be surfaced by the runtime scorer.
- Deprecated, superseded, archived, experimental, or invalid items must be filtered out before semantic scoring.
- Non-active items must not be scored lower; they must be excluded.
- Lifecycle transitions require human-governed review.
- Corpus changes require validation before use.
- Corpus regeneration must be explicit, not automatic.
```

---

# 11. Metadata eligibility gate

Metadata filtering must happen before semantic scoring or candidate promotion.

The future scoring flow should be:

```text
candidate pool
    |
    v
metadata eligibility gate
    |
    v
semantic scoring
    |
    v
ambiguity gate
    |
    v
advisory-only guard
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

---

# 12. Generated vector index policy

The vector index is disposable generated evidence.

It is not canonical memory.

It is not freeze memory.

It is not source of truth.

It must not be stored in `project_freeze_ledger`.

It must not be stored in `project_freeze_after_update/frozen_features_memory`.

It must not be manually edited.

It must not be consulted to override the routing canon.

Recommended policy:

```text
- Missing index: normal operating mode.
- Stale index: normal operating mode.
- Corrupt index: normal operating mode.
- Model mismatch: normal operating mode.
- Corpus hash mismatch: normal operating mode.
```

All of these must fall back to lexical scoring.

No crash.

No automatic rebuild.

No startup rebuild.

No hidden background generation in this phase.

---

# 13. No automatic rebuild at startup

The design must explicitly forbid automatic index regeneration at startup.

If the index is missing, stale, corrupted, or mismatched:

```text
- mark semantic provider unavailable
- fall back to lexical scorer
- emit advisory warning
- require explicit human-governed rebuild in a future phase
```

Reason:

```text
Automatic rebuild creates hidden side effects.
Hidden side effects violate the shield boundary.
Generated vector artifacts must not become silent project memory.
```

---

# 14. Provider boundary

Future providers must be disabled by default.

The default provider is:

```text
disabled_null_provider
```

The disabled provider returns no semantic candidates and allows lexical fallback.

Future provider categories:

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
   - must be explicitly enabled
   - must be dependency-reviewed
   - must be version-pinned
   - must be optional

4. external_api_provider
   - forbidden in v3
   - requires separate governance and audit
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

---

# 15. Semantic evidence output shape

Approved future semantic candidate shape:

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

---

# 16. Ambiguity policy

Ambiguity must be explicit and durable.

If top candidates are too close, output must mark ambiguity and suppress candidate promotion.

Recommended design rule:

```text
If top score and second score differ by <= frozen ambiguity_delta, mark AMBIGUOUS_SEMANTIC_MATCH.
```

Suggested initial design constant:

```text
ambiguity_delta = 0.05
```

This is a design placeholder, not an implementation threshold. It must be frozen before implementation.

If ambiguity occurs:

```text
- do not promote any candidate
- do not auto-load prompts
- do not decide route
- do not decide May proceed now
- output ambiguity status
- ask routing canon / human process to decide
```

Ambiguity threshold must not be runtime-adjustable.

Changing ambiguity thresholds requires a governed patch and freeze.

---

# 17. Determinism-anchor discrepancy protocol

Future semantic output may disagree with lexical evidence.

This must be visible, not hidden.

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
- semantic disagreement logged as advisory evidence only
```

Core rule:

```text
Disagreement cannot increase authority.
Disagreement can only increase caution.
```

---

# 18. Human-in-the-loop validation gates

Semantic candidates must go through human-governed validation before any future display or use.

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

---

# 19. Semantic veto as future governed correction

A human semantic veto is useful, but must not become self-learning.

Allowed future concept:

```text
Human marks candidate as false positive.
The false positive is added to a review queue.
A future governed corpus update adds a negative example or suppression rule.
Validation runs.
Freeze occurs.
Only then does behavior change.
```

Forbidden concept:

```text
Human clicks veto.
Runtime silently updates corpus, index, model, thresholds, or weights.
```

---

# 20. Privacy and no-query-persistence policy

The semantic scorer must not persist real user request text by default.

Forbidden:

```text
- storing user queries for training
- storing user queries in vector indexes
- embedding user queries into persistent memory
- uploading user queries to external APIs
- silently logging full request text
```

Allowed future logging, only if governed:

```text
- non-sensitive curated evaluation cases
- hashed request identifiers
- aggregate metrics
- explicitly opt-in debug logs
```

---

# 21. External building block adoption policy

KANDA should not reinvent the wheel, but external code must be treated as a supply-chain risk.

Future candidates to study:

```text
- sentence-transformers
- all-MiniLM-L6-v2
- FAISS
- Qdrant
- Chroma
```

This phase does not adopt them.

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

Rule:

```text
No external ML or vector dependency may become core runtime behavior without explicit governed adapter boundary and freeze approval.
```

---

# 22. Recommended future implementation order

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

---

# 23. Retrieval evaluation plan

Before implementation, define a frozen evaluation corpus.

Evaluation categories:

```text
1. Positive routing cases
2. Near-miss cases
3. Ambiguous cases
4. Adversarial instruction cases
5. Stale context cases
6. Out-of-domain cases
7. Freeze/shield boundary cases
8. Fast Path false-positive cases
```

Metrics:

```text
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
```

Design target examples:

```text
- 0% authority leakage
- 0 deprecated candidates surfaced
- 0 superseded candidates surfaced
- 100% fallback on stale/corrupt/missing index
- p95 semantic overhead target defined before implementation
```

---

# 24. Latency, CPU, RAM, and local-first budget

This is a Windows/PyCharm local-first app.

The design must set budgets before implementation.

Suggested design constraints:

```text
- default semantic provider disabled
- no model load at startup
- no startup index rebuild
- no blocking UI thread
- no required torch install
- no required vector DB install
- p95 advisory lookup overhead target defined before runtime implementation
- memory footprint ceiling defined before runtime implementation
```

Initial conservative budget:

```text
Design target:
- semantic disabled overhead: near zero
- fallback path: existing lexical scorer speed preserved
- future semantic lookup p95 target: under 100 ms if using precomputed vectors
```

If future local model loading exceeds this, it must remain optional and disabled by default.

---

# 25. Threat model

Threats to address:

```text
1. Authority creep
2. Stale corpus contamination
3. Deprecated prompt retrieval
4. Superseded context retrieval
5. Embedding drift
6. Model version mismatch
7. Index poisoning
8. Manual index tampering
9. Partial index generation
10. External dependency lock-in
11. External API data exposure
12. User-query persistence
13. Ambiguity fatigue
14. High-score de facto authority
15. Cross-box invasion
```

For each threat, design response:

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

---

# 26. Fitness-function test matrix

Future tests must enforce the architecture law.

The design-only patch should include tests that verify the design document requires:

```text
- advisory-only semantic evidence
- lexical fallback
- disabled-by-default provider
- metadata eligibility gate
- corpus lifecycle state machine
- source_structural_hash
- isolation_domain
- corpus_hash
- embedding_model_id
- embedding_model_version
- vector index disposable generated cache
- no automatic rebuild at startup
- no external API provider in v3
- no user-query persistence
- no authority output fields
- retrieval evaluation metrics
- latency/resource budget
- external building block adoption policy
- threat model
```

Tests should also verify no forbidden files are added in this phase.

---

# 27. Explicit forbidden behavior

The design must explicitly forbid:

```text
- semantic output deciding final route
- semantic output deciding required prompts
- semantic output deciding May proceed now
- semantic output auto-loading prompts
- semantic output writing freeze memory
- semantic output modifying startup
- semantic output modifying prompt-library
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
```

---

# 28. Required design-only patch validation

The validation must prove:

```text
1. Design document exists.
2. Manifest registers the design artifact.
3. No runtime behavior changed.
4. No ML dependency was added.
5. No provider implementation was added.
6. No vector index was added.
7. No corpus generator was added.
8. No prompt workspace files were touched.
9. No freeze boxes were touched.
10. No project_freeze_ledger files were touched.
11. Design document contains required architecture sections.
12. Design document contains explicit forbidden behavior.
13. Design document contains future evaluation metrics.
14. Design document contains future adoption gates for external libraries.
15. KANDA_FREEZE_HINT.json documents design-only scope.
```

---

# 29. Future implementation gate

No future ML implementation may begin until this design is:

```text
- installed
- validated
- frozen
```

Future implementation must have its own feature name, feature ID, patch boundary, tests, validation evidence, and freeze entry.

The next implementation after this design should probably be:

```text
Routing Signal Scorer v3 Mock Semantic Evidence Contract v1
```

Not real embeddings yet.

---

# 30. Final canon for this phase

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
