"""Data models for KANDA Reasoner Portable creation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProtectedRoot:
    """One governed owner root that Portable direct writes must not enter."""

    label: str
    owner_id: str
    owner_slug: str
    root_kind: str
    path: Path


@dataclass(frozen=True)
class RegistryBoundary:
    """Tool-owned build authority plus optional registry destination firewall."""

    registry_path: Path
    registry_sha256: str
    current_project_id: str
    selection_mode: str
    tool_root: Path
    tool_support_root: Path
    tool_transient_root: Path
    protected_roots: tuple[ProtectedRoot, ...]
    tool_owner_roots: tuple[ProtectedRoot, ...]

    @property
    def selected_owner_roots(self) -> tuple[ProtectedRoot, ...]:
        """Compatibility alias; Portable mutation scope is always Tool-owned."""

        return self.tool_owner_roots


@dataclass(frozen=True)
class BuildPaths:
    """Resolved Tool, staging, publication, and registry-boundary paths."""

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
    registry_boundary: RegistryBoundary | None = None


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
