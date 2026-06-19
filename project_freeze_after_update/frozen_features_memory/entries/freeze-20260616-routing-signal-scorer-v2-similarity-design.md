---
freeze_id: "freeze-20260616-routing-signal-scorer-v2-similarity-design"
feature_title: "Routing Signal Scorer v2 Similarity Design"
box: "kanda_reasoner_app/routing_signal_scorer/design + tests"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-routing-signal-scorer-v2-similarity-design.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_design.md"
  - "tests/test_routing_signal_scorer_v2_similarity_design.py"
  - "kanda_reasoner_app/routing_signal_scorer"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "This milestone is design-only and must not implement runtime similarity."
  - "Do not add TF-IDF, embeddings, vector stores, sklearn, numpy, torch, faiss, sentence-transformers, or self-learning behavior in this milestone."
  - "Do not modify deterministic router behavior."
  - "Do not let similarity output decide May proceed now."
  - "Do not let similarity output override the router canon."
  - "Do not auto-load prompts from similarity output."
  - "Do not output final required prompts/groups from similarity output."
  - "Preserve v1 diagnostic, manual-pilot, and advisory behavior."
  - "Fast Path simple explanation protection remains mandatory."
  - "High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios must continue to recommend pre_output_contract_gates through the existing advisory/diagnostic chain."
  - "The canon decides final route, required prompts, missing context, and whether work may proceed."
  - "Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260616-routing-signal-scorer-v2-similarity-design

## freeze identity

Freeze ID: `freeze-20260616-routing-signal-scorer-v2-similarity-design`

Feature title: `Routing Signal Scorer v2 Similarity Design`

Date: `2026-06-16`

Primary box: `kanda_reasoner_app/routing_signal_scorer/design + tests`

Box type: `Design-Only Similarity Planning / Prompt-Call Accuracy Support`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This patch creates a design-only safety boundary for possible future similarity support. It preserves the rule: the scorer may suggest, the canon decides. Source patch ZIP: routing_signal_scorer_v2_similarity_design_patch.zip. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_design_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_design.md`
- `tests/test_routing_signal_scorer_v2_similarity_design.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_design.md`
- `tests/test_routing_signal_scorer_v2_similarity_design.py`
- `kanda_reasoner_app/routing_signal_scorer`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `This milestone is design-only and must not implement runtime similarity.`
- `Do not add TF-IDF, embeddings, vector stores, sklearn, numpy, torch, faiss, sentence-transformers, or self-learning behavior in this milestone.`
- `Do not modify deterministic router behavior.`
- `Do not let similarity output decide May proceed now.`
- `Do not let similarity output override the router canon.`
- `Do not auto-load prompts from similarity output.`
- `Do not output final required prompts/groups from similarity output.`
- `Preserve v1 diagnostic, manual-pilot, and advisory behavior.`
- `Fast Path simple explanation protection remains mandatory.`
- `High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios must continue to recommend pre_output_contract_gates through the existing advisory/diagnostic chain.`
- `The canon decides final route, required prompts, missing context, and whether work may proceed.`
- `Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_design
CONTRACT_TEST_OK: design-only similarity spec, no-runtime-similarity boundary, conservative thresholds, Fast Path protection, and no-router-override guarantees validated
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_DESIGN_VALIDATION_OK
```

## known warnings

This patch intentionally does not implement runtime similarity. It adds a design/spec document and tests only. The next safe milestone is a fixed similarity test corpus, not TF-IDF or embeddings runtime. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Design. Human review is still required before Confirm and Write.

## planned next step

After installing, validating, and freezing this design, consider routing_signal_scorer_v2_similarity_test_corpus before any runtime similarity implementation.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T23:17:47Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
