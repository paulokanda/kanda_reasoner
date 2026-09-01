# project-path: kanda_reasoner_app/reasoner_symbol_atlas/review_session.py
"""Operation-scoped evidence reuse for one Complete Engineering Review."""

from __future__ import annotations

from contextlib import contextmanager
from functools import wraps
from contextvars import ContextVar
from dataclasses import dataclass, field
import hashlib
import os
from pathlib import Path
from typing import Iterator

__all__ = [
    "ProjectSymbolAtlasReviewSessionIdentity",
    "reasoner_symbol_atlas_options_reuse",
    "reasoner_symbol_atlas_project_root_reuse",
    "reasoner_symbol_atlas_review_session",
    "reasoner_symbol_atlas_reuse_scope",
]

_EXCLUDED_DIR_NAMES = frozenset(
    {
        ".git",
        ".hg",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "env",
        "node_modules",
        "site-packages",
        "venv",
    }
)


@dataclass(frozen=True)
class ProjectSymbolAtlasReviewSessionIdentity:
    """Immutable identity for one selected-Project review operation."""

    project_root: str
    stable_project_id: str
    project_root_fingerprint: str
    operation_id: str


@dataclass
class _ProjectSymbolAtlasReviewSessionState:
    identity: ProjectSymbolAtlasReviewSessionIdentity
    freshness_stamps: dict[tuple[str, ...], str] = field(default_factory=dict)
    cache: dict[tuple[object, ...], object] = field(default_factory=dict)


_ACTIVE_SESSION: ContextVar[_ProjectSymbolAtlasReviewSessionState | None] = (
    ContextVar("reasoner_symbol_atlas_review_session", default=None)
)


def _resolved_root(project_root: str | Path) -> Path:
    return Path(project_root).expanduser().resolve(strict=False)


def _normalize_extra_paths(
    project_root: Path,
    extra_paths: tuple[str, ...],
) -> tuple[Path, ...]:
    normalized: list[Path] = []
    for value in extra_paths:
        text = str(value or "").strip()
        if not text:
            continue
        path = Path(text).expanduser()
        if not path.is_absolute():
            path = project_root / path
        normalized.append(path.resolve(strict=False))
    return tuple(sorted(set(normalized), key=lambda item: str(item).lower()))


def _update_file_stat(
    digest: "hashlib._Hash",
    project_root: Path,
    path: Path,
) -> None:
    try:
        stat = path.stat()
    except OSError:
        return
    try:
        relative = path.relative_to(project_root)
        display = relative.as_posix()
    except ValueError:
        display = str(path)
    digest.update(display.encode("utf-8", errors="surrogatepass"))
    digest.update(b"\0")
    digest.update(str(int(stat.st_size)).encode("ascii"))
    digest.update(b"\0")
    digest.update(str(int(stat.st_mtime_ns)).encode("ascii"))
    digest.update(b"\n")


def _build_freshness_stamp(
    project_root: Path,
    extra_paths: tuple[str, ...] = (),
) -> str:
    """Hash active Python file metadata plus selected evidence-file metadata."""
    digest = hashlib.sha256()
    for root_text, dir_names, file_names in os.walk(project_root):
        dir_names[:] = [
            name
            for name in dir_names
            if name.lower() not in _EXCLUDED_DIR_NAMES
        ]
        root = Path(root_text)
        for file_name in sorted(file_names):
            if not file_name.lower().endswith(".py"):
                continue
            _update_file_stat(digest, project_root, root / file_name)
    for path in _normalize_extra_paths(project_root, extra_paths):
        _update_file_stat(digest, project_root, path)
    return digest.hexdigest()


def _matching_state(
    project_root: str | Path,
) -> _ProjectSymbolAtlasReviewSessionState | None:
    state = _ACTIVE_SESSION.get()
    if state is None:
        return None
    requested_root = _resolved_root(project_root)
    session_root = _resolved_root(state.identity.project_root)
    if requested_root != session_root:
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_PROJECT_MISMATCH")
    return state


def _review_cache_scope_key(
    project_root: Path,
    evidence_paths: tuple[str, ...],
) -> tuple[str, ...]:
    return tuple(
        str(path)
        for path in _normalize_extra_paths(project_root, evidence_paths)
    )


def _review_cache_get(
    project_root: str | Path,
    cache_key: tuple[object, ...],
    *,
    evidence_paths: tuple[str, ...] = (),
) -> object | None:
    state = _matching_state(project_root)
    if state is None:
        return None
    root = _resolved_root(project_root)
    scope_key = _review_cache_scope_key(root, evidence_paths)
    stamp = _build_freshness_stamp(root, evidence_paths)
    previous = state.freshness_stamps.get(scope_key)
    if previous and previous != stamp:
        stale_keys = [key for key in state.cache if key[0] == scope_key]
        for key in stale_keys:
            state.cache.pop(key, None)
    state.freshness_stamps[scope_key] = stamp
    return state.cache.get((scope_key,) + cache_key)


def _review_cache_put(
    project_root: str | Path,
    cache_key: tuple[object, ...],
    value: object,
    *,
    evidence_paths: tuple[str, ...] = (),
) -> None:
    state = _matching_state(project_root)
    if state is None:
        return
    root = _resolved_root(project_root)
    scope_key = _review_cache_scope_key(root, evidence_paths)
    stamp = _build_freshness_stamp(root, evidence_paths)
    previous = state.freshness_stamps.get(scope_key)
    if previous and previous != stamp:
        stale_keys = [key for key in state.cache if key[0] == scope_key]
        for key in stale_keys:
            state.cache.pop(key, None)
    state.freshness_stamps[scope_key] = stamp
    state.cache[(scope_key,) + cache_key] = value


@contextmanager
def reasoner_symbol_atlas_review_session(
    *,
    project_root: str | Path,
    stable_project_id: str,
    project_root_fingerprint: str,
    operation_id: str,
) -> Iterator[ProjectSymbolAtlasReviewSessionIdentity]:
    """Open one bounded selected-Project evidence-reuse session.

    The session is an immutable-evidence acceleration scope, not an authority
    owner. It is context-local, never persistent, and never shared across
    projects, operations, or threads.
    """
    if _ACTIVE_SESSION.get() is not None:
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_ALREADY_ACTIVE")
    root = _resolved_root(project_root)
    if not root.is_dir():
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_PROJECT_ROOT_INVALID")
    identity = ProjectSymbolAtlasReviewSessionIdentity(
        project_root=str(root),
        stable_project_id=str(stable_project_id).strip(),
        project_root_fingerprint=str(project_root_fingerprint).strip(),
        operation_id=str(operation_id).strip(),
    )
    if not identity.stable_project_id:
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_PROJECT_ID_REQUIRED")
    if not identity.project_root_fingerprint:
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_ROOT_FINGERPRINT_REQUIRED")
    if not identity.operation_id:
        raise RuntimeError("SYMBOL_ATLAS_REVIEW_SESSION_OPERATION_ID_REQUIRED")
    state = _ProjectSymbolAtlasReviewSessionState(identity=identity)
    token = _ACTIVE_SESSION.set(state)
    try:
        yield identity
    finally:
        state.cache.clear()
        state.freshness_stamps.clear()
        _ACTIVE_SESSION.reset(token)


def _reuse_identity_values(project_root: Path) -> tuple[str, str]:
    root_text = str(project_root).casefold().encode(
        "utf-8",
        errors="surrogatepass",
    )
    stable_id = "operation-local-" + hashlib.sha256(root_text).hexdigest()[:24]
    root_fingerprint = _build_freshness_stamp(project_root)
    return stable_id, root_fingerprint


@contextmanager
def reasoner_symbol_atlas_reuse_scope(
    *,
    project_root: str | Path,
    operation_id: str,
) -> Iterator[ProjectSymbolAtlasReviewSessionIdentity]:
    """Reuse immutable evidence within one read-only operation and nested calls."""
    root = _resolved_root(project_root)
    active = _ACTIVE_SESSION.get()
    if active is not None:
        state = _matching_state(root)
        if state is None:
            raise RuntimeError("SYMBOL_ATLAS_REUSE_SESSION_UNAVAILABLE")
        yield state.identity
        return
    stable_id, root_fingerprint = _reuse_identity_values(root)
    with reasoner_symbol_atlas_review_session(
        project_root=root,
        stable_project_id=stable_id,
        project_root_fingerprint=root_fingerprint,
        operation_id=operation_id,
    ) as identity:
        yield identity


def reasoner_symbol_atlas_options_reuse(operation_id: str):
    """Decorate a function whose first argument exposes project_root."""
    def decorate(function):
        @wraps(function)
        def wrapped(options, *args, **kwargs):
            with reasoner_symbol_atlas_reuse_scope(
                project_root=options.project_root,
                operation_id=operation_id,
            ):
                return function(options, *args, **kwargs)
        return wrapped
    return decorate


def reasoner_symbol_atlas_project_root_reuse(operation_id: str):
    """Decorate a function whose first argument is a Project root."""
    def decorate(function):
        @wraps(function)
        def wrapped(project_root, *args, **kwargs):
            with reasoner_symbol_atlas_reuse_scope(
                project_root=project_root,
                operation_id=operation_id,
            ):
                return function(project_root, *args, **kwargs)
        return wrapped
    return decorate
