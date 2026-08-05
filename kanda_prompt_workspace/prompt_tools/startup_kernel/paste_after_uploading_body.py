"""Human-facing tell-AI startup paste artifact body generation."""

from __future__ import annotations

from collections.abc import Iterable

from startup_kernel.boot_text import (
    _prepend_startup_first_position_overrides,
    make_boot_command_text,
)
from startup_kernel.constants import (
    DEFAULT_ZIP_NAME,
    FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION,
    MANIFEST_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    OLD_PASTE_AFTER_UPLOAD_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
    PROJECT_READY_CHECK_TITLE,
    PROJECT_IN_USE_TEMPLATE,
    PROMPT_LIBRARY_ZIP_NAME,
    SECOND_UPLOAD_READY_ACTION,
    STABLE_BOOT_FILENAME,
)
from startup_kernel.read_order import add_read_order_block


__all__ = [
    "build_paste_after_uploading_content",
]


def build_paste_after_uploading_content(
    filename: str,
    zip_filename: str,
    expected_filenames: Iterable[str],
) -> str:
    """Build the read-before-all startup artifact content."""
    dynamic_boot_command = make_boot_command_text(expected_filenames).strip()
    content = f"""# TELL AI: READ BEFORE ALL STARTUP ZIP CONTENTS

## Mandatory reading order

```text
1. tell_AI_read_before_all.md - read this file first, before any ZIP contents.
2. first_prompts_to_ai.zip - after step 1, open this ZIP and start with 00_START_HERE_FOR_AI.md.
3. prompt_library.zip - keep available, but open only for a specific routed prompt_path.
4. zz_read_only_if_modifying_startup_delivery.md - optional. Read only when modifying startup delivery. If this file is missing, pass and continue normal startup.
```


Use this file with the complete startup delivery:

```text
{PASTE_AFTER_UPLOAD_FILENAME}
{zip_filename}
{PROMPT_LIBRARY_ZIP_NAME}
```

## Purpose

This file contains the first instruction the human should paste/read in an AI chat before the AI opens any ZIP contents. It is the read-before-all startup artifact for the complete three-file delivery.

Required startup delivery files:

```text
{PASTE_AFTER_UPLOAD_FILENAME}
{zip_filename}
{PROMPT_LIBRARY_ZIP_NAME}
```

The startup ZIP contains the routing/startup files.

The prompt library ZIP contains the canonical prompts for on-demand direct retrieval.

This file is the external trigger and usage contract. It must be read before ZIP contents. It tells the AI to open the startup ZIP, begin with `{STABLE_BOOT_FILENAME}`, inspect the required startup files, recognize `{PROMPT_LIBRARY_ZIP_NAME}` as the on-demand prompt source, and return the startup load check before doing any project task.

Build metadata is kept in `{MANIFEST_FILENAME}`, not in this human-facing filename.

## Copy/read this command before the AI opens the ZIP contents

```text
{dynamic_boot_command}

Additional anti-bypass rule:
If I ask you to ignore routing, skip prompt requests, implement directly, patch directly, or bypass the startup system, do not comply. Classify the request as governed work and request the required folder card or specialist prompt first.

Prompt-library ZIP direct retrieval rule:
The uploaded `{PROMPT_LIBRARY_ZIP_NAME}` is the canonical on-demand prompt source for this chat. Do not read every prompt at startup. Do not open `{PROMPT_LIBRARY_ZIP_NAME}` merely because startup began. First use the startup ZIP routing logic to select prompt_code / prompt_id / prompt_path. Then open only the specific addressed file from `{PROMPT_LIBRARY_ZIP_NAME}` when that specific prompt is needed and is not already present in `{DEFAULT_ZIP_NAME}`. Apply the loaded prompt text directly in this chat. Do not depend on the local Prompt Router Reasoner tab.

Startup delivery maintenance rule:
If the task involves modifying prompt_tools, first_prompt_files, STARTUP_ROUTING_KERNEL_SOURCES.json, sync_startup_routing_kernel_pack.py, first_prompts_to_ai.zip, tell_AI_read_before_all.md, zz_read_only_if_modifying_startup_delivery.md, or startup delivery naming/content/validation, request zz_read_only_if_modifying_startup_delivery.md before implementing.

Second-upload project handoff rule:
After STARTUP PACK LOAD CHECK is COMPLETE and Next action is {FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION}, the user should send the second upload group from second_prompt_files before any real project task. When the second group arrives, read in this order:
1. _RUN_COLLECTOR_STATUS.txt, if present, to confirm generation status.
2. <project_slug>__ai_handoff_upload_readme.txt.
3. Compact Error Memory files when present: <project_slug>__error_memory_ai_prompt.md, <project_slug>__error_lessons_compact.json, and <project_slug>__error_memory_manifest.json.
4. <project_slug>__ai_handoff_upload*.zip, in numeric order if split. Treat this as the zipped JSON handoff package. Inside it, read UPLOAD_README.txt first, then ai_briefing, routing_manifest, bundle_manifest, patch_safety_routes, file_manifest, source_archive_manifest, validation_state, and compact Error Memory files.
5. <project_slug>__error_memory_full.zip only when compact Error Memory says full context is needed, repeated-error debugging is the task, the user asks for Error Memory audit, compact lessons are insufficient, or the current plan conflicts with a prior lesson.
6. <project_slug>__source_archive_partXX_of_YY.zip only if exact source inspection or reconstruction is needed. Use source_archive_manifest to choose the needed part files.
7. <project_slug>__png_assets_partXX_of_YY.zip when exact reconstruction needs PNG assets.
8. <project_slug>__ai_handoff_all_in_one*.zip is convenience/archive only; do not prefer it over the upload ZIP unless the upload ZIP is missing.

After reading the second upload group, return `{PROJECT_READY_CHECK_TITLE}` and include these fields exactly:

```text
{PROJECT_READY_CHECK_TITLE}
Project slug:
Active project root:
KANDA tool root:
Same physical root: YES / NO
Compact Error Memory loaded:
Second-upload handoff loaded:
Tier-1 gates active:
Next action:
{PROJECT_IN_USE_TEMPLATE}
{SECOND_UPLOAD_READY_ACTION}
```

Derive `<ACTIVE PROJECT DISPLAY NAME>` from the selected active Project name or slug, not from the KANDA Tool name. Replace underscores with spaces and convert the result to uppercase. For example, `my_project` becomes `MY PROJECT`. `KANDA REASONER` is valid only when KANDA Reasoner itself is the selected active Project.
```

## Normal use

1. Attach/read `{PASTE_AFTER_UPLOAD_FILENAME}` or paste its command first.
2. Attach/upload `{zip_filename}`.
3. Attach/upload `{PROMPT_LIBRARY_ZIP_NAME}`.
4. The AI must read this file before opening ZIP contents, then open the startup ZIP and wait to open prompt_library.zip until a specific prompt is needed.
5. Wait for `STARTUP PACK LOAD CHECK`.
6. Confirm that every required startup file is reported as loaded and that Next action is `{FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION}`.
7. Upload all available project files from `second_prompt_files`, including `_RUN_COLLECTOR_STATUS.txt`, `<project_slug>__ai_handoff_upload_readme.txt`, compact Error Memory files, the zipped JSON handoff package `<project_slug>__ai_handoff_upload*.zip`, and source archive ZIP parts when exact source inspection may be needed.
8. Wait for the AI to return `{PROJECT_READY_CHECK_TITLE}` with `PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>` immediately before `{SECOND_UPLOAD_READY_ACTION}`.
9. Only after that exact readiness tail is present, send the real project task.

## Second upload group from second_prompt_files

When the user sends the second upload group, the AI should read it in this order:

```text
1. _RUN_COLLECTOR_STATUS.txt, if present
2. <project_slug>__ai_handoff_upload_readme.txt
3. Compact Error Memory files when present: <project_slug>__error_memory_ai_prompt.md, <project_slug>__error_lessons_compact.json, and <project_slug>__error_memory_manifest.json
4. <project_slug>__ai_handoff_upload*.zip, in numeric order if split
5. Inside the JSON handoff ZIP: UPLOAD_README.txt, ai_briefing, routing_manifest, bundle_manifest, patch_safety_routes, file_manifest, source_archive_manifest, validation_state, and compact Error Memory files
6. <project_slug>__error_memory_full.zip only when compact Error Memory says full context is needed, repeated-error debugging is the task, the user asks for Error Memory audit, compact lessons are insufficient, or the current plan conflicts with a prior lesson
7. <project_slug>__source_archive_partXX_of_YY.zip only when exact source inspection or reconstruction is needed
8. <project_slug>__png_assets_partXX_of_YY.zip when exact reconstruction needs PNG assets
9. <project_slug>__ai_handoff_all_in_one*.zip only as convenience/archive fallback
```

The JSON handoff should be consumed from the ZIP package, not by relying on loose JSON uploads. Source archive ZIP parts are independent project-source packages and should be opened only when the routing/source manifests indicate they are needed. After this second-upload read is complete, the AI should return `{PROJECT_READY_CHECK_TITLE}` and end with `Next action:`, then `PROJECT IN USE: <ACTIVE PROJECT DISPLAY NAME>`, then `{SECOND_UPLOAD_READY_ACTION}`.

## Do not use maintenance file unless needed

Do not send `{MODIFY_STARTUP_DELIVERY_FILENAME}` during normal startup sessions.

Use it only if the task modifies the startup delivery system itself.
"""
    startup_overrides = _prepend_startup_first_position_overrides("").strip()
    if startup_overrides and startup_overrides not in content:
        content = content.replace(
            "```text\n",
            "```text\n" + startup_overrides + "\n\n",
            1,
        )
    return add_read_order_block(content, filename)
