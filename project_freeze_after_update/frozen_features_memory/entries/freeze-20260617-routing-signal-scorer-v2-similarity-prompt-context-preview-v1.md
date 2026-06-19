---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-prompt-context-preview-v1"
feature_title: "Routing Signal Scorer v2 Similarity Prompt Context Preview v1"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-prompt-context-preview-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "kanda_reasoner_app/routing_signal_scorer/design"
  - "tests/test_routing_signal_scorer_v2_similarity_prompt_context_preview.py"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Candidate prompt contexts are advisory hints only."
  - "Do not treat candidate prompt contexts as final required prompts."
  - "Do not auto-load prompts from similarity output."
  - "Do not let similarity output decide May proceed now."
  - "Do not let similarity output override deterministic KANDA routing."
  - "Do not add embeddings, TF-IDF dependency, vector stores, self-learning, or stronger ML."
  - "Preserve UI/log preview adapter behavior."
  - "Preserve decision report, explainability, threshold policy, runtime-lite, corpus, v1 advisory, and v1 diagnostic behavior."
  - "Preserve rule-hook independence and pre_output_contract_gates visibility for high-risk artifacts."
  - "Preserve freeze hint autofill state-machine protections."
  - "Keep project-specific frozen memory under project_freeze_after_update/frozen_features_memory."
  - "Do not store active project frozen memory inside project_freeze_ledger."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-prompt-context-preview-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-prompt-context-preview-v1`

Feature title: `Routing Signal Scorer v2 Similarity Prompt Context Preview v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `Advisory-only candidate prompt-context preview adapter`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

KANDA_FREEZE_HINT.json is ZIP delivery metadata only and must not be installed into the project root. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_prompt_context_preview_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_prompt_context_preview.md`
- `tests/test_routing_signal_scorer_v2_similarity_prompt_context_preview.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `kanda_reasoner_app/routing_signal_scorer/design`
- `tests/test_routing_signal_scorer_v2_similarity_prompt_context_preview.py`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Candidate prompt contexts are advisory hints only.`
- `Do not treat candidate prompt contexts as final required prompts.`
- `Do not auto-load prompts from similarity output.`
- `Do not let similarity output decide May proceed now.`
- `Do not let similarity output override deterministic KANDA routing.`
- `Do not add embeddings, TF-IDF dependency, vector stores, self-learning, or stronger ML.`
- `Preserve UI/log preview adapter behavior.`
- `Preserve decision report, explainability, threshold policy, runtime-lite, corpus, v1 advisory, and v1 diagnostic behavior.`
- `Preserve rule-hook independence and pre_output_contract_gates visibility for high-risk artifacts.`
- `Preserve freeze hint autofill state-machine protections.`
- `Keep project-specific frozen memory under project_freeze_after_update/frozen_features_memory.`
- `Do not store active project frozen memory inside project_freeze_ledger.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_prompt_context_preview_v1
CONTRACT_TEST_OK: candidate prompt-context preview exposes route-family-derived context hints without final required prompts, prompt loading, May proceed now, router override, stronger ML boundaries, or prior routing scorer and freeze-tab regressions
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_PROMPT_CONTEXT_PREVIEW_V1_VALIDATION_OK
```

## known warnings

This milestone is a candidate-context preview only. It does not implement final prompt routing, automatic prompt loading, or stronger machine learning. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Prompt Context Preview v1. Human review is still required before Confirm and Write.

## planned next step

After freezing, consider a read-only GUI integration or audit-view wiring milestone that displays the candidate prompt-context preview without changing routing authority.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T10:00:18Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
