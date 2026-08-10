# project-path: kanda_reasoner_app/memory_ownership/context.py
"""Immutable Tool-versus-Project durable-memory owner identities."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from kanda_reasoner_app.project_operation_authority import (
    ProjectOperationAuthorityError,
    resolve_registered_project_boundary,
)
from kanda_reasoner_app.project_support_boundary import (
    TOOL_PROJECT_SLUG,
    canonical_tool_support_root,
)

__all__ = [
    "MemoryOwnerContext",
    "MemoryOwnershipError",
    "OwnerScope",
    "project_owner_context",
    "tool_owner_context",
]


class MemoryOwnershipError(RuntimeError):
    """Raised when durable-memory ownership cannot be proven safely."""


class OwnerScope(str, Enum):
    """Canonical durable-memory owner scopes."""

    TOOL = "TOOL"
    PROJECT = "PROJECT"


@dataclass(frozen=True)
class MemoryOwnerContext:
    """System-assigned identity for one durable-memory owner."""

    owner_scope: OwnerScope
    owner_id: str
    owner_slug: str
    owner_root_fingerprint: str
    affected_box: str
    source_root: Path
    support_root: Path

    def canonical_fields(self) -> dict[str, str]:
        """Return canonical owner metadata for persisted records."""
        return {
            "owner_scope": self.owner_scope.value,
            "owner_id": self.owner_id,
            "owner_slug": self.owner_slug,
            "owner_root_fingerprint": self.owner_root_fingerprint,
            "affected_box": self.affected_box,
        }


def _path_key(path: Path) -> str:
    """Return a platform-aware canonical path identity."""
    return os.path.normcase(str(path.expanduser().resolve(strict=False)))


def _path_fingerprint(path: Path) -> str:
    """Return a deterministic canonical-root fingerprint."""
    return hashlib.sha256(_path_key(path).encode("utf-8")).hexdigest()


def _tool_owner_id(tool_root: Path) -> str:
    """Return a stable Tool owner identity for this installation root."""
    basis = "kanda_reasoner_tool:" + _path_key(tool_root)
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()


def tool_owner_context(
    tool_source_root: str | Path | None = None,
    *,
    affected_box: str = "KANDA Reasoner Tool",
) -> MemoryOwnerContext:
    """Return the canonical Tool durable-memory owner context."""
    if tool_source_root is None:
        support_root = canonical_tool_support_root()
        source_root = support_root.parent / TOOL_PROJECT_SLUG
    else:
        source_root = Path(tool_source_root).expanduser().resolve(strict=False)
        support_root = canonical_tool_support_root(source_root)
    return MemoryOwnerContext(
        owner_scope=OwnerScope.TOOL,
        owner_id=_tool_owner_id(source_root),
        owner_slug=TOOL_PROJECT_SLUG,
        owner_root_fingerprint=_path_fingerprint(source_root),
        affected_box=str(affected_box or "KANDA Reasoner Tool"),
        source_root=source_root,
        support_root=support_root,
    )


def project_owner_context(
    selected_project_root: str | Path,
    *,
    tool_source_root: str | Path | None = None,
    affected_box: str = "Active Project",
) -> MemoryOwnerContext:
    """Return the selected Project durable-memory owner context.

    The explicitly supplied Project root is the operation target. Physical root
    equality with the Tool never changes the logical owner scope from PROJECT.
    """
    try:
        boundary = resolve_registered_project_boundary(
            selected_project_root,
            tool_source_root=tool_source_root,
        )
    except ProjectOperationAuthorityError as exc:
        raise MemoryOwnershipError(str(exc)) from exc
    if not boundary.active_project_root.exists():
        raise MemoryOwnershipError(
            "PROJECT_MEMORY_OWNER_ROOT_MISSING:"
            + str(boundary.active_project_root)
        )
    return MemoryOwnerContext(
        owner_scope=OwnerScope.PROJECT,
        owner_id=boundary.active_project_id,
        owner_slug=boundary.active_project_slug,
        owner_root_fingerprint=boundary.active_project_root_fingerprint,
        affected_box=str(affected_box or "Active Project"),
        source_root=boundary.active_project_root,
        support_root=boundary.active_project_support_root,
    )
