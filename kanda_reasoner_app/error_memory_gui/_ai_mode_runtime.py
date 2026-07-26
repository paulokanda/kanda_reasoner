# project-path: kanda_reasoner_app/error_memory_gui/_ai_mode_runtime.py
"""Error Memory correction modes over the central Web AI configuration."""

from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import (
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QRadioButton,
)

from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)
from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    application_web_ai_configuration,
)

__all__ = [
    "build_mode_group",
    "central_configuration",
    "local_configuration",
    "initialize_mode_controls",
    "selected_mode",
    "set_running_state",
    "sync_mode_controls",
    "wire_mode_controls",
]

HEURISTIC_MODE = "heuristic"
LOCAL_AI_MODE = "local"
WEB_AI_MODE = "web"


def initialize_mode_controls(owner: Any) -> None:
    """Create only the three workflow mode choices required by Error Memory."""
    owner._error_memory_web_ai_configuration = application_web_ai_configuration()
    owner._error_memory_local_ai_configuration = application_local_ai_configuration()
    owner._error_memory_heuristic_radio = QRadioButton("Heuristic", owner)
    owner._error_memory_local_ai_radio = QRadioButton("Local AI", owner)
    owner._error_memory_web_ai_radio = QRadioButton("Web AI", owner)
    owner._error_memory_heuristic_radio.setObjectName("error_memory_mode_heuristic")
    owner._error_memory_local_ai_radio.setObjectName("error_memory_mode_local_ai")
    owner._error_memory_web_ai_radio.setObjectName("error_memory_mode_web_ai")
    owner._error_memory_ai_mode_group = QButtonGroup(owner)
    for button in (
        owner._error_memory_heuristic_radio,
        owner._error_memory_local_ai_radio,
        owner._error_memory_web_ai_radio,
    ):
        owner._error_memory_ai_mode_group.addButton(button)
    owner._error_memory_heuristic_radio.setChecked(True)
    owner._error_memory_ai_running = False


def build_mode_group(owner: Any) -> QGroupBox:
    """Return the compact per-workflow mode selector without Web settings."""
    group = QGroupBox("Correction Engine", owner)
    group.setObjectName("error_memory_correction_engine_group")
    row = QHBoxLayout(group)
    row.addWidget(owner._error_memory_heuristic_radio)
    row.addWidget(owner._error_memory_local_ai_radio)
    row.addWidget(owner._error_memory_web_ai_radio)
    row.addStretch(1)
    return group


def wire_mode_controls(owner: Any) -> None:
    """Bind mode changes and central configuration changes to visible state."""
    for button in (
        owner._error_memory_heuristic_radio,
        owner._error_memory_local_ai_radio,
        owner._error_memory_web_ai_radio,
    ):
        button.toggled.connect(lambda _checked=False, tab=owner: sync_mode_controls(tab))
    controller = central_configuration(owner)
    controller.configuration_changed.connect(
        lambda _snapshot, tab=owner: sync_mode_controls(tab)
    )
    controller.catalog_changed.connect(
        lambda _models, tab=owner: sync_mode_controls(tab)
    )
    local = local_configuration(owner)
    local.configuration_changed.connect(
        lambda _snapshot, tab=owner: sync_mode_controls(tab)
    )
    local.catalog_changed.connect(
        lambda _models, tab=owner: sync_mode_controls(tab)
    )
    sync_mode_controls(owner)


def selected_mode(owner: Any) -> str:
    """Return the selected correction mode, preserving local legacy callers."""
    web = getattr(owner, "_error_memory_web_ai_radio", None)
    local = getattr(owner, "_error_memory_local_ai_radio", None)
    heuristic = getattr(owner, "_error_memory_heuristic_radio", None)
    if web is not None and web.isChecked():
        return WEB_AI_MODE
    if local is not None and local.isChecked():
        return LOCAL_AI_MODE
    if heuristic is not None and heuristic.isChecked():
        return HEURISTIC_MODE
    return LOCAL_AI_MODE


def central_configuration(owner: Any) -> WebAIConfigurationController:
    """Return the single QApplication-scoped Web AI configuration owner."""
    controller = getattr(owner, "_error_memory_web_ai_configuration", None)
    if not isinstance(controller, WebAIConfigurationController):
        controller = application_web_ai_configuration()
        owner._error_memory_web_ai_configuration = controller
    return controller


def local_configuration(owner: Any) -> LocalAIConfigurationController:
    """Return the single QApplication-scoped Local AI configuration owner."""
    controller = getattr(owner, "_error_memory_local_ai_configuration", None)
    if not isinstance(controller, LocalAIConfigurationController):
        controller = application_local_ai_configuration()
        owner._error_memory_local_ai_configuration = controller
    return controller


def set_running_state(owner: Any, running: bool) -> None:
    """Lock mode changes while one correction worker is active."""
    owner._error_memory_ai_running = bool(running)
    for name in (
        "_error_memory_heuristic_radio",
        "_error_memory_local_ai_radio",
        "_error_memory_web_ai_radio",
    ):
        button = getattr(owner, name, None)
        if button is not None:
            button.setEnabled(not running)
    sync_mode_controls(owner)


def sync_mode_controls(owner: Any) -> None:
    """Project the selected mode onto action labels and safe enablement."""
    action = getattr(owner, "correct_with_ai_button", None)
    if action is None:
        return
    if bool(getattr(owner, "_error_memory_ai_running", False)):
        action.setEnabled(False)
        action.setText("Correcting with AI...")
        return

    has_modes = any(
        getattr(owner, name, None) is not None
        for name in (
            "_error_memory_heuristic_radio",
            "_error_memory_local_ai_radio",
            "_error_memory_web_ai_radio",
        )
    )
    if not has_modes:
        action.setText("Correct with AI")
        action.setEnabled(True)
        return

    mode = selected_mode(owner)
    heuristic_button = getattr(owner, "heuristic_correction_button", None)
    if mode == HEURISTIC_MODE:
        action.setText("Correct with Heuristic")
        can_apply = bool(
            heuristic_button is not None and heuristic_button.isEnabled()
        )
        action.setEnabled(can_apply)
        action.setToolTip(
            "Apply deterministic Level 1 normalization. No model request is sent."
        )
        return
    if mode == LOCAL_AI_MODE:
        action.setText("Correct with Local AI")
        action.setEnabled(True)
        action.setToolTip(
            "Run the globally configured Local AI model in a background worker and "
            "load the result as preview only. Current: "
            + local_configuration(owner).summary()
        )
        return

    controller = central_configuration(owner)
    action.setText("Correct with Web AI")
    action.setEnabled(True)
    action.setToolTip(
        "Use the single Config AI Web selection and load the result as preview "
        "only. Current configuration: " + controller.summary()
    )
