# project-path: kanda_reasoner_app/reasoner_symbol_atlas/evidence_freshness_helpers_private.py
"""Private helpers for Project Symbol Atlas evidence freshness."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.reasoner_context_collector import (
    collect_canonical_project_python_files,
)

from .reference_folder_policy import (
    PROJECT_SYMBOL_ATLAS_INACTIVE_REFERENCE_FOLDERS,
)
from .complete_json_adapter import (
    load_reasoner_symbol_atlas_complete_json,
    resolve_reasoner_symbol_atlas_complete_json_path,
)
from .schemas import normalize_project_atlas_text

_STATUS_FRESH = "fresh"
_STATUS_JSON_CANONICAL = "json_canonical"
_STATUS_STALE = "stale"

__all__: list[str] = []


@dataclass(frozen=True)
class _EvidenceSnapshot:
    """Represent evidence snapshot."""
    
    payload: dict[str, Any]
    json_path: Path
    project_root: str
    generated_at: str
    generated_dt: datetime | None
    evidence_files: tuple[str, ...]
    evidence_hashes: dict[str, str]


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
    
    return resolve_reasoner_symbol_atlas_complete_json_path(
        project_root,
        json_path or None,
    )


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
        evidence_hashes=_source_hashes_from_index(source_index, project_root),
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
        payload.get("generated_at_utc"),
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


def _source_hashes_from_index(
    source_index: dict[str, Any],
    project_root: Path,
) -> dict[str, str]:
    """Return canonical SHA-256 values keyed by project-relative Python path."""

    hashes: dict[str, str] = {}
    for key, value in source_index.items():
        if not isinstance(value, dict):
            continue
        path_text = normalize_project_atlas_text(
            value.get("file") or value.get("path") or value.get("relative_path") or key
        )
        relative = _as_project_relative_path(project_root, path_text)
        digest = normalize_project_atlas_text(
            value.get("sha256") or value.get("file_sha256")
        ).lower()
        if (
            relative
            and relative.endswith(".py")
            and len(digest) == 64
            and all(char in "0123456789abcdef" for char in digest)
        ):
            hashes[relative] = digest
    return hashes


def _collect_live_files(
    project_root: Path,
    include_non_python_files: bool,
) -> dict[str, datetime]:
    """Collect live files using the canonical complete-JSON Python scope by default."""

    result: dict[str, datetime] = {}
    if not include_non_python_files:
        candidates = collect_canonical_project_python_files(project_root)
    else:
        candidates = tuple(
            path
            for path in project_root.rglob("*")
            if path.is_file() and not _should_skip(path, project_root)
        )

    for path in candidates:
        try:
            relative = path.relative_to(project_root).as_posix()
            modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except (OSError, ValueError):
            continue
        result[relative] = modified
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
    limit: int | None,
    *,
    project_root: Path | None = None,
    evidence_hashes: dict[str, str] | None = None,
) -> tuple[str, ...]:
    """Return true post-generation content changes, using mtime only as a candidate gate."""

    if generated_dt is None:
        return ()
    precision_tolerance = (
        timedelta(seconds=1) if generated_dt.microsecond == 0 else timedelta(0)
    )
    threshold = generated_dt + precision_tolerance
    hashes = evidence_hashes or {}
    modified: list[str] = []

    for relative, mtime in live_files.items():
        if relative not in evidence_files or mtime <= threshold:
            continue
        evidence_hash = hashes.get(relative, "")
        if evidence_hash and project_root is not None:
            live_hash = _sha256_file(project_root / relative)
            if live_hash and live_hash == evidence_hash:
                continue
        modified.append(relative)

    ordered = tuple(sorted(modified))
    return ordered if limit is None else ordered[: max(0, int(limit))]


def _sha256_file(path: Path) -> str:
    """Return the SHA-256 of one live source file, or empty text on read failure."""

    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return ""
    return digest.hexdigest()


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
        return _STATUS_STALE, tuple(notes)
    if new_files:
        return (
            _STATUS_JSON_CANONICAL,
            (
                "Complete JSON is authoritative; live-only files are post-evidence candidates.",
                "Use Tab 4/5 again only when those files should become canonical project evidence.",
            ),
        )
    if generated_dt is None:
        return (
            _STATUS_JSON_CANONICAL,
            ("Complete JSON is authoritative; generated_at was not parseable.",),
        )
    return (
        _STATUS_FRESH,
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
