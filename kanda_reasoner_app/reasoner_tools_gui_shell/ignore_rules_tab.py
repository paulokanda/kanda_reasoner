"""Project ignore-rules tab for the Reasoner tools GUI shell."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesTab",
]

from pathlib import Path

from PySide6.QtWidgets import QLabel, QListWidget, QWidget

from .ignore_rules_tab_help.browse_state import IgnoreRulesBrowseStateMixin
from .ignore_rules_tab_help.list_actions import IgnoreRulesListActionsMixin
from .ignore_rules_tab_help.prefs_io import IgnoreRulesPrefsMixin
from .ignore_rules_tab_help.rule_defaults import IgnoreRulesDefaultsMixin
from .ignore_rules_tab_help.ui_builders import IgnoreRulesUiMixin


class IgnoreRulesTab(
    IgnoreRulesUiMixin,
    IgnoreRulesListActionsMixin,
    IgnoreRulesPrefsMixin,
    IgnoreRulesDefaultsMixin,
    IgnoreRulesBrowseStateMixin,
    QWidget,
):
    """Manage project exclusion rules shared by validation and collection.

    Files, folders, and extensions listed here are treated as not part
    of the currently selected project by architecture validation and
    project collection. Each project root owns an independent rule set.
    Changes are auto-saved to prefs immediately after modification.
    """

    def __init__(self, prefs_path: Path, parent=None) -> None:
        super().__init__(parent)
        self.prefs_path = prefs_path
        self._rules = {"folders": [], "files": [], "extensions": []}
        self._project_root: Path | None = None
        self._project_key = "__global__"
        self._loading_rules = False

        self.project_label = QLabel()
        self.project_label.setWordWrap(True)
        self.project_scope_label = QLabel()
        self.project_scope_label.setWordWrap(True)
        self.project_scope_label.setStyleSheet(
            "border: 1px solid #0B3D91; "
            "color: #0B3D91; "
            "font-weight: bold; "
            "padding: 4px 8px;"
        )
        self.folder_list = QListWidget()
        self.file_list = QListWidget()
        self.ext_list = QListWidget()

        self._build_ui()
        self._load_rules()

    def set_project_root(self, project_root: Path | None) -> None:
        """Switch the active project and load its exclusion rules."""
        self._project_root = project_root
        self._project_key = self._project_key_from_root(project_root)
        self._refresh_project_label()
        self._load_rules()

    @staticmethod
    def _project_key_from_root(project_root: Path | None) -> str:
        """Return the stable prefs key for a project root."""
        if project_root is None:
            return "__global__"

        try:
            return str(project_root.expanduser().resolve())
        except Exception:
            return str(project_root.expanduser())

    def _refresh_project_label(self) -> None:
        """Update the project label shown above the rule lists."""
        if self._project_key == "__global__":
            self.project_label.setText("Active project: global fallback")
            self.project_scope_label.setText(
                "Scope: no project root is selected. These rules are fallback "
                "rules only. Select a project root to save exclusions for that "
                "project without affecting other projects."
            )
            return

        profile_text = "Reasoner project defaults: inactive"
        if self._is_reasoner_project_root():
            profile_text = "Reasoner project defaults: active"

        self.project_label.setText("Active project: " + self._project_key)
        self.project_scope_label.setText(
            "Scope: exclusions on this tab are saved only for this project root. "
            "Other project roots keep separate exclusion lists. " + profile_text
        )
