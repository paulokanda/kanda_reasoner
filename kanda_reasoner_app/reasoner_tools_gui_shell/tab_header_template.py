# project-path: kanda_reasoner_app/reasoner_tools_gui_shell/tab_header_template.py
"""Reusable one-line tab header template for lazy tool tabs."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

__all__ = [
    "TAB_HEADER_AI_GROUP_BLUEPRINT",
    "TAB_HEADER_HELP_FILE_TEXT",
    "TabHeaderTemplate",
]


TAB_HEADER_HELP_FILE_TEXT = "Help"
TAB_HEADER_AI_GROUP_BLUEPRINT = (
    "AI model:",
    "AI model dropdown",
    "Refresh AI Models",
    "AI Review First Check",
    TAB_HEADER_HELP_FILE_TEXT,
)


class TabHeaderTemplate:
    """Build the standard tab header: tab name, Project Root slot, AI group.

    The AI group blueprint is: ``AI model:`` label, AI model dropdown,
    ``Refresh AI Models`` button, ``AI Review First Check`` button, and the
    help-file action.
    """

    def __init__(
        self,
        tab_name: str,
        *,
        help_handler: Callable[[], None] | None = None,
    ) -> None:
        self.layout = QHBoxLayout()
        self.layout.setSpacing(6)

        self.title_label = QLabel(tab_name)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        self.title_label.setFont(title_font)
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label, 1)

        self.project_root_host, self.project_root_layout = self._new_slot()
        self.ai_group_host, self.ai_group_layout = self._new_slot()
        self.layout.addWidget(self.project_root_host, 0)
        self.layout.addWidget(self.ai_group_host, 0)
        self.ai_model_label: QLabel | None = None
        self.ai_model_combo: QComboBox | None = None
        self.refresh_ai_models_button: QPushButton | None = None
        self.ai_review_first_check_button: QPushButton | None = None

        self.help_button: QPushButton | None = None
        if help_handler is not None:
            self.help_button = QPushButton(TAB_HEADER_HELP_FILE_TEXT)
            self.help_button.setToolTip("Open this tab's help file.")
            self.help_button.setStyleSheet("color: #003366; font-weight: bold;")
            self.help_button.clicked.connect(help_handler)
            self.layout.addWidget(self.help_button, 0, Qt.AlignRight)

    @staticmethod
    def _new_slot() -> tuple[QWidget, QHBoxLayout]:
        """Return a compact host widget with a zero-margin horizontal layout."""
        host = QWidget()
        host.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        layout = QHBoxLayout(host)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        return host, layout

    def add_widget_before_help(self, widget: QWidget, *, spacing_after: int = 0) -> None:
        """Add a non-template widget before the trailing Help action."""
        insert_index = self.layout.count()
        if self.help_button is not None:
            insert_index = self.layout.indexOf(self.help_button)
        self.layout.insertWidget(insert_index, widget, 0)
        if spacing_after:
            self.layout.insertSpacing(insert_index + 1, spacing_after)

    def install_ai_group_blueprint(
        self,
        *,
        refresh_handler: Callable[[], None] | None = None,
        review_handler: Callable[[], None] | None = None,
    ) -> None:
        """Install the standard AI group widgets into the template AI slot."""
        if self.ai_model_combo is not None:
            return

        self.ai_model_label = QLabel("AI model:")
        self.ai_model_combo = QComboBox()
        self.ai_model_combo.setMinimumWidth(210)
        self.ai_model_combo.setToolTip("Select the local AI model used by this tab.")
        self.ai_model_combo.addItem("Auto (first available Ollama model)")

        self.refresh_ai_models_button = QPushButton("Refresh AI Models")
        self.refresh_ai_models_button.setToolTip("Refresh local Ollama model choices.")
        if refresh_handler is not None:
            self.refresh_ai_models_button.clicked.connect(refresh_handler)

        if review_handler is not None:
            self.ai_review_first_check_button = QPushButton("AI Review First Check")
            self.ai_review_first_check_button.setToolTip("Run this tab's AI review first check.")
            self.ai_review_first_check_button.clicked.connect(review_handler)

        self.ai_group_layout.addWidget(self.ai_model_label)
        self.ai_group_layout.addWidget(self.ai_model_combo)
        self.ai_group_layout.addWidget(self.refresh_ai_models_button)
        if self.ai_review_first_check_button is not None:
            self.ai_group_layout.addWidget(self.ai_review_first_check_button)
