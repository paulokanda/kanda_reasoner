# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab.py
"""Project ignore-rules tab for the Reasoner tools GUI shell."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesTab",
]

from pathlib import Path

from PySide6.QtCore import QSignalBlocker
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
)

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
        """Support init behavior.
        
        Parameters
        ----------
        prefs_path : Path
            The prefs path value.
        parent : object, optional
            The optional parent value.
        """
        
        super().__init__(parent)
        self.prefs_path = prefs_path
        self._rules = {"folders": [], "files": [], "extensions": []}
        self._project_root: Path | None = None
        self._project_key = "__global__"
        self._loading_rules = False

        self.project_label = QLabel()
        self.project_label.setWordWrap(True)
        self.project_label.hide()
        self.project_root_label = QLabel("Project Root:")
        self.project_root_label.setStyleSheet("color: #0B3D91; font-weight: bold;")
        self.project_root_edit = QLineEdit()
        self.project_root_edit.setPlaceholderText("Select project root for exclusion rules")
        self.project_root_edit.setMinimumWidth(260)
        self.project_root_edit.setMaximumWidth(310)
        self.project_root_edit.editingFinished.connect(self._apply_project_root_from_edit)
        self.project_root_search_button = QPushButton("Search")
        self.project_root_search_button.clicked.connect(self._browse_project_root)
        self.project_scope_label = QLabel()
        self.project_scope_label.setWordWrap(False)
        self.project_scope_label.setStyleSheet(
            "border: 1px solid #0B3D91; "
            "color: #0B3D91; "
            "font-weight: bold; "
            "padding: 4px 8px;"
        )
        self.exclusion_help_button = QPushButton("Help")
        self.exclusion_help_button.setToolTip(
            "Open the Exclusion Rules first-time user help."
        )
        self.exclusion_help_button.clicked.connect(
            self._open_exclusion_rules_help
        )
        self._exclusion_help_dialog = None
        self.folder_list = QListWidget()
        self.file_list = QListWidget()
        self.ext_list = QListWidget()

        self._build_ui()
        self._load_rules()


    def _open_exclusion_rules_help(self) -> None:
        """Open the local Exclusion Rules help document."""
        try:
            from .help_docs.renderer import (
                open_help_document_for_legacy_catalog,
            )

            rich_dialog = open_help_document_for_legacy_catalog(
                self,
                "exclusion_rules.json",
                window_title="Help - Exclusion Rules",
            )
        except Exception:
            rich_dialog = None

        if rich_dialog is not None:
            self._exclusion_help_dialog = rich_dialog
            return

        try:
            from .gui_support import (
                _format_help_catalog_text,
                _help_catalog_path,
            )

            catalog_path = _help_catalog_path("exclusion_rules.json")
            if not catalog_path.is_file():
                QMessageBox.warning(
                    self,
                    "Help catalog not found",
                    "Expected Exclusion Rules help was not found:\n"
                    f"{catalog_path}",
                )
                return

            dialog = QMainWindow(self)
            dialog.setWindowTitle("Help - Exclusion Rules")
            dialog.resize(1000, 750)

            editor = QTextEdit(dialog)
            editor.setReadOnly(True)
            editor.setPlainText(_format_help_catalog_text(catalog_path))
            dialog.setCentralWidget(editor)
            dialog.show()
            self._exclusion_help_dialog = dialog
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Help could not be opened",
                f"Failed to open Exclusion Rules help.\n\nDetails: {exc}",
            )

    def set_project_root(self, project_root: Path | None) -> None:
        """Switch the active project and load its exclusion rules."""
        self._project_root = project_root
        self._project_key = self._project_key_from_root(project_root)
        self._sync_project_root_edit(project_root)
        self._refresh_project_label()
        self._load_rules()

    def _sync_project_root_edit(self, project_root: Path | None) -> None:
        """Mirror the active project root into the editable Project Root field."""
        text = "" if project_root is None else str(project_root)
        if self.project_root_edit.text().strip() == text:
            return

        blocker = QSignalBlocker(self.project_root_edit)
        try:
            self.project_root_edit.setText(text)
        finally:
            del blocker

    def _apply_project_root_from_edit(self) -> None:
        """Apply a manually typed project root to the exclusion-rule scope."""
        text = self.project_root_edit.text().strip()
        if not text:
            self.set_project_root(None)
            return
        self.set_project_root(Path(text).expanduser())

    def _browse_project_root(self) -> None:
        """Browse for the project root used by this exclusion-rule profile."""
        start = self.project_root_edit.text().strip() or self._get_last_browse_path()
        selected = QFileDialog.getExistingDirectory(
            self,
            "Select Project Root",
            start,
        )
        if not selected:
            return

        self._set_last_browse_path(selected)
        self.project_root_edit.setText(selected)
        self.set_project_root(Path(selected).expanduser())

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
        """Update the scope label shown beside the Project Root controls."""
        self.project_label.setText("")
        self.project_label.hide()
        if self._project_key == "__global__":
            self.project_scope_label.setText(
                "Scope: no project root is selected. These rules are fallback "
                "rules only. Select a project root to save exclusions for that "
                "project without affecting other projects."
            )
            return

        profile_text = "Reasoner project defaults: inactive"
        if self._is_reasoner_project_root():
            profile_text = "Reasoner project defaults: active"

        self.project_scope_label.setText(
            "Scope: exclusions on this tab are saved only for this project root. "
            "Other project roots keep separate exclusion lists. " + profile_text
        )
