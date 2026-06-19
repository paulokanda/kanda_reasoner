---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-threshold-policy-v1"
feature_title: "Routing Signal Scorer v2 Similarity Threshold Policy v1"
box: "kanda_reasoner_app/routing_signal_scorer + tests + project_freeze_after_update"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-threshold-policy-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_threshold_policy.md"
  - "tests/test_routing_signal_scorer_v2_similarity_threshold_policy.py"
  - "kanda_reasoner_app/routing_signal_scorer/contract.py"
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_test_corpus.json"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Runtime-lite similarity remains advisory only."
  - "Do not add embeddings, TF-IDF dependency, vector store, or self-learning."
  - "Default visibility floor remains 0.18 unless governed update is validated and frozen."
  - "Similarity promotion floor remains 0.30 unless governed update is validated and frozen."
  - "High similarity label threshold remains 0.55 unless governed update is validated and frozen."
  - "Visible low similarity matches must not promote route families, hooks, or caution flags."
  - "Rule-based high-risk hooks must not be muted by similarity threshold filtering."
  - "Similarity must not decide route override, required prompts final, automatic prompt loading, or May proceed now."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-threshold-policy-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-threshold-policy-v1`

Feature title: `Routing Signal Scorer v2 Similarity Threshold Policy v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests + project_freeze_after_update`

Box type: `design-only threshold policy shielding`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Design-only threshold policy shield for runtime-lite similarity. Freezes visibility, promotion, and high-similarity boundaries before stronger ML work is considered. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_threshold_policy_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_threshold_policy.md`
- `tests/test_routing_signal_scorer_v2_similarity_threshold_policy.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_threshold_policy.md`
- `tests/test_routing_signal_scorer_v2_similarity_threshold_policy.py`
- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_test_corpus.json`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Runtime-lite similarity remains advisory only.`
- `Do not add embeddings, TF-IDF dependency, vector store, or self-learning.`
- `Default visibility floor remains 0.18 unless governed update is validated and frozen.`
- `Similarity promotion floor remains 0.30 unless governed update is validated and frozen.`
- `High similarity label threshold remains 0.55 unless governed update is validated and frozen.`
- `Visible low similarity matches must not promote route families, hooks, or caution flags.`
- `Rule-based high-risk hooks must not be muted by similarity threshold filtering.`
- `Similarity must not decide route override, required prompts final, automatic prompt loading, or May proceed now.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_threshold_policy_v1
CONTRACT_TEST_OK: threshold policy design freezes 0.18 visibility, 0.30 promotion, and 0.55 high-similarity boundaries while proving low-similarity non-promotion, rule-hook independence, high-similarity non-authority, and forbidden stronger-ML runtime absence with prior runtime-lite regressions preserved
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_THRESHOLD_POLICY_V1_VALIDATION_OK
```

## known warnings

Starter draft only. Replace placeholders with the current validated feature data. No validation evidence has been inferred or invented. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Threshold Policy v1. Human review is still required before Confirm and Write.

## planned next step

Replace placeholders with current feature evidence, then Preview Freeze Entry before Confirm and Write.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T01:37:42Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
