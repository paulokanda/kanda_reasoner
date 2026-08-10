# project-path: kanda_reasoner_app/portable_smoke_isolation.py
"""Token-bound path overrides used only by Portable packaged-GUI smoke tests."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

__all__ = [
    "PORTABLE_SMOKE_ENABLED_ENV",
    "PORTABLE_SMOKE_ROOT_ENV",
    "PORTABLE_SMOKE_TOKEN_ENV",
    "PortableSmokeIsolationBoundary",
    "PortableSmokeIsolationError",
    "resolve_portable_smoke_isolation",
]

PORTABLE_SMOKE_ENABLED_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ENABLED"
PORTABLE_SMOKE_ROOT_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_ROOT"
PORTABLE_SMOKE_TOKEN_ENV = "KANDA_PORTABLE_SMOKE_ISOLATION_TOKEN"
MARKER_NAME = "KANDA_PORTABLE_SMOKE_ISOLATION.json"
SCHEMA_VERSION = "1.0"


class PortableSmokeIsolationError(RuntimeError):
    """Raised when smoke-isolation authority is incomplete or inconsistent."""


@dataclass(frozen=True)
class PortableSmokeIsolationBoundary:
    """Validated disposable owner roots for one packaged-GUI smoke run."""

    root: Path
    runtime_root: Path
    project_root: Path
    token_sha256: str

    def _require_owner(self, owner_root: str | Path) -> Path:
        owner = Path(owner_root).expanduser().resolve(strict=False)
        for canonical in (self.runtime_root, self.project_root):
            if os.path.normcase(str(owner)) == os.path.normcase(str(canonical)):
                return canonical
            try:
                owner.relative_to(canonical)
            except ValueError:
                continue
            return canonical
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_OWNER_ROOT_NOT_ALLOWED:" + str(owner)
        )

    def tool_support_root(self, tool_root: str | Path) -> Path:
        """Return isolated Tool Support for the validated runtime root."""
        owner = self._require_owner(tool_root)
        return (
            self.root
            / "tool_support"
            / f"{owner.name}_show_project_to_AI"
        ).resolve(strict=False)

    def project_support_root(self, project_root: str | Path) -> Path:
        """Return isolated Project Support for an allowed smoke owner."""
        owner = self._require_owner(project_root)
        return (
            self.root
            / "project_support"
            / f"{owner.name}_show_project_to_AI"
        ).resolve(strict=False)

    def transient_root(self, owner_root: str | Path) -> Path:
        """Return isolated transient storage for an allowed smoke owner."""
        owner = self._require_owner(owner_root)
        return (
            self.root
            / "transient"
            / f"{owner.name}_delete_after_daily_work"
        ).resolve(strict=False)


def _read_marker(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_MARKER_UNREADABLE:" + str(path)
        ) from exc
    if not isinstance(payload, dict):
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_MARKER_NOT_OBJECT:" + str(path)
        )
    return payload


def _absolute_directory(text: str, label: str) -> Path:
    if not text.strip():
        raise PortableSmokeIsolationError(label + "_REQUIRED")
    path = Path(text).expanduser()
    if not path.is_absolute():
        raise PortableSmokeIsolationError(label + "_MUST_BE_ABSOLUTE")
    resolved = path.resolve(strict=False)
    if not resolved.is_dir() or resolved.is_symlink():
        raise PortableSmokeIsolationError(label + "_INVALID:" + str(resolved))
    return resolved


def resolve_portable_smoke_isolation() -> PortableSmokeIsolationBoundary | None:
    """Return validated smoke isolation or None when the mode is not enabled."""
    enabled = os.environ.get(PORTABLE_SMOKE_ENABLED_ENV, "").strip()
    root_text = os.environ.get(PORTABLE_SMOKE_ROOT_ENV, "").strip()
    token = os.environ.get(PORTABLE_SMOKE_TOKEN_ENV, "").strip()
    if not enabled and not root_text and not token:
        return None
    if enabled != "1" or not root_text or not token:
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_ENVIRONMENT_INCOMPLETE"
        )

    root = _absolute_directory(root_text, "PORTABLE_SMOKE_ROOT")
    marker_path = root / MARKER_NAME
    if not marker_path.is_file() or marker_path.is_symlink():
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_MARKER_MISSING:" + str(marker_path)
        )
    marker = _read_marker(marker_path)
    if marker.get("schema_version") != SCHEMA_VERSION:
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_MARKER_SCHEMA_MISMATCH"
        )
    if Path(str(marker.get("root") or "")).resolve(strict=False) != root:
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_MARKER_ROOT_MISMATCH"
        )
    token_sha256 = hashlib.sha256(token.encode("utf-8")).hexdigest()
    if marker.get("token_sha256") != token_sha256:
        raise PortableSmokeIsolationError(
            "PORTABLE_SMOKE_TOKEN_MISMATCH"
        )

    runtime_root = _absolute_directory(
        str(marker.get("runtime_root") or ""),
        "PORTABLE_SMOKE_RUNTIME_ROOT",
    )
    project_root = _absolute_directory(
        str(marker.get("project_root") or ""),
        "PORTABLE_SMOKE_PROJECT_ROOT",
    )
    for candidate in (runtime_root, project_root):
        try:
            candidate.relative_to(root)
        except ValueError as exc:
            raise PortableSmokeIsolationError(
                "PORTABLE_SMOKE_OWNER_OUTSIDE_ROOT:" + str(candidate)
            ) from exc

    return PortableSmokeIsolationBoundary(
        root=root,
        runtime_root=runtime_root,
        project_root=project_root,
        token_sha256=token_sha256,
    )
