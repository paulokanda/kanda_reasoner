---
freeze_id: "freeze-20260615-phase2-conditional-context-rubric-v1"
feature_title: "Phase 2 Conditional Context Rubric v1"
box: "kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup delivery"
status: "frozen"
date: "2026-06-15"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260615-phase2-conditional-context-rubric-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
do_not_touch_summary:
  - "Keep Conditional required context as a first-class Phase 2 prompt-call accuracy criterion; do not hide conditional-required context inside Recommended."
  - "Preserve the required-IF examples for Python source changes, startup delivery changes, and frozen/protected behavior changes."
  - "Keep Estimated context load as small / medium / large guidance to discourage over-requesting while preserving safety."
  - "Preserve the practical request-size guidance: normally up to 8 required prompts/groups and up to 5 recommended prompts/groups unless a larger package is justified."
  - "Keep Phase 2 focused on manual pilots and rubric-guided evaluation; do not create JSON expected outputs, validators, resolver maps, dispatchers, or startup condensation as part of this frozen behavior. Do not create JSON expected outputs, validators, resolver maps, dispatchers, or startup condensation inside this frozen baseline."
  - "Future Phase 2 automation must be built only after additional manual pilots demonstrate stable prompt-call behavior."
  - "Future routing updates must preserve startup delivery sync and update first_prompts_to_ai.zip through the governed startup sync process."
superseded_by: null
---

# freeze-20260615-phase2-conditional-context-rubric-v1

## freeze identity

Freeze ID: `freeze-20260615-phase2-conditional-context-rubric-v1`

Feature title: `Phase 2 Conditional Context Rubric v1`

Date: `2026-06-15`

Primary box: `kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY + kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation + startup delivery`

Box type: `Prompt-Call Accuracy Rubric / Startup Prompt Request Canon`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This freeze captures the validated Phase 2 prompt-call accuracy rubric update. It makes conditional required context first-class, adds scoring for required-IF-true context, adds `Estimated context load: small / medium / large` to routing guidance, and adds practical caps for normal required and recommended prompt/group requests. The purpose is to improve prompt-call precision while avoiding over-requesting and without prematurely creating JSON schemas, validators, resolver maps, dispatchers, or startup condensation.

## validated files

- `kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md`

## generated files

- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`

## protected paths

- `kanda_prompt_workspace/prompt_library/ROUTING_TESTS/PHASE_2_PROMPT_CALL_ACCURACY/phase2_prompt_call_rubric.md`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/ai_prompt_request_canon.md`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`


## validated behavior

- The Phase 2 rubric now includes `Conditional required context` as a first-class category.
- Conditional-required context must not be hidden inside Recommended.
- The rubric includes examples where `08_python_engineering_core` is required IF Python source code, generator code, validation code, or install logic may be modified.
- The rubric includes `paste_if_modify_startup_delivery.md` as required IF startup delivery, startup ZIP generation, source maps, first_AI_deliver, or startup naming may be modified.
- The rubric includes active project freeze context as required IF frozen behavior, protected paths, freeze workflow, project memory, or governance artifacts may be touched.
- The rubric now scores conditional context handling as PASS / PARTIAL / FAIL.
- The prompt request canon now includes `Estimated context load:` guidance.
- The prompt request canon now reminds the AI to request the smallest safe context package, not the largest possible context package.
- Practical over-request guidance is installed: normally up to 8 required prompts/groups and up to 5 recommended prompts/groups unless the larger package is explicitly justified.
- No Phase 2 JSON expected outputs, Phase 2 validator, resolver map, dispatcher, or startup condensation was created.
- Startup delivery regenerated successfully and remained `STATUS: IN_SYNC`.

## validation evidence

Human pasted validation evidence:

```text
STARTUP PROMPT REQUEST KERNEL CHECK
Workspace root: E:\kanda_reasoner\kanda_prompt_workspace
Delivery directory: E:\kanda_reasoner\kanda_prompt_workspaceirst_AI_deliver
Active project root for freeze context: E:\kanda_reasoner

STATUS: IN_SYNC
ZIP checked: first_prompts_to_ai.zip
Paste-after-uploading file: paste_after_first_prompts_to_ai.md
Startup delivery maintenance file: paste_if_modify_startup_delivery.md
Manifest generated at: 2026-06-16T00:17:28.926657Z

VALIDATION OK: phase2_conditional_context_rubric_v1

VALIDATION OK
phase2_conditional_context_rubric_v1 is installed and startup delivery is in sync.
```

## do-not-regress rules

- Keep Conditional required context as a first-class Phase 2 prompt-call accuracy criterion; do not hide conditional-required context inside Recommended.
- Preserve the required-IF examples for Python source changes, startup delivery changes, and frozen/protected behavior changes.
- Keep Estimated context load as small / medium / large guidance to discourage over-requesting while preserving safety.
- Preserve the practical request-size guidance: normally up to 8 required prompts/groups and up to 5 recommended prompts/groups unless a larger package is justified.
- Keep Phase 2 focused on manual pilots and rubric-guided evaluation; do not create JSON expected outputs, validators, resolver maps, dispatchers, or startup condensation as part of this frozen behavior. Do not create JSON expected outputs, validators, resolver maps, dispatchers, or startup condensation inside this frozen baseline.
- Future Phase 2 automation must be built only after additional manual pilots demonstrate stable prompt-call behavior.
- Future routing updates must preserve startup delivery sync and update first_prompts_to_ai.zip through the governed startup sync process.


## next allowed step

The next roadmap step may be additional Phase 2 manual pilots or a lightweight routing failure log, implemented as separate governed patches only if needed. Do not bundle JSON schema work, validator work, resolver map creation, dispatcher work, or startup condensation into this frozen baseline.
