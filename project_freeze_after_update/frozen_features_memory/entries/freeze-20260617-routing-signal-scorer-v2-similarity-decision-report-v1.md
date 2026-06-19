---
freeze_id: "freeze-20260617-routing-signal-scorer-v2-similarity-decision-report-v1"
feature_title: "Routing Signal Scorer v2 Similarity Decision Report v1"
box: "kanda_reasoner_app/routing_signal_scorer + tests"
status: "frozen"
date: "2026-06-17"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260617-routing-signal-scorer-v2-similarity-decision-report-v1.md"
protected_paths:
  - "kanda_reasoner_app/routing_signal_scorer"
  - "tests/test_routing_signal_scorer_v2_similarity_decision_report.py"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Decision report is human-readable audit output only."
  - "Decision report must not make final route, May proceed now, required prompt, or prompt-loading decisions."
  - "Similarity remains advisory-only and deterministic lexical runtime-lite."
  - "High similarity remains non-authoritative."
  - "Low similarity remains visible but not promoted."
  - "Rule-based diagnostic hooks remain independent of similarity matches."
  - "Do not add embeddings, TF-IDF dependency, vector store, self-learning, or cross-project memory."
  - "Canon still decides final route."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260617-routing-signal-scorer-v2-similarity-decision-report-v1

## freeze identity

Freeze ID: `freeze-20260617-routing-signal-scorer-v2-similarity-decision-report-v1`

Feature title: `Routing Signal Scorer v2 Similarity Decision Report v1`

Date: `2026-06-17`

Primary box: `kanda_reasoner_app/routing_signal_scorer + tests`

Box type: `runtime-lite advisory explainability extension`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

Adds a compact human-readable decision report to runtime-lite similarity advisory output so logs/UI can audit the top match, score, threshold level, route-family suggestion eligibility, advisory-only reason, and rule-hook independence without changing routing authority. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source patch ZIP: routing_signal_scorer_v2_similarity_decision_report_v1_patch.zip.

## validated files

- `kanda_reasoner_app/routing_signal_scorer/contract.py`
- `kanda_reasoner_app/routing_signal_scorer/__init__.py`
- `kanda_reasoner_app/routing_signal_scorer/box_manifest.json`
- `tests/test_routing_signal_scorer_v2_similarity_decision_report.py`

## generated files

- None recorded.

## protected paths

- `kanda_reasoner_app/routing_signal_scorer`
- `tests/test_routing_signal_scorer_v2_similarity_decision_report.py`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Decision report is human-readable audit output only.`
- `Decision report must not make final route, May proceed now, required prompt, or prompt-loading decisions.`
- `Similarity remains advisory-only and deterministic lexical runtime-lite.`
- `High similarity remains non-authoritative.`
- `Low similarity remains visible but not promoted.`
- `Rule-based diagnostic hooks remain independent of similarity matches.`
- `Do not add embeddings, TF-IDF dependency, vector store, self-learning, or cross-project memory.`
- `Canon still decides final route.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: routing_signal_scorer_v2_similarity_decision_report_v1
CONTRACT_TEST_OK: runtime-lite similarity decision report exposes compact human-readable top-match, score, threshold-level, route-eligibility, advisory-only, and rule-hook-independence lines while preserving no-authority, forbidden stronger-ML absence, and prior routing scorer regressions
SANDBOX_ROUTING_SIGNAL_SCORER_V2_SIMILARITY_DECISION_REPORT_V1_VALIDATION_OK
```

## known warnings

Starter draft only. Replace placeholders with the current validated feature data. No validation evidence has been inferred or invented. Auto-filled from saved KANDA_FREEZE_HINT.json intake data for Routing Signal Scorer v2 Similarity Decision Report v1. Human review is still required before Confirm and Write.

## planned next step

Replace placeholders with current feature evidence, then Preview Freeze Entry before Confirm and Write.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-17T02:07:19Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
