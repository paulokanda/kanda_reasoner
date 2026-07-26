# project-path: tools/workbench_support_boundary_validation_fixture.py
"""Isolated path overrides for Workbench boundary validation."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

from kanda_reasoner_app.manage_architecture.large_file_refactor_planner import (
    workbench_project_support_paths as support_paths_module,
)

__all__ = [
    "expected_external_root",
    "isolated_workbench_paths",
]


def expected_external_root(project_root: Path, suffix: str) -> Path:
    """Return the canonical external path without creating it."""
    root = project_root.expanduser().resolve(strict=False)
    base = Path(root.anchor) if root.drive else root.parent
    return (base / (root.name + suffix)).resolve(strict=False)


@contextmanager
def isolated_workbench_paths(
    sandbox: Path,
    consumer_module: ModuleType,
):
    """Redirect validation-only support writes inside a temporary root."""
    support_base = sandbox / "_isolated_project_support"
    daily_base = sandbox / "_isolated_daily_work"

    def fixture_support_root(active_project_root: str | Path) -> Path:
        project = Path(active_project_root).expanduser().resolve(strict=False)
        return support_base / (project.name + "_show_project_to_AI")

    def fixture_daily_root(active_project_root: str | Path) -> Path:
        project = Path(active_project_root).expanduser().resolve(strict=False)
        return daily_base / (project.name + "_delete_after_daily_work")

    with patch.object(
        support_paths_module,
        "project_support_root",
        fixture_support_root,
    ), patch.object(
        support_paths_module,
        "daily_work_root",
        fixture_daily_root,
    ), patch.object(
        consumer_module,
        "project_support_root",
        fixture_support_root,
    ), patch.object(
        consumer_module,
        "daily_work_root",
        fixture_daily_root,
    ):
        yield support_base, daily_base
