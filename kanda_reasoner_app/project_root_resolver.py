# project-path: kanda_reasoner_app/project_root_resolver.py
"""Project-root resolution helpers for source and compiled execution.

The helpers in this module keep project identity dynamic. They must not
hardcode one project folder name as the active root. The current Kanda Reasoner
source tree can be selected, but the same code must also work when the tool is
used against another project root.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable

from kanda_reasoner_app._project_support_path_contracts import (
    _canonical_transient_garbage_root,
)

__all__ = [
    "CANONICAL_PROJECT_ROOT_ENV",
    "PROJECT_ROOT_ENV_NAMES",
    "default_smoke_output_json_path",
    "find_reasoner_source_root",
    "is_reasoner_project_root",
    "normalize_project_root_text",
    "resolve_active_project_root",
    "resolve_observed_project_root",
    "resolve_selected_project_root",
    "resolve_app_runtime_root",
]

CANONICAL_PROJECT_ROOT_ENV = "kanda_reasoner_project_root"
PROJECT_ROOT_ENV_NAMES = (
    CANONICAL_PROJECT_ROOT_ENV,
    "KANDA_REASONER_PROJECT_ROOT",
    "KANDA_RUNTIME_PROJECT_ROOT",
    "PROJECT_REASONER_PROJECT_ROOT",
    "PROJECT_REASONER_SCAN_ROOT",
    "KANDA_REASONER_SCAN_ROOT",
)
_CANONICAL_REASONER_PACKAGE_NAME = "kanda_reasoner_app"
_LEGACY_REASONER_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))
_REASONER_PACKAGE_NAMES = (
    _CANONICAL_REASONER_PACKAGE_NAME,
    _LEGACY_REASONER_PACKAGE_NAME,
)
_REASONER_ENTRYPOINT_NAME = "reasoner_tools_gui.py"


def _path_from_text(value: object) -> Path | None:
    """Return a Path for a non-empty value, or None."""
    text = str(value or "").strip()
    if not text:
        return None
    return Path(text).expanduser()


def _looks_like_windows_absolute_path(value: object) -> bool:
    """Return True for drive-qualified Windows paths on any platform."""
    text = str(value or "").strip()
    return len(text) >= 3 and text[1] == ":" and text[2] in ("\\", "/")


def _safe_resolve(path: Path) -> Path:
    """Resolve a path while tolerating missing folders and bad anchors."""
    if os.name != "nt" and _looks_like_windows_absolute_path(path):
        return path
    try:
        return path.resolve()
    except Exception:
        try:
            return path.absolute()
        except Exception:
            return path


def _iter_parent_candidates(start: Path) -> Iterable[Path]:
    """Yield a path and its parents from a filesystem anchor candidate."""
    resolved = _safe_resolve(start)
    if resolved.is_file():
        resolved = resolved.parent
    yield resolved
    yield from resolved.parents


def is_reasoner_project_root(project_root: str | Path | None) -> bool:
    """Return True when project_root appears to be the Reasoner source tree."""
    if project_root is None:
        return False
    root = _safe_resolve(Path(project_root).expanduser())
    if (root / _REASONER_ENTRYPOINT_NAME).is_file():
        for package_name in _REASONER_PACKAGE_NAMES:
            if (root / package_name).is_dir():
                return True
    if root.name in _REASONER_PACKAGE_NAMES:
        return (root / "__init__.py").is_file()
    return False



def find_reasoner_source_root(start: str | Path | None = None) -> Path | None:
    """Find the nearest Reasoner source-tree root from start or this module."""
    starts: list[Path] = []
    explicit = _path_from_text(start)
    if explicit is not None:
        starts.append(explicit)
    starts.append(Path(__file__))
    starts.append(Path.cwd())

    for candidate_start in starts:
        for candidate in _iter_parent_candidates(candidate_start):
            if candidate.name in _REASONER_PACKAGE_NAMES:
                parent = candidate.parent
                if is_reasoner_project_root(parent):
                    return _safe_resolve(parent)
            if is_reasoner_project_root(candidate):
                return _safe_resolve(candidate)
    return None


def resolve_app_runtime_root() -> Path:
    """Return the folder that owns the running source tree or executable."""
    source_root = find_reasoner_source_root()
    if source_root is not None:
        return source_root
    executable = _safe_resolve(Path(sys.executable).expanduser())
    if executable.is_file():
        return executable.parent
    return _safe_resolve(Path.cwd())


def _env_project_root() -> Path | None:
    """Return the first configured project root from supported env variables."""
    for env_name in PROJECT_ROOT_ENV_NAMES:
        value = os.environ.get(env_name, "").strip()
        if value:
            return _safe_resolve(Path(value).expanduser())
    return None


def _usable_persisted_root(path: Path | None, source_root: Path | None) -> Path | None:
    """Return a safe persisted root without relying on retired project names."""
    if path is None:
        return None
    resolved = _safe_resolve(path)
    if not resolved.exists():
        return None
    return resolved


def normalize_project_root_text(text: str | Path | None) -> Path | None:
    """Normalize user-entered project-root text without assuming a fixed name."""
    path = _path_from_text(text)
    if path is None:
        return None
    if os.name != "nt" and _looks_like_windows_absolute_path(path):
        return path
    candidate = _safe_resolve(path)
    try:
        anchor = Path(candidate.anchor) if candidate.anchor else None
        if anchor is not None and candidate == anchor:
            source_root = find_reasoner_source_root()
            if source_root is not None and source_root.drive.lower() == candidate.drive.lower():
                return source_root
            return None
    except Exception:
        return candidate
    return candidate



def resolve_observed_project_root(
    project_root: str | Path | None = None,
    *,
    persisted_root: str | Path | None = None,
) -> Path | None:
    """Resolve explicit Project observation without Tool/runtime fallback.

    Project observation may come from an explicit path, a configured Project
    environment path, or a persisted Project path. When none is usable, the
    result is ``None``. Tool source, runtime executable location, and current
    working directory are never substituted as Project observation identity.
    """
    explicit = normalize_project_root_text(project_root)
    if explicit is not None and explicit.exists() and explicit.is_dir():
        return explicit

    env_root = _env_project_root()
    if env_root is not None and env_root.exists() and env_root.is_dir():
        return env_root

    persisted = normalize_project_root_text(persisted_root)
    if persisted is not None and persisted.exists() and persisted.is_dir():
        return persisted

    return None


def resolve_selected_project_root(
    project_root: str | Path | None = None,
    *,
    persisted_root: str | Path | None = None,
) -> Path | None:
    """Compatibility facade for strict observed-Project root resolution."""
    return resolve_observed_project_root(
        project_root,
        persisted_root=persisted_root,
    )

def resolve_active_project_root(
    project_root: str | Path | None = None,
    *,
    persisted_root: str | Path | None = None,
) -> Path:
    """Resolve the active project root using dynamic, compilation-safe inputs.

    Priority:
    1. Explicit project_root argument.
    2. Canonical and legacy environment variables.
    3. Existing non-legacy persisted GUI root.
    4. Detected Reasoner source tree.
    5. Runtime executable folder.
    6. Current working directory.
    """
    explicit = normalize_project_root_text(project_root)
    if explicit is not None:
        return explicit

    env_root = _env_project_root()
    if env_root is not None:
        return env_root

    source_root = find_reasoner_source_root()
    persisted = _usable_persisted_root(normalize_project_root_text(persisted_root), source_root)
    if persisted is not None:
        return persisted

    if source_root is not None:
        return source_root

    runtime_root = resolve_app_runtime_root()
    if runtime_root is not None:
        return runtime_root

    return _safe_resolve(Path.cwd())


def default_smoke_output_json_path(project_root: str | Path | None = None) -> Path:
    """Return a transient, non-source path for static-context smoke output."""
    root = resolve_active_project_root(project_root)
    transient_root = _canonical_transient_garbage_root(root)
    return (
        transient_root
        / "static_context_smoke"
        / "real_project_static_context_smoke.json"
    )
