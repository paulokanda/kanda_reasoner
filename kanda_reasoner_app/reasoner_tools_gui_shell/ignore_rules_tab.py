# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/ignore_rules_tab.py
"""Project ignore-rules tab for the Reasoner tools GUI shell."""

from __future__ import annotations

__all__ = [
    "IgnoreRulesTab",
]

from pathlib import Path

from PySide6.QtCore import QSignalBlocker, Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
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

    def __init__(
        self,
        prefs_path: Path,
        parent=None,
        *,
        select_project_handler=None,
        eject_project_handler=None,
    ) -> None:
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
        self._select_project_handler = select_project_handler
        self._eject_project_handler = eject_project_handler

        self.project_label = QLabel()
        self.project_label.setWordWrap(True)
        self.project_label.hide()
        self.project_root_label = QLabel("Active Project:")
        label_font = self.project_root_label.font()
        label_font.setBold(True)
        self.project_root_label.setFont(label_font)
        self.project_root_label.setStyleSheet(
            "color: #0B3D91; "
            "font-weight: 700; "
            "padding: 0px;"
        )
        self.project_root_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.project_root_label.setMinimumWidth(0)
        self.project_root_label.setMargin(0)
        self.project_root_label.setSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Preferred,
        )
        self.project_root_edit = QLineEdit()
        self.project_root_edit.setReadOnly(True)
        self.project_root_edit.setPlaceholderText("No active Project selected")
        self.project_root_edit.setMinimumWidth(0)
        self.project_root_edit.setMaximumWidth(360)
        self.project_root_edit.setSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Preferred,
        )
        path_font = self.project_root_edit.font()
        path_font.setBold(True)
        self.project_root_edit.setFont(path_font)
        self.project_root_edit.setStyleSheet(
            "color: #166534; "
            "font-weight: 700;"
        )
        self.select_project_button = QPushButton("Select Active Project")
        self.select_project_button.clicked.connect(self._request_select_active_project)
        self.eject_project_button = QPushButton("Eject Active Project")
        self.eject_project_button.clicked.connect(self._request_eject_active_project)
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
        self.refresh_active_project_controls()


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
        self.refresh_active_project_controls(project_root)

    def _sync_project_root_edit(self, project_root: Path | None) -> None:
        """Mirror the active Project root into the read-only shell projection."""
        text = "" if project_root is None else str(project_root)
        if self.project_root_edit.text().strip() == text:
            return

        blocker = QSignalBlocker(self.project_root_edit)
        try:
            self.project_root_edit.setText(text)
        finally:
            del blocker

    def _request_select_active_project(self) -> None:
        """Delegate Project selection to the shell-owned command authority."""
        if callable(self._select_project_handler):
            self._select_project_handler()

    def _request_eject_active_project(self) -> None:
        """Delegate Project eject to the shell-owned command authority."""
        if callable(self._eject_project_handler):
            self._eject_project_handler()

    def refresh_active_project_controls(
        self,
        active_root: Path | None = None,
    ) -> None:
        """Refresh the Exclusion Rules projection of shell Project authority."""
        root = self._project_root if active_root is None else active_root
        self._sync_project_root_edit(root)
        self.select_project_button.setEnabled(callable(self._select_project_handler))
        self.eject_project_button.setEnabled(
            callable(self._eject_project_handler) and root is not None
        )

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
