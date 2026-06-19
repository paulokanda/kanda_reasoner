# Routing Signal Scorer v2 Similarity Runtime Lite

Feature ID: routing_signal_scorer_v2_similarity_runtime_lite
Implementation status: RUNTIME_LITE
Authority status: ADVISORY_ONLY

## Purpose

Add a small deterministic lexical-similarity advisor on top of the frozen
routing_signal_scorer_v2_similarity_test_corpus. This is the first runtime
similarity milestone after the corpus freeze.

## Boundary

The runtime-lite layer may suggest similar frozen corpus scenarios. It must not
replace the deterministic KANDA router, decide May proceed now, auto-load
prompts, output final required prompt groups, or override canon decisions.

## Method

The implementation uses standard-library token overlap against the curated JSON
corpus. It does not use embeddings, a vector store, TF-IDF dependencies,
external models, online learning, or cross-project memory.

## Required output limits

- authority: advisory_only
- does_not_override_router: true
- canon_decides_final_route: true
- may_proceed_now_decision: not_provided_by_similarity
- route_override: null
- required_prompts_final_decision: not_provided_by_similarity
- automatic_prompt_loading: false
- self_learning_enabled: false

## Conservative behavior

If no corpus case meets the threshold, the layer returns no similar cases and
keeps deterministic routing unchanged. Similar cases are scenario anchors only.
The existing rule-based advisory remains the main non-authoritative signal.

## Do not regress

- Preserve all v1 diagnostic and advisory behavior.
- Preserve the v2 similarity design and corpus tests.
- Preserve Fast Path false-positive protection.
- Preserve pre_output_contract_gates recommendations for high-risk artifact
  families through the existing diagnostic/advisory chain.
- Do not introduce non-standard dependencies.
