# Routing Signal Scorer v3 Offline Evaluation Corpus Design v1

Feature ID: `routing_signal_scorer_v3_offline_evaluation_corpus_design_v1`

This is a standard-library-only design and validation contract for a future
offline evaluation corpus. It is not a real evaluation runner, not an
embedding benchmark, not a corpus generator, and not a semantic runtime.

The semantic layer remains an untrusted evidence witness.

It may provide evidence. It may never provide authority.

## Purpose

Before any real embedding provider, vector index, or semantic evidence layer
can be enabled, KANDA needs a frozen gold-standard evaluation corpus design.
The evaluation corpus exists to measure whether semantic evidence improves
over the deterministic lexical baseline without causing stale retrieval,
false positives, authority leakage, privacy leakage, or latency regression.

This phase freezes the evaluation contract only.

## Non-goals

This phase does not implement real evaluation. It does not run ML models,
generate embeddings, create vector indexes, load sentence-transformers,
install FAISS, call external APIs, store user queries, tune thresholds, or
enable semantic runtime behavior.

## Evaluation corpus categories

The future frozen gold set must cover at least these categories:

- `positive_routing_cases`
- `near_miss_cases`
- `ambiguous_cases`
- `adversarial_instruction_cases`
- `stale_context_cases`
- `out_of_domain_cases`
- `freeze_shield_boundary_cases`
- `fast_path_false_positive_cases`

These categories prevent the evaluation from becoming a narrow success demo.
Near-miss, stale-context, out-of-domain, and Fast Path false-positive cases are
as important as positive matches.

## Required metrics

Metrics must be declared before the evaluation run. They must not be chosen
after seeing results.

Required metrics:

- `Precision@1`
- `Precision@3`
- `Recall@1`
- `Recall@3`
- `MRR`
- `NDCG@10`
- `false_positive_rate`
- `stale_candidate_suppression_rate`
- `deprecated_candidate_suppression_rate`
- `ambiguity_detection_rate`
- `authority_leakage_rate`
- `p95_latency_overhead_ms`

## Required zero-tolerance thresholds

The future evaluation corpus must require:

- zero authority leakage
- zero deprecated candidates surfaced
- zero superseded candidates surfaced
- zero stale candidates surfaced
- zero external API calls
- zero user-query persistence

A semantic layer that improves top-1 retrieval but leaks authority is a failed
semantic layer.

## Privacy policy

The evaluation corpus must use synthetic or curated cases only.

It must not contain raw user query text, private chat history, freeze-entry
text, prompt-file body text, terminal logs, or project memory dumps. It may
contain concise synthetic request summaries and expected behavior labels.

## Authority boundary

Evaluation output may never produce or authorize:

- `final_route`
- `required_prompts`
- `may_proceed_now`
- `route_override`
- `auto_load_prompts`
- `write_freeze_memory`
- `modify_startup`
- `modify_prompt_library`
- `self_update_corpus`

Evaluation can only produce review evidence.

## Threshold governance

Thresholds must be declared before an evaluation run.

Thresholds may not be auto-adjusted after results. If thresholds need to
change, that requires a separate governed patch and freeze. Evaluation results
may recommend a threshold review, but they may not mutate thresholds.

## Review gates

Required review gates:

- human review required
- gold-set freeze required
- thresholds declared before run
- semantic-vs-lexical disagreement review required
- false-positive review required
- stale-candidate review required
- authority-leakage review required
- no runtime enablement from evaluation alone

## Relationship to previous v3 phases

This design depends on the frozen semantic readiness architecture, mock
semantic evidence contract, Metadata Vector Manifest schema, and offline
corpus governance design. It does not supersede them.

The evaluation corpus tests future semantic evidence against the law already
frozen by those phases: metadata eligibility first, active-only candidates,
no raw prompt text, no user-query persistence, no vector values in schema
phases, no automatic rebuild, no external API provider in v3, and no runtime
ML behavior without a future governed implementation patch.

## Future implementation gate

A future semantic implementation may only proceed after a frozen offline
evaluation corpus exists and demonstrates that semantic evidence remains
advisory-only, stale-safe, privacy-safe, and bounded.

This design does not authorize evaluation execution.

This design does not authorize semantic runtime enablement.

This design does not authorize embeddings.

This design does not authorize vector indexes.

This design does not authorize threshold changes.
