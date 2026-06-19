---
freeze_id: "freeze-20260616-phase-2-prompt-call-accuracy-routing-matrix-v1"
feature_title: "Phase 2 Prompt-Call Accuracy Routing Matrix v1"
box: "kanda_prompt_workspace startup routing, prompt-library governance, and Freeze Feature After Update routing behavior"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-phase-2-prompt-call-accuracy-routing-matrix-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_library"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
  - "project_freeze_after_update/freeze_hint_intake"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Fast Path must remain available for simple explanations, wording rewrites, and status interpretation tasks when there is no code, patch, prompt-library, startup, file, freeze-memory, or GUI behavior change."
  - "Governed prompt-library work must require prompt-authoring/audit/canon context, relevant folder cards or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes, metadata, and validation."
  - "Do not proceed from memory for governed prompt-library patches when required prompts, folder cards, or indexes are missing."
  - "Do not request all prompt files blindly"
  - "use selective context loading for the smallest sufficient governed context set."
  - "Startup delivery artifacts are generated outputs"
  - "do not edit first_prompts_to_ai.zip directly."
  - "paste_after_first_prompts_to_ai.md is the active startup paste file"
  - "paste_after_uploading_startup_zip.md is stale/deprecated."
  - "Startup source changes require source-map/sync workflow, regenerated artifacts, and validation."
  - "Freeze Feature After Update Preview must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "External AI review must remain optional/fallback/supporting, not a mandatory gate before local Confirm and Write."
  - "freeze_code_intake_and_form_protocol must remain on-request/routed, not always-loaded in every startup session."
  - "Freeze-ready patch ZIPs must include root-level KANDA_FREEZE_HINT.json, not docs/KANDA_FREEZE_HINT.json."
  - "KANDA_FREEZE_HINT.json validation evidence must be recognizer-friendly, such as VALIDATION OK: <feature_id>, CONTRACT_TEST_OK: ..., and STATUS: IN_SYNC when applicable."
  - "Strict freeze-form replies must contain exactly KANDA_FREEZE_FORM_JSON_BEGIN, one valid JSON object, and KANDA_FREEZE_FORM_JSON_END, with no markdown fences or extra explanation."
  - "Project-specific freeze memory belongs under the selected active project root at project_freeze_after_update/frozen_features_memory."
  - "Do not write project-specific frozen feature memory under project_freeze_ledger."
  - "For external active projects, write freeze memory under the external active project root, not under E:/kanda_reasoner."
  - "Patch ZIPs must contain only updated files required by the patch plus required sidecar metadata"
  - "do not package the whole project."
  - "Do not freeze newly delivered features until the patch is installed and post-install validation evidence is available."
  - "Stale exposure warnings after successful local freeze write mean exposed AI-send context may be stale"
  - "do not redo successful freeze entries just because exposure is stale."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
superseded_by: null
---

# freeze-20260616-phase-2-prompt-call-accuracy-routing-matrix-v1

## freeze identity

Freeze ID: `freeze-20260616-phase-2-prompt-call-accuracy-routing-matrix-v1`

Feature title: `Phase 2 Prompt-Call Accuracy Routing Matrix v1`

Date: `2026-06-16`

Primary box: `kanda_prompt_workspace startup routing, prompt-library governance, and Freeze Feature After Update routing behavior`

Box type: `Prompt Routing Validation / Manual Test Matrix / Freeze Milestone`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This freeze milestone records that the Phase 2 prompt-call accuracy routing matrix and Phase 2B extended matrix were completed successfully, covering Fast Path vs Routed Work Path, prompt-library governance, startup sync, freeze sidecar/intake, active-project placement, patch delivery, validation evidence, and anti-overrouting behavior. Freeze-intake data was loaded from project_freeze_after_update/freeze_hint_intake. Source freeze-intake ZIP: phase2_prompt_routing_tests_freeze_hint_v1.zip.

## validated files

- `None - this freeze records a manual prompt/routing validation milestone and does not validate changed project source files.`

## generated files

- `KANDA_FREEZE_HINT.json`
- `PHASE2_PROMPT_ROUTING_TESTS_SUMMARY.md`

## protected paths

- `kanda_prompt_workspace/prompt_library`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `project_freeze_after_update/freeze_hint_intake`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Fast Path must remain available for simple explanations, wording rewrites, and status interpretation tasks when there is no code, patch, prompt-library, startup, file, freeze-memory, or GUI behavior change.`
- `Governed prompt-library work must require prompt-authoring/audit/canon context, relevant folder cards or _FOLDER_ASSIMILATION, existing prompt-library assets/indexes, metadata, and validation.`
- `Do not proceed from memory for governed prompt-library patches when required prompts, folder cards, or indexes are missing.`
- `Do not request all prompt files blindly`
- `use selective context loading for the smallest sufficient governed context set.`
- `Startup delivery artifacts are generated outputs`
- `do not edit first_prompts_to_ai.zip directly.`
- `paste_after_first_prompts_to_ai.md is the active startup paste file`
- `paste_after_uploading_startup_zip.md is stale/deprecated.`
- `Startup source changes require source-map/sync workflow, regenerated artifacts, and validation.`
- `Freeze Feature After Update Preview must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `External AI review must remain optional/fallback/supporting, not a mandatory gate before local Confirm and Write.`
- `freeze_code_intake_and_form_protocol must remain on-request/routed, not always-loaded in every startup session.`
- `Freeze-ready patch ZIPs must include root-level KANDA_FREEZE_HINT.json, not docs/KANDA_FREEZE_HINT.json.`
- `KANDA_FREEZE_HINT.json validation evidence must be recognizer-friendly, such as VALIDATION OK: <feature_id>, CONTRACT_TEST_OK: ..., and STATUS: IN_SYNC when applicable.`
- `Strict freeze-form replies must contain exactly KANDA_FREEZE_FORM_JSON_BEGIN, one valid JSON object, and KANDA_FREEZE_FORM_JSON_END, with no markdown fences or extra explanation.`
- `Project-specific freeze memory belongs under the selected active project root at project_freeze_after_update/frozen_features_memory.`
- `Do not write project-specific frozen feature memory under project_freeze_ledger.`
- `For external active projects, write freeze memory under the external active project root, not under E:/kanda_reasoner.`
- `Patch ZIPs must contain only updated files required by the patch plus required sidecar metadata`
- `do not package the whole project.`
- `Do not freeze newly delivered features until the patch is installed and post-install validation evidence is available.`
- `Stale exposure warnings after successful local freeze write mean exposed AI-send context may be stale`
- `do not redo successful freeze entries just because exposure is stale.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`

## validation evidence

```text
VALIDATION OK: phase-2-prompt-call-accuracy-routing-matrix-v1
MANUAL_TEST_MATRIX_OK: 35/35 routing tests passed
PHASE_2_SMART_TEST_MATRIX_OK: 20/20 core routing tests passed
PHASE_2B_EXTENDED_TEST_MATRIX_OK: 15/15 extended routing tests passed
RETEST_OK: T20 stale exposure interpretation repaired and passed
NO_CODE_PATCH: this ZIP is freeze-intake metadata for a manual validation milestone, not an installable source-code patch
```

## known warnings

This is a freeze-intake metadata ZIP for a manual prompt/routing validation milestone. It is not an installable code patch and should not overwrite project source files. Use it only to populate the Freeze Feature After Update workflow for the milestone freeze. If the app reports STALE_EXPOSURE after writing, regenerate or reload fresh AI-send exposure rather than duplicating the freeze entry. Human review is still required before Confirm and Write.

## planned next step

Stage this ZIP where the Freeze Feature After Update workflow can scan it, create or preview the local freeze entry, then Confirm and Write only under the active project's project_freeze_after_update/frozen_features_memory after human review.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T03:31:16Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
