# project-path: kanda_reasoner_app/source_hygiene/ruff_correction_storage.py
"""Ownership-safe storage and hashing for Ruff correction workflows."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any, Mapping

from kanda_reasoner_app.project_analysis_evidence_paths import (
    show_project_to_ai_root_from_hint,
)
from kanda_reasoner_app.generated_artifact_hygiene import (
    project_delete_after_daily_work_dir,
)

__all__ = [
    "RuffCorrectionPaths",
    "atomic_write_bytes",
    "atomic_write_json",
    "canonical_json_bytes",
    "copy_file",
    "ensure_project_relative_file",
    "load_json_object",
    "resolve_ruff_correction_paths",
    "safe_preview_id",
    "utc_now",
]


@dataclass(frozen=True)
class RuffCorrectionPaths:
    """Canonical project-owned and transient Ruff correction paths."""

    project_root: Path
    show_project_to_ai_root: Path
    daily_work_root: Path
    feature_support_root: Path
    previews_root: Path
    backups_root: Path
    receipts_root: Path
    locks_root: Path
    shadows_root: Path

    def preview_root(self, preview_id: str) -> Path:
        """Return the durable root for one preview identifier."""
        return self.previews_root / safe_preview_id(preview_id)

    def shadow_root(self, preview_id: str) -> Path:
        """Return the transient shadow root for one preview identifier."""
        return self.shadows_root / safe_preview_id(preview_id)


_SAFE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{7,119}$")


def resolve_ruff_correction_paths(
    project_root: str | Path,
) -> RuffCorrectionPaths:
    """Resolve canonical roots without writing inside active project source."""
    root = Path(project_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("RUFF_CORRECTION_PROJECT_ROOT_NOT_DIRECTORY")
    if root == Path(root.anchor):
        raise ValueError("RUFF_CORRECTION_BROAD_PROJECT_ROOT_BLOCKED")

    show_root = show_project_to_ai_root_from_hint(root).resolve()
    daily_root = project_delete_after_daily_work_dir(root).resolve()
    support = show_root / "source_hygiene" / "ruff_corrections"
    return RuffCorrectionPaths(
        project_root=root,
        show_project_to_ai_root=show_root,
        daily_work_root=daily_root,
        feature_support_root=support,
        previews_root=support / "previews",
        backups_root=support / "backups",
        receipts_root=support / "receipts",
        locks_root=support / "locks",
        shadows_root=daily_root / "source_hygiene" / "ruff_correction_shadows",
    )


def safe_preview_id(value: str) -> str:
    """Validate one preview identifier before path construction."""
    candidate = str(value or "").strip().lower()
    if not _SAFE_ID_PATTERN.fullmatch(candidate):
        raise ValueError("RUFF_CORRECTION_PREVIEW_ID_INVALID")
    return candidate


def ensure_project_relative_file(
    project_root: Path,
    value: str | Path,
    *,
    require_exists: bool = True,
) -> tuple[Path, str]:
    """Resolve one file inside the active project and return its relative path."""
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    resolved = candidate.expanduser().resolve()
    try:
        relative = resolved.relative_to(project_root.resolve())
    except ValueError as exc:
        raise ValueError("RUFF_CORRECTION_PATH_OUTSIDE_PROJECT_ROOT") from exc
    if require_exists and (not resolved.exists() or not resolved.is_file()):
        raise ValueError("RUFF_CORRECTION_SOURCE_FILE_MISSING:" + relative.as_posix())
    if relative.as_posix().startswith("../"):
        raise ValueError("RUFF_CORRECTION_PATH_OUTSIDE_PROJECT_ROOT")
    return resolved, relative.as_posix()


def utc_now() -> str:
    """Return a stable UTC timestamp."""
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha256_bytes(data: bytes) -> str:
    """Return the SHA256 digest for bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return the SHA256 digest for one file."""
    digest = hashlib.sha256()
    with io.FileIO(path, mode="rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    """Return deterministic ASCII JSON bytes."""
    text = json.dumps(
        dict(value),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return text.encode("ascii")


def atomic_write_bytes(path: str | Path, payload: bytes) -> None:
    """Atomically replace one file using a temporary sibling."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=target.name + ".",
        suffix=".tmp",
        dir=str(target.parent),
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, target)
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass


def atomic_write_text(path: str | Path, text: str) -> None:
    """Atomically write UTF-8 text with LF line endings."""
    normalized = str(text).replace("\r\n", "\n").replace("\r", "\n")
    atomic_write_bytes(path, normalized.encode("utf-8"))


def atomic_write_json(path: str | Path, value: Mapping[str, Any]) -> None:
    """Atomically write readable deterministic JSON."""
    text = (
        json.dumps(
            dict(value),
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    atomic_write_text(path, text)


def load_json_object(path: str | Path) -> dict[str, Any]:
    """Read one JSON object and reject scalar or list payloads."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("RUFF_CORRECTION_JSON_READ_FAILED") from exc
    if not isinstance(payload, dict):
        raise ValueError("RUFF_CORRECTION_JSON_OBJECT_REQUIRED")
    return payload


def copy_file(source: str | Path, target: str | Path) -> None:
    """Copy one file while creating its destination parent."""
    source_path = Path(source)
    target_path = Path(target)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
