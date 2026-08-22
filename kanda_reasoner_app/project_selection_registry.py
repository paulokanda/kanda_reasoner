# project-path: kanda_reasoner_app/project_selection_registry.py
"""Tool-owned registry for explicit active-Project selection identity."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    ProjectSupportBoundaryError,
    ProjectToolBoundaryIdentity,
    canonical_project_support_root,
    canonical_tool_support_root,
    legacy_physical_project_identity,
    normalize_project_selection_mode,
    resolve_explicit_project_tool_boundary_identity,
)

__all__ = [
    "ProjectObservation",
    "ProjectSelectionRecord",
    "ProjectSelectionRegistry",
    "ProjectSelectionRegistryError",
]

REGISTRY_SCHEMA_VERSION = "1.0"
REGISTRY_DIR_NAME = "tool_project_registry"
REGISTRY_FILE_NAME = "projects.json"


class ProjectSelectionRegistryError(RuntimeError):
    """Raised when the Tool-owned selection registry is unreadable or unsafe."""




@dataclass(frozen=True)
class ProjectObservation:
    """Describe one selected Project without carrying operation authority."""

    stable_project_id: str
    project_slug: str
    project_root: Path
    project_root_fingerprint: str
    project_support_root: Path
    selection_ticket: int

@dataclass(frozen=True)
class ProjectSelectionRecord:
    """Persist one explicitly selected Project under Tool ownership."""

    stable_project_id: str
    project_slug: str
    project_root: str
    project_root_fingerprint: str
    project_support_root: str
    selection_mode: ProjectSelectionMode
    updated_at_utc: str

    def as_json(self) -> dict[str, str]:
        """Return a deterministic JSON-compatible representation."""
        return {
            "stable_project_id": self.stable_project_id,
            "project_slug": self.project_slug,
            "project_root": self.project_root,
            "project_root_fingerprint": self.project_root_fingerprint,
            "project_support_root": self.project_support_root,
            "selection_mode": self.selection_mode.value,
            "updated_at_utc": self.updated_at_utc,
        }

    @classmethod
    def from_json(cls, payload: Any) -> "ProjectSelectionRecord":
        """Build one validated record from decoded JSON."""
        if not isinstance(payload, dict):
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_RECORD_NOT_OBJECT"
            )
        required = (
            "stable_project_id",
            "project_slug",
            "project_root",
            "project_root_fingerprint",
            "project_support_root",
            "selection_mode",
            "updated_at_utc",
        )
        missing = [name for name in required if not str(payload.get(name, "")).strip()]
        if missing:
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_RECORD_FIELDS_MISSING:" + ",".join(missing)
            )
        return cls(
            stable_project_id=str(payload["stable_project_id"]).strip(),
            project_slug=str(payload["project_slug"]).strip(),
            project_root=str(payload["project_root"]).strip(),
            project_root_fingerprint=str(
                payload["project_root_fingerprint"]
            ).strip(),
            project_support_root=str(payload["project_support_root"]).strip(),
            selection_mode=normalize_project_selection_mode(
                payload["selection_mode"]
            ),
            updated_at_utc=str(payload["updated_at_utc"]).strip(),
        )


class ProjectSelectionRegistry:
    """Persist explicit Project selection outside the Tool source tree."""

    def __init__(
        self,
        *,
        tool_source_root: str | Path | None = None,
        registry_path: str | Path | None = None,
    ) -> None:
        """Initialize one registry bound to the current Tool installation."""
        tool_support_root = canonical_tool_support_root(tool_source_root)
        self.tool_support_root = tool_support_root
        if registry_path is None:
            path = tool_support_root / REGISTRY_DIR_NAME / REGISTRY_FILE_NAME
        else:
            path = Path(registry_path).expanduser().resolve(strict=False)
        self.registry_path = path
        self.tool_source_root = (
            Path(tool_source_root).expanduser().resolve(strict=False)
            if tool_source_root is not None
            else None
        )

    def load_current_record(self) -> ProjectSelectionRecord | None:
        """Return the current selection record without granting authority."""
        payload = self._load_payload()
        current_id = str(payload.get("current_project_id", "")).strip()
        if not current_id:
            return None
        projects = payload.get("projects", {})
        if not isinstance(projects, dict):
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_REGISTRY_PROJECTS_NOT_OBJECT"
            )
        record_payload = projects.get(current_id)
        if record_payload is None:
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_CURRENT_ID_NOT_FOUND:" + current_id
            )
        return ProjectSelectionRecord.from_json(record_payload)

    def load_current_observation(
        self,
        *,
        selection_ticket: int = 0,
    ) -> ProjectObservation | None:
        """Return the current Project as non-authoritative observation state."""
        record = self.load_current_record()
        if record is None:
            return None
        root = Path(record.project_root).expanduser().resolve(strict=False)
        if not root.exists() or not root.is_dir():
            return None
        expected_support = self._path_key(record.project_support_root)
        actual_support = self._path_key(canonical_project_support_root(root))
        if expected_support != actual_support:
            return None
        _, root_fingerprint = legacy_physical_project_identity(root)
        if record.project_root_fingerprint != root_fingerprint:
            return None
        return ProjectObservation(
            stable_project_id=record.stable_project_id,
            project_slug=record.project_slug,
            project_root=root,
            project_root_fingerprint=root_fingerprint,
            project_support_root=canonical_project_support_root(root),
            selection_ticket=int(selection_ticket),
        )

    def resolve_current_boundary(self) -> ProjectToolBoundaryIdentity | None:
        """Return the legacy authority boundary for compatibility callers."""
        record = self.load_current_record()
        if record is None:
            return None
        try:
            boundary = resolve_explicit_project_tool_boundary_identity(
                record.project_root,
                selection_mode=record.selection_mode,
                stable_project_id=record.stable_project_id,
                tool_source_root=self.tool_source_root,
            )
        except (ProjectSupportBoundaryError, OSError):
            return None
        expected_support = self._path_key(record.project_support_root)
        actual_support = self._path_key(boundary.active_project_support_root)
        if expected_support != actual_support:
            return None
        if (
            record.project_root_fingerprint
            != boundary.active_project_root_fingerprint
        ):
            return None
        return boundary

    def resolve_boundary_for_root(
        self,
        project_root: str | Path,
    ) -> ProjectToolBoundaryIdentity:
        """Return the current boundary only when it matches the requested root."""
        requested = Path(project_root).expanduser().resolve(strict=False)
        boundary = self.resolve_current_boundary()
        if boundary is None:
            raise ProjectSelectionRegistryError(
                "ACTIVE_PROJECT_SELECTION_REQUIRED"
            )
        if self._path_key(boundary.active_project_root) != self._path_key(
            requested
        ):
            raise ProjectSelectionRegistryError(
                "ACTIVE_PROJECT_SELECTION_ROOT_MISMATCH:" + str(requested)
            )
        return boundary

    def register_explicit_root(
        self,
        project_root: str | Path,
    ) -> ProjectToolBoundaryIdentity:
        """Register a user-selected root with explicit self-host detection."""
        try:
            return self.register_explicit_selection(
                project_root,
                ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
            )
        except ProjectSelectionRegistryError as exc:
            if "SELF_HOSTING_REQUIRES_EXPLICIT_SELECTION" not in str(exc):
                raise
        return self.register_explicit_selection(
            project_root,
            ProjectSelectionMode.EXPLICIT_SELF_HOSTING,
        )

    def register_explicit_selection(
        self,
        project_root: str | Path,
        selection_mode: ProjectSelectionMode | str,
    ) -> ProjectToolBoundaryIdentity:
        """Register an explicit human selection and return strict identity."""
        mode = normalize_project_selection_mode(selection_mode)
        if mode is ProjectSelectionMode.UNSELECTED:
            raise ProjectSelectionRegistryError(
                "CANNOT_REGISTER_UNSELECTED_PROJECT"
            )
        root = Path(project_root).expanduser().resolve(strict=False)
        payload = self._load_payload()
        existing = self._record_for_root(payload, root)
        stable_id = (
            existing.stable_project_id
            if existing is not None
            else str(uuid.uuid4())
        )
        try:
            boundary = resolve_explicit_project_tool_boundary_identity(
                root,
                selection_mode=mode,
                stable_project_id=stable_id,
                tool_source_root=self.tool_source_root,
            )
        except ProjectSupportBoundaryError as exc:
            raise ProjectSelectionRegistryError(str(exc)) from exc

        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        record = ProjectSelectionRecord(
            stable_project_id=stable_id,
            project_slug=boundary.active_project_slug,
            project_root=str(boundary.active_project_root),
            project_root_fingerprint=(
                boundary.active_project_root_fingerprint
            ),
            project_support_root=str(boundary.active_project_support_root),
            selection_mode=boundary.selection_mode,
            updated_at_utc=now,
        )
        projects = payload.setdefault("projects", {})
        if not isinstance(projects, dict):
            projects = {}
            payload["projects"] = projects
        projects[stable_id] = record.as_json()
        payload["current_project_id"] = stable_id
        payload["schema_version"] = REGISTRY_SCHEMA_VERSION
        self._write_payload(payload)
        return boundary

    def register_legacy_external_root(
        self,
        project_root: str | Path | None,
    ) -> ProjectToolBoundaryIdentity | None:
        """Migrate a legacy external selection, never inferred self-hosting."""
        text = str(project_root or "").strip()
        if not text:
            return None
        root = Path(text).expanduser().resolve(strict=False)
        try:
            return self.register_explicit_selection(
                root,
                ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
            )
        except ProjectSelectionRegistryError as exc:
            if "SELF_HOSTING_REQUIRES_EXPLICIT_SELECTION" in str(exc):
                return None
            return None

    def clear_current_selection(self) -> None:
        """Clear current Project observation while preserving history records."""
        payload = self._load_payload()
        payload["current_project_id"] = ""
        payload["schema_version"] = REGISTRY_SCHEMA_VERSION
        self._write_payload(payload)

    def _record_for_root(
        self,
        payload: dict[str, Any],
        root: Path,
    ) -> ProjectSelectionRecord | None:
        """Return a previous record for the same canonical root."""
        projects = payload.get("projects", {})
        if not isinstance(projects, dict):
            return None
        root_key = self._path_key(root)
        for item in projects.values():
            try:
                record = ProjectSelectionRecord.from_json(item)
            except ProjectSelectionRegistryError:
                continue
            if self._path_key(record.project_root) == root_key:
                return record
        return None

    def _load_payload(self) -> dict[str, Any]:
        """Load registry JSON, returning an empty valid payload when absent."""
        path = self.registry_path
        if not path.exists():
            return {
                "schema_version": REGISTRY_SCHEMA_VERSION,
                "current_project_id": "",
                "projects": {},
            }
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_REGISTRY_UNREADABLE:" + str(path)
            ) from exc
        if not isinstance(payload, dict):
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_REGISTRY_NOT_OBJECT"
            )
        schema = str(payload.get("schema_version", "")).strip()
        if schema and schema != REGISTRY_SCHEMA_VERSION:
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_REGISTRY_SCHEMA_UNSUPPORTED:" + schema
            )
        return payload

    def _write_payload(self, payload: dict[str, Any]) -> None:
        """Atomically persist registry JSON under Tool Support."""
        path = self.registry_path
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(path.name + ".tmp")
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        try:
            temporary.write_text(text, encoding="utf-8", newline="\n")
            os.replace(temporary, path)
        except OSError as exc:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            raise ProjectSelectionRegistryError(
                "PROJECT_SELECTION_REGISTRY_WRITE_FAILED:" + str(path)
            ) from exc

    @staticmethod
    def _path_key(path: str | Path) -> str:
        """Return one normalized comparison key for persisted paths."""
        value = Path(path).expanduser().resolve(strict=False)
        return os.path.normcase(str(value))
