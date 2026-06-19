---
freeze_id: "freeze-20260617-routing-signal-scorer-v3-schema-only-precomputed-artifact-example-v1"
feature_title: "Routing Signal Scorer v3 Schema-Only Precomputed Artifact Example v1"
box: "kanda_reasoner_app/routing_signal_scorer"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v3-schema-only-precomputed-artifact-example-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer/schema_only_precomputed_artifact_example.py"
  - "kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.md"
  - "kanda_reasoner_app/routing_signal_scorer/design/examples/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json"
  - "kanda_reasoner_app/routing_signal_scorer/box_manifest.json"
  - "tests/test_routing_signal_scorer_v3_schema_only_precomputed_artifact_example.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Preserve advisory only."
  - "Preserve standard library only."
  - "Preserve schema only precomputed artifact example."
  - "Preserve schema only artifact example static fixture only."
  - "Preserve schema only artifact example no generation."
  - "Preserve schema only artifact example no reader."
  - "Preserve schema only artifact example no loading."
  - "Preserve schema only artifact example no raw text."
  - "Preserve schema only artifact example no embedding values."
  - "Preserve schema only artifact example no vector values."
  - "Preserve schema only artifact example no vector index."
  - "Preserve schema only artifact example no provider config."
  - "Preserve schema only artifact example no authority fields."
  - "Preserve schema only artifact example review evidence only."
  - "Preserve schema only artifact example no runtime enablement."
  - "Preserve schema only artifact example no threshold tuning."
  - "Preserve schema only artifact example requires separate governed generation patch."
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

# freeze-20260617-routing-signal-scorer-v3-schema-only-precomputed-artifact-example-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v3-schema-only-precomputed-artifact-example-v1`

Feature title: `Routing Signal Scorer v3 Schema-Only Precomputed Artifact Example v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer`

Box type: `standard-library-only schema-only precomputed artifact example fixture contract`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Auto-filled by the Freeze Feature After Update tab as a safe current-feature starter. This draft intentionally avoids stale legacy freeze-workflow titles, paths, and validation markers. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/schema_only_precomputed_artifact_example.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.md`
- `kanda_reasoner_app/routing_signal_scorer/design/examples/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_schema_only_precomputed_artifact_example.py`
- `tests/test_routing_signal_scorer_v3_advisory_precomputed_artifact_ui_preview_design.py`
- `tests/test_routing_signal_scorer_v3_disabled_artifact_reader_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_precomputed_semantic_evidence_artifact_design.py`
- `tests/test_routing_signal_scorer_v3_provider_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_disabled_evaluation_runner_design.py`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_gold_set_schema.py`
- `tests/test_routing_signal_scorer_v3_offline_evaluation_corpus_design.py`
- `tests/test_routing_signal_scorer_v3_offline_corpus_governance_design.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer/schema_only_precomputed_artifact_example.py`
- `kanda_reasoner_app/routing_signal_scorer/design/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.md`
- `kanda_reasoner_app/routing_signal_scorer/design/examples/routing_signal_scorer_v3_schema_only_precomputed_artifact_example.json`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v3_schema_only_precomputed_artifact_example.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Preserve advisory only.`
- `Preserve standard library only.`
- `Preserve schema only precomputed artifact example.`
- `Preserve schema only artifact example static fixture only.`
- `Preserve schema only artifact example no generation.`
- `Preserve schema only artifact example no reader.`
- `Preserve schema only artifact example no loading.`
- `Preserve schema only artifact example no raw text.`
- `Preserve schema only artifact example no embedding values.`
- `Preserve schema only artifact example no vector values.`
- `Preserve schema only artifact example no vector index.`
- `Preserve schema only artifact example no provider config.`
- `Preserve schema only artifact example no authority fields.`
- `Preserve schema only artifact example review evidence only.`
- `Preserve schema only artifact example no runtime enablement.`
- `Preserve schema only artifact example no threshold tuning.`
- `Preserve schema only artifact example requires separate governed generation patch.`
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
VALIDATION OK: routing_signal_scorer_v3_schema_only_precomputed_artifact_example_v1
CONTRACT_TEST_OK: schema-only precomputed artifact example validates redacted static fixture shape, source references, no raw/private text, no embedding/vector values, no provider config, no authority fields, disabled generation/reader/loading/runtime flags, review-evidence-only permitted uses, stdlib-only dependency ceiling, manifest registration, and v3 UI-preview/reader/precomputed/provider/runner/gold-set/evaluation/governance/manifest/mock/design/v2 shield regressions without artifact generator, artifact reader, artifact loading, raw text materialization, vector materialization, provider execution, runtime behavior, threshold tuning, or cross-box mutation.
SANDBOX_ROUTING_SIGNAL_SCORER_V3_SCHEMA_ONLY_PRECOMPUTED_ARTIFACT_EXAMPLE_V1_VALIDATION_OK
```

## known warnings

['This is a schema-only static example fixture and intentionally does not implement artifact generation, artifact reading, artifact loading, raw text materialization, vector materialization, providers, semantic UI behavior, prompt-router behavior, contract.py export, or __init__.py export.', 'Actual artifact generation remains a future governed phase and must remain review-evidence-only, manually gated, schema-validated, and separately frozen.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Schema-Only Precomputed Artifact Example v1. Human review is still required before Confirm and Write.

## planned next step

After freeze, consider v3 closure handoff or a separately governed disabled generation boundary; do not implement real embeddings yet.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T14:55:29Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
