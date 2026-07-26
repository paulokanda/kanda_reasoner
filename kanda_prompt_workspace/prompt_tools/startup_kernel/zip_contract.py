"""Generated startup ZIP contract helpers."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path
from typing import Any, Iterable

from startup_freeze_context import ACTIVE_FREEZE_CONTEXT_FILENAME
from startup_kernel.constants import (
    MANIFEST_FILENAME,
    MODIFY_STARTUP_DELIVERY_FILENAME,
    README_FILENAME,
    READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME,
    STABLE_BOOT_FILENAME,
    STARTUP_ARTIFACT_READ_ORDER_MARKER,
)


__all__ = [
    "read_manifest_from_zip",
    "validate_generated_zip_contract",
]

def read_manifest_from_zip(zip_path: Path) -> dict[str, Any] | None:
    try:
        with zipfile.ZipFile(zip_path, "r") as z:
            if MANIFEST_FILENAME not in z.namelist():
                return None
            with z.open(MANIFEST_FILENAME) as f:
                return json.loads(f.read().decode("utf-8"))
    except (OSError, zipfile.BadZipFile, json.JSONDecodeError):
        return None

def validate_generated_zip_contract(
    zip_path: Path,
    expected_generated_filenames: Iterable[str] | None = None,
) -> None:
    with zipfile.ZipFile(zip_path, "r") as z:
        names = set(z.namelist())

        if expected_generated_filenames is None:
            expected_generated = {
                "01_ai_prompt_request_canon.md",
                "02_prompt_navigation_index.md",
                "03_GROUP_ASSIMILATION_INDEX.md",
                "04_FOLDER_ASSIMILATION_CARDS_INDEX.md",
                "05_start_of_day_master_stack.md",
                "06_session_start_upload_checklist.md",
                "07_daily_patch_delivery_guardrails.md",
            }
        else:
            expected_generated = set(expected_generated_filenames)

        required = {
            STABLE_BOOT_FILENAME,
            README_FILENAME,
            MANIFEST_FILENAME,
        } | expected_generated

        missing = sorted(required - names)
        if missing:
            raise ValueError(f"Generated ZIP is missing required files: {missing}")

        old_boot_files = sorted(name for name in names if name.startswith("00_START_HERE_FOR_AI__CERT_"))
        if old_boot_files:
            raise ValueError(f"Generated ZIP contains obsolete certificate-suffixed boot files: {old_boot_files}")

        if MODIFY_STARTUP_DELIVERY_FILENAME in names:
            raise ValueError(f"{MODIFY_STARTUP_DELIVERY_FILENAME} must stay outside the normal startup ZIP.")

        notice_text = z.read(READ_BEFORE_ANY_STARTUP_ARTIFACT_FILENAME).decode("utf-8-sig")
        boot_text = z.read(STABLE_BOOT_FILENAME).decode("utf-8-sig")
        manifest_text = z.read(MANIFEST_FILENAME).decode("utf-8-sig")
        freeze_context_text = z.read(ACTIVE_FREEZE_CONTEXT_FILENAME).decode("utf-8-sig") if ACTIVE_FREEZE_CONTEXT_FILENAME in names else ""

    if STARTUP_ARTIFACT_READ_ORDER_MARKER not in notice_text:
        raise ValueError("Startup ZIP read-order notice is missing the tell_AI first instruction.")

    required_boot_phrases = [
        "Anti-bypass rule",
        "Do not implement anything",
        "Do not create a patch",
        "zz_read_only_if_modifying_startup_delivery.md",
        "Routed Work Path",
        "07_daily_patch_delivery_guardrails.md",
    ]

    missing_phrases = [phrase for phrase in required_boot_phrases if phrase not in boot_text]
    if missing_phrases:
        raise ValueError(f"Stable boot file is missing anti-bypass phrases: {missing_phrases}")

    missing_expected_in_boot = sorted(
        name for name in expected_generated if name not in boot_text
    )
    if missing_expected_in_boot:
        raise ValueError(
            f"Stable boot file is missing expected startup files: {missing_expected_in_boot}"
        )

    if "00_START_HERE_FOR_AI__CERT_" in manifest_text:
        raise ValueError("Manifest still references obsolete certificate-suffixed boot filename.")

    required_freeze_context_phrases = [
        "ACTIVE PROJECT FREEZE CONTEXT",
        "Post-validation freeze awareness rule",
        "Freeze Feature After Update tab",
        "generated exposure copy",
        "First-prompt delivery certification",
        "Create First Prompt Files must insert this file into first_prompts_to_ai.zip",
        "<project_drive>/<project_name>_show_project_to_AI/project_freeze_after_update/frozen_features_memory/",
        "Runtime source is completely correct",
    ]
    missing_freeze_context_phrases = [
        phrase for phrase in required_freeze_context_phrases if phrase not in freeze_context_text
    ]
    if missing_freeze_context_phrases:
        raise ValueError(
            f"Active freeze context file is missing required phrases: {missing_freeze_context_phrases}"
        )

    forbidden_freeze_context_phrases = [
        "<active_project_root>/project_freeze_after_update/frozen_features_memory/",
        "E:\\kanda_reasoner\\project_freeze_after_update\\frozen_features_memory",
        "E:/kanda_reasoner/project_freeze_after_update/frozen_features_memory",
    ]
    present_forbidden_freeze_context_phrases = [
        phrase for phrase in forbidden_freeze_context_phrases if phrase in freeze_context_text
    ]
    if present_forbidden_freeze_context_phrases:
        raise ValueError(
            "Active freeze context file contains stale freeze-memory path phrase(s): "
            + str(present_forbidden_freeze_context_phrases)
        )

