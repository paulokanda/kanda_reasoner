---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-policy-runtime-alignment-v1"
feature_title: "Routing Signal Scorer v2 Similarity Policy Runtime Alignment v1"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-policy-runtime-alignment-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/contract.py"
  - "kanda_reasoner_app/routing_signal_scorer/__init__.py"
  - "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_threshold_policy.md"
  - "tests/test_routing_signal_scorer_v2_similarity_policy_runtime_alignment.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Runtime-lite similarity remains advisory only and must not override the router canon."
  - "Thresholds must remain centralized as 0.18 visibility, 0.30 promotion, and 0.55 high similarity."
  - "Runtime output must expose threshold-policy metadata so policy/runtime drift is visible."
  - "Low similarity may be visible but must not promote similarity-derived route families, hooks, or caution flags."
  - "High similarity remains advisory and must not provide May proceed now, final prompts, or route override authority."
  - "Rule-based hooks remain independent of similarity filtering."
  - "Do not add embeddings, TF-IDF dependency, vector store, self-learning, or cross-project memory."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-policy-runtime-alignment-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-policy-runtime-alignment-v1`

Feature title: `Routing Signal Scorer v2 Similarity Policy Runtime Alignment v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `runtime-lite policy-alignment hardening`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Align runtime-lite with the frozen similarity threshold policy by centralizing constants, exposing policy metadata in runtime output, and adding regression coverage without adding stronger ML or routing authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_policy_runtime_alignment_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v2_similarity_policy_runtime_alignment.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_threshold_policy.md`
- `tests/test_routing_signal_scorer_v2_similarity_policy_runtime_alignment.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Runtime-lite similarity remains advisory only and must not override the router canon.`
- `Thresholds must remain centralized as 0.18 visibility, 0.30 promotion, and 0.55 high similarity.`
- `Runtime output must expose threshold-policy metadata so policy/runtime drift is visible.`
- `Low similarity may be visible but must not promote similarity-derived route families, hooks, or caution flags.`
- `High similarity remains advisory and must not provide May proceed now, final prompts, or route override authority.`
- `Rule-based hooks remain independent of similarity filtering.`
- `Do not add embeddings, TF-IDF dependency, vector store, self-learning, or cross-project memory.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_policy_runtime_alignment_v1
CONTRACT_TEST_OK: runtime-lite now exposes and uses centralized threshold-policy constants for 0.18 visibility, 0.30 promotion, and 0.55 high similarity while preserving low-similarity non-promotion, high-similarity non-authority, rule-hook independence, public exports, forbidden stronger-ML absence, and prior routing scorer regressions
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_POLICY_RUNTIME_ALIGNMENT_V1_VALIDATION_OK
```

## known warnings

Starter draft only. Replace placeholders with the current validated feature data. No validation evidence has been inferred or invented. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Policy Runtime Alignment v1. Human review is still required before Confirm and Write.

## planned next step

Replace placeholders with current feature evidence, then Preview Freeze Entry before Confirm and Write.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T01:45:46Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
