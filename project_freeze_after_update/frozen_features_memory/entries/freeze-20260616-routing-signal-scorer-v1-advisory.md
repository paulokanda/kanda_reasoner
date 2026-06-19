---
freeze_id: "freeze-20260616-routing-signal-scorer-v1-advisory"
feature_title: "Routing Signal Scorer v1 Advisory"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-routing-signal-scorer-v1-advisory.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "tests/test_routing_signal_scorer_v1_advisory.py"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Routing Signal Scorer advisory mode may suggest likely route families, hooks, and caution flags only."
  - "The advisory must remain non-authoritative and must not replace deterministic KANDA routing."
  - "The advisory must not decide May proceed now."
  - "The advisory must not output final required prompts/groups."
  - "The advisory must not auto-load prompts."
  - "The advisory must not override the router canon."
  - "The canon decides final route, required prompts, missing context, and whether work may proceed."
  - "The diagnostic scorer must continue to protect Fast Path simple explanation scenarios from over-routing."
  - "High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios should recommend pre_output_contract_gates."
  - "Prompt-library and startup-delivery scenarios should be flagged as governed hints, not final route decisions."
  - "Confirmation-gate bypass attempts must be flagged as caution risks."
  - "Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260616-routing-signal-scorer-v1-advisory

## freeze identity

Freeze ID: `freeze-20260616-routing-signal-scorer-v1-advisory`

Feature title: `Routing Signal Scorer v1 Advisory`

Date: `2026-06-16`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `Diagnostic Scorer Advisory Layer / Prompt-Call Accuracy Support`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This evolves the frozen diagnostic scorer by adding an advisory wrapper that converts diagnostic signals into non-authoritative route-family suggestions and caution flags. It preserves the rule: the scorer may suggest, the canon decides. Source patch ZIP: routing_signal_scorer_v1_advisory_patch.zip. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v1_advisory_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v1_advisory.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `tests/test_routing_signal_scorer_v1_advisory.py`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Routing Signal Scorer advisory mode may suggest likely route families, hooks, and caution flags only.`
- `The advisory must remain non-authoritative and must not replace deterministic KANDA routing.`
- `The advisory must not decide May proceed now.`
- `The advisory must not output final required prompts/groups.`
- `The advisory must not auto-load prompts.`
- `The advisory must not override the router canon.`
- `The canon decides final route, required prompts, missing context, and whether work may proceed.`
- `The diagnostic scorer must continue to protect Fast Path simple explanation scenarios from over-routing.`
- `High-risk patch, terminal, freeze JSON, freeze sidecar, freeze memory, and external-project-root scenarios should recommend pre_output_contract_gates.`
- `Prompt-library and startup-delivery scenarios should be flagged as governed hints, not final route decisions.`
- `Confirmation-gate bypass attempts must be flagged as caution risks.`
- `Project-specific freeze-intake state must remain under project_freeze_after_update/freeze_hint_intake.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v1_advisory
CONTRACT_TEST_OK: advisory-only route-family suggestions, caution flags, hook recommendations, diagnostic wrapping, Fast Path protection, and no-router-override behavior validated
SANDBOX_ROUTING_SIGNAL_SCORER_V1_ADVISORY_VALIDATION_OK
```

## known warnings

This patch adds advisory recommendations only. It does not make the scorer a final router, does not add ML/embeddings, does not update startup delivery, and does not auto-load prompts. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v1 Advisory. Human review is still required before Confirm and Write.

## planned next step

Install and validate Routing Signal Scorer v1 Advisory, then freeze it before considering any future similarity or ML-assisted scorer version.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T23:09:14Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
