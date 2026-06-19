# Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1

Feature ID: `routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1`

This is a schema contract only. It defines the safe shape of a future frozen offline evaluation gold set. It does not run evaluation, generate embeddings, create vector indexes, tune thresholds, enable semantic runtime behavior, or change routing decisions.

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

## Purpose

The prior offline evaluation corpus design froze what must be measured before semantic evidence can be trusted. This milestone adds the next narrow contract: the gold-set artifact shape itself.

A future gold set is a frozen, human-reviewed collection of synthetic or curated evaluation cases. It is used to test retrieval/evidence behavior before any semantic provider, embedding model, vector index, or UI display is enabled.

## Non-goals

This schema phase does not authorize:

- evaluation execution
- an evaluation runner
- embeddings
- vector values
- vector indexes
- corpus generation
- semantic provider implementation
- ML dependencies
- threshold auto-tuning
- semantic runtime enablement
- prompt-router mutation
- freeze-box mutation
- `contract.py` export
- `__init__.py` export

## Gold-set artifact rule

A gold set may describe expected semantic-evidence behavior. It may never contain routing authority.

A valid gold set must include:

- `gold_set_id`
- `schema_version`
- `status`
- `declared_before_run`
- `case_records`
- `case_categories`
- `metrics_contract`
- `acceptance_thresholds`
- `privacy_policy`
- `review_gates`
- `forbidden_actions`

Metrics and thresholds must be declared before the evaluation run.

The gold set can only produce review evidence.

The gold set cannot enable semantic runtime behavior.

The gold set cannot change thresholds.

## Required case categories

The frozen gold set must cover:

- `positive_routing_cases`
- `near_miss_cases`
- `ambiguous_cases`
- `adversarial_instruction_cases`
- `stale_context_cases`
- `out_of_domain_cases`
- `freeze_shield_boundary_cases`
- `fast_path_false_positive_cases`

Missing category coverage invalidates the gold set.

## Required metrics contract

A future evaluation must define these metrics before execution:

- `precision_at_1`
- `precision_at_3`
- `recall_at_1`
- `recall_at_3`
- `mrr`
- `ndcg_at_10`
- `false_positive_rate`
- `stale_candidate_suppression_rate`
- `deprecated_candidate_suppression_rate`
- `superseded_candidate_suppression_rate`
- `ambiguity_detection_rate`
- `authority_leakage_rate`
- `privacy_leakage_rate`
- `p95_latency_overhead_ms`

## Zero-tolerance requirements

The schema requires explicit acceptance thresholds for:

- zero authority leakage
- zero privacy leakage
- zero stale candidate surfacing
- zero deprecated candidate surfacing
- zero superseded candidate surfacing
- zero external API calls
- zero user-query persistence

## Privacy boundary

Synthetic or curated cases only.

A future gold set must not contain:

- raw user-query text
- private chat history
- private project text
- freeze-entry text
- prompt-file body text
- terminal-log text
- training persistence payloads

Synthetic request templates are allowed only as artificial, non-private cases.

## Forbidden authority fields

Gold-set records must reject:

- `final_route`
- `required_prompts`
- `may_proceed_now`
- `route_override`
- `auto_load_prompts`
- `write_freeze_memory`
- `modify_startup`
- `modify_prompt_library`
- `self_update_corpus`

## Case-record rule

Every case must declare:

- `case_id`
- `category`
- `case_is_synthetic`
- `synthetic_request_template`
- `expected_behavior`
- `expected_candidate_ids`
- `forbidden_candidate_ids`
- `expected_confidence_band`
- `must_mark_ambiguity`
- `must_fallback_to_lexical`
- `source_context_status`
- `no_authority_fields_expected`
- `contains_raw_user_text`
- `contains_private_project_text`
- `contains_prompt_body_text`
- `contains_freeze_entry_text`

Only synthetic or curated cases are allowed.

Ambiguous cases must require ambiguity marking.

Stale, deprecated, or superseded source-context cases must declare forbidden candidate IDs.

## Advisory-only outcome

A gold-set evaluation may later show that semantic evidence is useful.

That still does not authorize runtime semantic enablement.

That still does not authorize threshold changes.

That still does not authorize prompt auto-loading.

That still does not authorize final routing decisions.

Any future evaluation runner, gold-set artifact, embedding provider, or semantic runtime switch requires a separate governed patch and freeze.

## External dependency boundary

This phase adds no external dependency.

It remains standard-library-only.

No `numpy`, `pandas`, `sklearn`, `scipy`, `torch`, `sentence_transformers`, `transformers`, `faiss`, `chromadb`, `qdrant_client`, `langchain`, or `llama_index` may be imported by this schema module.

## Final rule

The offline evaluation gold set is a frozen test target, not a decision maker.

It may define what future evidence must satisfy.

It may never enable semantic runtime behavior, tune thresholds, install ML dependencies, generate vectors, create indexes, or override the routing canon.
