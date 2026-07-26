# project-path: scripts/validate_ai_response_patch_delivery_staging_gate.py
"""Root-drive to daily-work staging gate for patch install blocks.

This module validates the user-facing PowerShell wrapper, not the inner
INSTALL.ps1 copied inside a patch ZIP. The wrapper must treat the drive-root
ZIP as a temporary drop-off only, stage the used ZIP under
<project>_delete_after_daily_work, delete the drive-root copy after staging,
and extract only from the staged ZIP.
"""

from __future__ import annotations

__all__ = []

import re

try:
    from scripts.validate_ai_response_patch_delivery_contract import DAILY_WORK_TOKEN, _fail
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from validate_ai_response_patch_delivery_contract import DAILY_WORK_TOKEN, _fail


def _compact(text: str) -> str:
    """Return a whitespace-normalized lowercase copy of *text*."""
    return re.sub(r"\s+", " ", str(text or "").lower()).strip()


def _find_staged_zip_var(lowered: str) -> str:
    """Return the staged-ZIP variable used by the install block."""
    candidates = ("$staged_patch_zip", "$work_patch_zip", "$daily_patch_zip")
    for candidate in candidates:
        if candidate in lowered:
            return candidate
    _fail(
        "Install block must use a named staged ZIP variable such as "
        "$STAGED_PATCH_ZIP or $WORK_PATCH_ZIP inside the daily-work folder."
    )
    return ""


def _require(fragment: str, lowered: str, message: str) -> None:
    """Fail if *fragment* is absent from *lowered*."""
    if fragment not in lowered:
        _fail(message)


def _require_order(lowered: str, first: str, second: str, message: str) -> None:
    """Fail if *first* does not appear before *second*."""
    first_index = lowered.find(first)
    second_index = lowered.find(second)
    if first_index == -1 or second_index == -1 or first_index > second_index:
        _fail(message)


def validate_root_drive_staging_install_block(block: str) -> None:
    """Validate strict root-drive-to-daily-work staging behavior."""
    lowered = _compact(block)
    staged_var = _find_staged_zip_var(lowered)
    root_var = "$root_patch_zip"

    _require("$project_root", lowered, "Install block must define $PROJECT_ROOT.")
    _require("$patch_name", lowered, "Install block must define $PATCH_NAME.")
    _require("$drive_root", lowered, "Install block must derive $DRIVE_ROOT from $PROJECT_ROOT.")
    _require(
        "[system.io.path]::getpathroot",
        lowered,
        "Install block must derive DRIVE_ROOT with [System.IO.Path]::GetPathRoot.",
    )
    _require(root_var, lowered, "Install block must define $ROOT_PATCH_ZIP at the project drive root.")
    _require(
        DAILY_WORK_TOKEN,
        lowered,
        "Install block must stage under the project _delete_after_daily_work folder.",
    )
    _require(
        "zip is not in root of drive:\\ where project is",
        lowered,
        "Install block must fail with the exact bridge error when the ZIP is not staged or at drive root.",
    )

    root_definition_ok = (
        "$root_patch_zip = join-path $drive_root" in lowered
        or "$root_patch_zip=join-path $drive_root" in lowered
    )
    if not root_definition_ok:
        _fail("$ROOT_PATCH_ZIP must be built from $DRIVE_ROOT, not from Downloads, Desktop, project root, or a fixed drive.")

    staged_definition_ok = (
        f"{staged_var} = join-path" in lowered
        or f"{staged_var}=join-path" in lowered
    ) and ("$daily_root" in lowered or "$work_dir" in lowered)
    if not staged_definition_ok:
        _fail("The staged ZIP variable must be built with Join-Path from $DAILY_ROOT or $WORK_DIR.")

    copy_root_to_staged = (
        f"copy-item -path {root_var} -destination {staged_var}" in lowered
        or f"copy-item {root_var} {staged_var}" in lowered
    )
    move_root_to_staged = (
        f"move-item -path {root_var} -destination {staged_var}" in lowered
        or f"move-item {root_var} {staged_var}" in lowered
    )
    if not (copy_root_to_staged or move_root_to_staged):
        _fail("Install block must stage the drive-root ZIP into daily work before extraction using Copy-Item or Move-Item.")

    root_remove_present = f"remove-item -path {root_var}" in lowered or f"remove-item {root_var}" in lowered
    if copy_root_to_staged and not root_remove_present:
        _fail("Install block must delete the temporary drive-root ZIP copy after successful copy-staging.")

    staged_test_present = f"test-path {staged_var}" in lowered or f"test-path -path {staged_var}" in lowered
    if not staged_test_present:
        _fail("Install block must verify the staged daily-work ZIP exists before extraction.")

    if "expand-archive -path $root_patch_zip" in lowered or "expand-archive $root_patch_zip" in lowered:
        _fail("Install block must not extract from the drive-root ZIP; extract only from the staged daily-work ZIP.")

    if f"expand-archive -path {staged_var}" not in lowered and f"expand-archive {staged_var}" not in lowered:
        _fail("Install block must extract only from the staged daily-work ZIP variable.")

    stage_term = "copy-item" if copy_root_to_staged else "move-item"
    _require_order(lowered, stage_term, "expand-archive", "Install block must stage the ZIP before Expand-Archive.")
    if copy_root_to_staged:
        _require_order(lowered, "remove-item", "expand-archive", "Install block must delete the root-drive copy before extraction.")
