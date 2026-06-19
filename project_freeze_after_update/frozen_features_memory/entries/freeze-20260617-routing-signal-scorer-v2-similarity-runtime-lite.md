---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite"
feature_title: "Routing Signal Scorer v2 Similarity Runtime Lite"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Runtime-lite similarity remains advisory only."
  - "The scorer may suggest"
  - "the canon decides."
  - "Do not let similarity decide May proceed now."
  - "Do not let similarity override the router."
  - "Do not auto-load prompts from similarity output."
  - "Do not output final required prompts/groups from similarity output."
  - "Do not introduce embeddings, vector stores, non-standard dependencies, self-learning, or cross-project route memory."
  - "Preserve v1 diagnostic, manual-pilot, advisory, v2 design, and v2 corpus behavior."
  - "Preserve Fast Path false-positive protection."
  - "Preserve pre_output_contract_gates recommendations for high-risk artifacts through the existing diagnostic/advisory chain."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-runtime-lite`

Feature title: `Routing Signal Scorer v2 Similarity Runtime Lite`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `advisory-only deterministic lexical similarity runtime`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

KANDA_FREEZE_HINT.json is delivery metadata only and must not be installed into the project root. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_runtime_lite_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v2_similarity_runtime_lite.md`
- `tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Runtime-lite similarity remains advisory only.`
- `The scorer may suggest`
- `the canon decides.`
- `Do not let similarity decide May proceed now.`
- `Do not let similarity override the router.`
- `Do not auto-load prompts from similarity output.`
- `Do not output final required prompts/groups from similarity output.`
- `Do not introduce embeddings, vector stores, non-standard dependencies, self-learning, or cross-project route memory.`
- `Preserve v1 diagnostic, manual-pilot, advisory, v2 design, and v2 corpus behavior.`
- `Preserve Fast Path false-positive protection.`
- `Preserve pre_output_contract_gates recommendations for high-risk artifacts through the existing diagnostic/advisory chain.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_runtime_lite
CONTRACT_TEST_OK: advisory-only deterministic lexical similarity runtime, frozen corpus matching, Fast Path false-positive protection, high-risk hook preservation, no external dependencies, no self-learning, and no-router-override guarantees validated
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_RUNTIME_LITE_VALIDATION_OK
```

## known warnings

This is runtime-lite lexical similarity only. It is not embeddings, TF-IDF dependency, a classifier, self-learning, or router authority. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Runtime Lite. Human review is still required before Confirm and Write.

## planned next step

After freezing, consider Box Shielding Protocol for routing_signal_scorer or continue with a later similarity calibration milestone only if needed.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T01:08:06Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
