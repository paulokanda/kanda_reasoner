# project-path: kanda_reasoner_app/reasoner_engine/config_web_ai_tab.py
"""Gateway configuration surface for the shared Project Web AI tab."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from kanda_reasoner_app.reasoner_engine.config_web_ai_ui_support import (
    configure_opaque_combo,
)
from kanda_reasoner_app.web_ai_configuration import (
    application_web_ai_configuration,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ModelDescriptor,
    provider_profiles,
)

__all__ = ["ConfigWebAITab"]


class ConfigWebAITab(QWidget):
    """Edit gateway-based Web AI configuration without Project identity."""

    def __init__(self) -> None:
        """Build the gateway panel and bind its shared controller."""
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
            "Configure gateway access through OpenRouter or Kilo. Direct provider "
            "APIs are configured in Direct API Providers. Both routes feed the "
            "same Project Web AI conversation and Active Project context."
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
        for profile in provider_profiles("gateway"):
            self.gateway_combo.addItem(profile.display_name, profile.gateway_id)
        configure_opaque_combo(self.gateway_combo)
        form.addRow("Gateway", self.gateway_combo)

        key_row = QHBoxLayout()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Session-only API key")
        self.load_env_button = QPushButton("Use Key / Load Environment")
        key_row.addWidget(self.api_key_edit, 1)
        key_row.addWidget(self.load_env_button)
        form.addRow("API key", key_row)

        self.credential_status = QLabel()
        self.credential_status.setWordWrap(True)
        form.addRow("Credential", self.credential_status)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumContentsLength(40)
        configure_opaque_combo(self.model_combo)
        form.addRow("Model", self.model_combo)

        catalog_row = QHBoxLayout()
        self.refresh_button = QPushButton("Refresh Models")
        self.free_only_checkbox = QCheckBox("Free models only")
        self.free_only_checkbox.setChecked(True)
        self.free_only_checkbox.setEnabled(False)
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
            "Only approved zero-cost Python-coding gateway models are shown. "
            "Availability can change and free does not mean private."
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
        self.load_env_button.clicked.connect(self._accept_or_load_key)
        self.refresh_button.clicked.connect(self._controller.refresh_models)
        self.free_only_checkbox.toggled.connect(
            self._controller.set_free_models_only
        )
        self.model_combo.currentIndexChanged.connect(self._model_changed)

    def _bind_controller(self) -> None:
        self._controller.configuration_changed.connect(
            lambda _snapshot: self._render_all()
        )
        self._controller.catalog_changed.connect(
            lambda _models: self._render_models()
        )
        self._controller.status_changed.connect(self._show_status)

    def _gateway_changed(self, _index: int) -> None:
        self._controller.set_gateway_id(str(self.gateway_combo.currentData() or ""))

    def _api_key_changed(self, text: str) -> None:
        if self._controller.profile().provider_class == "gateway":
            self._controller.set_api_key(text)

    def _accept_or_load_key(self) -> None:
        pasted_key = self.api_key_edit.text().strip()
        if pasted_key:
            self._controller.set_api_key(
                pasted_key,
                source="manual session field",
            )
            self._render_all()
            self.status_label.setText(
                "Accepted the pasted API key for this session."
            )
            return

        self._controller.load_environment_key()
        self._render_all()

    def _model_changed(self, _index: int) -> None:
        model = self.model_combo.currentData()
        self._controller.set_selected_model_id(
            model.model_id if isinstance(model, ModelDescriptor) else ""
        )

    def _render_all(self) -> None:
        profile = self._controller.profile()
        self.load_env_button.setToolTip(
            "If the field contains a key, use it for this session. "
            "If the field is empty, load "
            + profile.api_key_env
            + " from the process or Windows User environment."
        )
        gateway_index = self.gateway_combo.findData(profile.gateway_id)
        if gateway_index >= 0 and gateway_index != self.gateway_combo.currentIndex():
            self.gateway_combo.blockSignals(True)
            self.gateway_combo.setCurrentIndex(gateway_index)
            self.gateway_combo.blockSignals(False)
        active = profile.provider_class == "gateway"
        self.setEnabled(active or self.gateway_combo.count() > 0)
        if self.api_key_edit.text() != (self._controller.api_key() if active else ""):
            self.api_key_edit.blockSignals(True)
            self.api_key_edit.setText(self._controller.api_key() if active else "")
            self.api_key_edit.blockSignals(False)
        self.credential_status.setText(
            self._controller.credential_source() if active else "Direct provider selected"
        )
        self.catalog_status.setText(self._controller.catalog_status())
        self.privacy_status.setText(profile.privacy_summary)
        self._render_models()

    def _render_models(self) -> None:
        selected_id = self._controller.selected_model_id()
        profile = self._controller.profile()
        self.model_combo.blockSignals(True)
        self.model_combo.clear()
        if profile.provider_class == "gateway":
            for model in self._controller.visible_models():
                self.model_combo.addItem(
                    "[FREE] " + model.display_name + " - " + model.model_id,
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
        if model is None or profile.provider_class != "gateway":
            self.capability_status.setText("No gateway model selected.")
            return
        structured = (
            "YES"
            if "response_format" in set(model.supported_parameters)
            else "NO/UNKNOWN"
        )
        self.capability_status.setText(
            "Structured output: "
            + structured
            + " | Context window: "
            + str(model.context_window or "unknown")
            + " | Access: "
            + model.price_label()
        )

    def _show_status(self, message: str) -> None:
        self.status_label.setText(str(message))
        self.refresh_button.setEnabled(
            self._controller.catalog_status() != "Loading..."
        )
