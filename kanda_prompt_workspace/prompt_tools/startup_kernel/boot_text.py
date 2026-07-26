"""Boot command and first-position override helpers."""

from __future__ import annotations

from typing import Iterable

from startup_kernel.constants import (
    FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION,
    FREEZE_CODE_INTAKE_FIRST_POSITION_OVERRIDE_RULE_V1,
    MANIFEST_FILENAME,
    PRE_OUTPUT_CONTRACT_GATES_FIRST_POSITION_HOOK_V1,
    README_FILENAME,
    RG028_FREEZE_WORKFLOW_FIRST_POSITION_OVERRIDE_RULE_V3,
    RG029_STARTUP_STALE_FILENAME_FIRST_POSITION_OVERRIDE_RULE_V1,
    STABLE_BOOT_FILENAME,
    T9T013_RG015_FIRST_POSITION_OVERRIDE_RULE_V8,
)
from startup_kernel.start_here_lists import build_active_bridge_report


__all__ = [
    "make_boot_command_text",
]


def _prepend_startup_first_position_overrides(content: str) -> str:
    """Prepend mandatory first-position routing overrides."""
    ordered_overrides = [
        (
            "Mandatory prompt-authoring RG-015 first-position hard override "
            "loaded.",
            T9T013_RG015_FIRST_POSITION_OVERRIDE_RULE_V8.strip(),
        ),
        (
            "Mandatory RG-028 freeze-workflow exact context override loaded.",
            RG028_FREEZE_WORKFLOW_FIRST_POSITION_OVERRIDE_RULE_V3.strip(),
        ),
        (
            "Mandatory RG-029 startup-delivery stale-filename exact context "
            "override loaded.",
            RG029_STARTUP_STALE_FILENAME_FIRST_POSITION_OVERRIDE_RULE_V1.strip(),
        ),
        (
            "Mandatory freeze-code intake hook loaded.",
            FREEZE_CODE_INTAKE_FIRST_POSITION_OVERRIDE_RULE_V1.strip(),
        ),
        (
            "Mandatory pre-output contract gate hook loaded.",
            PRE_OUTPUT_CONTRACT_GATES_FIRST_POSITION_HOOK_V1.strip(),
        ),
    ]
    blocks_to_prepend = [
        block
        for marker, block in ordered_overrides
        if marker not in content
    ]
    if blocks_to_prepend:
        content = "\n\n".join(blocks_to_prepend) + "\n\n" + content.lstrip()
    return content


def make_boot_command_text(expected_filenames: Iterable[str]) -> str:
    """Return the stable startup boot command text."""
    expected = list(expected_filenames)
    numbered_file_list = "\n".join(expected)
    required_report_lines = [
        f"0. {STABLE_BOOT_FILENAME} - loaded/missing - one-line role"
    ]
    required_report_lines.extend(
        f"{index}. {name} - loaded/missing - one-line role"
        for index, name in enumerate(expected, start=1)
    )
    required_report_lines.append(
        f"{len(expected) + 1}. {README_FILENAME} - loaded/missing - "
        "one-line role"
    )
    required_report_lines.append(
        f"{len(expected) + 2}. {MANIFEST_FILENAME} - loaded/missing - "
        "one-line role"
    )
    required_report_list = "\n".join(required_report_lines)
    active_bridge_report = build_active_bridge_report()

    return f"""Read the uploaded startup prompt request kernel ZIP now.

First, open and read this file from inside the ZIP:

{STABLE_BOOT_FILENAME}

Then inspect these required startup support files:

{README_FILENAME}
{MANIFEST_FILENAME}

Then inspect every numbered startup file in order:

{numbered_file_list}

Before answering any project task, return only:

STARTUP PACK LOAD CHECK

Files recognized:
{required_report_list}

Beginning-of-day active bridges:
{active_bridge_report}

Startup status:
COMPLETE / INCOMPLETE

Routing behavior:
[one paragraph]

Next action:
{FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION} or REQUEST_MISSING_FILES

Do not solve any project task yet.

If all required startup files are present and readable, use:

Startup status:
COMPLETE

Next action:
{FIRST_UPLOAD_PROJECT_FILES_WAIT_ACTION}

If any required file above is missing or unreadable, mark Startup status as
INCOMPLETE and request the missing files.
"""
