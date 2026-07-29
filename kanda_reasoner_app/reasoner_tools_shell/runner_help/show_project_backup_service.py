"""Verified ZIP backup service for a selected Project Support folder."""

from __future__ import annotations

import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Callable

from kanda_reasoner_app.project_analysis_evidence_paths import (
    project_analysis_evidence_root,
)

__all__ = ["create_show_project_backup", "validate_backup_destination"]

_ALREADY_COMPRESSED_SUFFIXES = {
    ".7z",
    ".bz2",
    ".edf",
    ".gz",
    ".h5",
    ".hdf5",
    ".jpeg",
    ".jpg",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".rar",
    ".webp",
    ".xz",
    ".zip",
}


def create_show_project_backup(
    project_root: str | Path,
    destination_dir: str | Path,
    *,
    timestamp: datetime | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, object]:
    """Create and verify an atomic ZIP of the selected Project Support root."""
    selected_root = Path(project_root).expanduser().resolve(strict=False)
    if not selected_root.is_dir():
        raise FileNotFoundError(
            "Selected project root is not a directory: " + str(selected_root)
        )
    support_root = project_analysis_evidence_root(selected_root).resolve(strict=False)
    if not support_root.is_dir():
        raise FileNotFoundError("Show Project folder does not exist: " + str(support_root))
    destination = validate_backup_destination(selected_root, destination_dir)

    snapshot = _snapshot_support_root(support_root)
    total_bytes = sum(item[2] for item in snapshot if item[0] == "file")
    if not snapshot:
        raise ValueError("Show Project folder is empty: " + str(support_root))
    _require_free_space(destination, total_bytes)

    archive_path = _unique_archive_path(
        destination,
        support_root.name,
        timestamp or datetime.now(),
    )
    partial_path = _partial_archive_path(destination, archive_path.name)
    expected_files = {
        support_root.name + "/" + relative.as_posix(): size
        for kind, relative, size, _mtime_ns in snapshot
        if kind == "file"
    }
    expected_dirs = {
        support_root.name + "/" + relative.as_posix().rstrip("/") + "/"
        for kind, relative, _size, _mtime_ns in snapshot
        if kind == "dir"
    }

    try:
        _emit(progress, "Creating backup archive: " + archive_path.name)
        _write_backup_zip(
            partial_path,
            support_root,
            snapshot,
            progress,
        )
        _emit(progress, "Validating backup ZIP integrity...")
        _validate_backup_zip(partial_path, expected_files, expected_dirs)
        os.replace(partial_path, archive_path)
        _emit(progress, "Show Project backup created successfully.")
        return {
            "archive_path": str(archive_path),
            "source_root": str(support_root),
            "file_count": len(expected_files),
            "directory_count": len(expected_dirs) + 1,
            "source_bytes": total_bytes,
            "archive_bytes": archive_path.stat().st_size,
        }
    finally:
        if partial_path.exists():
            try:
                partial_path.unlink()
            except OSError:
                pass


def validate_backup_destination(
    project_root: str | Path,
    destination_dir: str | Path,
) -> Path:
    """Return a destination outside Project source and Project Support roots."""
    selected_root = Path(project_root).expanduser().resolve(strict=False)
    destination = Path(destination_dir).expanduser().resolve(strict=False)
    if not destination.is_dir():
        raise FileNotFoundError("Backup destination is not a directory: " + str(destination))
    support_root = project_analysis_evidence_root(selected_root).resolve(strict=False)
    if _is_within(destination, selected_root):
        raise ValueError(
            "Backup destination must stay outside the selected Project source root."
        )
    if _is_within(destination, support_root):
        raise ValueError("Backup destination must stay outside the Show Project folder.")
    return destination


def _write_backup_zip(
    partial_path: Path,
    support_root: Path,
    snapshot: list[tuple[str, Path, int, int]],
    progress: Callable[[str], None] | None,
) -> None:
    with zipfile.ZipFile(
        partial_path,
        "w",
        allowZip64=True,
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=6,
    ) as archive:
        _write_directory_entry(archive, support_root.name + "/")
        for index, item in enumerate(snapshot, start=1):
            kind, relative, size, mtime_ns = item
            source_path = support_root / relative
            archive_name = support_root.name + "/" + relative.as_posix()
            if kind == "dir":
                _write_directory_entry(archive, archive_name)
                continue
            _verify_source_identity(source_path, size, mtime_ns)
            archive.write(
                source_path,
                archive_name,
                compress_type=_compression_for(source_path),
            )
            _verify_source_identity(source_path, size, mtime_ns)
            if index == 1 or index % 100 == 0 or index == len(snapshot):
                _emit(
                    progress,
                    "Backing up Show Project files: "
                    + str(index)
                    + "/"
                    + str(len(snapshot)),
                )


def _snapshot_support_root(root: Path) -> list[tuple[str, Path, int, int]]:
    snapshot: list[tuple[str, Path, int, int]] = []
    for current_root, dir_names, file_names in os.walk(root, followlinks=False):
        current_path = Path(current_root)
        relative_current = current_path.relative_to(root)
        for name in sorted(dir_names):
            child = current_path / name
            if _is_link_like(child):
                raise ValueError(
                    "Symbolic links are not allowed in Show Project backup: "
                    + str(child)
                )
            relative = relative_current / name
            snapshot.append(("dir", relative, 0, child.stat().st_mtime_ns))
        for name in sorted(file_names):
            child = current_path / name
            if _is_link_like(child):
                raise ValueError(
                    "Symbolic links are not allowed in Show Project backup: "
                    + str(child)
                )
            stat_result = child.stat()
            relative = relative_current / name
            snapshot.append(
                ("file", relative, stat_result.st_size, stat_result.st_mtime_ns)
            )
    snapshot.sort(key=lambda item: (item[1].as_posix().lower(), item[0]))
    return snapshot


def _is_link_like(path: Path) -> bool:
    """Return True for symbolic links and Windows directory junctions."""
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    return bool(callable(is_junction) and is_junction())


def _verify_source_identity(path: Path, expected_size: int, expected_mtime_ns: int) -> None:
    stat_result = path.stat()
    if stat_result.st_size != expected_size or stat_result.st_mtime_ns != expected_mtime_ns:
        raise RuntimeError("Show Project content changed during backup: " + str(path))


def _require_free_space(destination: Path, source_bytes: int) -> None:
    required = source_bytes + (64 * 1024 * 1024)
    free = shutil.disk_usage(destination).free
    if free < required:
        raise OSError(
            "Not enough free space for backup. Required at least "
            + str(required)
            + " bytes; available "
            + str(free)
            + " bytes."
        )


def _unique_archive_path(destination: Path, root_name: str, moment: datetime) -> Path:
    stamp = moment.strftime("%Y-%m-%d_%H%M%S")
    base_name = root_name + "_backup_" + stamp
    candidate = destination / (base_name + ".zip")
    counter = 2
    while candidate.exists():
        candidate = destination / (base_name + "_" + f"{counter:02d}" + ".zip")
        counter += 1
    return candidate


def _partial_archive_path(destination: Path, final_name: str) -> Path:
    handle = tempfile.NamedTemporaryFile(
        mode="wb",
        delete=False,
        dir=str(destination),
        prefix="." + final_name + ".",
        suffix=".partial",
    )
    path = Path(handle.name)
    handle.close()
    return path


def _compression_for(path: Path) -> int:
    if path.suffix.lower() in _ALREADY_COMPRESSED_SUFFIXES:
        return zipfile.ZIP_STORED
    return zipfile.ZIP_DEFLATED


def _write_directory_entry(archive: zipfile.ZipFile, archive_name: str) -> None:
    normalized = archive_name.replace("\\", "/").rstrip("/") + "/"
    info = zipfile.ZipInfo(normalized)
    info.external_attr = 0o40775 << 16
    archive.writestr(info, b"")


def _validate_backup_zip(
    archive_path: Path,
    expected_files: dict[str, int],
    expected_dirs: set[str],
) -> None:
    with zipfile.ZipFile(archive_path, "r") as archive:
        if archive.testzip() is not None:
            raise RuntimeError("Backup ZIP integrity validation failed.")
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise RuntimeError("Backup ZIP contains duplicate archive paths.")
        actual_files = {
            info.filename: info.file_size for info in infos if not info.is_dir()
        }
        actual_dirs = {info.filename for info in infos if info.is_dir()}
        if actual_files != expected_files:
            raise RuntimeError(
                "Backup ZIP file inventory does not match the source snapshot."
            )
        required_dirs = set(expected_dirs)
        first_name = next(iter(expected_files or expected_dirs), "")
        if first_name:
            required_dirs.add(first_name.split("/", 1)[0] + "/")
        if not required_dirs.issubset(actual_dirs):
            raise RuntimeError("Backup ZIP directory inventory is incomplete.")


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _emit(progress: Callable[[str], None] | None, message: str) -> None:
    if progress is not None:
        progress(message)
