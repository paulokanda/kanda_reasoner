# project-path: kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py
"""Single editable Web AI configuration surface for all KANDA tabs."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    application_web_ai_configuration,
)
from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor, gateway_profiles

__all__ = ["ConfigWebAITab"]


class ConfigWebAITab(QWidget):
    """Edit the one application-scoped Web AI gateway and model selection."""

    def __init__(self) -> None:
        """Build the central configuration panel and bind its controller."""
        super().__init__()
        self._controller = application_web_ai_configuration()
        self._build_ui()
        self._bind_controller()
        self._render_all()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("Config Web AI")
        title.setStyleSheet("font-size: 21px; font-weight: 700;")
        root.addWidget(title)
        subtitle = QLabel(
            "Configure OpenRouter or Kilo once. Workflow tabs only choose "
            "Heuristic, Local AI, or Web AI. Active Project identity is never "
            "stored in this global configuration."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #5f6368;")
        root.addWidget(subtitle)

        panel = QFrame()
        panel.setObjectName("configWebAIPanel")
        panel.setStyleSheet(
            "QFrame#configWebAIPanel { border: 1px solid #cfd5dc; "
            "border-radius: 8px; background: #ffffff; }"
        )
        form = QFormLayout(panel)
        form.setContentsMargins(18, 18, 18, 18)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(11)

        self.gateway_combo = QComboBox()
        for profile in gateway_profiles():
            self.gateway_combo.addItem(profile.display_name, profile.gateway_id)
        _force_opaque_combo(self.gateway_combo)
        form.addRow("Gateway", self.gateway_combo)

        key_row = QHBoxLayout()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Session-only API key")
        self.load_env_button = QPushButton("Load Environment Key")
        key_row.addWidget(self.api_key_edit, 1)
        key_row.addWidget(self.load_env_button)
        form.addRow("API key", key_row)

        self.credential_status = QLabel()
        self.credential_status.setWordWrap(True)
        form.addRow("Credential", self.credential_status)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumContentsLength(40)
        _force_opaque_combo(self.model_combo)
        form.addRow("Model", self.model_combo)

        catalog_row = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh Models")
        self.free_only_checkbox = QCheckBox("Free models only")
        self.free_only_checkbox.setChecked(True)
        catalog_row.addWidget(self.refresh_button)
        catalog_row.addWidget(self.free_only_checkbox)
        catalog_row.addStretch(1)
        form.addRow("Catalog", catalog_row)

        self.catalog_status = QLabel("Not loaded")
        self.catalog_status.setWordWrap(True)
        form.addRow("Catalog status", self.catalog_status)

        self.capability_status = QLabel()
        self.capability_status.setWordWrap(True)
        form.addRow("Capabilities", self.capability_status)

        self.privacy_status = QLabel()
        self.privacy_status.setWordWrap(True)
        form.addRow("Privacy", self.privacy_status)

        root.addWidget(panel)

        warning = QLabel(
            "API keys remain in memory only. Free does not mean private. "
            "Every workflow still requires approval for its exact Project payload."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "color: #7a4e00; background: #fff7df; border: 1px solid #e1c36a; "
            "border-radius: 6px; padding: 8px;"
        )
        root.addWidget(warning)
        self.status_label = QLabel("Ready.")
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)
        root.addStretch(1)

        self.gateway_combo.currentIndexChanged.connect(self._gateway_changed)
        self.api_key_edit.textChanged.connect(self._api_key_changed)
        self.load_env_button.clicked.connect(self._load_environment_key)
        self.refresh_button.clicked.connect(self._controller.refresh_models)
        self.free_only_checkbox.toggled.connect(self._controller.set_free_models_only)
        self.model_combo.currentIndexChanged.connect(self._model_changed)

    def _bind_controller(self) -> None:
        self._controller.configuration_changed.connect(lambda _snapshot: self._render_all())
        self._controller.catalog_changed.connect(lambda _models: self._render_models())
        self._controller.status_changed.connect(self._show_status)

    def _gateway_changed(self, _index: int) -> None:
        self._controller.set_gateway_id(str(self.gateway_combo.currentData() or ""))

    def _api_key_changed(self, text: str) -> None:
        self._controller.set_api_key(text)

    def _load_environment_key(self) -> None:
        if not self._controller.load_environment_key():
            profile = self._controller.profile()
            QMessageBox.information(
                self,
                "Environment key not found",
                profile.api_key_env
                + " was not found in the process or Windows User environment.",
            )
        self._render_all()

    def _model_changed(self, _index: int) -> None:
        model = self.model_combo.currentData()
        self._controller.set_selected_model_id(
            model.model_id if isinstance(model, ModelDescriptor) else ""
        )

    def _render_all(self) -> None:
        profile = self._controller.profile()
        gateway_index = self.gateway_combo.findData(profile.gateway_id)
        if gateway_index >= 0 and gateway_index != self.gateway_combo.currentIndex():
            self.gateway_combo.blockSignals(True)
            self.gateway_combo.setCurrentIndex(gateway_index)
            self.gateway_combo.blockSignals(False)
        if self.api_key_edit.text() != self._controller.api_key():
            self.api_key_edit.blockSignals(True)
            self.api_key_edit.setText(self._controller.api_key())
            self.api_key_edit.blockSignals(False)
        if self.free_only_checkbox.isChecked() != self._controller.free_models_only():
            self.free_only_checkbox.blockSignals(True)
            self.free_only_checkbox.setChecked(self._controller.free_models_only())
            self.free_only_checkbox.blockSignals(False)
        self.credential_status.setText(self._controller.credential_source())
        self.catalog_status.setText(self._controller.catalog_status())
        self.privacy_status.setText(profile.privacy_summary)
        self._render_models()

    def _render_models(self) -> None:
        selected_id = self._controller.selected_model_id()
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        for model in self._controller.visible_models():
            prefix = "[FREE] " if model.free_status else ""
            self.model_combo.addItem(
                prefix + model.display_name + " - " + model.model_id,
                model,
            )
        selected_index = -1
        for index in range(self.model_combo.count()):
            value = self.model_combo.itemData(index)
            if isinstance(value, ModelDescriptor) and value.model_id == selected_id:
                selected_index = index
                break
        self.model_combo.setCurrentIndex(selected_index)
        self.model_combo.blockSignals(False)
        model = self._controller.selected_model()
        if model is None:
            self.capability_status.setText("No model selected.")
        else:
            structured = "YES" if "response_format" in set(model.supported_parameters) else "NO/UNKNOWN"
            self.capability_status.setText(
                "Structured output: " + structured
                + " | Context window: " + str(model.context_window or "unknown")
                + " | Cost: " + model.price_label()
            )

    def _show_status(self, message: str) -> None:
        self.status_label.setText(str(message))
        self.refresh_button.setEnabled(self._controller.catalog_status() != "Loading...")


def _force_opaque_combo(combo: QComboBox) -> None:
    """Force a durable opaque popup while preserving the light closed control."""
    combo.setAutoFillBackground(True)
    combo_palette = combo.palette()
    combo_palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
    combo_palette.setColor(QPalette.ColorRole.Button, QColor("#ffffff"))
    combo_palette.setColor(QPalette.ColorRole.Text, QColor("#1f2933"))
    combo.setPalette(combo_palette)

    popup = combo.view()
    viewport = popup.viewport()
    popup.setObjectName("configWebAIComboPopup")
    viewport.setObjectName("configWebAIComboPopupViewport")
    popup.setStyleSheet(
        "QAbstractItemView {"
        "background-color: #1d2128;"
        "color: #f4f6f8;"
        "border: 1px solid #3d4552;"
        "outline: 0;"
        "selection-background-color: #2f4f48;"
        "selection-color: #ffffff;"
        "}"
    )
    viewport.setStyleSheet("background-color: #1d2128;")

    for surface in (popup, viewport):
        surface.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        surface.setAutoFillBackground(True)
        palette = surface.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Window, QColor("#1d2128"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#f4f6f8"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#2f4f48"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        surface.setPalette(palette)
