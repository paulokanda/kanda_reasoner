# KANDA Startup Prompt Request Kernel Generator v3.0

This generator creates the human-facing startup delivery package for new AI chats.

## Box ownership

- `prompt_library/` owns canonical prompt source.
- `prompt_tools/` owns the generator and source map.
- `first_prompt_files/` owns generated human delivery artifacts.

Generated artifacts are never canonical source.

## Normal delivery

- `first_prompts_to_ai.zip`
- `prompt_library.zip`
- `tell_AI_read_before_all.md`

Use `zz_read_only_if_modifying_startup_delivery.md` only for startup-delivery maintenance.

## Required startup ZIP members

- `00_START_HERE_FOR_AI.md`
- `01_ai_prompt_request_canon.md`
- `02_prompt_navigation_index.md`
- `03_GROUP_ASSIMILATION_INDEX.md`
- `04_FOLDER_ASSIMILATION_CARDS_INDEX.md`
- `05_start_of_day_master_stack.md`
- `06_session_start_upload_checklist.md`
- `07_daily_patch_delivery_guardrails.md`
- `08_handoff_at_end_of_work.md`
- `09_patch_install_delivery_error_register.md (migrated; not generated)`
- `12_error_memory_ai_formulary_startup_canon.md`
- `13_durable_document_artifact_routing_canon.md`
- `14_project_tool_boundary_canon.md`
- `README_STARTUP_PROMPT_REQUEST_KERNEL.md`
- `STARTUP_PROMPT_REQUEST_KERNEL_MANIFEST.json`

Generated filename 09 is now a migrated conditional Class 05 slot and is not generated. Generated filenames 10 and 11 are retired compatibility slots. Load order is owned by `STARTUP_ROUTING_KERNEL_SOURCES.json`, not inferred from contiguous filename numbers.

`prompt_router_reasoner_startup_check` and `chatgpt_kanda_routing_choice_output_protocol` are on-request prompts and must not be placed in normal startup delivery.

## Required behavior

1. Read `tell_AI_read_before_all.md` first.
2. Open `00_START_HERE_FOR_AI.md` first inside the startup ZIP.
3. Read numbered members in source-map order.
4. Keep `prompt_library.zip` available for exact-path retrieval only.
5. Return `STARTUP PACK LOAD CHECK` and wait for the second upload group.
6. Return `PROJECT READY CHECK` ending with `Next action:`, `PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>`, and `WAIT_FOR_TASK` only after the selected Project handoff is loaded and the Tool Error Memory context status is reported. Derive the display name from the selected active Project, not the KANDA Tool; replace underscores with spaces and convert it to uppercase.

## Validation

Run Python compile when Python changed, generator dry run, sync, post-sync check, delivery-folder inspection, startup ZIP inspection, prompt-library ZIP and manifest inspection, and obsolete-reference scans.

Preserve `--check`, `--dry-run`, and `--sync` behavior.
