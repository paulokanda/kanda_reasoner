# project-path: kanda_reasoner_app/project_structure_visualizer/__init__.py
"""Read-only Project Structure 3D visualization package."""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = ["ProjectStructure3DWidget"]


def __getattr__(name: str) -> Any:
    """Resolve the public widget lazily."""
    if name == "ProjectStructure3DWidget":
        module = import_module(
            "kanda_reasoner_app.project_structure_visualizer."
            "project_structure_3d_tab"
        )
        return module.ProjectStructure3DWidget
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
