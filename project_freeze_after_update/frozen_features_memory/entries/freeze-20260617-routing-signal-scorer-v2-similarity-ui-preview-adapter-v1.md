---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-ui-preview-adapter-v1"
feature_title: "Routing Signal Scorer v2 Similarity UI Preview Adapter v1"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-ui-preview-adapter-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "tests/test_routing_signal_scorer_v2_similarity_ui_preview_adapter.py"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "The UI preview adapter is presentation-only and must remain advisory-only."
  - "Do not change deterministic router behavior."
  - "Do not add router override behavior."
  - "Do not decide May proceed now."
  - "Do not decide final required prompts."
  - "Do not auto-load prompts from preview output."
  - "Do not add embeddings, TF-IDF dependencies, vector stores, external ML dependencies, or self-learning behavior."
  - "Preserve compact human-readable decision report lines in GUI/log preview output."
  - "Preserve top match, score, threshold level, route-family eligibility, matched route families, advisory-only reason, rule-hook independence, and recommended hooks in preview output."
  - "Preserve rule-based diagnostic hook independence from similarity matches."
  - "Preserve all previous routing-signal scorer v1 and v2 regressions."
  - "Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store active project frozen memory inside project_freeze_ledger."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-ui-preview-adapter-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-ui-preview-adapter-v1`

Feature title: `Routing Signal Scorer v2 Similarity UI Preview Adapter v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `advisory_similarity_gui_log_preview_adapter`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

KANDA_FREEZE_HINT.json is ZIP delivery metadata only and must not be installed into the project root. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_ui_preview_adapter_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_ui_preview_adapter.md`
- `tests/test_routing_signal_scorer_v2_similarity_ui_preview_adapter.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `tests/test_routing_signal_scorer_v2_similarity_ui_preview_adapter.py`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `The UI preview adapter is presentation-only and must remain advisory-only.`
- `Do not change deterministic router behavior.`
- `Do not add router override behavior.`
- `Do not decide May proceed now.`
- `Do not decide final required prompts.`
- `Do not auto-load prompts from preview output.`
- `Do not add embeddings, TF-IDF dependencies, vector stores, external ML dependencies, or self-learning behavior.`
- `Preserve compact human-readable decision report lines in GUI/log preview output.`
- `Preserve top match, score, threshold level, route-family eligibility, matched route families, advisory-only reason, rule-hook independence, and recommended hooks in preview output.`
- `Preserve rule-based diagnostic hook independence from similarity matches.`
- `Preserve all previous routing-signal scorer v1 and v2 regressions.`
- `Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store active project frozen memory inside project_freeze_ledger.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_ui_preview_adapter_v1
CONTRACT_TEST_OK: GUI/log preview exposes advisory similarity decision report without changing routing authority, prompt loading, May proceed now, stronger ML boundaries, or prior routing scorer regressions
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_UI_PREVIEW_ADAPTER_V1_VALIDATION_OK
```

## known warnings

This patch exposes an advisory decision-report preview only. It does not connect a new GUI button and does not change routing decisions. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity UI Preview Adapter v1. Human review is still required before Confirm and Write.

## planned next step

After validation passes, freeze as Routing Signal Scorer v2 Similarity UI Preview Adapter v1 before adding stronger integration or learning milestones.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T09:38:11Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
