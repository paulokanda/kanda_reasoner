# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/analyzer_tool_runtime_paths.py
"""Resolve the separate Tool-owned runtime container for analyzer binaries."""
from __future__ import annotations

import os
from pathlib import Path

from .workbench_project_support_paths import daily_work_root, project_support_root

__all__ = [
    "ANALYZER_ENVIRONMENT_SLOT",
    "ANALYZER_RUNTIME_NAMESPACE",
    "TOOL_RUNTIME_ROOT_SUFFIX",
    "analyzer_environment_freeze_path",
    "analyzer_environment_install_report_path",
    "analyzer_environment_manifest_path",
    "analyzer_environment_python",
    "analyzer_environment_requirements_copy_path",
    "analyzer_environment_root",
    "analyzer_environment_script",
    "analyzer_tool_runtime_root",
    "analyzer_tool_runtime_root_blockers",
]

TOOL_RUNTIME_ROOT_SUFFIX = "_tool_runtime"
ANALYZER_RUNTIME_NAMESPACE = "advanced_quality_review_analyzers"
ANALYZER_ENVIRONMENT_SLOT = "v1"


def analyzer_tool_runtime_root(tool_root: str | Path) -> Path:
    """Return the separate sibling container owned by KANDA Tool runtime state."""
    source_root = Path(tool_root).expanduser().resolve(strict=False)
    return source_root.parent / (source_root.name + TOOL_RUNTIME_ROOT_SUFFIX)


def analyzer_environment_root(tool_root: str | Path) -> Path:
    """Return the pinned Advanced Quality Review virtual-environment root."""
    return (
        analyzer_tool_runtime_root(tool_root)
        / ANALYZER_RUNTIME_NAMESPACE
        / ANALYZER_ENVIRONMENT_SLOT
        / "environment"
    )


def analyzer_environment_python(tool_root: str | Path) -> Path:
    """Return the environment Python executable path for the current platform."""
    root = analyzer_environment_root(tool_root)
    if os.name == "nt":
        return root / "Scripts" / "python.exe"
    return root / "bin" / "python"


def analyzer_environment_script(tool_root: str | Path, script_name: str) -> Path:
    """Return one environment console-script path without PATH lookup."""
    name = str(script_name or "").strip()
    if not name or Path(name).name != name:
        raise ValueError("ANALYZER_SCRIPT_NAME_INVALID")
    root = analyzer_environment_root(tool_root)
    if os.name == "nt":
        suffix = "" if name.lower().endswith(".exe") else ".exe"
        return root / "Scripts" / (name + suffix)
    return root / "bin" / name


def analyzer_environment_manifest_path(tool_root: str | Path) -> Path:
    """Return the durable Tool-runtime manifest path for the installed environment."""
    return _metadata_root(tool_root) / "environment_manifest.json"


def analyzer_environment_freeze_path(tool_root: str | Path) -> Path:
    """Return the resolved full-distribution lock snapshot path."""
    return _metadata_root(tool_root) / "installed_packages.freeze.txt"


def analyzer_environment_install_report_path(tool_root: str | Path) -> Path:
    """Return the pip installation report path owned by Tool runtime support."""
    return _metadata_root(tool_root) / "pip_install_report.json"


def analyzer_environment_requirements_copy_path(tool_root: str | Path) -> Path:
    """Return the copied exact top-level analyzer requirement specification path."""
    return _metadata_root(tool_root) / "analyzer_requirements.lock.txt"


def analyzer_tool_runtime_root_blockers(
    tool_root: str | Path,
    candidate: str | Path,
    *,
    active_project_root: str | Path | None = None,
) -> tuple[str, ...]:
    """Return blockers when Tool runtime support leaks into Project-owned containers."""
    source_root = Path(tool_root).expanduser().resolve(strict=False)
    runtime_root = analyzer_tool_runtime_root(source_root).resolve(strict=False)
    checked = Path(candidate).expanduser().resolve(strict=False)
    blockers: list[str] = []
    if not _is_within(checked, runtime_root):
        blockers.append("ANALYZER_RUNTIME_OUTSIDE_TOOL_RUNTIME_CONTAINER")
    if _is_within(checked, source_root):
        blockers.append("ANALYZER_RUNTIME_INSIDE_TOOL_SOURCE_ROOT")
    if active_project_root is not None:
        project_root = Path(active_project_root).expanduser().resolve(strict=False)
        support_root = project_support_root(project_root).resolve(strict=False)
        garbage_root = daily_work_root(project_root).resolve(strict=False)
        if _is_within(checked, project_root):
            blockers.append("ANALYZER_RUNTIME_INSIDE_PROJECT_SOURCE_ROOT")
        if _is_within(checked, support_root):
            blockers.append("ANALYZER_RUNTIME_INSIDE_PROJECT_SUPPORT_ROOT")
        if _is_within(checked, garbage_root):
            blockers.append("ANALYZER_RUNTIME_INSIDE_PROJECT_DAILY_WORK_ROOT")
    return tuple(sorted(set(blockers)))


def _metadata_root(tool_root: str | Path) -> Path:
    """Return metadata root adjacent to, but outside, the virtual environment."""
    return analyzer_environment_root(tool_root).parent / "metadata"


def _is_within(candidate: Path, owner: Path) -> bool:
    """Return whether candidate is owner or a descendant of owner."""
    try:
        candidate.relative_to(owner)
    except ValueError:
        return False
    return True
