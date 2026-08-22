# project-path: scripts/validate_ai_response_patch_delivery_staging_gate.py
"""Root-drive to verified daily-work staging gate for patch install blocks."""

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


def _require_dynamic_daily_root(lowered: str) -> None:
    _require(
        "$project_name",
        lowered,
        "Install block must derive $PROJECT_NAME from $PROJECT_ROOT.",
    )
    project_name_ok = (
        "$project_name = split-path $project_root -leaf" in lowered
        or "$project_name=split-path $project_root -leaf" in lowered
    )
    if not project_name_ok:
        _fail("$PROJECT_NAME must be derived with Split-Path $PROJECT_ROOT -Leaf.")
    daily_root_ok = (
        "$daily_root = join-path $drive_root ($project_name + \"_delete_after_daily_work\")"
        in lowered
        or "$daily_root=join-path $drive_root ($project_name + \"_delete_after_daily_work\")"
        in lowered
        or "$work_dir = join-path $drive_root ($project_name + \"_delete_after_daily_work\")"
        in lowered
        or "$work_dir=join-path $drive_root ($project_name + \"_delete_after_daily_work\")"
        in lowered
    )
    if not daily_root_ok:
        _fail(
            "Daily-work root must be derived from $DRIVE_ROOT plus the current "
            "$PROJECT_NAME; hardcoded Project daily-work roots are forbidden."
        )


def _require_sha256_verification(lowered: str, staged_var: str) -> None:
    _require(
        "get-filehash",
        lowered,
        "Install block must SHA-256 verify root and staged ZIP copies.",
    )
    _require(
        "-algorithm sha256",
        lowered,
        "Install block must use SHA256 for staging integrity verification.",
    )
    root_hash_present = "$root_hash" in lowered or "$roothash" in lowered
    staged_hash_present = "$staged_hash" in lowered or "$stagedhash" in lowered
    if not root_hash_present or not staged_hash_present:
        _fail("Install block must retain both root and staged SHA-256 hashes.")
    if "$root_patch_zip" not in lowered or staged_var not in lowered:
        _fail("SHA-256 verification must bind the root ZIP and staged ZIP paths.")
    comparison_present = any(
        token in lowered
        for token in (
            "$root_hash -ne $staged_hash",
            "$roothash -ne $stagedhash",
            "$root_hash.hash -ne $staged_hash.hash",
            "$roothash.hash -ne $stagedhash.hash",
        )
    )
    if not comparison_present:
        _fail("Install block must compare root and staged SHA-256 values before cleanup.")


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
    _require_dynamic_daily_root(lowered)
    _require(root_var, lowered, "Install block must define $ROOT_PATCH_ZIP at the project drive root.")
    _require(
        DAILY_WORK_TOKEN,
        lowered,
        "Install block must stage under the project _delete_after_daily_work folder.",
    )
    _require(
        "zip is not in root of drive:\\ where project is",
        lowered,
        "Install block must fail with the exact bridge error when the ZIP is not at drive root.",
    )

    root_definition_ok = (
        "$root_patch_zip = join-path $drive_root" in lowered
        or "$root_patch_zip=join-path $drive_root" in lowered
    )
    if not root_definition_ok:
        _fail(
            "$ROOT_PATCH_ZIP must be built from $DRIVE_ROOT, not from Downloads, "
            "Desktop, project root, or a fixed drive."
        )

    staged_definition_ok = (
        f"{staged_var} = join-path" in lowered
        or f"{staged_var}=join-path" in lowered
    ) and ("$daily_root" in lowered or "$work_dir" in lowered)
    if not staged_definition_ok:
        _fail("The staged ZIP variable must be built with Join-Path from $DAILY_ROOT or $WORK_DIR.")

    if re.search(r"(?<!re)move-item\b", lowered) and root_var in lowered:
        _fail("Move-Item is forbidden for root intake; use copy, SHA-256 verify, then delete source.")

    copy_root_to_staged = (
        f"copy-item -literalpath {root_var} -destination {staged_var}" in lowered
        or f"copy-item -path {root_var} -destination {staged_var}" in lowered
        or f"copy-item {root_var} {staged_var}" in lowered
    )
    if not copy_root_to_staged:
        _fail("Install block must copy the drive-root ZIP into daily work before verification.")

    _require_sha256_verification(lowered, staged_var)

    root_remove_present = (
        f"remove-item -literalpath {root_var}" in lowered
        or f"remove-item -path {root_var}" in lowered
        or f"remove-item {root_var}" in lowered
    )
    if not root_remove_present:
        _fail("Install block must delete the drive-root ZIP only after verified copy-staging.")

    staged_test_present = (
        f"test-path {staged_var}" in lowered
        or f"test-path -literalpath {staged_var}" in lowered
        or f"test-path -path {staged_var}" in lowered
    )
    if not staged_test_present:
        _fail("Install block must verify the staged daily-work ZIP exists before extraction.")

    if "expand-archive -path $root_patch_zip" in lowered or "expand-archive $root_patch_zip" in lowered:
        _fail("Install block must not extract from the drive-root ZIP; extract only from the staged daily-work ZIP.")

    if (
        f"expand-archive -literalpath {staged_var}" not in lowered
        and f"expand-archive -path {staged_var}" not in lowered
        and f"expand-archive {staged_var}" not in lowered
    ):
        _fail("Install block must extract only from the staged daily-work ZIP variable.")

    _require_order(lowered, "copy-item", "get-filehash", "Install block must copy before hashing the staged ZIP.")
    _require_order(lowered, "get-filehash", "remove-item", "Install block must verify SHA-256 before deleting the root ZIP.")
    _require_order(lowered, "remove-item", "expand-archive", "Install block must remove the verified root copy before extraction.")
