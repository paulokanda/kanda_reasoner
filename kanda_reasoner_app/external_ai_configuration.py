# project-path: kanda_reasoner_app/external_ai_configuration.py
"""Application-scoped selection for manual external Python-coding assistants."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, QSettings, Signal
from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.python_coding_ai_catalog import (
    ExternalPythonCodingAssistant,
    external_python_coding_assistants,
    get_external_python_coding_assistant,
)

__all__ = [
    "ExternalAIConfigurationController",
    "ExternalAIConfigurationSnapshot",
    "application_external_ai_configuration",
    "install_application_external_ai_configuration",
]

_APP_ATTRIBUTE = "_kanda_external_ai_configuration_controller"
_SETTINGS_ORGANIZATION = "Kanda"
_SETTINGS_APPLICATION = "AIConfiguration"
_ASSISTANT_KEY = "external_ai/selected_assistant_id"
_DEFAULT_ASSISTANT_ID = "deepseek_chat"


@dataclass(frozen=True, slots=True)
class ExternalAIConfigurationSnapshot:
    """Immutable Tool-owned external-assistant preference."""

    revision: str
    assistant_id: str
    display_name: str
    official_url: str
    free_status: str
    last_verified_date: str


class ExternalAIConfigurationController(QObject):
    """Own one application-level external assistant selection."""

    configuration_changed = Signal(object)
    status_changed = Signal(str)
    open_configuration_requested = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
        *,
        settings: Any | None = None,
    ) -> None:
        """Load only the selected assistant ID; never resolve a Project."""
        super().__init__(parent)
        self._settings = settings if settings is not None else QSettings(
            _SETTINGS_ORGANIZATION,
            _SETTINGS_APPLICATION,
        )
        saved = str(self._settings.value(_ASSISTANT_KEY, _DEFAULT_ASSISTANT_ID) or "")
        self._assistant_id = self._normalized_existing_id(saved)
        self._revision = uuid.uuid4().hex

    def assistants(self) -> tuple[ExternalPythonCodingAssistant, ...]:
        """Return the canonical manual assistant catalog."""
        return external_python_coding_assistants()

    def assistant_id(self) -> str:
        """Return the selected stable assistant ID."""
        return self._assistant_id

    def selected_assistant(self) -> ExternalPythonCodingAssistant:
        """Return the selected assistant descriptor."""
        return get_external_python_coding_assistant(self._assistant_id)

    def set_assistant_id(self, assistant_id: str) -> None:
        """Persist one valid Tool-owned assistant preference."""
        clean = self._normalized_existing_id(assistant_id)
        if clean == self._assistant_id:
            return
        self._assistant_id = clean
        self._settings.setValue(_ASSISTANT_KEY, clean)
        self._touch()
        self.status_changed.emit(
            "Selected external Python-coding assistant: "
            + self.selected_assistant().display_name
        )

    def snapshot(self) -> ExternalAIConfigurationSnapshot:
        """Return one immutable selection snapshot with no Project fields."""
        assistant = self.selected_assistant()
        return ExternalAIConfigurationSnapshot(
            revision=self._revision,
            assistant_id=assistant.assistant_id,
            display_name=assistant.display_name,
            official_url=assistant.validated_url(),
            free_status=assistant.free_status,
            last_verified_date=assistant.last_verified_date,
        )

    def request_open_configuration(self) -> None:
        """Ask the shell to reveal the external-assistant configuration tab."""
        self.open_configuration_requested.emit()

    def _normalized_existing_id(self, assistant_id: object) -> str:
        clean = str(assistant_id or "").strip().lower()
        valid = {assistant.assistant_id for assistant in external_python_coding_assistants()}
        return clean if clean in valid else _DEFAULT_ASSISTANT_ID

    def _touch(self) -> None:
        self._revision = uuid.uuid4().hex
        self.configuration_changed.emit(self.snapshot())


def install_application_external_ai_configuration(
    controller: ExternalAIConfigurationController,
) -> None:
    """Install one explicit QApplication-scoped configuration owner."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before External AI setup.")
    setattr(app, _APP_ATTRIBUTE, controller)


def application_external_ai_configuration() -> ExternalAIConfigurationController:
    """Return the QApplication-scoped owner, creating a test-safe owner if needed."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before External AI use.")
    controller = getattr(app, _APP_ATTRIBUTE, None)
    if not isinstance(controller, ExternalAIConfigurationController):
        controller = ExternalAIConfigurationController(app)
        setattr(app, _APP_ATTRIBUTE, controller)
    return controller
