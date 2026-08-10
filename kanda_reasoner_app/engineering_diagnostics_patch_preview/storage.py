# project-path: kanda_reasoner_app/engineering_diagnostics_patch_preview/storage.py
"""Project-owned support and disposable paths for governed patch previews."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile

from kanda_reasoner_app.generated_artifact_hygiene import (
    project_delete_after_daily_work_dir,
)
from kanda_reasoner_app.project_analysis_evidence_paths import (
    show_project_to_ai_root_from_hint,
)

__all__ = [
    "GovernedPatchPreviewPaths",
    "atomic_write_bytes",
    "atomic_write_json",
    "atomic_write_text",
    "resolve_patch_preview_paths",
    "governed_preview_sha256_bytes",
    "governed_preview_sha256_file",
    "utc_now",
]


@dataclass(frozen=True, slots=True)
class GovernedPatchPreviewPaths:
    """Canonical support and disposable roots for the selected Project."""

    project_root: Path
    support_root: Path
    previews_root: Path
    daily_work_root: Path
    workspaces_root: Path

    def preview_root(self, preview_id: str) -> Path:
        """Return one durable preview support root."""
        return self.previews_root / preview_id

    def workspace_root(self, preview_id: str) -> Path:
        """Return one disposable isolated workspace root."""
        return self.workspaces_root / preview_id


def resolve_patch_preview_paths(project_root: str | Path) -> GovernedPatchPreviewPaths:
    """Resolve Project support and daily-work paths without source mutation."""
    root = Path(project_root).expanduser().resolve(strict=True)
    if not root.is_dir() or root == Path(root.anchor):
        raise ValueError("PATCH_PREVIEW_PROJECT_ROOT_INVALID")
    support = (
        show_project_to_ai_root_from_hint(root).resolve()
        / "engineering_diagnostics_patch_preview"
    )
    daily = project_delete_after_daily_work_dir(root).resolve()
    return GovernedPatchPreviewPaths(
        project_root=root,
        support_root=support,
        previews_root=support / "previews",
        daily_work_root=daily,
        workspaces_root=daily / "engineering_diagnostics_patch_preview" / "workspaces",
    )


def utc_now() -> str:
    """Return a stable UTC timestamp."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
        "+00:00", "Z"
    )


def governed_preview_sha256_bytes(payload: bytes) -> str:
    """Return SHA-256 for one byte payload."""
    return hashlib.sha256(payload).hexdigest()


def governed_preview_sha256_file(path: str | Path) -> str:
    """Return SHA-256 for one bounded preview target file."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def atomic_write_bytes(path: str | Path, payload: bytes) -> None:
    """Atomically replace one support-state file."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(
        prefix=target.name + ".", suffix=".tmp", dir=str(target.parent)
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink(missing_ok=True)


def atomic_write_text(path: str | Path, text: str) -> None:
    """Atomically write UTF-8 text with LF endings."""
    normalized = str(text).replace("\r\n", "\n").replace("\r", "\n")
    atomic_write_bytes(path, normalized.encode("utf-8"))


def atomic_write_json(path: str | Path, value: dict[str, object]) -> None:
    """Atomically write readable deterministic JSON."""
    atomic_write_text(
        path,
        json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n",
    )
