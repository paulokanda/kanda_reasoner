"""Introductory 00_START_HERE_FOR_AI.md body section."""

from __future__ import annotations

from startup_kernel.constants import (
    FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION,
    MANIFEST_FILENAME,
    PROJECT_READY_CHECK_TITLE,
    README_FILENAME,
    SECOND_UPLOAD_READY_ACTION,
    STABLE_BOOT_FILENAME,
    PASTE_AFTER_UPLOAD_FILENAME,
)


__all__ = [
    "make_start_here_intro_section",
]


def make_start_here_intro_section(
    date_cert: str,
    generated_at: str,
    numbered_list: str,
    required_report_list: str,
    active_bridge_report: str,
    expected_count: int,
) -> str:
    """Return the first half of the stable startup boot file body."""
    return f"""# 00_START_HERE_FOR_AI.md

Version: 1.1
Status: stable startup boot file
Role: first file to read inside the startup prompt request kernel
Scope: startup routing only
Do not use as: implementation prompt, patch prompt, governance update prompt, or full project canon

Certificate: `{date_cert}`
Generated: `{generated_at}`

## Purpose

This file is the first boot file for a new AI work session.

Its job is to make the AI inspect the startup prompt request kernel, confirm which required startup files are loaded, understand routing behavior, and wait for the user's real task.

This file must not solve the project task.

This file must not create code.

This file must not modify files.

This file must not infer missing specialist prompts from memory.

## Startup package expected files

The startup pack should contain these files at the ZIP root:

0. {STABLE_BOOT_FILENAME}
{numbered_list}
{expected_count + 1}. {README_FILENAME}
{expected_count + 2}. {MANIFEST_FILENAME}

If a file is missing, report it as missing.

Do not pretend it was loaded.

## Required first action

Read this file first.

Then inspect every numbered file in the startup pack in numeric order.

Also inspect:

```text
{README_FILENAME}
{MANIFEST_FILENAME}
```

After inspection, return only the startup load check.

Do not answer any project task before the startup load check.

Do not summarize the whole project.

Do not implement anything.

Do not create a patch.

Do not create a ZIP.

Do not request specialist prompts yet unless the startup pack itself is incomplete.

## Required startup load check output

Return exactly this structure:

```text
STARTUP PACK LOAD CHECK

Files recognized:
{required_report_list}

Beginning-of-day active bridges:
{active_bridge_report}

Startup status:
COMPLETE / INCOMPLETE

Routing behavior:
[one paragraph explaining how you will use Fast Path, Routed Work Path, group routing, folder cards, and specialist prompts]

Next action:
{FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION} or REQUEST_MISSING_FILES
```

If all required startup files are present and readable, use:

```text
Startup status:
COMPLETE

Next action:
Waiting for all files (Project Files) from second_prompt_files folder
```

If any required startup file is missing or unreadable, use:

```text
Startup status:
INCOMPLETE

Next action:
REQUEST_MISSING_FILES
```

## Required second-upload project readiness behavior

After the first startup load check is complete, the AI is not ready for project work yet.
The next expected human action is to upload all available files from the `second_prompt_files` folder.

When the second upload group arrives, read it using the second-upload order from `{PASTE_AFTER_UPLOAD_FILENAME}`.
After the second upload group has been read, return exactly this readiness structure:

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
{SECOND_UPLOAD_READY_ACTION}
```

Use `Same physical root: YES` only when the active project root and KANDA tool root are intentionally the same root; otherwise use `NO`. For this project, `kanda_reasoner` can be both the active project and the KANDA tool, so the distinction must be stated explicitly instead of merged silently.

Only after `{PROJECT_READY_CHECK_TITLE}` ends with `Next action: {SECOND_UPLOAD_READY_ACTION}` should the AI handle the real project task."""
