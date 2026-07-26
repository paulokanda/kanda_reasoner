# project-path: kanda_reasoner_app/web_ai_configuration.py
"""Application-scoped Web AI configuration for all KANDA workflow tabs.

The controller owns only reusable Tool configuration: gateway, session-only
credential, dynamic model catalog, free-model filtering, and the selected
model.  Active Project identity is deliberately absent and must be resolved by
each workflow at request time.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.reasoner_engine.project_web_ai_workers import (
    ProjectWebAIModelCatalogWorker,
)
from kanda_reasoner_app.web_ai_credentials import resolve_environment_key
from kanda_reasoner_app.web_ai_provider_contracts import (
    GatewayProfile,
    ModelDescriptor,
    get_gateway_profile,
)

__all__ = [
    "WebAIConfigurationController",
    "WebAIConfigurationSnapshot",
    "application_web_ai_configuration",
    "install_application_web_ai_configuration",
]

_APP_ATTRIBUTE = "_kanda_web_ai_configuration_controller"


@dataclass(frozen=True, slots=True, kw_only=True)
class WebAIConfigurationSnapshot:
    """Immutable non-Project Web AI configuration used by one request."""

    revision: str
    gateway_id: str
    model_id: str
    free_models_only: bool
    catalog_timestamp: str
    credential_source: str
    credential_available: bool
    privacy_summary: str
    structured_output_supported: bool


class WebAIConfigurationController(QObject):
    """Own one application-scoped Web AI configuration and catalog."""

    configuration_changed = Signal(object)
    catalog_changed = Signal(object)
    status_changed = Signal(str)
    open_configuration_requested = Signal()

    def __init__(self, parent: QObject | None = None) -> None:
        """Initialize safe defaults without resolving any active Project."""
        super().__init__(parent)
        self._gateway_id = "openrouter"
        self._free_models_only = True
        self._selected_model_id = ""
        self._api_keys: dict[str, str] = {}
        self._credential_sources: dict[str, str] = {}
        self._all_models: list[ModelDescriptor] = []
        self._catalog_status = "Not loaded"
        self._revision = uuid.uuid4().hex
        self._operation_id = ""
        self._catalog_thread: QThread | None = None
        self._catalog_worker: ProjectWebAIModelCatalogWorker | None = None

    def profile(self) -> GatewayProfile:
        """Return the selected immutable gateway profile."""
        return get_gateway_profile(self._gateway_id)

    def gateway_id(self) -> str:
        """Return the selected gateway identifier."""
        return self._gateway_id

    def set_gateway_id(self, gateway_id: str) -> None:
        """Select a gateway and invalidate incompatible catalog state."""
        clean = str(gateway_id or "").strip().lower()
        profile = get_gateway_profile(clean)
        if profile.gateway_id == self._gateway_id:
            return
        self.cancel_catalog_refresh()
        self._gateway_id = profile.gateway_id
        self._all_models = []
        self._selected_model_id = ""
        self._catalog_status = "Not loaded"
        self._touch()
        self.catalog_changed.emit(tuple())

    def free_models_only(self) -> bool:
        """Return whether the shared model view is free-only."""
        return self._free_models_only

    def set_free_models_only(self, enabled: bool) -> None:
        """Set the shared model filter without changing catalog ownership."""
        value = bool(enabled)
        if value == self._free_models_only:
            return
        self._free_models_only = value
        if self._selected_model_id and self.selected_model() is None:
            self._selected_model_id = ""
        self._touch()
        self.catalog_changed.emit(tuple(self.visible_models()))

    def api_key(self) -> str:
        """Return the current gateway credential from memory only."""
        return self._api_keys.get(self._gateway_id, "")

    def credential_source(self) -> str:
        """Return a safe source label for the selected credential."""
        return self._credential_sources.get(self._gateway_id, "not configured")

    def set_api_key(self, value: str, *, source: str = "manual session field") -> None:
        """Store one session-only key without persistence or logging."""
        clean = str(value or "").strip()
        if clean:
            self._api_keys[self._gateway_id] = clean
            self._credential_sources[self._gateway_id] = str(source or "session")
        else:
            self._api_keys.pop(self._gateway_id, None)
            self._credential_sources.pop(self._gateway_id, None)
        self._touch()

    def load_environment_key(self) -> bool:
        """Load the selected gateway key through the canonical Tool owner."""
        return self._load_environment_key(silent=False)

    def _load_environment_key(self, *, silent: bool) -> bool:
        profile = self.profile()
        value, source = resolve_environment_key(profile.api_key_env)
        if not value:
            if not silent:
                self.status_changed.emit(
                    profile.api_key_env
                    + " was not found in the process or Windows User environment."
                )
            return False
        self._api_keys[profile.gateway_id] = value
        self._credential_sources[profile.gateway_id] = source
        self._touch()
        self.status_changed.emit(
            "Loaded " + profile.api_key_env + " from " + source + " for this session."
        )
        return True

    def all_models(self) -> tuple[ModelDescriptor, ...]:
        """Return the selected gateway's normalized catalog."""
        return tuple(self._all_models)

    def visible_models(self) -> tuple[ModelDescriptor, ...]:
        """Return models after the shared free-only filter."""
        return tuple(
            model
            for model in self._all_models
            if not self._free_models_only or model.free_status
        )

    def selected_model_id(self) -> str:
        """Return the shared selected model identifier."""
        return self._selected_model_id

    def set_selected_model_id(self, model_id: str) -> None:
        """Select one visible model exactly; never substitute another model."""
        clean = str(model_id or "").strip()
        valid_ids = {model.model_id for model in self.visible_models()}
        if clean and clean not in valid_ids:
            clean = ""
        if clean == self._selected_model_id:
            return
        self._selected_model_id = clean
        self._touch()

    def selected_model(self) -> ModelDescriptor | None:
        """Return the exact selected normalized model descriptor."""
        for model in self.visible_models():
            if model.model_id == self._selected_model_id:
                return model
        return None

    def catalog_status(self) -> str:
        """Return a safe human-readable catalog status."""
        return self._catalog_status

    def refresh_models(self) -> bool:
        """Refresh the selected gateway catalog off the GUI thread."""
        if self._catalog_thread is not None:
            self.status_changed.emit("A Web AI model refresh is already running.")
            return False
        profile = self.profile()
        api_key = self.api_key()
        if profile.api_key_required and not api_key:
            self.status_changed.emit(profile.display_name + " requires an API key.")
            return False
        operation_id = uuid.uuid4().hex
        thread = QThread(self)
        worker = ProjectWebAIModelCatalogWorker(profile, api_key, operation_id)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.completed.connect(self._catalog_completed)
        worker.failed.connect(self._catalog_failed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._catalog_finished)
        self._operation_id = operation_id
        self._catalog_thread = thread
        self._catalog_worker = worker
        self._catalog_status = "Loading..."
        self.status_changed.emit(
            "Refreshing " + profile.display_name + " model catalog..."
        )
        thread.start()
        return True

    def cancel_catalog_refresh(self) -> None:
        """Invalidate one catalog result; catalog workers are short-lived reads."""
        self._operation_id = uuid.uuid4().hex

    def _catalog_completed(self, operation_id: str, models: object) -> None:
        if operation_id != self._operation_id or not isinstance(models, list):
            return
        self._all_models = [
            model
            for model in models
            if isinstance(model, ModelDescriptor)
            and model.gateway_id == self._gateway_id
        ]
        visible = self.visible_models()
        visible_ids = {model.model_id for model in visible}
        if self._selected_model_id not in visible_ids:
            self._selected_model_id = visible[0].model_id if visible else ""
        timestamp = (
            self._all_models[0].catalog_timestamp
            if self._all_models
            else "unknown"
        )
        self._catalog_status = f"{len(self._all_models)} models; updated {timestamp}"
        self._touch()
        self.catalog_changed.emit(tuple(visible))
        self.status_changed.emit(
            "Model catalog loaded from " + self.profile().display_name + "."
        )

    def _catalog_failed(self, operation_id: str, message: str) -> None:
        if operation_id != self._operation_id:
            return
        self._all_models = []
        self._selected_model_id = ""
        self._catalog_status = "FAILED"
        self._touch()
        self.catalog_changed.emit(tuple())
        self.status_changed.emit(str(message))

    def _catalog_finished(self) -> None:
        self._catalog_thread = None
        self._catalog_worker = None

    def snapshot(self) -> WebAIConfigurationSnapshot:
        """Return an immutable request configuration with no Project identity."""
        model = self.selected_model()
        return WebAIConfigurationSnapshot(
            revision=self._revision,
            gateway_id=self._gateway_id,
            model_id="" if model is None else model.model_id,
            free_models_only=self._free_models_only,
            catalog_timestamp="" if model is None else model.catalog_timestamp,
            credential_source=self.credential_source(),
            credential_available=bool(self.api_key()),
            privacy_summary=self.profile().privacy_summary,
            structured_output_supported=bool(
                model is not None
                and "response_format" in set(model.supported_parameters)
            ),
        )

    def ready_for_chat(self) -> bool:
        """Return whether the central configuration can issue a chat request."""
        model = self.selected_model()
        if model is None:
            return False
        profile = self.profile()
        if profile.api_key_required and not self.api_key():
            return False
        if not model.free_status and not self.api_key():
            return False
        return True

    def summary(self) -> str:
        """Return one compact non-secret configuration summary."""
        profile = self.profile()
        model = self.selected_model()
        model_text = "No model selected" if model is None else model.model_id
        key_text = "credential ready" if self.api_key() else "credential missing"
        return profile.display_name + " | " + model_text + " | " + key_text

    def request_open_configuration(self) -> None:
        """Ask the shell to reveal the single editable Config Web AI tab."""
        self.open_configuration_requested.emit()

    def _touch(self) -> None:
        self._revision = uuid.uuid4().hex
        self.configuration_changed.emit(self.snapshot())


def install_application_web_ai_configuration(
    controller: WebAIConfigurationController,
) -> None:
    """Install one explicit QApplication-scoped configuration owner."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before Web AI configuration setup.")
    setattr(app, _APP_ATTRIBUTE, controller)


def application_web_ai_configuration() -> WebAIConfigurationController:
    """Return the QApplication-scoped owner, creating a test-safe owner if needed."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before Web AI configuration use.")
    controller = getattr(app, _APP_ATTRIBUTE, None)
    if not isinstance(controller, WebAIConfigurationController):
        controller = WebAIConfigurationController(app)
        setattr(app, _APP_ATTRIBUTE, controller)
    return controller
