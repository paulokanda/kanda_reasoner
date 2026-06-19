---
freeze_id: "freeze-20260616-rg-029-startup-stale-filename-override-v1"
feature_title: "RG-029 Startup Stale Filename Override v1"
box: "kanda_prompt_workspace/startup_routing_kernel + kanda_prompt_workspace/first_AI_deliver + kanda_prompt_workspace/prompt_tools"
status: "frozen"
date: "2026-06-16"
entry: "project_freeze_after_update/frozen_features_memory/entries/freeze-20260616-rg-029-startup-stale-filename-override-v1.md"
protected_paths:
  - "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py"
  - "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
  - "kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md"
  - "kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md"
  - "kanda_prompt_workspace/first_AI_deliver/STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json"
  - "kanda_prompt_workspace/startup_routing_kernel/STARTUP_ROUTING_KERNEL_SOURCES.json"
  - "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/cooperative_implementation_methodology.md"
  - "project_freeze_after_update/frozen_features_memory"
do_not_touch_summary:
  - "The RG-029 startup-delivery stale-filename override must remain active in the startup boot context."
  - "When a request names paste_after_uploading_startup_zip.md for active startup delivery, the AI must explicitly identify it as stale/deprecated."
  - "The active human-facing startup paste file must remain paste_after_first_prompts_to_ai.md unless a separate governed startup-delivery change is approved and validated."
  - "Startup delivery changes must request paste_if_modify_startup_delivery.md before implementation."
  - "Startup delivery changes must request sync_startup_routing_kernel_pack.py before implementation."
  - "Startup delivery changes must request STARTUP_ROUTING_KERNEL_SOURCES.json before implementation."
  - "Startup delivery changes must request current first_AI_deliver artifacts, including first_prompts_to_ai.zip and paste_after_first_prompts_to_ai.md."
  - "The AI must not directly edit stale or generated startup paste files as source of truth."
  - "cooperative_implementation_methodology must remain a frozen on-request prompt and must not be auto-loaded every day through the startup boot sequence unless a separate governed startup-delivery change is explicitly approved and validated."
  - "For the RG-029 scenario, the AI must classify the task as Routed Work Path."
  - "For the RG-029 scenario, Estimated context load must be large."
  - "For the RG-029 scenario, May proceed now must be NO."
  - "Do not treat automatic loading of cooperative_implementation_methodology as a harmless generated-file edit."
  - "Do not create Phase 2 JSON expected outputs, validators, resolver maps, prompt dispatchers, or startup condensation as part of this freeze."
  - "Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory."
  - "Do not store project-specific frozen memory inside project_freeze_ledger."
superseded_by: null
---

# freeze-20260616-rg-029-startup-stale-filename-override-v1

## freeze identity

Freeze ID: `freeze-20260616-rg-029-startup-stale-filename-override-v1`

Feature title: `RG-029 Startup Stale Filename Override v1`

Date: `2026-06-16`

Primary box: `kanda_prompt_workspace/startup_routing_kernel + kanda_prompt_workspace/first_AI_deliver + kanda_prompt_workspace/prompt_tools`

Box type: `Startup Delivery / Routing Guardrail / Prompt-Call Accuracy`

Status: `frozen after explicit human confirmation and validation evidence`

## summary

This freeze preserves the current startup-delivery rule that paste_after_uploading_startup_zip.md is stale/deprecated and paste_after_first_prompts_to_ai.md is the active human-facing startup paste file. It also protects the decision that cooperative_implementation_methodology remains frozen as an on-request prompt rather than becoming an always-loaded startup prompt.

## validated files

- `kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`

## generated files

- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md`
- `kanda_prompt_workspace/first_AI_deliver/STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`

## protected paths

- `kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py`
- `kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip`
- `kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md`
- `kanda_prompt_workspace/first_AI_deliver/paste_if_modify_startup_delivery.md`
- `kanda_prompt_workspace/first_AI_deliver/STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`
- `kanda_prompt_workspace/startup_routing_kernel/STARTUP_ROUTING_KERNEL_SOURCES.json`
- `kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/cooperative_implementation_methodology.md`
- `project_freeze_after_update/frozen_features_memory`

## do-not-regress rules

- `The RG-029 startup-delivery stale-filename override must remain active in the startup boot context.`
- `When a request names paste_after_uploading_startup_zip.md for active startup delivery, the AI must explicitly identify it as stale/deprecated.`
- `The active human-facing startup paste file must remain paste_after_first_prompts_to_ai.md unless a separate governed startup-delivery change is approved and validated.`
- `Startup delivery changes must request paste_if_modify_startup_delivery.md before implementation.`
- `Startup delivery changes must request sync_startup_routing_kernel_pack.py before implementation.`
- `Startup delivery changes must request STARTUP_ROUTING_KERNEL_SOURCES.json before implementation.`
- `Startup delivery changes must request current first_AI_deliver artifacts, including first_prompts_to_ai.zip and paste_after_first_prompts_to_ai.md.`
- `The AI must not directly edit stale or generated startup paste files as source of truth.`
- `cooperative_implementation_methodology must remain a frozen on-request prompt and must not be auto-loaded every day through the startup boot sequence unless a separate governed startup-delivery change is explicitly approved and validated.`
- `For the RG-029 scenario, the AI must classify the task as Routed Work Path.`
- `For the RG-029 scenario, Estimated context load must be large.`
- `For the RG-029 scenario, May proceed now must be NO.`
- `Do not treat automatic loading of cooperative_implementation_methodology as a harmless generated-file edit.`
- `Do not create Phase 2 JSON expected outputs, validators, resolver maps, prompt dispatchers, or startup condensation as part of this freeze.`
- `Project-specific frozen memory must remain under project_freeze_after_update/frozen_features_memory.`
- `Do not store project-specific frozen memory inside project_freeze_ledger.`

## validation evidence

```text
STARTUP PROMPT REQUEST KERNEL CHECK
STATUS: IN_SYNC
Manifest generated at: 2026-06-16T01:10:55.628644Z
VALIDATION OK: rg029_startup_stale_filename_override_v1
rg029_startup_stale_filename_override_v1 is installed and startup delivery is in sync.
RG-029 retest: PASS / CLOSED.
RG-029 retest confirmed stale filename detection, active startup paste filename recognition, required startup maintenance context, on-request methodology prompt protection, Estimated context load: large, and May proceed now: NO.
```

## known warnings

This freeze protects the RG-029 startup stale-filename routing behavior only. It does not freeze RG-030, create a routing failure log, create JSON expected outputs, create validators, create a resolver map, build a dispatcher, or condense the startup kernel.

## planned next step

After freezing RG-029, continue with the next Phase 2 manual pilot: RG-030 Fast Path no-overrouting test.

## local freeze writer provenance

Generated by `local_freeze_writer_engine_v1` at `2026-06-16T01:25:00Z`.

This entry was created locally for the selected active project. The reusable `project_freeze_ledger` engine remains blueprint logic only and is not the owner of this project-specific memory.
