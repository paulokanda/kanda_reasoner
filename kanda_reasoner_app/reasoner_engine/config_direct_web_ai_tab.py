# project-path: kanda_reasoner_app/reasoner_engine/config_direct_web_ai_tab.py
"""Direct-provider configuration for the shared Project Web AI tab."""

from __future__ import annotations

from PySide6.QtCore import QSignalBlocker
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
    WebAIConfigurationController,
    application_web_ai_configuration,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ModelDescriptor,
    get_gateway_profile,
    provider_profiles,
)

__all__ = ["ConfigDirectWebAITab"]


class ConfigDirectWebAITab(QWidget):
    """Configure official no-gateway APIs used by Project Web AI."""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        controller: WebAIConfigurationController | None = None,
    ) -> None:
        super().__init__(parent)
        self._controller = controller or application_web_ai_configuration()
        self._build_ui()
        self._wire_events()
        self._render_all()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(14)

        title = QLabel("Direct API Providers")
        title.setStyleSheet("font-size: 21px; font-weight: 700;")
        root.addWidget(title)
        subtitle = QLabel(
            "Configure official direct provider APIs without OpenRouter or Kilo. "
            "Gemini, Mistral, Qwen, and Groq use the existing Project Web AI "
            "conversation, approval, cancellation, and Active Project context."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #5f6368;")
        root.addWidget(subtitle)

        panel = QFrame()
        panel.setObjectName("configDirectWebAIPanel")
        panel.setStyleSheet(
            "QFrame#configDirectWebAIPanel { border: 1px solid #cfd5dc; "
            "border-radius: 8px; background: #ffffff; }"
        )
        form = QFormLayout(panel)
        form.setContentsMargins(18, 18, 18, 18)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(11)

        self.provider_combo = QComboBox()
        for profile in provider_profiles("direct"):
            self.provider_combo.addItem(profile.display_name, profile.gateway_id)
        configure_opaque_combo(self.provider_combo)
        form.addRow("Direct provider", self.provider_combo)

        key_row = QHBoxLayout()
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("Session-only provider API key")
        self.load_env_button = QPushButton("Use Key / Load Environment")
        key_row.addWidget(self.api_key_edit, 1)
        key_row.addWidget(self.load_env_button)
        form.addRow("API key", key_row)

        self.credential_status = QLabel()
        self.credential_status.setWordWrap(True)
        form.addRow("Credential", self.credential_status)

        self.base_url_edit = QLineEdit()
        self.base_url_edit.setPlaceholderText("Official HTTPS base URL")
        form.addRow("Base URL", self.base_url_edit)

        self.free_access_checkbox = QCheckBox()
        form.addRow("Free access guard", self.free_access_checkbox)

        self.free_access_status = QLabel()
        self.free_access_status.setWordWrap(True)
        form.addRow("Free access", self.free_access_status)

        self.model_combo = QComboBox()
        self.model_combo.setMinimumContentsLength(40)
        configure_opaque_combo(self.model_combo)
        form.addRow("Python model", self.model_combo)

        self.refresh_button = QPushButton("Refresh Approved Models")
        form.addRow("Catalog", self.refresh_button)

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
            "Only integrated APIs are listed. Gemini requires an unbilled Free Tier "
            "project, Mistral requires Free mode, Qwen requires remaining free quota "
            "with Free Quota Only, and Groq requires the Free Plan. DeepSeek direct "
            "API is excluded because it is metered."
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            "color: #7a4e00; background: #fff7df; border: 1px solid #e1c36a; "
            "border-radius: 6px; padding: 8px;"
        )
        root.addWidget(warning)
        self.status_label = QLabel("Select a direct provider to activate it.")
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)
        root.addStretch(1)

    def _wire_events(self) -> None:
        self.provider_combo.activated.connect(self._provider_activated)
        self.api_key_edit.textChanged.connect(self._api_key_changed)
        self.load_env_button.clicked.connect(self._accept_or_load_key)
        self.base_url_edit.editingFinished.connect(self._base_url_changed)
        self.free_access_checkbox.toggled.connect(
            self._free_access_confirmation_changed
        )
        self.refresh_button.clicked.connect(self._refresh_models)
        self.model_combo.currentIndexChanged.connect(self._model_changed)
        self._controller.configuration_changed.connect(
            lambda _snapshot: self._render_all()
        )
        self._controller.catalog_changed.connect(
            lambda _models: self._render_models()
        )
        self._controller.status_changed.connect(self.status_label.setText)

    def _selected_direct_provider_id(self) -> str:
        return str(self.provider_combo.currentData() or "").strip()

    def _activate_selected_provider(self) -> None:
        provider_id = self._selected_direct_provider_id()
        if provider_id and self._controller.gateway_id() != provider_id:
            self._controller.set_gateway_id(provider_id)

    def _provider_activated(self, _index: int) -> None:
        self._activate_selected_provider()

    def _api_key_changed(self, text: str) -> None:
        if self._controller.profile().provider_class == "direct":
            self._controller.set_api_key(text)

    def _accept_or_load_key(self) -> None:
        pasted_key = self.api_key_edit.text().strip()
        self._activate_selected_provider()
        if pasted_key:
            self._controller.set_api_key(
                pasted_key,
                source="manual session field",
            )
            self._render_all()
            self.status_label.setText(
                "Accepted the pasted API key for this provider and session."
            )
            return

        self._controller.load_environment_key()
        self._render_all()

    def _base_url_changed(self) -> None:
        self._activate_selected_provider()
        if self._controller.profile().provider_class == "direct":
            self._controller.set_base_url_override(self.base_url_edit.text())

    def _free_access_confirmation_changed(self, checked: bool) -> None:
        self._activate_selected_provider()
        if self._controller.profile().provider_class == "direct":
            self._controller.set_free_access_confirmed(checked)

    def _refresh_models(self) -> None:
        self._activate_selected_provider()
        self._controller.refresh_models()

    def _model_changed(self, _index: int) -> None:
        model = self.model_combo.currentData()
        self._controller.set_selected_model_id(
            model.model_id if isinstance(model, ModelDescriptor) else ""
        )

    def _render_all(self) -> None:
        active_profile = self._controller.profile()
        is_direct = active_profile.provider_class == "direct"
        if is_direct:
            index = self.provider_combo.findData(active_profile.gateway_id)
            if index >= 0:
                with QSignalBlocker(self.provider_combo):
                    self.provider_combo.setCurrentIndex(index)
        selected_id = self._selected_direct_provider_id()
        display_profile = get_gateway_profile(selected_id)
        selected_is_active = (
            is_direct and active_profile.gateway_id == display_profile.gateway_id
        )
        self.load_env_button.setToolTip(
            "If the field contains a key, activate "
            + display_profile.display_name
            + " and use the key for this session. If the field is empty, load "
            + display_profile.api_key_env
            + " from the process or Windows User environment."
        )
        expected_key = self._controller.api_key() if selected_is_active else ""
        if self.api_key_edit.text() != expected_key:
            with QSignalBlocker(self.api_key_edit):
                self.api_key_edit.setText(expected_key)
        expected_url = display_profile.base_url
        if self.base_url_edit.text() != expected_url:
            with QSignalBlocker(self.base_url_edit):
                self.base_url_edit.setText(expected_url)
        if selected_is_active and self._controller.api_key():
            credential = (
                "Key loaded for this session from "
                + self._controller.credential_source()
                + ". The secret remains masked and is not persisted."
            )
        elif selected_is_active:
            credential = "Direct provider active; API key not configured."
        else:
            credential = (
                display_profile.display_name
                + " will activate when you use a pasted key, load an environment "
                "key, change the base URL, or toggle the free-access guard."
            )
        self.credential_status.setText(credential)
        self.free_access_status.setText(
            display_profile.free_access_summary
            + " The guard starts enabled by default. KANDA cannot verify provider "
            "billing, so the provider account must remain on its free access mode."
        )
        required = display_profile.requires_free_confirmation
        self.free_access_checkbox.setEnabled(required)
        if display_profile.gateway_id == "gemini":
            label = "Require an unbilled Gemini Free Tier project."
        elif display_profile.gateway_id == "mistral":
            label = "Require Mistral Free mode."
        elif display_profile.gateway_id == "qwen":
            label = "Require Qwen Free Quota Only."
        elif display_profile.gateway_id == "groq":
            label = "Require a Groq Free Plan organization."
        else:
            label = "Require provider free access."
        self.free_access_checkbox.setText(label)
        with QSignalBlocker(self.free_access_checkbox):
            self.free_access_checkbox.setChecked(
                self._controller.free_access_confirmed()
                if selected_is_active
                else True
            )
        self.catalog_status.setText(
            self._controller.catalog_status() if selected_is_active else "Not loaded"
        )
        self.privacy_status.setText(display_profile.privacy_summary)
        self.refresh_button.setEnabled(
            selected_is_active
            and self._controller.catalog_status() != "Loading..."
        )
        self._render_models()

    def _render_models(self) -> None:
        profile = self._controller.profile()
        selected_id = self._controller.selected_model_id()
        with QSignalBlocker(self.model_combo):
            self.model_combo.clear()
            if profile.provider_class == "direct":
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
        model = self._controller.selected_model()
        if model is None or profile.provider_class != "direct":
            self.capability_status.setText("No direct Python-coding model selected.")
            return
        self.capability_status.setText(
            "Context window: "
            + str(model.context_window or "unknown")
            + " | Access: "
            + model.price_label()
        )
