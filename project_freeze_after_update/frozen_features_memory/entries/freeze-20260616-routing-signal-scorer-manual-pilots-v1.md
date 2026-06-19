---
freeze_id: "freeze-20260616-routing-signal-scorer-manual-pilots-v1"
feature_title: "Routing Signal Scorer Manual Pilots v1"
box: "tests + kanda_reasoner_app/routing_signal_scorer"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-routing-signal-scorer-manual-pilots-v1.md"
protected_paths:
  - "tests/test_routing_signal_scorer_manual_pilots_v1.py"
  - "kanda_reasoner_app/routing_signal_scorer"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "The manual pilot tests must validate diagnostic-only scoring behavior without changing final KANDA routing authority."
  - "The scorer may suggest signals and hooks, but the deterministic canon decides routing."
  - "The scorer must not output May proceed now decisions, route overrides, required prompt final decisions, or automatic prompt loading decisions."
  - "Simple explanation scenarios must remain Fast Path diagnostic signals without recommending pre_output_contract_gates."
  - "Patch delivery, terminal output, freeze-form JSON, freeze-hint sidecar, freeze-memory write, and external project root scenarios must recommend pre_output_contract_gates when high-risk signals are detected."
  - "RG-028 confirmation-gate bypass must remain high-risk."
  - "RG-029 stale startup filename/startup-delivery changes must be detected as startup-delivery and governed prompt-library sensitive."
  - "RG-030 simple explanation must not be over-routed by the scorer."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260616-routing-signal-scorer-manual-pilots-v1

## freeze identity

Freeze ID: `freeze-20260616-routing-signal-scorer-manual-pilots-v1`

Feature title: `Routing Signal Scorer Manual Pilots v1`

Date: `2026-06-16`

Primary box: `tests + kanda_reasoner_app/routing_signal_scorer`

Box type: `Regression Tests / Manual Pilot Matrix / Diagnostic Scorer Validation`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This milestone records behavior-class pilot coverage for the frozen diagnostic scorer. It proves the scorer can detect high-risk routing signals while remaining diagnostic-only and preserving Fast Path no-overrouting. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_manual_pilots_v1_patch.zip.

## validated files

- `tests/test_routing_signal_scorer_manual_pilots_v1.py`
- `kanda_reasoner_app/routing_signal_scorer/contract.py`

## generated files

- `routing_signal_scorer_manual_pilots_v1_patch.zip`

## protected paths

- `tests/test_routing_signal_scorer_manual_pilots_v1.py`
- `kanda_reasoner_app/routing_signal_scorer`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `The manual pilot tests must validate diagnostic-only scoring behavior without changing final KANDA routing authority.`
- `The scorer may suggest signals and hooks, but the deterministic canon decides routing.`
- `The scorer must not output May proceed now decisions, route overrides, required prompt final decisions, or automatic prompt loading decisions.`
- `Simple explanation scenarios must remain Fast Path diagnostic signals without recommending pre_output_contract_gates.`
- `Patch delivery, terminal output, freeze-form JSON, freeze-hint sidecar, freeze-memory write, and external project root scenarios must recommend pre_output_contract_gates when high-risk signals are detected.`
- `RG-028 confirmation-gate bypass must remain high-risk.`
- `RG-029 stale startup filename/startup-delivery changes must be detected as startup-delivery and governed prompt-library sensitive.`
- `RG-030 simple explanation must not be over-routed by the scorer.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_manual_pilots_v1
CONTRACT_TEST_OK: 12 manual-pilot diagnostic scorer scenarios passed, including Fast Path protection, patch/terminal/freeze hook recommendation, RG-028, RG-029, RG-030, and no-router-override behavior
SANDBOX_ROUTING_SIGNAL_SCORER_MANUAL_PILOTS_V1_VALIDATION_OK
```

## known warnings

This patch adds regression/manual-pilot tests only. It does not change the diagnostic scorer implementation, deterministic router behavior, startup delivery, or prompt-loading behavior. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer Manual Pilots v1. Human review is still required before Confirm and Write.

## planned next step

Install and validate the manual-pilot regression tests. If validation passes, freeze Routing Signal Scorer Manual Pilots v1 before considering an advisory scorer version.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T23:03:08Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
