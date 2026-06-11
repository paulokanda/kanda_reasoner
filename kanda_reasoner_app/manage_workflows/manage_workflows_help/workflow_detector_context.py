"""Workflow detector execution context.

The context is intentionally small and read-only. It gives detector gates a
stable way to inspect the active project root and generated workflow data
without importing unrelated boxes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


__all__ = [
    "WorkflowDetectorContext",
]


@dataclass(frozen=True)
class WorkflowDetectorContext:
    """Input context passed to one workflow detector gate."""

    project_root: Path
    workflow_manifest: dict[str, Any] = field(default_factory=dict)
    workflows_doc: str = ""

    def resolved_root(self) -> Path:
        """Return the normalized project root."""
        return Path(self.project_root).expanduser().resolve()

    def resolve_project_path(self, relative_path: str | Path) -> Path:
        """Resolve a path relative to the active project root."""
        path = Path(relative_path)
        if path.is_absolute():
            return path.expanduser().resolve()
        return (self.resolved_root() / path).resolve()
