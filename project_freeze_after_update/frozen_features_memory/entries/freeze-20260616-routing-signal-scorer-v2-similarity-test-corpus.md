---
freeze_id: "freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus"
feature_title: "Routing Signal Scorer v2 Similarity Test Corpus"
box: "kanda_reasoner_app/routing_signal_scorer/design + tests"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_test_corpus.json"
  - "tests/test_routing_signal_scorer_v2_similarity_test_corpus.py"
  - "kanda_reasoner_app/routing_signal_scorer"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "This milestone is corpus-only and must not implement runtime similarity."
  - "Do not add TF-IDF, embeddings, vector stores, sklearn, numpy, torch, faiss, sentence-transformers, or self-learning behavior in this milestone."
  - "Do not modify deterministic router behavior."
  - "Do not modify scorer runtime behavior."
  - "Do not let similarity output decide May proceed now."
  - "Do not let similarity output override the router canon."
  - "Do not auto-load prompts from similarity output."
  - "Do not output final required prompts/groups from similarity output."
  - "Preserve v1 diagnostic, manual-pilot, advisory, and v2 similarity design behavior."
  - "Fast Path simple explanation protection remains mandatory."
  - "Similarity false-positive traps must not classify conceptual patch explanations as installable patch delivery."
  - "High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios must continue to recommend pre_output_contract_gates through the existing advisory/diagnostic chain."
  - "The canon decides final route, required prompts, missing context, and whether work may proceed."
  - "Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback and must not become the normal freeze path."
superseded_by: null
---

# freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus

## freeze identity

Freeze ID: `freeze-20260616-routing-signal-scorer-v2-similarity-test-corpus`

Feature title: `Routing Signal Scorer v2 Similarity Test Corpus`

Date: `2026-06-16`

Primary box: `kanda_reasoner_app/routing_signal_scorer/design + tests`

Box type: `Corpus-only similarity planning and prompt-call accuracy support`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This freeze records the curated fixed test corpus required before any runtime similarity work. Source patch ZIP: routing_signal_scorer_v2_similarity_test_corpus_patch.zip. KANDA_FREEZE_HINT.json is delivery metadata only and must not be installed into the project root.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_test_corpus.json`
- `tests/test_routing_signal_scorer_v2_similarity_test_corpus.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_test_corpus.json`
- `tests/test_routing_signal_scorer_v2_similarity_test_corpus.py`
- `kanda_reasoner_app/routing_signal_scorer`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `This milestone is corpus-only and must not implement runtime similarity.`
- `Do not add TF-IDF, embeddings, vector stores, sklearn, numpy, torch, faiss, sentence-transformers, or self-learning behavior in this milestone.`
- `Do not modify deterministic router behavior.`
- `Do not modify scorer runtime behavior.`
- `Do not let similarity output decide May proceed now.`
- `Do not let similarity output override the router canon.`
- `Do not auto-load prompts from similarity output.`
- `Do not output final required prompts/groups from similarity output.`
- `Preserve v1 diagnostic, manual-pilot, advisory, and v2 similarity design behavior.`
- `Fast Path simple explanation protection remains mandatory.`
- `Similarity false-positive traps must not classify conceptual patch explanations as installable patch delivery.`
- `High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios must continue to recommend pre_output_contract_gates through the existing advisory/diagnostic chain.`
- `The canon decides final route, required prompts, missing context, and whether work may proceed.`
- `Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback and must not become the normal freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_test_corpus
CONTRACT_TEST_OK: corpus-only similarity scenarios, expected labels, Fast Path false-positive trap, RG anchors, no-runtime-similarity boundary, and no-router-override guarantees validated
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_TEST_CORPUS_VALIDATION_OK

VALIDATION OK
routing_signal_scorer_v2_similarity_test_corpus is installed and validated.
```

## known warnings

The Freeze Feature After Update autofill initially returned placeholders or stale legacy freeze-hint data. This corrected form is for the current validated feature only. The patch intentionally does not implement runtime similarity, TF-IDF, embeddings, self-learning, router changes, or scorer runtime behavior changes. Runtime-lite should only be considered after this corpus is frozen.

## planned next step

After this corpus is frozen, consider routing_signal_scorer_v2_similarity_runtime_lite as a separate advisory-only and conservative milestone, with no router override and no May proceed now decision.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T23:45:38Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
