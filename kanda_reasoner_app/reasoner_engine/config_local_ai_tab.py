# project-path: kanda_reasoner_app/reasoner_engine/config_local_ai_tab.py
"""Tool-owned Local AI configuration surface for the Config AI tab."""

from __future__ import annotations

from PySide6.QtCore import QSignalBlocker
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)

__all__ = ["ConfigLocalAITab"]


class ConfigLocalAITab(QWidget):
    """Edit the single application-scoped Local AI endpoint and model."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        controller: LocalAIConfigurationController | None = None,
    ) -> None:
        super().__init__(parent)
        self._controller = controller or application_local_ai_configuration()
        self._build_ui()
        self._wire_events()
        self._hydrate()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        title = QLabel("Config Local AI")
        font = QFont()
        font.setBold(True)
        font.setPointSize(13)
        title.setFont(font)
        root.addWidget(title)

        explanation = QLabel(
            "This Tool-owned configuration is shared by every KANDA workflow that "
            "uses Local AI. It stores no active Project identity, Project Root, "
            "Project Support path, source snapshot, or write authority."
        )
        explanation.setWordWrap(True)
        root.addWidget(explanation)

        group = QGroupBox("Global Local AI configuration")
        form = QFormLayout(group)
        self.base_url_edit = QLineEdit()
        self.base_url_edit.setPlaceholderText("http://127.0.0.1:11434/v1")
        form.addRow("OpenAI-compatible base URL:", self.base_url_edit)

        model_row = QWidget()
        model_layout = QHBoxLayout(model_row)
        model_layout.setContentsMargins(0, 0, 0, 0)
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.refresh_button = QPushButton("Refresh Local AI Models")
        model_layout.addWidget(self.model_combo, 1)
        model_layout.addWidget(self.refresh_button)
        form.addRow("Global Local AI model:", model_row)
        root.addWidget(group)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)

        boundary = QLabel(
            "Tool-versus-Project boundary: configuration is global Tool state. "
            "Each tab still resolves the exact active Project and builds its own "
            "request identity immediately before a Local AI call."
        )
        boundary.setWordWrap(True)
        boundary.setStyleSheet("color: #666666;")
        root.addWidget(boundary)
        root.addStretch(1)

    def _wire_events(self) -> None:
        self.base_url_edit.editingFinished.connect(self._commit_base_url)
        self.model_combo.currentTextChanged.connect(self._commit_model)
        self.refresh_button.clicked.connect(self._controller.refresh_models)
        self._controller.configuration_changed.connect(lambda _snapshot: self._hydrate())
        self._controller.catalog_changed.connect(lambda _models: self._hydrate())
        self._controller.status_changed.connect(self.status_label.setText)

    def _commit_base_url(self) -> None:
        self._controller.set_base_url(self.base_url_edit.text())
        self.base_url_edit.setText(self._controller.base_url())

    def _commit_model(self, value: str) -> None:
        self._controller.set_selected_model_id(value)

    def _hydrate(self) -> None:
        snapshot = self._controller.snapshot()
        with QSignalBlocker(self.base_url_edit):
            self.base_url_edit.setText(snapshot.base_url)
        current = snapshot.model_id
        with QSignalBlocker(self.model_combo):
            self.model_combo.clear()
            for model in snapshot.available_models:
                self.model_combo.addItem(model)
            if current and self.model_combo.findText(current) < 0:
                self.model_combo.addItem(current)
            self.model_combo.setCurrentText(current)
        self.status_label.setText(
            "Status: " + snapshot.catalog_status + "\nActive: " + self._controller.summary()
        )
