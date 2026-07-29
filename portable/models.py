"""Data models for Portable creation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BuildPaths:
    """Resolved project, staging, and publication paths."""

    project_root: Path
    drive_root: Path
    project_support_root: Path
    transient_root: Path
    run_root: Path
    pyinstaller_work: Path
    pyinstaller_dist: Path
    pyinstaller_config: Path
    temporary_root: Path
    stage_parent: Path
    candidate_zip: Path
    clean_extract_root: Path
    final_zip: Path
    spec_path: Path
    governed_python: Path
    zip_helper: Path


@dataclass(frozen=True)
class BuiltApplication:
    """Detected one-folder application output."""

    app_root: Path
    executable: Path


@dataclass(frozen=True)
class ZipEvidence:
    """Validated evidence for a Portable ZIP."""

    size_bytes: int
    sha256: str
    member_count: int
    maximum_path_bytes: int
    top_level_name: str
