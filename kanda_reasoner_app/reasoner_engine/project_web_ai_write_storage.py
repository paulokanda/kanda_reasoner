# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_write_storage.py
"""Own contained filesystem primitives for Project Web AI apply transactions."""

from __future__ import annotations

import hashlib
import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_contracts import (
    ProjectWebAIApplyAuthorization,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
    ProjectWebAIShadowPreview,
)

__all__ = [
    "atomic_replace_source",
    "contained_project_file",
    "contained_shadow_file",
    "exclusive_apply_lock",
    "require_distinct_apply_roots",
    "project_web_ai_sha256_bytes",
    "write_source_backups",
    "write_transaction_state",
]


def write_source_backups(backup_root: Path, source_before: dict[str, bytes]) -> None:
    """Write exact immutable source backups below the transient root."""
    for relative_path, raw in source_before.items():
        target = (backup_root / relative_path).resolve(strict=False)
        try:
            target.relative_to(backup_root)
        except ValueError as exc:
            raise RuntimeError("APPLY_BACKUP_PATH_ESCAPE") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())


def atomic_replace_source(
    target: Path,
    raw: bytes,
    mode: int,
    transaction_id: str,
) -> None:
    """Replace one existing source file using a verified temporary sibling."""
    temp = target.with_name(
        "." + target.name + ".kanda-web-ai-" + transaction_id[:12] + ".tmp"
    )
    temp.unlink(missing_ok=True)
    try:
        with temp.open("xb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temp, mode)
        if (
            project_web_ai_sha256_bytes(temp.read_bytes())
            != project_web_ai_sha256_bytes(raw)
        ):
            raise RuntimeError("APPLY_TEMP_FILE_HASH_MISMATCH")
        os.replace(temp, target)
    finally:
        temp.unlink(missing_ok=True)


def contained_project_file(root: Path, relative_path: str) -> Path:
    """Return one existing non-link file structurally contained in Project."""
    relative = Path(relative_path.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError("APPLY_UNSAFE_RELATIVE_PATH:" + relative_path)
    lexical = root / relative
    _reject_link_components(root, lexical)
    resolved = lexical.resolve(strict=True)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise RuntimeError("APPLY_PROJECT_PATH_ESCAPE:" + relative_path) from exc
    if not resolved.is_file() or resolved.is_symlink():
        raise RuntimeError("APPLY_TARGET_NOT_REGULAR_FILE:" + relative_path)
    return resolved


def contained_shadow_file(
    preview: ProjectWebAIShadowPreview,
    relative_path: str,
) -> Path:
    """Return one exact non-link Shadow file inside Preview authority."""
    shadow_root = Path(preview.shadow_root).resolve(strict=True)
    relative = Path(relative_path.replace("\\", "/"))
    if relative.is_absolute() or ".." in relative.parts:
        raise RuntimeError("APPLY_UNSAFE_SHADOW_RELATIVE_PATH:" + relative_path)
    lexical = shadow_root / relative
    _reject_link_components(shadow_root, lexical)
    target = lexical.resolve(strict=True)
    try:
        target.relative_to(shadow_root)
    except ValueError as exc:
        raise RuntimeError("APPLY_SHADOW_PATH_ESCAPE:" + relative_path) from exc
    if not target.is_file() or target.is_symlink():
        raise RuntimeError("APPLY_SHADOW_FILE_INVALID:" + relative_path)
    return target


def require_distinct_apply_roots(
    project: Path,
    daily: Path,
    support: Path,
) -> None:
    """Reject Project, durable support, and transient ownership overlap."""
    for first, second, marker in (
        (project, daily, "PROJECT_DAILY_OVERLAP"),
        (project, support, "PROJECT_SUPPORT_OVERLAP"),
        (daily, support, "DAILY_SUPPORT_OVERLAP"),
    ):
        if _paths_overlap(first, second):
            raise RuntimeError("APPLY_ROOT_" + marker)


@contextmanager
def exclusive_apply_lock(
    lock_path: Path,
    transaction_id: str,
) -> Iterator[None]:
    """Hold one operation lock using exclusive file creation."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise RuntimeError("APPLY_OPERATION_ALREADY_LOCKED") from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(transaction_id + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        yield
    finally:
        lock_path.unlink(missing_ok=True)


def write_transaction_state(
    path: Path,
    authorization: ProjectWebAIApplyAuthorization,
    *,
    status: str,
    error: str,
    updated_at_utc: str,
    receipt_path: str = "",
) -> None:
    """Write transient transaction state for recovery diagnostics."""
    payload = {
        "transaction_id": authorization.transaction_id,
        "authorization_id": authorization.authorization_id,
        "operation_id": authorization.operation_id,
        "status": status,
        "error": error,
        "receipt_path": receipt_path,
        "updated_at_utc": updated_at_utc,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    temp.write_text(
        json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temp, path)


def project_web_ai_sha256_bytes(raw: bytes) -> str:
    """Return one SHA-256 digest."""
    return hashlib.sha256(raw).hexdigest()


def _reject_link_components(root: Path, candidate: Path) -> None:
    """Reject symlink or Windows junction components below Project root."""
    relative = candidate.relative_to(root)
    current = root
    is_junction = getattr(os.path, "isjunction", lambda _path: False)
    for part in relative.parts:
        current = current / part
        if current.is_symlink() or is_junction(current):
            raise RuntimeError(
                "APPLY_LINK_OR_JUNCTION_COMPONENT:" + relative.as_posix()
            )


def _paths_overlap(first: Path, second: Path) -> bool:
    """Return whether either canonical root contains the other."""
    if first == second:
        return True
    for parent, child in ((first, second), (second, first)):
        try:
            child.relative_to(parent)
        except ValueError:
            continue
        return True
    return False
