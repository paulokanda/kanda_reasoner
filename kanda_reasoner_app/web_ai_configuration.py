# project-path: kanda_reasoner_app/web_ai_configuration.py
"""Application-scoped remote Web AI configuration for all KANDA workflow tabs.

The controller owns reusable Tool configuration only: provider, session-only
credential, optional direct-provider base URL, free-access confirmation,
dynamic model catalog, and selected model. Active Project identity is absent
and must be resolved by each workflow at request time.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, replace
from urllib.parse import urlsplit

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.python_coding_ai_catalog import (
    is_approved_free_python_coding_model,
)
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
    provider_class: str
    model_id: str
    free_models_only: bool
    free_access_kind: str
    free_access_confirmed: bool
    catalog_timestamp: str
    credential_source: str
    credential_available: bool
    privacy_summary: str
    structured_output_supported: bool
    base_url: str


class WebAIConfigurationController(QObject):
    """Own one application-scoped remote provider configuration and catalog."""

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
        self._base_url_overrides: dict[str, str] = {}
        self._free_access_confirmations: dict[str, bool] = {}
        self._all_models: list[ModelDescriptor] = []
        self._catalog_status = "Not loaded"
        self._revision = uuid.uuid4().hex
        self._operation_id = ""
        self._catalog_thread: QThread | None = None
        self._catalog_worker: ProjectWebAIModelCatalogWorker | None = None

    def profile(self) -> GatewayProfile:
        """Return the selected immutable provider profile with a safe override."""
        profile = get_gateway_profile(self._gateway_id)
        override = self._base_url_overrides.get(profile.gateway_id, "")
        return replace(profile, base_url=override) if override else profile

    def gateway_id(self) -> str:
        """Return the selected provider identifier."""
        return self._gateway_id

    def set_gateway_id(self, gateway_id: str) -> None:
        """Select a provider and invalidate incompatible catalog state."""
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
        """Return the locked approved-free Python-coding policy."""
        return True

    def set_free_models_only(self, enabled: bool) -> None:
        """Preserve compatibility while refusing paid or unapproved visibility."""
        if not bool(enabled):
            self.status_changed.emit(
                "Web AI is locked to approved free Python-coding access."
            )
        if not self._free_models_only:
            self._free_models_only = True
            self._touch()
            self.catalog_changed.emit(tuple(self.visible_models()))

    def api_key(self) -> str:
        """Return the selected provider credential from memory only."""
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
        """Load the selected provider key through the canonical Tool owner."""
        profile = self.profile()
        value, source = resolve_environment_key(profile.api_key_env)
        if not value:
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

    def base_url_override(self) -> str:
        """Return the selected provider session-only base URL override."""
        return self._base_url_overrides.get(self._gateway_id, "")

    def set_base_url_override(self, value: str) -> None:
        """Store one validated HTTPS base URL override in memory only."""
        clean = str(value or "").strip().rstrip("/")
        default_url = get_gateway_profile(self._gateway_id).base_url.rstrip("/")
        if clean:
            parsed = urlsplit(clean)
            if parsed.scheme.lower() != "https" or not parsed.hostname:
                self.status_changed.emit("Provider base URL must be a valid HTTPS URL.")
                return
            if parsed.username or parsed.password or parsed.fragment:
                self.status_changed.emit(
                    "Provider base URL must not contain credentials or fragments."
                )
                return
        normalized_override = "" if clean == default_url else clean
        current_override = self._base_url_overrides.get(self._gateway_id, "")
        if normalized_override == current_override:
            return
        if normalized_override:
            self._base_url_overrides[self._gateway_id] = normalized_override
        else:
            self._base_url_overrides.pop(self._gateway_id, None)
        self._all_models = []
        self._selected_model_id = ""
        self._catalog_status = "Not loaded"
        self._touch()
        self.catalog_changed.emit(tuple())

    def free_access_confirmation_required(self) -> bool:
        """Return whether this provider needs an explicit free-mode assertion."""
        return self.profile().requires_free_confirmation

    def free_access_confirmed(self) -> bool:
        """Return the session-only free-access guard for this provider."""
        if not self.free_access_confirmation_required():
            return True
        return self._free_access_confirmations.get(self._gateway_id, True)

    def set_free_access_confirmed(self, confirmed: bool) -> None:
        """Store one session-only assertion without changing provider billing."""
        self._free_access_confirmations[self._gateway_id] = bool(confirmed)
        self._touch()

    def all_models(self) -> tuple[ModelDescriptor, ...]:
        """Return the selected provider's normalized catalog."""
        return tuple(self._all_models)

    def visible_models(self) -> tuple[ModelDescriptor, ...]:
        """Return only approved free Python-coding models for the provider."""
        return tuple(
            model
            for model in self._all_models
            if is_approved_free_python_coding_model(model)
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
        """Refresh or construct the selected provider catalog off the GUI thread."""
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
        """Invalidate one catalog result; workers are short-lived reads."""
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
        timestamp = self._all_models[0].catalog_timestamp if self._all_models else "unknown"
        self._catalog_status = (
            f"{len(self._all_models)} provider models; "
            f"{len(visible)} approved free Python-coding models; updated {timestamp}"
        )
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
        profile = self.profile()
        model = self.selected_model()
        return WebAIConfigurationSnapshot(
            revision=self._revision,
            gateway_id=self._gateway_id,
            provider_class=profile.provider_class,
            model_id="" if model is None else model.model_id,
            free_models_only=self._free_models_only,
            free_access_kind=profile.free_access_kind,
            free_access_confirmed=self.free_access_confirmed(),
            catalog_timestamp="" if model is None else model.catalog_timestamp,
            credential_source=self.credential_source(),
            credential_available=bool(self.api_key()),
            privacy_summary=profile.privacy_summary,
            structured_output_supported=bool(
                model is not None
                and "response_format" in set(model.supported_parameters)
            ),
            base_url=profile.base_url,
        )

    def ready_for_chat(self) -> bool:
        """Return whether the central configuration can issue a chat request."""
        model = self.selected_model()
        if model is None or not model.free_status:
            return False
        profile = self.profile()
        if profile.api_key_required and not self.api_key():
            return False
        if not self.free_access_confirmed():
            return False
        return True

    def summary(self) -> str:
        """Return one compact non-secret configuration summary."""
        profile = self.profile()
        model = self.selected_model()
        model_text = "No model selected" if model is None else model.model_id
        key_text = "credential ready" if self.api_key() else "credential missing"
        return (
            profile.display_name
            + " | "
            + profile.provider_class
            + " | "
            + model_text
            + " | "
            + key_text
        )

    def request_open_configuration(self) -> None:
        """Ask the shell to reveal the appropriate Config AI subtab."""
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
