# project-path: kanda_reasoner_app/engineering_safety/capability_bridge.py
"""Read-only shared capability bridge for Engineering Safety consumers.

This module is intentionally independent of the Engineering Safety GUI panel.
It exposes a narrow shared contract over the canonical private catalog and
command implementation so Diagnostics can inspect Pontual Audit capabilities
without importing the panel that owns Full Audit.
"""

from __future__ import annotations

from dataclasses import dataclass

import _reasoner_tools_gui_engineering_safety_panel_commands as _panel_commands
from _reasoner_tools_gui_engineering_safety_panel_catalog import (
    _build_engineering_safety_panel_catalog,
)

__all__ = [
    "EngineeringSafetyCapabilityView",
    "get_engineering_safety_capability_views",
    "run_engineering_safety_capability",
]


@dataclass(frozen=True)
class EngineeringSafetyCapabilityView:
    """Read-only description of one canonical Pontual Audit capability."""

    section: str
    label: str
    command_name: str
    description: str


_CAPABILITY_VIEWS: tuple[EngineeringSafetyCapabilityView, ...] = (
    _build_engineering_safety_panel_catalog(EngineeringSafetyCapabilityView)
)


def get_engineering_safety_capability_views(
) -> tuple[EngineeringSafetyCapabilityView, ...]:
    """Return immutable Pontual Audit capability descriptors."""
    return _CAPABILITY_VIEWS


def run_engineering_safety_capability(
    command_name: str,
    project_root: str | None = None,
):
    """Run one capability through the canonical boundary-safe command owner."""
    return _panel_commands._run_command(command_name, project_root)
