# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_project_support_paths.py
"""Project-owned support paths for the Large File Refactor Workbench."""
from __future__ import annotations

import hashlib
from pathlib import Path

from kanda_reasoner_app.project_support_boundary import (
    assert_no_forbidden_nested_support_root,
    canonical_transient_garbage_root,
)

__all__ = [
    "ai_refactoring_card_exchange_root",
    "analyzer_cache_root",
    "analyzer_engine_cache_root",
    "ai_refactoring_exchange_root",
    "daily_work_root",
    "analyzer_cache_root_blockers",
    "exchange_root_blockers",
    "preview_root_blockers",
    "preview_runs_root",
    "project_support_root",
    "quality_evidence_root",
    "quality_evidence_root_blockers",
    "resolve_workbench_preview_root",
    "shadow_runs_root",
    "workbench_path_class",
    "workbench_support_root",
]

_WORKBENCH_SUPPORT_DIR = "large_file_refactor_workbench"
_PREVIEW_DIR = "preview"
_QUALITY_EVIDENCE_DIR = "quality_evidence"
_AI_EXCHANGE_DIR = "ai_refactoring_exchange"
_ANALYZER_CACHE_DIR = "analyzer_cache"
_FORBIDDEN_SUPPORT_CHILDREN = {
    "project_error_memory",
    "project_freeze_after_update",
    "project_freeze_ledger",
}


def project_support_root(active_project_root: str | Path) -> Path:
    """Return the dynamic external support root for the selected project."""
    return assert_no_forbidden_nested_support_root(active_project_root)


def workbench_support_root(active_project_root: str | Path) -> Path:
    """Return the project-owned support box for this Workbench."""
    return project_support_root(active_project_root) / _WORKBENCH_SUPPORT_DIR


def quality_evidence_root(active_project_root: str | Path) -> Path:
    """Return durable Project-owned Advanced Quality Review evidence root."""
    return workbench_support_root(active_project_root) / _QUALITY_EVIDENCE_DIR


def quality_evidence_root_blockers(
    active_project_root: str | Path,
    candidate: str | Path,
) -> list[str]:
    """Return blockers when durable quality evidence escapes Project Support."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    path = Path(candidate).expanduser().resolve(strict=False)
    blockers: list[str] = []
    if _is_relative_to(path, project_root):
        blockers.append("QUALITY_EVIDENCE_INSIDE_PROJECT_SOURCE")
    if _is_relative_to(path, daily_work_root(project_root)):
        blockers.append("QUALITY_EVIDENCE_INSIDE_DAILY_WORK_GARBAGE")
    if not _is_relative_to(path, quality_evidence_root(project_root)):
        blockers.append("QUALITY_EVIDENCE_OUTSIDE_PROJECT_SUPPORT_ROOT")
    lowered = {part.lower() for part in path.parts}
    for forbidden in _FORBIDDEN_SUPPORT_CHILDREN:
        if forbidden in lowered:
            blockers.append(
                "QUALITY_EVIDENCE_INSIDE_PROTECTED_" + forbidden.upper()
            )
    return sorted(set(blockers))


def ai_refactoring_exchange_root(active_project_root: str | Path) -> Path:
    """Return durable Project-owned external AI exchange root."""
    return workbench_support_root(active_project_root) / _AI_EXCHANGE_DIR


def ai_refactoring_card_exchange_root(
    active_project_root: str | Path,
    project_card_identity: str,
) -> Path:
    """Return one card-specific external AI exchange folder without creating it."""
    safe_card_id = _safe_support_id(project_card_identity, "PROJECT_CARD_ID")
    return ai_refactoring_exchange_root(active_project_root) / safe_card_id


def exchange_root_blockers(
    active_project_root: str | Path,
    exchange_root: str | Path,
) -> list[str]:
    """Return ownership blockers for one Project-owned external AI exchange path."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    root = Path(exchange_root).expanduser().resolve(strict=False)
    blockers: list[str] = []
    if _is_relative_to(root, project_root):
        blockers.append("AI_EXCHANGE_ROOT_INSIDE_PROJECT_SOURCE")
    if not _is_relative_to(root, ai_refactoring_exchange_root(project_root)):
        blockers.append("AI_EXCHANGE_ROOT_OUTSIDE_PROJECT_SUPPORT")
    lowered = {part.lower() for part in root.parts}
    for forbidden in _FORBIDDEN_SUPPORT_CHILDREN:
        if forbidden in lowered:
            blockers.append("AI_EXCHANGE_ROOT_INSIDE_PROTECTED_" + forbidden.upper())
    return sorted(set(blockers))



def daily_work_root(active_project_root: str | Path) -> Path:
    """Return the canonical external transient garbage root."""
    return canonical_transient_garbage_root(active_project_root)



def analyzer_cache_root(active_project_root: str | Path) -> Path:
    """Return the disposable analyzer cache root under daily-work garbage."""
    return daily_work_root(active_project_root) / _ANALYZER_CACHE_DIR


def analyzer_engine_cache_root(
    active_project_root: str | Path,
    *,
    engine_id: str,
    engine_version: str,
    config_hash: str,
    analysis_key: str,
) -> Path:
    """Return one deterministic regenerable analyzer cache path."""
    engine = _safe_support_id(engine_id, "ANALYZER_ENGINE_ID")
    version = _safe_support_id(engine_version, "ANALYZER_ENGINE_VERSION")
    config = _safe_support_id(config_hash, "ANALYZER_CONFIG_HASH")
    analysis = _safe_support_id(analysis_key, "ANALYZER_ANALYSIS_KEY")
    return analyzer_cache_root(active_project_root) / engine / version / config / analysis


def analyzer_cache_root_blockers(
    active_project_root: str | Path,
    candidate: str | Path,
) -> list[str]:
    """Return blockers when analyzer cache escapes disposable daily-work ownership."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    path = Path(candidate).expanduser().resolve(strict=False)
    blockers: list[str] = []
    if _is_relative_to(path, project_root):
        blockers.append("ANALYZER_CACHE_INSIDE_PROJECT_SOURCE")
    if _is_relative_to(path, workbench_support_root(project_root)):
        blockers.append("ANALYZER_CACHE_INSIDE_PROJECT_SUPPORT")
    if not _is_relative_to(path, analyzer_cache_root(project_root)):
        blockers.append("ANALYZER_CACHE_OUTSIDE_DAILY_WORK_CACHE_ROOT")
    return sorted(set(blockers))

def shadow_runs_root(active_project_root: str | Path) -> Path:
    """Return the disposable Shadow root; Shadow is not project support state."""
    return daily_work_root(active_project_root) / "large_file_refactor_shadow"

def preview_runs_root(active_project_root: str | Path) -> Path:
    """Return the project-owned root for persistent Workbench Preview files."""
    return workbench_support_root(active_project_root) / _PREVIEW_DIR


def resolve_workbench_preview_root(
    active_project_root: str | Path,
    preview_id: str = "",
) -> Path:
    """Return one deterministic project-owned Preview root without creating it."""
    root = Path(active_project_root).expanduser().resolve(strict=False)
    selected_id = preview_id.strip() or hashlib.sha256(
        str(root).encode("utf-8")
    ).hexdigest()[:12]
    safe_id = _safe_preview_id(selected_id)
    return preview_runs_root(root) / safe_id


def preview_root_blockers(
    active_project_root: str | Path,
    preview_root: str | Path,
) -> list[str]:
    """Return ownership blockers for one project-specific Preview root."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    root = Path(preview_root).expanduser().resolve(strict=False)
    blockers: list[str] = []
    if _is_relative_to(root, project_root):
        blockers.append("PREVIEW_ROOT_INSIDE_PROJECT_SOURCE")
    if not _is_relative_to(root, preview_runs_root(project_root)):
        blockers.append("PREVIEW_ROOT_OUTSIDE_PROJECT_SUPPORT")
    lowered = {part.lower() for part in root.parts}
    for forbidden in _FORBIDDEN_SUPPORT_CHILDREN:
        if forbidden in lowered:
            blockers.append("PREVIEW_ROOT_INSIDE_PROTECTED_" + forbidden.upper())
    return sorted(set(blockers))



def workbench_path_class(
    active_project_root: str | Path,
    candidate: str | Path,
) -> str:
    """Classify a Workbench path without collapsing tool/project boundaries."""
    project_root = Path(active_project_root).expanduser().resolve(strict=False)
    path = Path(candidate).expanduser().resolve(strict=False)
    if _is_relative_to(path, project_root):
        return "active_project_source"
    if _is_relative_to(path, preview_runs_root(project_root)):
        return "active_project_preview_support"
    if _is_relative_to(path, workbench_support_root(project_root)):
        return "active_project_workbench_support"
    if _is_relative_to(path, daily_work_root(project_root)):
        return "daily_work_garbage"
    return "outside_active_project_boxes"

def _safe_preview_id(value: str) -> str:
    """Return a filesystem-safe Preview identifier."""
    return _safe_support_id(value, "PREVIEW_ID")


def _safe_support_id(value: str, label: str) -> str:
    """Return one bounded filesystem-safe Project Support identifier."""
    cleaned = "".join(
        character if character.isalnum() or character in {"-", "_"} else "_"
        for character in str(value or "")
    ).strip("_-.")
    if not cleaned:
        raise ValueError(label + "_EMPTY_AFTER_SANITIZATION")
    return cleaned[:96]


def _is_relative_to(path: Path, base: Path) -> bool:
    """Return whether path is contained by base after resolution."""
    try:
        path.resolve(strict=False).relative_to(base.resolve(strict=False))
        return True
    except ValueError:
        return False
