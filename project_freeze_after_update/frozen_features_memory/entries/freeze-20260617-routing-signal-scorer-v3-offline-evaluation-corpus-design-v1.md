---
freeze_id: "freeze-20260617-routing-signal-scorer-v3-offline-evaluation-corpus-design-v1"
feature_title: "Routing Signal Scorer v3 Offline Evaluation Corpus Design v1"
box: "kanda_reasoner_app/routing_signal_scorer"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v3-offline-evaluation-corpus-design-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/offline_evaluation_corpus_design.py"
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_corpus_design.md"
  - "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
  - "tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py"
  - "tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Preserve advisory only."
  - "Preserve standard library only."
  - "Preserve offline evaluation corpus design."
  - "Preserve gold set design validation only."
  - "Preserve thresholds declared before evaluation run."
  - "Preserve zero authority leakage required."
  - "Preserve zero stale deprecated superseded candidate surface required."
  - "Preserve synthetic or curated evaluation cases only."
  - "Preserve no raw user query text in evaluation corpus."
  - "Preserve no private project text in evaluation corpus."
  - "Preserve no threshold auto tuning from results."
  - "Preserve no semantic runtime enablement from evaluation alone."
  - "Preserve no evaluation runner added."
  - "Preserve no embeddings added."
  - "Preserve no vector values added."
  - "Preserve no vector index added."
  - "Preserve no provider implementation added."
  - "Preserve no ml dependency added."
  - "Preserve no runtime behavior change."
  - "Preserve no cross box mutation."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v3-offline-evaluation-corpus-design-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v3-offline-evaluation-corpus-design-v1`

Feature title: `Routing Signal Scorer v3 Offline Evaluation Corpus Design v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer`

Box type: `routing signal scorer offline evaluation corpus design contract`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Adds a standard-library-only offline evaluation corpus design contract for a future frozen gold set, requiring predeclared metrics/thresholds, synthetic or curated cases only, zero authority leakage, stale/deprecated suppression, and review gates without enabling runtime evaluation, ML, embeddings, vector indexes, corpus generation, provider logic, threshold auto-tuning, or cross-box mutation. Also updates the immediately prior offline corpus governance regression test to expect the new routing_signal_scorer manifest version after this manifest registration. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_offline_evaluation_corpus_design_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/offline_evaluation_corpus_design.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_corpus_design.md`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py`
- `tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/offline_evaluation_corpus_design.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_corpus_design.md`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py`
- `tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Preserve advisory only.`
- `Preserve standard library only.`
- `Preserve offline evaluation corpus design.`
- `Preserve gold set design validation only.`
- `Preserve thresholds declared before evaluation run.`
- `Preserve zero authority leakage required.`
- `Preserve zero stale deprecated superseded candidate surface required.`
- `Preserve synthetic or curated evaluation cases only.`
- `Preserve no raw user query text in evaluation corpus.`
- `Preserve no private project text in evaluation corpus.`
- `Preserve no threshold auto tuning from results.`
- `Preserve no semantic runtime enablement from evaluation alone.`
- `Preserve no evaluation runner added.`
- `Preserve no embeddings added.`
- `Preserve no vector values added.`
- `Preserve no vector index added.`
- `Preserve no provider implementation added.`
- `Preserve no ml dependency added.`
- `Preserve no runtime behavior change.`
- `Preserve no cross box mutation.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_offline_evaluation_corpus_design_v1
CONTRACT_TEST_OK: offline evaluation corpus design validates required gold-set categories, predeclared metrics and thresholds, zero-tolerance authority/stale/privacy rules, synthetic-only cases, review gates, stdlib-only dependency ceiling, manifest registration, and v3 governance/manifest/mock/design/v2 shield regressions without evaluation runner, embeddings, vector values, vector indexes, runtime behavior, threshold auto-tuning, or cross-box mutation.
SANDBOX_ROUTING_SIGNAL_SCORER_V3_OFFLINE_EVALUATION_CORPUS_DESIGN_V1_VALIDATION_OK
```

## known warnings

['This is an offline evaluation corpus design/validation contract only and intentionally does not implement an evaluation runner, embeddings, vector values, vector indexes, providers, semantic UI display, prompt-router behavior, contract.py export, or __init__.py export.', 'Actual evaluation corpus artifacts and evaluation execution remain future governed phases.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Offline Evaluation Corpus Design v1. Human review is still required before Confirm and Write.

## planned next step

After freeze, continue with a schema-only evaluation gold-set example or disabled evaluation runner design; do not implement real embeddings yet.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T13:46:51Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
