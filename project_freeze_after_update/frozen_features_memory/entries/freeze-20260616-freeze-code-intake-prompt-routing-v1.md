---
freeze_id: "freeze-20260616-freeze-code-intake-prompt-routing-v1"
feature_title: "Freeze Code Intake Prompt Routing v1"
box: "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing + kanda_prompt_workspace/prompt_tools + first_AI_deliver + selected active project/project_freeze_after_update/freeze_hint_intake"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-freeze-code-intake-prompt-routing-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md"
  - "kanda_prompt_workspace/prompt_library/METADATA/freeze_code_intake_and_form_protocol.meta.json"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md"
  - "kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md"
  - "kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
  - "kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md"
  - "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
  - "kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "Request or apply freeze_code_intake_and_form_protocol whenever freezing code, freezing a validated feature, reviewing a freeze form, preparing a New Local Freeze Entry, or delivering a freeze-ready patch ZIP."
  - "Patch ZIPs intended to be freeze-ready must include root-level KANDA_FREEZE_HINT.json unless intentionally non-freezeable and explained."
  - "KANDA_FREEZE_HINT.json must describe the current feature, not an older heuristic feature."
  - "KANDA_FREEZE_HINT.json must include recognizer-friendly validation evidence after local validation passes, including VALIDATION OK: feature_id."
  - "Do not approve freeze forms that reuse stale feature titles or stale validation evidence."
  - "Freeze-intake state belongs under the selected active project root at project_freeze_after_update/freeze_hint_intake."
  - "Frozen memory belongs under the selected active project root at project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger."
  - "The startup paste file must include the freeze-code intake prompt hook."
  - "Do not turn this on-request protocol into a monolithic always-loaded specialist prompt."
  - "Preview Freeze Entry must remain read-only and must not write files."
  - "Confirm and Write must require explicit human confirmation before writing governed freeze memory."
  - "After a local freeze write, the AI startup freeze context must be refreshed."
  - "External AI review remains advanced/fallback, not the normal local freeze path."
superseded_by: null
---

# freeze-20260616-freeze-code-intake-prompt-routing-v1

## freeze identity

Freeze ID: `freeze-20260616-freeze-code-intake-prompt-routing-v1`

Feature title: `Freeze Code Intake Prompt Routing v1`

Date: `2026-06-16`

Primary box: `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing + kanda_prompt_workspace/prompt_tools + first_AI_deliver + selected active project/project_freeze_after_update/freeze_hint_intake`

Box type: `Prompt Library / Startup Routing Hook / Freeze Intake Protocol`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This feature ensures future AI chats use a dedicated freeze-code intake protocol whenever code or a validated feature needs freezing. It keeps the prompt on-request, adds a startup paste hook, requires freeze-ready patch ZIPs to carry current-feature KANDA_FREEZE_HINT.json metadata, and preserves multi-project freeze-intake ownership under the selected active project root. Source patch ZIP: freeze_code_intake_prompt_routing_v1_patch.zip.

## validated files

- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md`
- `kanda_prompt_workspace/prompt_library/METADATA/freeze_code_intake_and_form_protocol.meta.json`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md`
- `kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py`

## generated files

- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md`

## protected paths

- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/freeze_code_intake_and_form_protocol.md`
- `kanda_prompt_workspace/prompt_library/METADATA/freeze_code_intake_and_form_protocol.meta.json`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/_FOLDER_ASSIMILATION.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/prompt_navigation_index.json`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md`
- `kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `Request or apply freeze_code_intake_and_form_protocol whenever freezing code, freezing a validated feature, reviewing a freeze form, preparing a New Local Freeze Entry, or delivering a freeze-ready patch ZIP.`
- `Patch ZIPs intended to be freeze-ready must include root-level KANDA_FREEZE_HINT.json unless intentionally non-freezeable and explained.`
- `KANDA_FREEZE_HINT.json must describe the current feature, not an older heuristic feature.`
- `KANDA_FREEZE_HINT.json must include recognizer-friendly validation evidence after local validation passes, including VALIDATION OK: feature_id.`
- `Do not approve freeze forms that reuse stale feature titles or stale validation evidence.`
- `Freeze-intake state belongs under the selected active project root at project_freeze_after_update/freeze_hint_intake.`
- `Frozen memory belongs under the selected active project root at project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific freeze-intake state or frozen memory inside project_freeze_ledger.`
- `The startup paste file must include the freeze-code intake prompt hook.`
- `Do not turn this on-request protocol into a monolithic always-loaded specialist prompt.`
- `Preview Freeze Entry must remain read-only and must not write files.`
- `Confirm and Write must require explicit human confirmation before writing governed freeze memory.`
- `After a local freeze write, the AI startup freeze context must be refreshed.`
- `External AI review remains advanced/fallback, not the normal local freeze path.`

## validation evidence

```text
VALIDATION OK: freeze_code_intake_prompt_routing_v1
SANDBOX_FREEZE_CODE_INTAKE_PROMPT_ROUTING_VALIDATION_OK
STARTUP PROMPT REQUEST KERNEL CHECK
STATUS: IN_SYNC
freeze_code_intake_prompt_routing_v1 is installed and startup delivery is in sync.
```

## known warnings

This feature adds prompt-library and startup routing logic. It does not retroactively add KANDA_FREEZE_HINT.json to old patch ZIPs and does not freeze prior routing repairs by itself. Human review is still required before Confirm and Write.

## planned next step

Freeze Freeze Code Intake Prompt Routing v1 now. After this freeze is confirmed and startup freeze context refreshes, freeze Freeze Hint Sidecar Delivery Contract v1 if it is still pending.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T02:45:15Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
