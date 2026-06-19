---
freeze_id: "freeze-20260617-routing-signal-scorer-v3-offline-evaluation-gold-set-schema-v1"
feature_title: "Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1"
box: "kanda_reasoner_app/routing_signal_scorer"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v3-offline-evaluation-gold-set-schema-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py"
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_gold_set_schema.md"
  - "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
  - "tests/test_routing_signal_scorer_v3_offline_evaluation_gold_set_schema.py"
  - "tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py"
  - "tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Preserve advisory only."
  - "Preserve standard library only."
  - "Preserve offline evaluation gold set schema."
  - "Preserve gold set schema validation only."
  - "Preserve no evaluation runner added."
  - "Preserve gold set cases synthetic or curated only."
  - "Preserve gold set case category coverage required."
  - "Preserve gold set metrics declared before run."
  - "Preserve gold set thresholds declared before run."
  - "Preserve gold set zero authority leakage required."
  - "Preserve gold set zero privacy leakage required."
  - "Preserve gold set no runtime enablement."
  - "Preserve gold set no threshold auto tuning."
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

# freeze-20260617-routing-signal-scorer-v3-offline-evaluation-gold-set-schema-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v3-offline-evaluation-gold-set-schema-v1`

Feature title: `Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer`

Box type: `standard-library-only offline evaluation gold-set schema contract`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Adds a schema-only offline evaluation gold-set contract for future synthetic/curated semantic-evidence evaluation cases without adding an evaluation runner, embeddings, vectors, indexes, providers, threshold tuning, runtime enablement, or cross-box mutation. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_gold_set_schema.md`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_gold_set_schema.py`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py`
- `tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/offline_evaluation_gold_set_schema.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_offline_evaluation_gold_set_schema.md`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_gold_set_schema.py`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py`
- `tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Preserve advisory only.`
- `Preserve standard library only.`
- `Preserve offline evaluation gold set schema.`
- `Preserve gold set schema validation only.`
- `Preserve no evaluation runner added.`
- `Preserve gold set cases synthetic or curated only.`
- `Preserve gold set case category coverage required.`
- `Preserve gold set metrics declared before run.`
- `Preserve gold set thresholds declared before run.`
- `Preserve gold set zero authority leakage required.`
- `Preserve gold set zero privacy leakage required.`
- `Preserve gold set no runtime enablement.`
- `Preserve gold set no threshold auto tuning.`
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
VALIDATION OK: routing_signal_scorer_v3_offline_evaluation_gold_set_schema_v1
CONTRACT_TEST_OK: offline evaluation gold-set schema validates synthetic/curated gold-set artifact shape, case-category coverage, predeclared metrics/thresholds, zero authority/privacy leakage, stale/deprecated suppression rules, forbidden raw/private text and authority fields, stdlib-only dependency ceiling, manifest registration, and v3 evaluation/governance/manifest/mock/design/v2 shield regressions without evaluation runner, embeddings, vector values, vector indexes, runtime behavior, threshold auto-tuning, or cross-box mutation.
SANDBOX_ROUTING_SIGNAL_SCORER_V3_OFFLINE_EVALUATION_GOLD_SET_SCHEMA_V1_VALIDATION_OK
```

## known warnings

['This is a gold-set schema contract only and intentionally does not implement an evaluation runner, gold-set artifact generation, embeddings, vector values, vector indexes, providers, semantic UI display, prompt-router behavior, contract.py export, or __init__.py export.', 'Actual evaluation gold-set artifacts and evaluation execution remain future governed phases.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Offline Evaluation Gold Set Schema v1. Human review is still required before Confirm and Write.

## planned next step

After freeze, continue with disabled evaluation runner design or schema-only gold-set artifact examples; do not implement real embeddings yet.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T13:55:44Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
