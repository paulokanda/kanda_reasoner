# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_web_controls_runtime.py
"""Docstring Assistant mode controls over the central Web AI configuration."""

from __future__ import annotations

import uuid
from importlib import import_module
from pathlib import Path
from typing import Any

from kanda_reasoner_app.project_support_boundary import (
    ProjectSupportBoundaryError,
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.web_ai_provider_contracts import ModelDescriptor

__all__ = [
    "api_key_from_owner",
    "apply_control_state",
    "build_ai_config",
    "build_ai_group",
    "configuration_revision",
    "gateway_id_from_owner",
    "initialize_controls",
    "invalidate_approval",
    "preferences_payload",
    "provider_mode_from_owner",
    "request_cloud_approval",
    "selected_model_descriptor",
    "selected_model_id",
    "wire_events",
]

_HEURISTIC_MODE = "heuristic"
_LOCAL_MODE = "local"
_WEB_MODE = "web"


def initialize_controls(owner: object, prefs: dict[str, object]) -> None:
    """Create three visible modes and hidden compatibility controls."""
    (
        QButtonGroup,
        QCheckBox,
        QComboBox,
        QLabel,
        QLineEdit,
        QPushButton,
        QRadioButton,
    ) = _qt_widgets(
        "QButtonGroup",
        "QCheckBox",
        "QComboBox",
        "QLabel",
        "QLineEdit",
        "QPushButton",
        "QRadioButton",
    )
    owner._web_ai_configuration = _controller(owner)
    owner._local_ai_configuration = _local_controller(owner)

    owner._heuristic_radio = QRadioButton("Heuristic")
    owner._local_ai_radio = QRadioButton("Local AI")
    owner._web_ai_radio = QRadioButton("Web AI")
    owner._ai_mode_group = QButtonGroup(owner)
    for button in (
        owner._heuristic_radio,
        owner._local_ai_radio,
        owner._web_ai_radio,
    ):
        owner._ai_mode_group.addButton(button)

    preferred = str(prefs.get("ai_provider_mode") or "Heuristic").strip().lower()
    if preferred.startswith("web"):
        owner._web_ai_radio.setChecked(True)
    elif preferred.startswith("local"):
        owner._local_ai_radio.setChecked(True)
    else:
        owner._heuristic_radio.setChecked(True)

    owner._web_ai_summary_label = QLabel()
    owner._web_ai_summary_label.setWordWrap(True)
    owner._open_web_ai_config_button = QPushButton("Open Config AI")

    # Compatibility controls remain non-visual so existing task code and saved
    # Local AI settings keep working while Web configuration has one owner.
    owner._ai_enabled_checkbox = QCheckBox("Enable AI assistance")
    owner._ai_provider_mode_combo = QComboBox()
    owner._ai_provider_mode_combo.addItems(["Local AI", "Web AI"])
    owner._gateway_combo = QComboBox()
    owner._gateway_combo.addItems(["OpenRouter", "Kilo Gateway"])
    owner._base_url_edit = QLineEdit(
        str(prefs.get("base_url") or "http://localhost:11434/v1")
    )
    owner._model_combo = QComboBox()
    owner._model_combo.setEditable(True)
    owner._model_combo.addItem(str(prefs.get("model") or "codellama:13b"))
    owner._refresh_models_button = QPushButton("Refresh models")
    owner._api_key_edit = QLineEdit()
    owner._api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
    owner._load_env_key_button = QPushButton("Load Environment Key")
    owner._free_models_checkbox = QCheckBox("Free models only")
    owner._free_models_checkbox.setChecked(True)
    owner._ai_privacy_label = QLabel()
    owner._web_ai_catalog_models: list[ModelDescriptor] = []
    owner._web_ai_catalog_thread = None
    owner._web_ai_catalog_worker = None
    owner._web_ai_catalog_operation_id = ""
    owner._docstring_web_approval_id = ""
    owner._docstring_web_approval_fingerprint = ""
    _sync_compatibility_controls(owner)
    _render_web_summary(owner)


def build_ai_group(owner: object) -> object:
    """Return only the workflow mode choices and central Web summary."""
    QGroupBox, QHBoxLayout, QVBoxLayout = _qt_widgets(
        "QGroupBox", "QHBoxLayout", "QVBoxLayout"
    )
    group = QGroupBox("AI Assistant")
    layout = QVBoxLayout(group)

    mode_row = QHBoxLayout()
    mode_row.addWidget(owner._heuristic_radio)
    mode_row.addWidget(owner._local_ai_radio)
    mode_row.addWidget(owner._web_ai_radio)
    mode_row.addStretch(1)
    layout.addLayout(mode_row)

    summary_row = QHBoxLayout()
    summary_row.addWidget(owner._web_ai_summary_label, 1)
    summary_row.addWidget(owner._open_web_ai_config_button)
    layout.addLayout(summary_row)
    return group


def preferences_payload(owner: object) -> dict[str, object]:
    """Return non-secret task preferences only."""
    mode = provider_mode_from_owner(owner)
    display = {
        _HEURISTIC_MODE: "Heuristic",
        _LOCAL_MODE: "Local AI",
        _WEB_MODE: "Web AI",
    }[mode]
    return {"ai_provider_mode": display}


def provider_mode_from_owner(owner: object) -> str:
    """Return heuristic, local, or web from the visible radio choices."""
    if _checked(owner, "_web_ai_radio", False):
        return _WEB_MODE
    if _checked(owner, "_local_ai_radio", False):
        return _LOCAL_MODE
    return _HEURISTIC_MODE


def gateway_id_from_owner(owner: object) -> str:
    """Return the central gateway for Web mode, otherwise local."""
    if provider_mode_from_owner(owner) != _WEB_MODE:
        return "local"
    return _controller(owner).gateway_id()


def api_key_from_owner(owner: object) -> str:
    """Return the central session-only credential for Web mode."""
    if provider_mode_from_owner(owner) != _WEB_MODE:
        return ""
    return _controller(owner).api_key()


def selected_model_descriptor(owner: object) -> ModelDescriptor | None:
    """Return the central selected Web model descriptor."""
    if provider_mode_from_owner(owner) != _WEB_MODE:
        return None
    return _controller(owner).selected_model()


def selected_model_id(owner: object) -> str:
    """Return the configured Local or Web model identifier."""
    if provider_mode_from_owner(owner) == _WEB_MODE:
        return _controller(owner).selected_model_id()
    return _local_controller(owner).selected_model_id()

def configuration_revision(owner: object) -> str:
    """Return the active central configuration revision."""
    if provider_mode_from_owner(owner) == _WEB_MODE:
        return _controller(owner).snapshot().revision
    if provider_mode_from_owner(owner) == _LOCAL_MODE:
        return _local_controller(owner).snapshot().revision
    return "heuristic"


def wire_events(owner: object) -> None:
    """Connect three mode choices to compatibility and central config state."""
    for name in ("_heuristic_radio", "_local_ai_radio", "_web_ai_radio"):
        _connect(owner, name, "toggled", lambda *_args, o=owner: _mode_changed(o))
    _connect(
        owner,
        "_open_web_ai_config_button",
        "clicked",
        lambda *_args, o=owner: _open_configuration(o),
    )
    _connect(owner, "_root_path_edit", "textChanged", _invalidate_slot(owner))
    controller = _controller(owner)
    controller.configuration_changed.connect(
        lambda _snapshot, o=owner: _central_config_changed(o)
    )
    controller.catalog_changed.connect(lambda _models, o=owner: _central_config_changed(o))
    controller.status_changed.connect(lambda _message, o=owner: _render_web_summary(o))
    local = _local_controller(owner)
    local.configuration_changed.connect(
        lambda _snapshot, o=owner: _central_config_changed(o)
    )
    local.catalog_changed.connect(lambda _models, o=owner: _central_config_changed(o))
    local.status_changed.connect(lambda _message, o=owner: _render_web_summary(o))
    _mode_changed(owner)


def apply_control_state(owner: object, enabled: bool | None = None) -> None:
    """Synchronize compatibility state; visible mode radios remain available."""
    del enabled
    _sync_compatibility_controls(owner)
    active = provider_mode_from_owner(owner) != _HEURISTIC_MODE
    for name in (
        "_config_path_edit",
        "_load_config_button",
        "_save_config_button",
        "_include_private_checkbox",
        "_min_confidence_combo",
        "_no_uncertain_checkbox",
        "_ai_docstring_verbosity_combo",
    ):
        _set_enabled(getattr(owner, name, None), active)
    _render_web_summary(owner)


def refresh_models(owner: object) -> None:
    """Refresh Local AI locally or Web AI through the central owner."""
    mode = provider_mode_from_owner(owner)
    if mode == _WEB_MODE:
        _controller(owner).refresh_models()
        return
    if mode == _LOCAL_MODE:
        _local_controller(owner).refresh_models()


def build_ai_config(owner: object) -> object:
    """Build task configuration while taking Web fields from one central owner."""
    config_class = import_module(
        "kanda_reasoner_app.insert_missing_docstrings_gui.ai_config"
    ).AIConfig
    mode = provider_mode_from_owner(owner)
    controller = _controller(owner)
    web = mode == _WEB_MODE
    cfg = config_class(
        provider_mode=_WEB_MODE if web else _LOCAL_MODE,
        gateway_id=controller.gateway_id() if web else "local",
        base_url=(
            _line_text(owner, "_base_url_edit") or "http://localhost:11434/v1"
            if web
            else _local_controller(owner).base_url()
        ),
        model=(
            controller.selected_model_id()
            if web
            else _local_controller(owner).selected_model_id()
        ),
        workers=max(1, _spin_value(owner, "_workers_spin", 1)),
        include_private=_checked(owner, "_include_private_checkbox", True),
        min_confidence=_combo_text(owner, "_min_confidence_combo") or "low",
        uncertain_annotation=not _checked(owner, "_no_uncertain_checkbox", False),
        free_models_only=controller.free_models_only() if web else False,
    )
    cfg._api_key = controller.api_key() if web else ""
    return cfg


def request_cloud_approval(
    owner: object,
    *,
    operation: str,
    item_count: int,
    payload_bytes: int,
    input_fingerprint: str,
) -> str:
    """Request approval for one exact Project payload and central config snapshot."""
    if provider_mode_from_owner(owner) != _WEB_MODE:
        return "local-no-cloud-approval"
    try:
        identity = resolve_project_tool_boundary_identity(
            Path(_line_text(owner, "_root_path_edit"))
        )
    except ProjectSupportBoundaryError as exc:
        _warn(owner, "Project boundary", str(exc))
        return ""
    controller = _controller(owner)
    model = controller.selected_model()
    if model is None or not controller.ready_for_chat():
        _warn(
            owner,
            "Web AI not configured",
            "Open Config AI > Config Web AI and complete gateway, credential, and model setup.",
        )
        return ""
    profile = controller.profile()
    description = "\n".join(
        [
            "Operation: " + str(operation),
            "Active Project: " + identity.active_project_slug,
            "Project source: " + str(identity.active_project_root),
            "Project Support: " + str(identity.active_project_support_root),
            "Gateway: " + profile.display_name,
            "Model: " + model.model_id,
            "Items included: " + str(max(0, int(item_count))),
            "Estimated payload bytes: " + str(max(0, int(payload_bytes))),
            "Exact source snippets are included for the selected symbols.",
            "API keys and unrelated Project files are not included.",
            "Privacy status: " + profile.privacy_summary,
            "Configuration revision: " + controller.snapshot().revision[:12],
            "",
            "Approve this request?",
        ]
    )
    QMessageBox = _qt_widgets("QMessageBox")[0]
    result = QMessageBox.question(
        owner,
        "Approve Docstring Web AI Request",
        description,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if result != QMessageBox.Yes:
        return ""
    approval_id = uuid.uuid4().hex
    owner._docstring_web_approval_id = approval_id
    owner._docstring_web_approval_fingerprint = (
        str(input_fingerprint) + "|" + controller.snapshot().revision
    )
    return approval_id


def invalidate_approval(owner: object) -> None:
    """Invalidate any request-specific cloud approval."""
    owner._docstring_web_approval_id = ""
    owner._docstring_web_approval_fingerprint = ""


def _open_configuration(owner: object) -> None:
    if provider_mode_from_owner(owner) == _LOCAL_MODE:
        _local_controller(owner).request_open_configuration()
    else:
        _controller(owner).request_open_configuration()


def _local_controller(owner: object) -> Any:
    module = import_module("kanda_reasoner_app.local_ai_configuration")
    controller_class = module.LocalAIConfigurationController
    controller = getattr(owner, "_local_ai_configuration", None)
    if not isinstance(controller, controller_class):
        controller = module.application_local_ai_configuration()
        owner._local_ai_configuration = controller
    return controller

def _controller(owner: object) -> Any:
    module = import_module("kanda_reasoner_app.web_ai_configuration")
    controller_class = module.WebAIConfigurationController
    controller = getattr(owner, "_web_ai_configuration", None)
    if not isinstance(controller, controller_class):
        controller = module.application_web_ai_configuration()
        owner._web_ai_configuration = controller
    return controller


def _mode_changed(owner: object) -> None:
    invalidate_approval(owner)
    _sync_compatibility_controls(owner)
    apply_control_state(owner)


def _central_config_changed(owner: object) -> None:
    invalidate_approval(owner)
    _sync_compatibility_controls(owner)
    _render_web_summary(owner)


def _sync_compatibility_controls(owner: object) -> None:
    mode = provider_mode_from_owner(owner)
    enabled = mode != _HEURISTIC_MODE
    checkbox = getattr(owner, "_ai_enabled_checkbox", None)
    if checkbox is not None:
        checkbox.blockSignals(True)
        checkbox.setChecked(enabled)
        checkbox.blockSignals(False)
    combo = getattr(owner, "_ai_provider_mode_combo", None)
    if combo is not None:
        combo.blockSignals(True)
        combo.setCurrentText("Web AI" if mode == _WEB_MODE else "Local AI")
        combo.blockSignals(False)
    if mode == _LOCAL_MODE:
        local = _local_controller(owner)
        base = getattr(owner, "_base_url_edit", None)
        if base is not None:
            base.setText(local.base_url())
        model_combo = getattr(owner, "_model_combo", None)
        if model_combo is not None:
            model_combo.clear()
            for model in local.available_models():
                model_combo.addItem(model)
            if local.selected_model_id() and model_combo.findText(local.selected_model_id()) < 0:
                model_combo.addItem(local.selected_model_id())
            model_combo.setCurrentText(local.selected_model_id())
    elif mode == _WEB_MODE:
        controller = _controller(owner)
        gateway = getattr(owner, "_gateway_combo", None)
        if gateway is not None:
            gateway.setCurrentText(
                "Kilo Gateway" if controller.gateway_id() == "kilo" else "OpenRouter"
            )
        model_combo = getattr(owner, "_model_combo", None)
        if model_combo is not None and controller.selected_model_id():
            model_combo.setCurrentText(controller.selected_model_id())
        key = getattr(owner, "_api_key_edit", None)
        if key is not None:
            key.setText(controller.api_key())
        free = getattr(owner, "_free_models_checkbox", None)
        if free is not None:
            free.setChecked(controller.free_models_only())


def _render_web_summary(owner: object) -> None:
    label = getattr(owner, "_web_ai_summary_label", None)
    setter = getattr(label, "setText", None)
    if not callable(setter):
        return
    mode = provider_mode_from_owner(owner)
    if mode == _HEURISTIC_MODE:
        setter("Deterministic heuristic drafting is active.")
    elif mode == _LOCAL_MODE:
        setter("Local AI: " + _local_controller(owner).summary())
    else:
        setter("Web AI: " + _controller(owner).summary())


def _invalidate_slot(owner: object):
    return lambda *args: invalidate_approval(owner)


def _checked(owner: object, name: str, default: bool) -> bool:
    widget = getattr(owner, name, None)
    method = getattr(widget, "isChecked", None)
    return bool(method()) if callable(method) else bool(default)


def _combo_text(owner: object, name: str) -> str:
    widget = getattr(owner, name, None)
    data = getattr(widget, "currentData", None)
    if name == "_model_combo" and callable(data):
        value = str(data() or "").strip()
        if value:
            return value
    method = getattr(widget, "currentText", None)
    return str(method() or "").strip() if callable(method) else ""


def _line_text(owner: object, name: str) -> str:
    widget = getattr(owner, name, None)
    method = getattr(widget, "text", None)
    return str(method() or "").strip() if callable(method) else ""


def _spin_value(owner: object, name: str, default: int) -> int:
    widget = getattr(owner, name, None)
    method = getattr(widget, "value", None)
    try:
        return int(method()) if callable(method) else int(default)
    except (TypeError, ValueError):
        return int(default)


def _set_enabled(widget: object, enabled: bool) -> None:
    method = getattr(widget, "setEnabled", None)
    if callable(method):
        method(bool(enabled))


def _connect(owner: object, name: str, signal_name: str, slot: object) -> None:
    widget = getattr(owner, name, None)
    signal = getattr(widget, signal_name, None)
    method = getattr(signal, "connect", None)
    if callable(method):
        method(slot)


def _warn(owner: object, title: str, message: str) -> None:
    QMessageBox = _qt_widgets("QMessageBox")[0]
    QMessageBox.warning(owner, str(title), str(message))


def _qt_widgets(*names: str) -> tuple[Any, ...]:
    module = import_module("PySide6.QtWidgets")
    return tuple(getattr(module, name) for name in names)
