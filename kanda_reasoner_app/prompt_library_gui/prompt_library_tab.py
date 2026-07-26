# project-path: kanda_reasoner_app/prompt_library_gui/prompt_library_tab.py
"""Read-only Prompt Library tab with canonical 3D group cubes."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .group_catalog import PromptGroup, filter_items_for_group, load_prompt_groups
from .group_dashboard import PromptGroupDashboard
from .group_window import PromptGroupWindow
from .library_catalog import PromptLibraryItem, load_prompt_library_items
from .library_paths import canonical_prompt_library_root, prompt_library_root

__all__ = [
    "PromptLibraryTab",
]


class PromptLibraryTab(QWidget):
    """Read-only GUI tab that launches current Prompt Library groups."""

    def __init__(self, library_root: Path | None = None) -> None:
        """Create the Prompt Library group dashboard."""
        super().__init__()
        self.library_root = library_root or prompt_library_root()
        self.items: list[PromptLibraryItem] = []
        self.groups: list[PromptGroup] = []
        self.group_windows: list[PromptGroupWindow] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        title = QLabel("Prompt Library")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        subtitle = QLabel(
            "Read-only dashboard for the canonical KANDA Prompt Library. "
            "Each cube represents one current ACTIVE_PROMPTS group. "
            "Deprecated and retired prompts are hidden. This tab does not "
            "edit prompts, run prompts, or change governance."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        button_row = QHBoxLayout()
        self.reload_button = QPushButton("Reload Canonical Library")
        self.reload_button.clicked.connect(self.reload_library)
        button_row.addWidget(self.reload_button)

        self.prompt_library_help_button = QPushButton("Help")
        self.prompt_library_help_button.setToolTip(
            "Open the Prompt Library first-time user help."
        )
        self.prompt_library_help_button.clicked.connect(
            self._open_prompt_library_help
        )
        button_row.addWidget(self.prompt_library_help_button)
        self._prompt_library_help_dialog = None
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self.dashboard = PromptGroupDashboard()
        self.dashboard.group_activated.connect(self.open_group_window)
        layout.addWidget(self.dashboard, 1)

        self.status_label = QLabel("")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        self.reload_library()


    def _open_prompt_library_help(self) -> None:
        """Open the local Prompt Library help document."""
        try:
            from ..reasoner_tools_gui_shell.help_docs.renderer import (
                open_help_document_for_legacy_catalog,
            )

            rich_dialog = open_help_document_for_legacy_catalog(
                self,
                "prompt_library.json",
                window_title="Help - Prompt Library",
            )
        except Exception:
            rich_dialog = None

        if rich_dialog is not None:
            self._prompt_library_help_dialog = rich_dialog
            return

        try:
            from ..reasoner_tools_gui_shell.gui_support import (
                _format_help_catalog_text,
                _help_catalog_path,
            )

            catalog_path = _help_catalog_path("prompt_library.json")
            if not catalog_path.is_file():
                QMessageBox.warning(
                    self,
                    "Help catalog not found",
                    "Expected Prompt Library help was not found:\n"
                    f"{catalog_path}",
                )
                return

            dialog = QMainWindow(self)
            dialog.setWindowTitle("Help - Prompt Library")
            dialog.resize(1080, 800)

            editor = QTextEdit(dialog)
            editor.setReadOnly(True)
            editor.setPlainText(_format_help_catalog_text(catalog_path))
            dialog.setCentralWidget(editor)
            dialog.show()
            self._prompt_library_help_dialog = dialog
        except Exception as exc:
            QMessageBox.warning(
                self,
                "Help could not be opened",
                "Failed to open Prompt Library help.\n\n"
                f"Details: {exc}",
            )

    def reload_library(self) -> None:
        """Reload current groups and prompts from the canonical workspace."""
        self.items = load_prompt_library_items(self.library_root)
        self.groups = load_prompt_groups(self.library_root)
        counts: dict[str, int] = {}
        for group in self.groups:
            counts[group.group_id] = len(filter_items_for_group(group, self.items))
        self.dashboard.set_groups(self.groups, counts)

        if self.groups:
            source_kind = "canonical workspace"
            if self.library_root != canonical_prompt_library_root():
                source_kind = "legacy compatibility fallback"
            self.status_label.setText(
                "Loaded "
                + str(len(self.groups))
                + " current prompt groups and "
                + str(len(self.items))
                + " current prompts from the "
                + source_kind
                + ": "
                + str(self.library_root)
                + ". Deprecated and retired entries are hidden."
            )
        else:
            self.status_label.setText(
                "No prompt groups found. Expected canonical catalog: "
                + str(
                    self.library_root
                    / "GROUPS"
                    / "PROMPT_GROUPS_DRAFT.json"
                )
            )

    def open_group_window(self, group: PromptGroup) -> None:
        """Open a floating read-only library window for one group."""
        items = filter_items_for_group(group, self.items)
        window = PromptGroupWindow(group, items, self.library_root)
        window.destroyed.connect(lambda _obj=None, win=window: self._forget_window(win))
        self.group_windows.append(window)
        window.show()
        self.status_label.setText("Opened group window: " + group.display_name)

    def _forget_window(self, window: PromptGroupWindow) -> None:
        """Forget a closed group window reference."""
        self.group_windows = [item for item in self.group_windows if item is not window]
