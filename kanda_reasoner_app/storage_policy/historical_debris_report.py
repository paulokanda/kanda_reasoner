# project-path: kanda_reasoner_app/storage_policy/historical_debris_report.py
"""Legacy debris report helpers for the Kanda Reasoner storage policy box.

This module detects old top-level Kanda maintenance folders and reports where
those folders should be migrated later. It is side-effect free: importing it
must not create folders, move files, delete files, or scan the source tree.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from kanda_reasoner_app.storage_policy.maintenance_root_resolver import (
    get_maintenance_root,
)
from kanda_reasoner_app.storage_policy.maintenance_subfolder_policy import (
    get_maintenance_subfolder,
)
from kanda_reasoner_app.storage_policy.path_resolver import (
    get_app_drive_or_anchor,
    normalize_path,
)

LEGACY_DEBRIS_FOLDER_NAMES = (
    "_kanda_patch_backups",
    "_kanda_restore_points",
    "_kanda_temp",
)

LEGACY_DEBRIS_DESTINATION_NAMES = {
    "_kanda_patch_backups": "patch_backups",
    "_kanda_restore_points": "restore_points",
    "_kanda_temp": "legacy_absorbed",
}

LEGACY_DEBRIS_REPORT_ACTION = "report_only"


@dataclass(frozen=True)
class LegacyDebrisFolderReport:
    """Report data for one legacy top-level debris folder."""

    legacy_name: str
    legacy_path: str
    exists: bool
    is_dir: bool
    file_count: int
    total_bytes: int
    latest_modified_timestamp: float | None
    recommended_destination_name: str
    recommended_destination_path: str
    action: str = LEGACY_DEBRIS_REPORT_ACTION


def _path_from_drive_or_anchor(drive_or_anchor: str, folder_name: str) -> Path:
    """Build a path from a Windows drive or POSIX anchor/base path."""
    anchor = str(drive_or_anchor).strip()

    if not anchor:
        raise ValueError("drive_or_anchor must not be empty.")

    if anchor.endswith(":"):
        return Path(f"{anchor}\\{folder_name}")

    return Path(anchor) / folder_name


def build_legacy_debris_path(
    legacy_name: str,
    drive_or_anchor: str | None = None,
) -> Path:
    """Return the legacy top-level debris folder path without creating it."""
    if legacy_name not in LEGACY_DEBRIS_FOLDER_NAMES:
        allowed = ", ".join(LEGACY_DEBRIS_FOLDER_NAMES)
        raise ValueError(
            f"Unknown legacy debris folder {legacy_name!r}. "
            f"Allowed values: {allowed}."
        )

    anchor = drive_or_anchor if drive_or_anchor is not None else get_app_drive_or_anchor()
    return _path_from_drive_or_anchor(anchor, legacy_name)


def get_legacy_debris_destination(
    legacy_name: str,
    maintenance_root: str | Path | None = None,
) -> Path:
    """Return the recommended canonical destination for one legacy folder."""
    if legacy_name not in LEGACY_DEBRIS_DESTINATION_NAMES:
        allowed = ", ".join(LEGACY_DEBRIS_FOLDER_NAMES)
        raise ValueError(
            f"Unknown legacy debris folder {legacy_name!r}. "
            f"Allowed values: {allowed}."
        )

    destination_name = LEGACY_DEBRIS_DESTINATION_NAMES[legacy_name]
    return get_maintenance_subfolder(destination_name, maintenance_root)


def _scan_path_stats(path: Path) -> tuple[int, int, float | None]:
    """Return file_count, total_bytes, latest_modified_timestamp for path."""
    if not path.exists():
        return 0, 0, None

    if path.is_file():
        stat_result = path.stat()
        return 1, int(stat_result.st_size), float(stat_result.st_mtime)

    file_count = 0
    total_bytes = 0
    latest_modified_timestamp: float | None = float(path.stat().st_mtime)

    for item in path.rglob("*"):
        try:
            stat_result = item.stat()
        except OSError:
            continue

        modified = float(stat_result.st_mtime)
        if latest_modified_timestamp is None or modified > latest_modified_timestamp:
            latest_modified_timestamp = modified

        if item.is_file():
            file_count += 1
            total_bytes += int(stat_result.st_size)

    return file_count, total_bytes, latest_modified_timestamp


def report_one_legacy_debris_folder(
    legacy_name: str,
    drive_or_anchor: str | None = None,
    maintenance_root: str | Path | None = None,
) -> LegacyDebrisFolderReport:
    """Return a report for one legacy debris folder without moving it."""
    legacy_path = build_legacy_debris_path(legacy_name, drive_or_anchor)
    destination_path = get_legacy_debris_destination(
        legacy_name,
        maintenance_root,
    )
    file_count, total_bytes, latest_modified_timestamp = _scan_path_stats(
        legacy_path,
    )

    return LegacyDebrisFolderReport(
        legacy_name=legacy_name,
        legacy_path=str(legacy_path),
        exists=legacy_path.exists(),
        is_dir=legacy_path.is_dir(),
        file_count=file_count,
        total_bytes=total_bytes,
        latest_modified_timestamp=latest_modified_timestamp,
        recommended_destination_name=LEGACY_DEBRIS_DESTINATION_NAMES[
            legacy_name
        ],
        recommended_destination_path=str(destination_path),
    )


def scan_legacy_debris_folders(
    drive_or_anchor: str | None = None,
    maintenance_root: str | Path | None = None,
) -> tuple[LegacyDebrisFolderReport, ...]:
    """Return reports for all known legacy debris folders.

    This function reports only. It never creates, moves, or deletes files.
    """
    return tuple(
        report_one_legacy_debris_folder(
            legacy_name,
            drive_or_anchor=drive_or_anchor,
            maintenance_root=maintenance_root,
        )
        for legacy_name in LEGACY_DEBRIS_FOLDER_NAMES
    )


def summarize_historical_debris_reports(
    reports: tuple[LegacyDebrisFolderReport, ...],
) -> str:
    """Return a human-readable legacy debris report summary."""
    lines = [
        "Kanda Reasoner legacy debris report",
        "Action: report only. No files were moved or deleted.",
    ]

    for report in reports:
        status = "present" if report.exists else "absent"
        lines.extend(
            (
                "",
                f"Legacy folder: {report.legacy_name}",
                f"Status: {status}",
                f"Path: {report.legacy_path}",
                f"Files: {report.file_count}",
                f"Bytes: {report.total_bytes}",
                "Recommended destination: "
                f"{report.recommended_destination_path}",
            )
        )

    return "\n".join(lines) + "\n"


def describe_legacy_debris_policy() -> dict[str, str]:
    """Return a copy of the legacy-folder-to-destination policy."""
    return dict(LEGACY_DEBRIS_DESTINATION_NAMES)


__all__ = [
    "LEGACY_DEBRIS_DESTINATION_NAMES",
    "LEGACY_DEBRIS_FOLDER_NAMES",
    "LEGACY_DEBRIS_REPORT_ACTION",
    "LegacyDebrisFolderReport",
    "build_legacy_debris_path",
    "describe_legacy_debris_policy",
    "get_legacy_debris_destination",
    "report_one_legacy_debris_folder",
    "scan_legacy_debris_folders",
    "summarize_historical_debris_reports",
]
