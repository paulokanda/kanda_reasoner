"""Internal ZIP writer helpers for JSON handoff export."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Any

from .handoff_zip_exporter_support import (
    artifact_record,
    external_readme_text,
    package_readme_text,
    safe_zip_member_name,
)
from .hashing import sha256_file
from .path_normalization import relative_posix_path
from .schema_models import ProjectContext

__all__ = [
    "candidate_zip_size",
    "split_artifacts_into_parts",
    "write_external_readme",
    "write_package_parts",
    "write_zip",
    "zip_record",
]


def write_zip(
    zip_path: Path,
    artifacts: list[Path],
    context: ProjectContext,
    base_folder: str,
    *,
    readme_text: str | None = None,
    readme_name: str = "UPLOAD_README.txt",
) -> None:
    """Write one standalone ZIP file."""
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        if readme_text is not None:
            archive.writestr(base_folder + "/" + readme_name, readme_text)
        for artifact in artifacts:
            archive.write(artifact, arcname=safe_zip_member_name(base_folder, artifact, context))


def candidate_zip_size(
    artifacts: list[Path],
    context: ProjectContext,
    temp_dir: Path,
    *,
    base_folder: str,
    readme_text: str,
    readme_name: str,
) -> int:
    """Return compressed size for a candidate package part."""
    candidate = temp_dir / "candidate.zip"
    if candidate.exists():
        candidate.unlink()
    write_zip(
        candidate,
        artifacts,
        context,
        base_folder,
        readme_text=readme_text,
        readme_name=readme_name,
    )
    return candidate.stat().st_size


def split_artifacts_into_parts(
    artifacts: list[Path],
    context: ProjectContext,
    part_size_bytes: int,
    temp_dir: Path,
    base_folder: str,
    *,
    readme_text: str,
    readme_name: str,
) -> tuple[list[list[Path]], list[str]]:
    """Split artifacts into standalone ZIP-compatible groups."""
    parts: list[list[Path]] = []
    current: list[Path] = []
    warnings: list[str] = []

    for artifact in artifacts:
        candidate = current + [artifact]
        candidate_size = candidate_zip_size(
            candidate,
            context,
            temp_dir,
            base_folder=base_folder,
            readme_text=readme_text,
            readme_name=readme_name,
        )
        if candidate_size <= part_size_bytes or not current:
            current = candidate
            if candidate_size > part_size_bytes:
                warnings.append(
                    "Single artifact compressed above target size: "
                    + relative_posix_path(artifact, context.root)
                )
            continue
        parts.append(current)
        current = [artifact]
        single_size = candidate_zip_size(
            current,
            context,
            temp_dir,
            base_folder=base_folder,
            readme_text=readme_text,
            readme_name=readme_name,
        )
        if single_size > part_size_bytes:
            warnings.append(
                "Single artifact compressed above target size: "
                + relative_posix_path(artifact, context.root)
            )

    if current:
        parts.append(current)
    return parts, warnings


def zip_record(
    path: Path,
    artifacts: list[Path],
    context: ProjectContext,
    package_name: str,
) -> dict[str, Any]:
    """Return metadata for one generated ZIP part."""
    return {
        "package": package_name,
        "filename": path.name,
        "path": str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "artifact_count": len(artifacts),
        "artifacts": [artifact_record(artifact, context) for artifact in artifacts],
    }


def write_package_parts(
    spec: dict[str, Any],
    context: ProjectContext,
    destination: Path,
    temp_root: Path,
    part_size_mb: int,
    part_size_bytes: int,
) -> tuple[list[dict[str, Any]], list[str], list[Path]]:
    """Write all standalone ZIP parts for one package spec."""
    stem = str(spec["stem"])
    package_name = str(spec["name"])
    artifacts = list(spec["artifacts"])
    readme_name = str(spec["readme_name"])
    placeholder_readme = package_readme_text(
        context,
        package_name,
        str(spec["purpose"]),
        "1",
        1,
        part_size_mb,
    )
    parts, warnings = split_artifacts_into_parts(
        artifacts,
        context,
        part_size_bytes,
        temp_root,
        stem,
        readme_text=placeholder_readme,
        readme_name=readme_name,
    )

    total_parts = len(parts)
    final_records: list[dict[str, Any]] = []
    created_paths: list[Path] = []
    for index, part_artifacts in enumerate(parts, start=1):
        if total_parts == 1:
            filename = stem + ".zip"
            part_label = "1"
        else:
            part_label = str(index).zfill(2)
            filename = stem + "_part" + part_label + "_of_" + str(total_parts).zfill(2) + ".zip"
        temp_zip = temp_root / filename
        readme = package_readme_text(
            context,
            package_name,
            str(spec["purpose"]),
            part_label,
            total_parts,
            part_size_mb,
        )
        write_zip(
            temp_zip,
            part_artifacts,
            context,
            stem,
            readme_text=readme,
            readme_name=readme_name,
        )
        final_zip = destination / filename
        if final_zip.exists():
            final_zip.unlink()
        shutil.move(str(temp_zip), str(final_zip))
        created_paths.append(final_zip)
        final_records.append(zip_record(final_zip, part_artifacts, context, package_name))
    return final_records, warnings, created_paths


def write_external_readme(destination: Path, context: ProjectContext, part_size_mb: int) -> dict[str, Any]:
    """Write the external upload README and return its metadata."""
    readme_path = destination / (context.project_slug + "__ai_handoff_upload_readme.txt")
    readme_path.write_text(external_readme_text(context, part_size_mb), encoding="utf-8")
    return {
        "filename": readme_path.name,
        "path": str(readme_path),
        "size_bytes": readme_path.stat().st_size,
        "sha256": sha256_file(readme_path),
    }
