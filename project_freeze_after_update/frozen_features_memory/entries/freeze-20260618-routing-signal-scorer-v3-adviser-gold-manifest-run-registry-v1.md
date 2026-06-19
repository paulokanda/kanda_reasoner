---
freeze_id: "freeze-20260618-routing-signal-scorer-v3-adviser-gold-manifest-run-registry-v1"
feature_title: "Routing Signal Scorer v3 Adviser Gold Manifest Run Registry v1"
box: "routing_signal_scorer"
status: "frozen"
date: "2026-06-18"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260618-routing-signal-scorer-v3-adviser-gold-manifest-run-registry-v1.md"
protected_paths:
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Adviser M6 remains offline gold-manifest and run-registry metadata logic only."
  - "M6 must build and validate supplied records only."
  - "M6 must not create a gold set, load gold cases from disk, write registry files, write scratch files, or mutate project memory."
  - "M6 must not execute a candidate scorer or create candidate outputs."
  - "No ML execution, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, or router authority are added by this milestone."
  - "hash_utils.py must hash supplied values only and must not read files or scan source trees."
  - "gold_manifest.py must require human-reviewed case entries before manifest inclusion."
  - "run_registry.py must preserve critical failures and promotion blockers as blockers."
  - "Runtime router code must not import adviser_offline."
  - "adviser_offline registry must not import runtime router code."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260618-routing-signal-scorer-v3-adviser-gold-manifest-run-registry-v1

## freeze identity

Freeze ID: `freeze-20260618-routing-signal-scorer-v3-adviser-gold-manifest-run-registry-v1`

Feature title: `Routing Signal Scorer v3 Adviser Gold Manifest Run Registry v1`

Date: `2026-06-18`

Primary box: `routing_signal_scorer`

Box type: `diagnostic_pre_router_signal_layer/adviser_offline_registry_metadata_sub_box`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

M6 adds only side-effect-free metadata record builders and validators for supplied gold-manifest and run-registry data. It does not create a gold set or execute a candidate. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/hash_utils.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/gold_manifest.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/run_registry.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_manifest_run_registry.py`
- `tests/test_routing_signal_scorer_v3_adviser_pure_comparison_harness.py`
- `tests/test_routing_signal_scorer_v3_adviser_severity_resource_limits.py`
- `tests/test_routing_signal_scorer_v3_adviser_contract_validator_output_guard.py`
- `tests/test_routing_signal_scorer_v3_adviser_schema_family_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_foundations_reference_box_boundary_design.py`
- `tests/test_routing_signal_scorer_v3_adviser_system_card_bug_bar_threat_model_design.py`
- `tests/test_routing_signal_scorer_v3_generator_candidate_human_decision_recording_patch_boundary_design.py`
- `tests/test_routing_signal_scorer_v2_similarity_runtime_lite.py`
- `tests/test_freeze_hint_autofill_state_machine.py`

## generated files

- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/hash_utils.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/gold_manifest.py`
- `kanda_reasoner_app/routing_signal_scorer/adviser_offline/registry/run_registry.py`
- `tests/test_routing_signal_scorer_v3_adviser_gold_manifest_run_registry.py`

## protected paths

- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Adviser M6 remains offline gold-manifest and run-registry metadata logic only.`
- `M6 must build and validate supplied records only.`
- `M6 must not create a gold set, load gold cases from disk, write registry files, write scratch files, or mutate project memory.`
- `M6 must not execute a candidate scorer or create candidate outputs.`
- `No ML execution, runtime integration, prompt auto-loading, artifact IO, embeddings, providers, source scanning, or router authority are added by this milestone.`
- `hash_utils.py must hash supplied values only and must not read files or scan source trees.`
- `gold_manifest.py must require human-reviewed case entries before manifest inclusion.`
- `run_registry.py must preserve critical failures and promotion blockers as blockers.`
- `Runtime router code must not import adviser_offline.`
- `adviser_offline registry must not import runtime router code.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v3_adviser_gold_manifest_run_registry_v1
CONTRACT_TEST_OK: adviser gold manifest and run registry, standard-library-only offline supplied-record metadata logic, no candidate scorer, no ML execution, no runtime import/export, no prompt auto-loading, no artifact IO, no embeddings, no providers, no gold set creation, no scratch writer, M0/M1/M2/M3/M4/M5 adviser regressions, current generator-candidate patch-boundary, runtime-lite, and freeze-hint state-machine regressions validated
SANDBOX_ROUTING_SIGNAL_SCORER_V3_ADVISER_GOLD_MANIFEST_RUN_REGISTRY_V1_VALIDATION_OK
```

## known warnings

['Offline gold-manifest/run-registry metadata milestone only.', 'No candidate scorer was added.', 'No gold set, scratch writer, runtime integration, ML execution, embeddings, providers, prompt auto-loading, artifact IO, source scanning, or router authority were added.', 'M0/M1/M2/M3/M4/M5 tests were updated only to allow the new M6 pure registry modules while preserving no-candidate/no-runtime restrictions.'] Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v3 Adviser Gold Manifest Run Registry v1. Human review is still required before Confirm and Write.

## planned next step

After freeze confirmation, proceed to M7: Routing Signal Scorer v3 Adviser Seed Case Corpus v1.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-18T12:43:14Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
