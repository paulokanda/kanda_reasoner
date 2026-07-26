# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_freshness_helpers_private.py
"""Private helpers for Project Symbol Atlas evidence freshness."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .reference_folder_policy import (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
)
from .complete_json_adapter import (
    collect_reasoner_symbol_atlas_complete_json_files,
    load_reasoner_symbol_atlas_complete_json,
)
from .schemas import normalize_project_atlas_text

_STATUS_FRESH = "fresh"
_STATUS_JSON_CANONICAL = "json_canonical"
_STATUS_STALE = "stale"

__all__: list[str] = []


class _EvidenceSnapshot:
    """Represent evidence snapshot."""
    
    payload: dict[str, Any]
    json_path: Path
    project_root: str
    generated_at: str
    generated_dt: datetime | None
    evidence_files: tuple[str, ...]


def _select_json_path(project_root: Path, json_path: str) -> Path | None:
    """Support select json path behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    json_path : str
        The json path value.
    
    Returns
    -------
    Path | None
        The resolved path.
    """
    
    if json_path.strip():
        return Path(json_path).expanduser().resolve(strict=False)
    candidates = collect_reasoner_symbol_atlas_complete_json_files(project_root)
    return candidates[0] if candidates else None


def _load_snapshot(project_root: Path, json_path: Path) -> _EvidenceSnapshot:
    """Support load snapshot behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    json_path : Path
        The json path value.
    
    Returns
    -------
    _EvidenceSnapshot
        The evidence snapshot result.
    """
    
    try:
        payload = load_reasoner_symbol_atlas_complete_json(json_path)
    except ValueError as exc:
        raise ValueError(str(exc)) from exc
    source_index = payload.get("source_file_index")
    if not isinstance(source_index, dict):
        raise ValueError("Complete JSON evidence is missing source_file_index.")
    generated_at = _find_generated_at(payload)
    return _EvidenceSnapshot(
        payload=payload,
        json_path=json_path,
        project_root=_find_evidence_project_root(payload),
        generated_at=generated_at,
        generated_dt=_parse_generated_at(generated_at),
        evidence_files=_source_files_from_index(source_index, project_root),
    )


def _find_generated_at(payload: dict[str, Any]) -> str:
    """Support find generated at behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    candidates = (
        payload.get("generated_at"),
        payload.get("created_at"),
        _nested_value(payload, ("metadata", "generated_at")),
        _nested_value(payload, ("metadata", "created_at")),
        _nested_value(payload, ("runtime_trace", "generated_at")),
    )
    for candidate in candidates:
        text = normalize_project_atlas_text(candidate)
        if text:
            return text
    return ""


def _find_evidence_project_root(payload: dict[str, Any]) -> str:
    """Support find evidence project root behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    
    Returns
    -------
    str
        The string result.
    """
    
    candidates = (
        payload.get("project_root"),
        _nested_value(payload, ("metadata", "project_root")),
        _nested_value(payload, ("runtime_trace", "project_root")),
    )
    for candidate in candidates:
        text = normalize_project_atlas_text(candidate)
        if text:
            return text
    return ""


def _nested_value(payload: dict[str, Any], keys: tuple[str, ...]) -> object:
    """Support nested value behavior.
    
    Parameters
    ----------
    payload : dict[str, Any]
        The payload value.
    keys : tuple[str, ...]
        The key values.
    
    Returns
    -------
    object
        The object result.
    """
    
    value: object = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def _parse_generated_at(value: str) -> datetime | None:
    """Support parse generated at behavior.
    
    Parameters
    ----------
    value : str
        The input value.
    
    Returns
    -------
    datetime | None
        The datetime result.
    """
    
    text = normalize_project_atlas_text(value)
    if not text:
        return None
    normalized = text.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _source_files_from_index(source_index: dict[str, Any], project_root: Path) -> tuple[str, ...]:
    """Support source files from index behavior.
    
    Parameters
    ----------
    source_index : dict[str, Any]
        The source index value.
    project_root : Path
        The project root path.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    paths: list[str] = []
    for key, value in source_index.items():
        path_text = ""
        if isinstance(value, dict):
            path_text = normalize_project_atlas_text(
                value.get("file") or value.get("path") or value.get("relative_path")
            )
        if not path_text:
            path_text = normalize_project_atlas_text(key)
        relative = _as_project_relative_path(project_root, path_text)
        if relative and relative.endswith(".py"):
            paths.append(relative)
    return tuple(sorted(set(paths)))


def _collect_live_files(
    project_root: Path,
    include_non_python_files: bool,
) -> dict[str, datetime]:
    """Support collect live files behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    include_non_python_files : bool
        The include non python files value.
    
    Returns
    -------
    dict[str, datetime]
        The mapped values.
    """
    
    result: dict[str, datetime] = {}
    pattern = "*" if include_non_python_files else "*.py"
    for path in project_root.rglob(pattern):
        if not path.is_file() or _should_skip(path, project_root):
            continue
        relative = path.relative_to(project_root).as_posix()
        result[relative] = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return result


def _should_skip(path: Path, project_root: Path) -> bool:
    """Support should skip behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    project_root : Path
        The project root path.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        parts = path.relative_to(project_root).parts
    except ValueError:
        return True
    skipped = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "build",
        "dist",
        "venv",
        ".venv",
        "env",
        "node_modules",
        "workbench",
        "project_analysis_evidence",
        *PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
        "snippets",
        "DEVELOPER_TOOLS_older",
        "legacy_cleanup",
        "oldies_deprecated",
        "older_deprecated",
        "tests_migrated_architecture",
    }
    noisy_markers = (
        "deprecated",
        "older",
        "oldies",
        "backup",
        "scratch",
        "copy",
    )
    for part in parts:
        if part in skipped:
            return True
        lowered = part.lower()
        if lowered.startswith("_tmp_") or lowered.startswith("tmp_"):
            return True
        if any(marker in lowered for marker in noisy_markers):
            return True
    return False


def _modified_after_generation(
    live_files: dict[str, datetime],
    evidence_files: set[str],
    generated_dt: datetime | None,
    limit: int,
) -> tuple[str, ...]:
    """Support modified after generation behavior.
    
    Parameters
    ----------
    live_files : dict[str, datetime]
        The live files value.
    evidence_files : set[str]
        The evidence files value.
    generated_dt : datetime | None
        The generated dt value.
    limit : int
        The limit value.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    if generated_dt is None:
        return ()
    modified = [
        path
        for path, mtime in live_files.items()
        if path in evidence_files and mtime > generated_dt
    ]
    return tuple(sorted(modified)[:limit])


def _classify_freshness(
    generated_dt: datetime | None,
    missing: tuple[str, ...],
    new_files: tuple[str, ...],
    modified: tuple[str, ...],
) -> tuple[str, tuple[str, ...]]:
    """Support classify freshness behavior.
    
    Parameters
    ----------
    generated_dt : datetime | None
        The generated dt value.
    missing : tuple[str, ...]
        The missing value.
    new_files : tuple[str, ...]
        The new files value.
    modified : tuple[str, ...]
        The modified value.
    
    Returns
    -------
    tuple[str, tuple[str, ...]]
        The tuple of values.
    """
    
    if missing or modified:
        notes = ["Canonical JSON conflicts with the live source tree."]
        if missing:
            notes.append("Some files recorded in evidence are missing from live source.")
        if modified:
            notes.append("Some live files were modified after evidence generation.")
        return PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_STALE, tuple(notes)
    if new_files:
        return (
            PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL,
            (
                "Complete JSON is authoritative; live-only files are post-evidence candidates.",
                "Use Tab 4/5 again only when those files should become canonical project evidence.",
            ),
        )
    if generated_dt is None:
        return (
            PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_JSON_CANONICAL,
            ("Complete JSON is authoritative; generated_at was not parseable.",),
        )
    return (
        PROJECT_SYMBOL_ATLAS_EVIDENCE_STATUS_FRESH,
        ("Evidence matches the live source tree checks performed.",),
    )


def _as_project_relative_path(project_root: Path, path_text: str) -> str:
    """Support as project relative path behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    path_text : str
        The path text value.
    
    Returns
    -------
    str
        The string result.
    """
    
    if not path_text:
        return ""
    candidate = Path(path_text)
    if candidate.is_absolute():
        try:
            return candidate.resolve(strict=False).relative_to(project_root).as_posix()
        except ValueError:
            return candidate.as_posix()
    return candidate.as_posix()


def _same_project_root(project_root: Path, evidence_root: str) -> bool:
    """Support same project root behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    evidence_root : str
        The evidence root value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    try:
        expected = project_root.resolve(strict=False)
        actual = Path(evidence_root).expanduser().resolve(strict=False)
    except OSError:
        return False
    return str(expected).casefold() == str(actual).casefold()
