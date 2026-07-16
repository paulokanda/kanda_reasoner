# KANDA Startup Prompt Request Kernel Generator v2.7

This generator creates the human-facing startup delivery package for new AI chats.

## Required generated delivery

```text
first_prompt_files/
  first_prompts_to_ai.zip
  tell_AI_read_before_all.md
  zz_read_only_if_modifying_startup_delivery.md
```

## Required ZIP contract

Inside `first_prompts_to_ai.zip`:

```text
00_START_HERE_FOR_AI.md
01_ai_prompt_request_canon.md
02_prompt_navigation_index.md
03_GROUP_ASSIMILATION_INDEX.md
04_FOLDER_ASSIMILATION_CARDS_INDEX.md
05_start_of_day_master_stack.md
06_session_start_upload_checklist.md
07_daily_patch_delivery_guardrails.md
08_handoff_at_end_of_work.md
09_patch_install_delivery_error_register.md
10_prompt_router_reasoner_startup_check.md
11_chatgpt_kanda_routing_choice_output_protocol.md
12_error_memory_ai_formulary_startup_canon.md
13_durable_document_artifact_routing_canon.md
README_STARTUP_PROMPT_REQUEST_KERNEL.md
STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json
```

## Daily patch delivery guardrail

The startup ZIP must include:

```text
07_daily_patch_delivery_guardrails.md
```

This file is an always-startup guardrail. It tells the receiving AI how to handle patch ZIP delivery, root cleanliness, terminal hygiene, and installer ZIP staging. In particular, generated installer commands must derive the project drive from `PROJECT_ROOT`, create `<drive>:\<project_in_use_name>_delete_after_daily_work\`, look first for the explicit expected ZIP at the project drive root, stage it into that folder, delete the root-drive ZIP copy after successful staging, install only from the staged ZIP, and stop with `zip is not in root of drive:\ where project is` when the expected ZIP cannot be found. The old generic Downloads/Desktop-first installer search pattern is forbidden for governed KANDA patch installs.

## End-of-work handoff guardrail

The startup ZIP must include:

```text
08_handoff_at_end_of_work.md
```

This file is an always-startup guardrail. It tells the receiving AI that when project work is active and the user says phrases such as `lets take a break`, `lets stop now`, `pause here`, `stop for today`, `chat is huge`, or `we continue later`, the AI must produce a complete contextualized handoff instead of a short goodbye.

The handoff must preserve completed work, validation evidence, freeze state, current artifact names, stale names, files changed, files not to modify, and the exact next safe action for the next AI chat.

## Human startup workflow

1. Upload `first_prompt_files/first_prompts_to_ai.zip` to the AI chat.
2. Open `first_prompt_files/tell_AI_read_before_all.md`.
3. Paste its command into the AI chat.
4. Wait for `STARTUP PACK LOAD CHECK`.
5. Confirm `00`, `01` to `13`, `README`, and `MANIFEST` are all loaded.
6. Only then send the real task.

## Startup delivery maintenance workflow

Use `first_prompt_files/zz_read_only_if_modifying_startup_delivery.md` only when asking an AI to modify the startup delivery system itself.

Do not use the maintenance file for normal startup sessions.

## Required boot behavior

The stable boot file inside the ZIP must be named:

```text
00_START_HERE_FOR_AI.md
```

The boot command in `tell_AI_read_before_all.md` must require the receiving AI to inspect and report:

```text
0. 00_START_HERE_FOR_AI.md
1. 01_ai_prompt_request_canon.md
2. 02_prompt_navigation_index.md
3. 03_GROUP_ASSIMILATION_INDEX.md
4. 04_FOLDER_ASSIMILATION_CARDS_INDEX.md
5. 05_start_of_day_master_stack.md
6. 06_session_start_upload_checklist.md
7. 07_daily_patch_delivery_guardrails.md
8. 08_handoff_at_end_of_work.md
9. 09_patch_install_delivery_error_register.md
10. 10_prompt_router_reasoner_startup_check.md
11. 11_chatgpt_kanda_routing_choice_output_protocol.md
12. 12_error_memory_ai_formulary_startup_canon.md
13. 13_durable_document_artifact_routing_canon.md
14. README_STARTUP_PROMPT_REQUEST_KERNEL.md
15. STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json
```

## Preserved architecture

- `prompt_library/` is canonical source.
- `prompt_tools/STARTUP_ROUTING_KERNEL_SOURCES.json` remains the source map.
- `prompt_tools/sync_startup_routing_kernel_pack.py` remains the generator.
- `first_prompt_files/` remains human delivery output.
- `07_daily_patch_delivery_guardrails.md` is a generated startup copy of the canonical daily delivery guardrail.
- `08_handoff_at_end_of_work.md` is a generated startup copy of the canonical end-of-work handoff guardrail.
- `13_durable_document_artifact_routing_canon.md` is a generated startup copy of the durable documentation and validation-evidence routing canon.
- Generated delivery files are not canonical source.

## Obsolete delivery names

Older human-facing delivery filenames were retired during the startup-delivery rename.

They should not remain in `first_prompt_files/` after sync, and active instructions should use only:

```text
tell_AI_read_before_all.md
zz_read_only_if_modifying_startup_delivery.md
```

The retired name `paste_after_uploading_startup_zip.md` may appear only as historical context or stale-name rejection evidence. It must not be treated as the current active startup paste file.
