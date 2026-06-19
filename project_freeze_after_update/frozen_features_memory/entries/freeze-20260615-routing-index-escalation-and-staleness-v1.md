---
freeze_id: "freeze-20260615-routing-index-escalation-and-staleness-v1"
feature_title: "Routing Index Escalation and Startup Staleness v1"
box: "kanda_prompt_workspace/prompt_library/ROUTING + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup delivery"
status: "frozen"
date: "2026-06-15"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260615-routing-index-escalation-and-staleness-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md"
  - "kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/session_start_upload_checklist.md"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
do_not_touch_summary:
  - "Keep the routing-index escalation order explicit: GROUP_ASSIMILATION_INDEX first, FOLDER_ASSIMILATION_CARDS_INDEX only after broad group routing narrows the task, and prompt_navigation_index when exact prompt file/path/ID selection or verification is needed."
  - "Preserve ROUTING_INDEX_CONFLICT behavior when routing indexes disagree; do not let the AI silently choose one index over another for governed work."
  - "Keep startup kernel staleness as a warning/review signal, not an automatic startup failure."
  - "Do not auto-repair, silently regenerate, or mutate startup delivery or freeze memory merely because STARTUP_KERNEL_STALENESS_REVIEW is flagged."
  - "Do not inject full freeze memory into normal startup; keep compact active freeze context plus on-demand full freeze exposure."
  - "Do not condense the startup kernel, remove STARTUP PACK LOAD CHECK, remove paste_after_first_prompts_to_ai.md, create a resolver map, build a dispatcher, or create a Phase 2 JSON validator as part of this frozen behavior."
  - "Future routing logic updates must preserve startup delivery sync and update first_prompts_to_ai.zip through the governed startup sync process."
superseded_by: null
---

# freeze-20260615-routing-index-escalation-and-staleness-v1

## freeze identity

Freeze ID: `freeze-20260615-routing-index-escalation-and-staleness-v1`

Feature title: `Routing Index Escalation and Startup Staleness v1`

Date: `2026-06-15`

Primary box: `kanda_prompt_workspace/prompt_library/ROUTING + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup delivery`

Box type: `Prompt Routing / Startup Session Guardrail`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This freeze captures the validated routing-index escalation and startup-kernel staleness awareness update. It preserves the current modular startup kernel while clarifying how the AI should move between group-level routing, folder-card routing, and exact prompt-file routing. It also adds a non-blocking startup-kernel staleness review warning so newer freeze-memory entries can trigger review without silently failing or mutating startup delivery.

## validated files

- `kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/session_start_upload_checklist.md`

## generated files

- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`

## protected paths

- `kanda_prompt_workspace/prompt_library/ROUTING/GROUP_ASSIMILATION_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ROUTING/FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_navigation_index.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/session_start_upload_checklist.md`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`


## validated behavior

- `GROUP_ASSIMILATION_INDEX.md` now states the first routing level for broad group selection.
- `FOLDER_ASSIMILATION_CARDS_INDEX.md` now states it should be used only after group routing narrows the task and the exact folder/card remains ambiguous.
- `prompt_navigation_index.md` now states it should be used when exact prompt file, prompt ID, companion prompt, path, or current route must be selected or verified.
- All three routing index layers include `ROUTING_INDEX_CONFLICT` behavior for disagreements.
- `session_start_upload_checklist.md` includes `STARTUP_KERNEL_STALENESS_REVIEW` as a non-blocking warning/review signal.
- Startup delivery regenerated successfully and remained `STATUS: IN_SYNC`.

## validation evidence

Human pasted validation evidence:

```text
STARTUP PROMPT REQUEST KERNEL CHECK
Workspace root: E:\kanda_reasoner\kanda_prompt_workspace
Delivery directory: E:\kanda_reasoner\kanda_prompt_workspace\first_AI_deliver
Active project root for freeze context: E:\kanda_reasoner

STATUS: IN_SYNC
ZIP checked: first_prompts_to_ai.zip
Paste-after-uploading file: paste_after_first_prompts_to_ai.md
Startup delivery maintenance file: paste_if_modify_startup_delivery.md
Manifest generated at: 2026-06-16T00:09:06.926055Z

VALIDATION OK: routing_index_escalation_and_staleness_v1

VALIDATION OK
routing_index_escalation_and_staleness_v1 is installed and startup delivery is in sync.
```

## do-not-regress rules

- Keep the routing-index escalation order explicit: GROUP_ASSIMILATION_INDEX first, FOLDER_ASSIMILATION_CARDS_INDEX only after broad group routing narrows the task, and prompt_navigation_index when exact prompt file/path/ID selection or verification is needed.
- Preserve ROUTING_INDEX_CONFLICT behavior when routing indexes disagree; do not let the AI silently choose one index over another for governed work.
- Keep startup kernel staleness as a warning/review signal, not an automatic startup failure.
- Do not auto-repair, silently regenerate, or mutate startup delivery or freeze memory merely because STARTUP_KERNEL_STALENESS_REVIEW is flagged.
- Do not inject full freeze memory into normal startup; keep compact active freeze context plus on-demand full freeze exposure.
- Do not condense the startup kernel, remove STARTUP PACK LOAD CHECK, remove paste_after_first_prompts_to_ai.md, create a resolver map, build a dispatcher, or create a Phase 2 JSON validator as part of this frozen behavior.
- Future routing logic updates must preserve startup delivery sync and update first_prompts_to_ai.zip through the governed startup sync process.


## next allowed step

The next roadmap step may be `phase2_conditional_context_rubric_v1_patch`, implemented as a separate governed patch. Do not bundle Phase 2 rubric changes, routing failure log creation, resolver map creation, dispatcher work, JSON validator work, or startup condensation into this frozen baseline.
