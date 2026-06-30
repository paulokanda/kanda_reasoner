# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/app_constants.py
"""Application constants for the root Reasoner tools GUI shell."""

from __future__ import annotations

from pathlib import Path

from kanda_reasoner_app import LEGACY_PACKAGE_NAME
from kanda_reasoner_app.project_root_resolver import resolve_app_runtime_root

__all__ = [
    "APP_DISPLAY_NAME",
    "APP_ICON_PATH",
    "APP_TITLE_DETAIL",
]

_PROJECT_ROOT = resolve_app_runtime_root()

APP_DISPLAY_NAME = "KANDA Reasoner"
APP_TITLE_DETAIL = "Knowledge and Architecture Navigator for Developer Assistance"
APP_ICON_PATH = (
    _PROJECT_ROOT
    / LEGACY_PACKAGE_NAME
    / "reasoner_tools_gui_help"
    / "kanda_reasoner_color_icon.ico"
)

_PREFS_FILENAME = ".reasoner_tools_gui_prefs.json"
_HELP_FILENAME = "reasoner_tools_gui_help.md"
_COLLECTOR_SUBTABS_TO_REMOVE = {
    "json splitter",
    "splitter",
    "manager",
    "workflow",
    "manage architecture",
    "manage workflow",
    "architecture manager",
    "workflow manager",
}
