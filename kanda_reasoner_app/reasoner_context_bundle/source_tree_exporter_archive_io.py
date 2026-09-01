# project-path: kanda_reasoner_app/reasoner_context_bundle/source_tree_exporter_archive_io.py
"""ZIP and archive-part file IO helpers for source-tree export."""

from __future__ import annotations

import hashlib
import os
import shutil
import zipfile
from pathlib import Path
from typing import Any

from .hashing import sha256_file
from .schema_models import ProjectContext
from .source_tree_exporter_inventory import _previous_png_record_map

def _write_zip(
    zip_path: Path,
    records: list[dict[str, Any]],
    *,
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int | None = 9,
) -> None:
    """Support write zip behavior.
    
    Parameters
    ----------
    zip_path : Path
        The zip path value.
    records : list[dict[str, Any]]
        The record values.
    compression : int, optional
        The optional compression value.
    compresslevel : int | None, optional
        The optional compresslevel value.
    """
    
    kwargs: dict[str, Any] = {
        "mode": "w",
        "compression": compression,
        "allowZip64": True,
        "strict_timestamps": False,
    }
    if compresslevel is not None:
        kwargs["compresslevel"] = compresslevel
    with zipfile.ZipFile(zip_path, **kwargs) as archive:
        for record in records:
            archive.write(Path(str(record["absolute_path"])), arcname=str(record["path"]))

def _hash_zip_member(archive: zipfile.ZipFile, member: str) -> tuple[int, str]:
    digest = hashlib.sha256()
    total = 0
    with archive.open(member, "r") as source:
        while True:
            chunk = source.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            digest.update(chunk)
    return total, digest.hexdigest()


def _verify_archive_parts_content(
    destination_path: Path,
    part_records: list[dict[str, Any]],
    included_files: list[dict[str, Any]],
) -> None:
    """Prove each archive member matches the captured source inventory."""
    expected_by_part: dict[str, list[dict[str, Any]]] = {}
    for record in included_files:
        filename = str(record.get("part_filename", ""))
        if not filename:
            raise RuntimeError(
                "SOURCE_ARCHIVE_MEMBER_PART_MISSING:"
                + str(record.get("path", ""))
            )
        expected_by_part.setdefault(filename, []).append(record)

    for part in part_records:
        filename = str(part.get("filename", ""))
        zip_path = destination_path / filename
        expected = expected_by_part.get(filename, [])
        expected_paths = {str(item.get("path", "")) for item in expected}
        try:
            with zipfile.ZipFile(zip_path, "r") as archive:
                actual_paths = set(archive.namelist())
                if actual_paths != expected_paths:
                    raise RuntimeError(
                        "SOURCE_ARCHIVE_MEMBER_SET_MISMATCH:" + filename
                    )
                for record in expected:
                    member = str(record.get("path", ""))
                    size_bytes, digest = _hash_zip_member(archive, member)
                    if size_bytes != int(record.get("size_bytes", -1)):
                        raise RuntimeError(
                            "SOURCE_ARCHIVE_MEMBER_SIZE_MISMATCH:" + member
                        )
                    if digest != str(record.get("sha256", "")).lower():
                        raise RuntimeError(
                            "SOURCE_ARCHIVE_MEMBER_HASH_MISMATCH:" + member
                        )
        except (OSError, zipfile.BadZipFile, KeyError) as exc:
            raise RuntimeError(
                "SOURCE_ARCHIVE_CONTENT_VERIFICATION_FAILED:" + filename
            ) from exc


def _reuse_previous_png_asset_parts(
    *,
    context: ProjectContext,
    destination_path: Path,
    previous_output_dir: str | Path,
    previous_manifest: dict[str, Any],
    png_asset_files: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[Path], str]:
    """Support reuse previous png asset parts behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    destination_path : Path
        The destination path value.
    previous_output_dir : str | Path
        The previous output dir value.
    previous_manifest : dict[str, Any]
        The previous manifest value.
    png_asset_files : list[dict[str, Any]]
        The png asset files value.
    
    Returns
    -------
    tuple[list[dict[str, Any]], list[Path]]
        The tuple of values.
    """
    
    previous_dir = Path(previous_output_dir).expanduser().resolve(strict=False)
    previous_parts = [dict(item) for item in previous_manifest.get("png_asset_parts", []) if isinstance(item, dict)]
    current_by_path = {str(item.get("path", "")): item for item in png_asset_files}
    previous_by_path = _previous_png_record_map(previous_manifest)
    created_paths: list[Path] = []
    reuse_methods: set[str] = set()
    for previous_part in previous_parts:
        filename = str(previous_part["filename"])
        source_path = previous_dir / filename
        destination_zip = destination_path / filename
        if destination_zip.exists():
            destination_zip.unlink()
        try:
            os.link(source_path, destination_zip)
            reuse_method = "hardlink"
        except OSError:
            shutil.copy2(source_path, destination_zip)
            reuse_method = "copy"
        reuse_methods.add(reuse_method)
        stat = destination_zip.stat()
        previous_part["file_mtime_ns"] = int(stat.st_mtime_ns)
        previous_part["reuse_method"] = reuse_method
        created_paths.append(destination_zip)
    for path_text, current_record in current_by_path.items():
        previous_record = previous_by_path[path_text]
        current_record["archive_family"] = "png_assets"
        current_record["part"] = int(previous_record.get("part", 0))
        current_record["part_filename"] = str(previous_record.get("part_filename", ""))
    method = "hardlink" if reuse_methods == {"hardlink"} else "copy"
    return previous_parts, created_paths, method

def _write_archive_groups(
    *,
    context: ProjectContext,
    destination_path: Path,
    temp_path: Path,
    groups: list[list[dict[str, Any]]],
    hard_cap: int,
    filename_builder: Any,
    archive_family: str,
    package_name: str,
    compression: int,
    compresslevel: int | None,
) -> tuple[list[dict[str, Any]], list[Path]]:
    """Support write archive groups behavior.
    
    Parameters
    ----------
    context : ProjectContext
        The context value.
    destination_path : Path
        The destination path value.
    temp_path : Path
        The temp path value.
    groups : list[list[dict[str, Any]]]
        The groups value.
    hard_cap : int
        The hard cap value.
    filename_builder : Any
        The filename builder value.
    archive_family : str
        The archive family value.
    package_name : str
        The package name value.
    compression : int
        The compression value.
    compresslevel : int | None
        The compresslevel value.
    
    Returns
    -------
    tuple[list[dict[str, Any]], list[Path]]
        The tuple of values.
    """
    
    part_records: list[dict[str, Any]] = []
    created_paths: list[Path] = []
    total_parts = len(groups)
    for index, group in enumerate(groups, start=1):
        filename = filename_builder(context.project_slug, index, total_parts)
        temp_zip = temp_path / filename
        if temp_zip.exists():
            temp_zip.unlink()
        _write_zip(temp_zip, group, compression=compression, compresslevel=compresslevel)
        actual_size = temp_zip.stat().st_size
        if actual_size > hard_cap:
            raise ValueError(
                package_name
                + " ZIP part exceeded selected radio-button hard cap after write: "
                + filename
                + " ("
                + str(actual_size)
                + " > "
                + str(hard_cap)
                + ")"
            )
        final_zip = destination_path / filename
        if final_zip.exists():
            final_zip.unlink()
        shutil.move(str(temp_zip), str(final_zip))
        created_paths.append(final_zip)
        part_sha = sha256_file(final_zip)
        for record in group:
            record["archive_family"] = archive_family
            record["part"] = index
            record["part_filename"] = filename
        part_records.append(
            {
                "archive_family": archive_family,
                "part_number": index,
                "filename": filename,
                "path": "show_project_to_AI/second_prompt_files/" + filename,
                "actual_size_bytes": actual_size,
                "selected_size_cap_bytes": hard_cap,
                "file_count": len(group),
                "sha256": part_sha,
                "file_mtime_ns": int(final_zip.stat().st_mtime_ns),
                "reuse_method": "created",
            }
        )
    return part_records, created_paths
