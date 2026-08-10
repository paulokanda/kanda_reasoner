"""Shared fail-closed ZIP member and physical extraction safety.

The policy validates the complete member set before writing any bytes, then
extracts each member manually and re-enumerates the physical tree.  This keeps
source-package installers and Portable release smoke extraction from trusting
``ZipFile.extractall`` as a boundary enforcement mechanism.
"""

from __future__ import annotations

import os
import shutil
import stat
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable

__all__ = [
    "ArchiveExtractionReport",
    "ArchiveMemberPlan",
    "ArchiveSafetyError",
    "safe_extract_zip",
    "validate_archive_members",
]


class ArchiveSafetyError(RuntimeError):
    """Raised when an archive member or extracted path violates containment."""


@dataclass(frozen=True)
class ArchiveMemberPlan:
    """Preflighted extraction destination for one ZIP member."""

    info: zipfile.ZipInfo
    normalized_name: str
    relative_path: PurePosixPath
    destination: Path
    is_directory: bool


@dataclass(frozen=True)
class ArchiveExtractionReport:
    """Evidence returned after safe extraction and physical revalidation."""

    destination_root: Path
    top_level_name: str
    member_count: int
    file_count: int
    directory_count: int
    maximum_member_path_bytes: int


def _normalized_member_name(
    name: str,
    *,
    reject_windows_ambiguous_names: bool = False,
) -> str:
    if "\x00" in name:
        raise ArchiveSafetyError("ARCHIVE_MEMBER_NUL_REJECTED")
    if "\\" in name:
        raise ArchiveSafetyError(
            "ARCHIVE_BACKSLASH_MEMBER_REJECTED:" + name
        )
    normalized = name
    while normalized.startswith("./"):
        normalized = normalized[2:]
    if not normalized:
        raise ArchiveSafetyError("ARCHIVE_EMPTY_MEMBER_NAME_REJECTED")
    if normalized.startswith("/") or normalized.startswith("//"):
        raise ArchiveSafetyError(
            "ARCHIVE_ABSOLUTE_MEMBER_REJECTED:" + name
        )
    if len(normalized) >= 2 and normalized[1] == ":":
        raise ArchiveSafetyError(
            "ARCHIVE_DRIVE_QUALIFIED_MEMBER_REJECTED:" + name
        )
    relative = PurePosixPath(normalized)
    if relative.is_absolute() or ".." in relative.parts:
        raise ArchiveSafetyError(
            "ARCHIVE_PARENT_TRAVERSAL_REJECTED:" + name
        )
    if any(part in {"", "."} for part in relative.parts):
        raise ArchiveSafetyError(
            "ARCHIVE_AMBIGUOUS_MEMBER_REJECTED:" + name
        )
    if reject_windows_ambiguous_names:
        for part in relative.parts:
            if ":" in part:
                raise ArchiveSafetyError(
                    "ARCHIVE_WINDOWS_ADS_MEMBER_REJECTED:" + name
                )
            if part.endswith(" ") or part.endswith("."):
                raise ArchiveSafetyError(
                    "ARCHIVE_WINDOWS_AMBIGUOUS_MEMBER_REJECTED:" + name
                )
    return relative.as_posix()


def _zip_info_rejection_marker(info: zipfile.ZipInfo) -> str | None:
    """Return a stable rejection marker for link or special ZIP entries."""
    unix_mode = (int(info.external_attr) >> 16) & 0xFFFF
    file_type = stat.S_IFMT(unix_mode)
    if file_type == stat.S_IFLNK:
        return "ARCHIVE_SYMLINK_MEMBER_REJECTED"
    if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
        return "ARCHIVE_SPECIAL_MEMBER_REJECTED"
    dos_attributes = int(info.external_attr) & 0xFFFF
    reparse_flag = 0x0400
    if dos_attributes & reparse_flag:
        return "ARCHIVE_REPARSE_MEMBER_REJECTED"
    return None


def _path_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _destination_for_member(root: Path, relative: PurePosixPath) -> Path:
    destination = root.joinpath(*relative.parts).resolve(strict=False)
    if destination == root or not _path_inside(destination, root):
        raise ArchiveSafetyError(
            "ARCHIVE_MEMBER_DESTINATION_ESCAPE_REJECTED:"
            + relative.as_posix()
        )
    return destination


def validate_archive_members(
    archive: zipfile.ZipFile,
    destination_root: str | Path,
    *,
    expected_top_level: str | None = None,
    require_single_top_level: bool = True,
    reject_windows_ambiguous_names: bool = False,
) -> tuple[ArchiveMemberPlan, ...]:
    """Preflight every member and return immutable extraction plans."""
    root = Path(destination_root).expanduser().resolve(strict=False)
    infos = archive.infolist()
    if not infos:
        raise ArchiveSafetyError("ARCHIVE_EMPTY_REJECTED")

    plans: list[ArchiveMemberPlan] = []
    folded_names: set[str] = set()
    top_levels: set[str] = set()
    for info in infos:
        raw_name = getattr(info, "orig_filename", info.filename)
        normalized = _normalized_member_name(
            raw_name,
            reject_windows_ambiguous_names=reject_windows_ambiguous_names,
        )
        folded = normalized.casefold()
        if folded in folded_names:
            raise ArchiveSafetyError(
                "ARCHIVE_CASE_COLLISION_REJECTED:" + normalized
            )
        folded_names.add(folded)
        relative = PurePosixPath(normalized)
        top_levels.add(relative.parts[0])
        rejection_marker = _zip_info_rejection_marker(info)
        if rejection_marker is not None:
            raise ArchiveSafetyError(rejection_marker + ":" + normalized)
        destination = _destination_for_member(root, relative)
        plans.append(
            ArchiveMemberPlan(
                info=info,
                normalized_name=normalized,
                relative_path=relative,
                destination=destination,
                is_directory=info.is_dir() or raw_name.endswith("/"),
            )
        )

    file_names = {
        plan.normalized_name.casefold()
        for plan in plans
        if not plan.is_directory
    }
    for plan in plans:
        parts = plan.relative_path.parts
        for end in range(1, len(parts)):
            ancestor = PurePosixPath(*parts[:end]).as_posix().casefold()
            if ancestor in file_names:
                raise ArchiveSafetyError(
                    "ARCHIVE_FILE_DIRECTORY_COLLISION_REJECTED:"
                    + plan.normalized_name
                )

    if require_single_top_level and len(top_levels) != 1:
        raise ArchiveSafetyError(
            "ARCHIVE_TOP_LEVEL_COUNT_REJECTED:"
            + ",".join(sorted(top_levels))
        )
    top_level = next(iter(top_levels)) if len(top_levels) == 1 else ""
    if expected_top_level is not None and top_level != expected_top_level:
        raise ArchiveSafetyError(
            "ARCHIVE_TOP_LEVEL_IDENTITY_REJECTED:"
            + top_level
            + "!="
            + expected_top_level
        )
    return tuple(plans)


def _is_reparse_point(path: Path) -> bool:
    try:
        result = path.lstat()
    except OSError as exc:
        raise ArchiveSafetyError(
            "ARCHIVE_POST_EXTRACTION_LSTAT_FAILED:" + str(path)
        ) from exc
    attributes = int(getattr(result, "st_file_attributes", 0) or 0)
    reparse_flag = int(getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0) or 0)
    return bool(reparse_flag and attributes & reparse_flag)


def _iter_physical_tree(root: Path) -> Iterable[Path]:
    pending = [root]
    while pending:
        current = pending.pop()
        try:
            entries = list(os.scandir(current))
        except OSError as exc:
            raise ArchiveSafetyError(
                "ARCHIVE_POST_EXTRACTION_ENUMERATION_FAILED:" + str(current)
            ) from exc
        for entry in entries:
            path = Path(entry.path)
            yield path
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                pending.append(path)


def _validate_physical_tree(root: Path) -> tuple[int, int]:
    files = 0
    directories = 0
    for path in _iter_physical_tree(root):
        if path.is_symlink() or _is_reparse_point(path):
            raise ArchiveSafetyError(
                "ARCHIVE_REPARSE_POINT_ESCAPE_REJECTED:" + str(path)
            )
        resolved = path.resolve(strict=False)
        if not _path_inside(resolved, root):
            raise ArchiveSafetyError(
                "ARCHIVE_POST_EXTRACTION_ESCAPE_REJECTED:" + str(path)
            )
        if path.is_dir():
            directories += 1
        elif path.is_file():
            files += 1
        else:
            raise ArchiveSafetyError(
                "ARCHIVE_POST_EXTRACTION_SPECIAL_FILE_REJECTED:" + str(path)
            )
    return files, directories


def safe_extract_zip(
    archive_path: str | Path,
    destination_root: str | Path,
    *,
    expected_top_level: str | None = None,
    require_empty_destination: bool = True,
) -> ArchiveExtractionReport:
    """Safely extract a ZIP after complete preflight and physical recheck."""
    archive_file = Path(archive_path).expanduser().resolve(strict=False)
    root = Path(destination_root).expanduser().resolve(strict=False)
    root.mkdir(parents=True, exist_ok=True)
    if require_empty_destination and any(root.iterdir()):
        raise ArchiveSafetyError(
            "ARCHIVE_DESTINATION_NOT_EMPTY:" + str(root)
        )

    created: list[Path] = []
    try:
        with zipfile.ZipFile(archive_file, "r") as archive:
            bad_member = archive.testzip()
            if bad_member is not None:
                raise ArchiveSafetyError(
                    "ARCHIVE_CRC_REJECTED:" + bad_member
                )
            plans = validate_archive_members(
                archive,
                root,
                expected_top_level=expected_top_level,
            )
            for plan in plans:
                if plan.is_directory:
                    plan.destination.mkdir(parents=True, exist_ok=True)
                    created.append(plan.destination)
                    continue
                plan.destination.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(plan.info, "r") as source_handle:
                    with plan.destination.open("xb") as destination_handle:
                        shutil.copyfileobj(
                            source_handle,
                            destination_handle,
                            length=1024 * 1024,
                        )
                created.append(plan.destination)

        file_count, directory_count = _validate_physical_tree(root)
        top_level = plans[0].relative_path.parts[0]
        maximum = max(
            len(plan.normalized_name.encode("utf-8"))
            for plan in plans
        )
        return ArchiveExtractionReport(
            destination_root=root,
            top_level_name=top_level,
            member_count=len(plans),
            file_count=file_count,
            directory_count=directory_count,
            maximum_member_path_bytes=maximum,
        )
    except Exception:
        for path in sorted(created, key=lambda item: len(item.parts), reverse=True):
            try:
                if path.is_dir():
                    path.rmdir()
                elif path.exists():
                    path.unlink()
            except OSError:
                pass
        raise
