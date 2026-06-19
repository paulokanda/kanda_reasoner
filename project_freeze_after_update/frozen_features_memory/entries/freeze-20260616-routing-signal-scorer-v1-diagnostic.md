---
freeze_id: "freeze-20260616-routing-signal-scorer-v1-diagnostic"
feature_title: "Routing Signal Scorer v1 Diagnostic"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-routing-signal-scorer-v1-diagnostic.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "tests/test_routing_signal_scorer_v1_diagnostic.py"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Routing Signal Scorer v1 Diagnostic must remain diagnostic-only."
  - "The scorer may suggest likely route families and hooks, but the deterministic KANDA routing canon decides final routing."
  - "The scorer must not return May proceed now decisions, route override decisions, or automatic prompt-loading decisions."
  - "Fast Path simple explanation requests must remain low-risk and must not recommend pre_output_contract_gates unless a high-risk artifact is present."
  - "Patch delivery, terminal output, freeze-form JSON, freeze hint sidecar, freeze-memory write, and external project root signals must recommend pre_output_contract_gates as a diagnostic hook."
  - "The first version must remain rules-only and must not introduce embeddings, TF-IDF, online learning, or a classifier."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "KANDA_FREEZE_HINT.json must remain patch ZIP root delivery metadata and must not be installed into the project root."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260616-routing-signal-scorer-v1-diagnostic

## freeze identity

Freeze ID: `freeze-20260616-routing-signal-scorer-v1-diagnostic`

Feature title: `Routing Signal Scorer v1 Diagnostic`

Date: `2026-06-16`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `Diagnostic Pre-Router Signal Layer / Prompt-Call Accuracy Support`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This feature implements the first safe step toward machine-learning-informed prompt routing: a deterministic, transparent, rules-only signal scorer that recommends risk hooks without overriding KANDA canon. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v1_diagnostic_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v1_diagnostic.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `tests/test_routing_signal_scorer_v1_diagnostic.py`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Routing Signal Scorer v1 Diagnostic must remain diagnostic-only.`
- `The scorer may suggest likely route families and hooks, but the deterministic KANDA routing canon decides final routing.`
- `The scorer must not return May proceed now decisions, route override decisions, or automatic prompt-loading decisions.`
- `Fast Path simple explanation requests must remain low-risk and must not recommend pre_output_contract_gates unless a high-risk artifact is present.`
- `Patch delivery, terminal output, freeze-form JSON, freeze hint sidecar, freeze-memory write, and external project root signals must recommend pre_output_contract_gates as a diagnostic hook.`
- `The first version must remain rules-only and must not introduce embeddings, TF-IDF, online learning, or a classifier.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `KANDA_FREEZE_HINT.json must remain patch ZIP root delivery metadata and must not be installed into the project root.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v1_diagnostic
CONTRACT_TEST_OK: diagnostic-only signal scoring, high-risk hook recommendations, Fast Path protection, and no-router-override behavior validated
SANDBOX_ROUTING_SIGNAL_SCORER_V1_DIAGNOSTIC_VALIDATION_OK
```

## known warnings

This is a diagnostic-only rules-based scorer. It is not a machine-learning classifier and does not change final routing behavior. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v1 Diagnostic. Human review is still required before Confirm and Write.

## planned next step

Install and validate the diagnostic scorer. After validation passes, freeze Routing Signal Scorer v1 Diagnostic before considering any advisory or ML-assisted routing layer.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T22:57:51Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
