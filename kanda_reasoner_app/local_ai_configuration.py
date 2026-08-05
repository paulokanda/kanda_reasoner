# project-path: kanda_reasoner_app/local_ai_configuration.py
"""Application-scoped Local AI configuration for all KANDA workflow tabs.

The controller owns reusable Tool configuration only: one local OpenAI-compatible
endpoint, one selected model, and one live model catalog. Active Project
identity and Project Support paths are deliberately absent and remain owned by
each workflow at request time.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Callable

from PySide6.QtCore import QObject, QSettings, QThread, Signal, Slot
from PySide6.QtWidgets import QApplication

from kanda_reasoner_app.local_ai_runtime_state import (
    LocalAIConfigurationSnapshot as _LocalAIConfigurationSnapshot,
    publish_runtime_local_ai_configuration_snapshot as _publish_runtime_configuration_snapshot,
)

__all__ = [
    "DEFAULT_LOCAL_AI_BASE_URL",
    "LocalAIConfigurationController",
    "application_local_ai_configuration",
    "install_application_local_ai_configuration",
    "normalize_local_ai_base_url",
]

_APP_ATTRIBUTE = "_kanda_local_ai_configuration_controller"
_SETTINGS_ORGANIZATION = "Kanda"
_SETTINGS_APPLICATION = "AIConfiguration"
_BASE_URL_KEY = "local_ai/base_url"
_MODEL_KEY = "local_ai/selected_model_id"
_LEGACY_APPLICATION = "ProjectReasonerV10"
_LEGACY_MODEL_KEY = "selected_model"
DEFAULT_LOCAL_AI_BASE_URL = "http://127.0.0.1:11434/v1"
class _LocalModelCatalogWorker(QObject):
    """Read one local model catalog outside the GUI thread."""

    completed = Signal(str, str, object)
    failed = Signal(str, str, str)
    finished = Signal()

    def __init__(
        self,
        *,
        operation_id: str,
        base_url: str,
        registry_factory: Callable[..., Any] | None = None,
    ) -> None:
        super().__init__()
        self._operation_id = operation_id
        self._base_url = base_url
        self._registry_factory = registry_factory

    @Slot()
    def run(self) -> None:
        """Load normalized model names and report a bounded result."""
        try:
            if self._registry_factory is None:
                from kanda_reasoner_app.reasoner_engine.v10_model_registry import (
                    LocalModelRegistry,
                )

                registry = LocalModelRegistry(
                    base_url=self._base_url,
                    preferred_model="",
                )
            else:
                registry = self._registry_factory(
                    base_url=self._base_url,
                    preferred_model="",
                )
            models = [
                str(model).strip()
                for model in registry.list_models()
                if str(model).strip()
            ]
            self.completed.emit(self._operation_id, self._base_url, models)
        except Exception as exc:  # defensive worker boundary
            self.failed.emit(
                self._operation_id,
                self._base_url,
                exc.__class__.__name__ + ": " + str(exc),
            )
        finally:
            self.finished.emit()


class LocalAIConfigurationController(QObject):
    """Own one application-scoped Local AI endpoint, model, and catalog."""

    configuration_changed = Signal(object)
    catalog_changed = Signal(object)
    status_changed = Signal(str)
    open_configuration_requested = Signal()

    def __init__(
        self,
        parent: QObject | None = None,
        *,
        settings: Any | None = None,
        registry_factory: Callable[..., Any] | None = None,
    ) -> None:
        """Load Tool-owned settings without resolving an active Project."""
        super().__init__(parent)
        self._settings = settings if settings is not None else QSettings(
            _SETTINGS_ORGANIZATION,
            _SETTINGS_APPLICATION,
        )
        self._registry_factory = registry_factory
        self._base_url = normalize_local_ai_base_url(
            self._settings.value(_BASE_URL_KEY, DEFAULT_LOCAL_AI_BASE_URL)
        )
        saved_model = str(self._settings.value(_MODEL_KEY, "") or "").strip()
        if not saved_model:
            legacy = QSettings(_SETTINGS_ORGANIZATION, _LEGACY_APPLICATION)
            saved_model = str(legacy.value(_LEGACY_MODEL_KEY, "") or "").strip()
        self._selected_model_id = saved_model
        self._models: list[str] = []
        self._catalog_status = "Not loaded"
        self._catalog_timestamp = ""
        self._operation_id = ""
        self._catalog_thread: QThread | None = None
        self._catalog_worker: _LocalModelCatalogWorker | None = None
        self._revision = self._build_revision()
        self._open_target = ""
        self._publish_runtime_snapshot()

    def base_url(self) -> str:
        """Return the one shared local OpenAI-compatible base URL."""
        return self._base_url

    def set_base_url(self, value: str) -> None:
        """Persist a normalized Tool-owned endpoint and clear stale catalog data."""
        clean = normalize_local_ai_base_url(value)
        if clean == self._base_url:
            return
        self.cancel_catalog_refresh()
        self._base_url = clean
        self._models = []
        self._catalog_status = "Not loaded"
        self._catalog_timestamp = ""
        self._settings.setValue(_BASE_URL_KEY, clean)
        self._touch()
        self.catalog_changed.emit(tuple())

    def selected_model_id(self) -> str:
        """Return the globally selected local model identifier."""
        return self._selected_model_id

    def set_selected_model_id(self, model_id: str) -> None:
        """Persist one global model selection without Project coupling."""
        clean = str(model_id or "").strip()
        if clean == self._selected_model_id:
            return
        self._selected_model_id = clean
        self._settings.setValue(_MODEL_KEY, clean)
        self._touch()

    def available_models(self) -> tuple[str, ...]:
        """Return the current normalized catalog with selected model first."""
        return tuple(_preferred_first(self._models, self._selected_model_id))

    def catalog_status(self) -> str:
        """Return one safe status for the current local catalog."""
        return self._catalog_status

    def refresh_models(self) -> bool:
        """Refresh the local catalog off the GUI thread."""
        if self._catalog_thread is not None:
            self.status_changed.emit("A Local AI model refresh is already running.")
            return False
        operation_id = uuid.uuid4().hex
        base_url = self._base_url
        thread = QThread(self)
        worker = _LocalModelCatalogWorker(
            operation_id=operation_id,
            base_url=base_url,
            registry_factory=self._registry_factory,
        )
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
        self.status_changed.emit("Refreshing Local AI model catalog...")
        thread.start()
        return True

    def cancel_catalog_refresh(self) -> None:
        """Invalidate an in-flight read without terminating the worker unsafely."""
        self._operation_id = uuid.uuid4().hex

    @Slot(str, str, object)
    def _catalog_completed(self, operation_id: str, base_url: str, models: object) -> None:
        if operation_id != self._operation_id or base_url != self._base_url:
            return
        normalized = sorted(
            {str(model).strip() for model in list(models or ()) if str(model).strip()},
            key=str.casefold,
        )
        self._models = normalized
        if not self._selected_model_id and normalized:
            self._selected_model_id = normalized[0]
            self._settings.setValue(_MODEL_KEY, self._selected_model_id)
        elif self._selected_model_id not in normalized and normalized:
            self._selected_model_id = normalized[0]
            self._settings.setValue(_MODEL_KEY, self._selected_model_id)
        self._catalog_timestamp = datetime.now(timezone.utc).replace(
            microsecond=0
        ).isoformat()
        self._catalog_status = (
            str(len(normalized)) + " models; updated " + self._catalog_timestamp
        )
        self._touch()
        self.catalog_changed.emit(self.available_models())
        self.status_changed.emit("Local AI model catalog loaded.")

    @Slot(str, str, str)
    def _catalog_failed(self, operation_id: str, base_url: str, message: str) -> None:
        if operation_id != self._operation_id or base_url != self._base_url:
            return
        self._models = []
        self._catalog_status = "FAILED"
        self._catalog_timestamp = ""
        self._touch()
        self.catalog_changed.emit(tuple())
        self.status_changed.emit(str(message))

    def _catalog_finished(self) -> None:
        self._catalog_thread = None
        self._catalog_worker = None

    def ready_for_chat(self) -> bool:
        """Return whether endpoint and global model are configured."""
        return bool(self._base_url and self._selected_model_id)

    def snapshot(self) -> _LocalAIConfigurationSnapshot:
        """Return immutable Tool configuration with no Project identity."""
        return _LocalAIConfigurationSnapshot(
            revision=self._revision,
            base_url=self._base_url,
            model_id=self._selected_model_id,
            catalog_status=self._catalog_status,
            catalog_timestamp=self._catalog_timestamp,
            available_models=self.available_models(),
            ready_for_chat=self.ready_for_chat(),
        )

    def summary(self) -> str:
        """Return one compact non-secret Local AI configuration summary."""
        model = self._selected_model_id or "No model selected"
        return self._base_url + " | " + model

    def request_open_configuration(self) -> None:
        """Ask the shell to reveal Config AI's Local AI subtab."""
        self._open_target = "local"
        self.open_configuration_requested.emit()

    def consume_open_target(self) -> str:
        """Return and clear the pending Config AI subtab target."""
        target = self._open_target
        self._open_target = ""
        return target

    def _touch(self) -> None:
        self._revision = self._build_revision()
        self._publish_runtime_snapshot()
        self.configuration_changed.emit(self.snapshot())

    def _publish_runtime_snapshot(self) -> None:
        _publish_runtime_configuration_snapshot(self.snapshot())

    def _build_revision(self) -> str:
        payload = {
            "base_url": self._base_url,
            "model_id": self._selected_model_id,
        }
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode("utf-8")
        ).hexdigest()


def normalize_local_ai_base_url(value: object) -> str:
    """Normalize an OpenAI-compatible base URL to one stable ``/v1`` root."""
    clean = str(value or "").strip().rstrip("/")
    if not clean:
        return DEFAULT_LOCAL_AI_BASE_URL
    suffix = "/chat/completions"
    if clean.endswith(suffix):
        clean = clean[: -len(suffix)]
    if not clean.endswith("/v1"):
        clean += "/v1"
    return clean


def _preferred_first(models: list[str], preferred: str) -> list[str]:
    ordered = list(models)
    clean = str(preferred or "").strip()
    if clean in ordered:
        ordered.remove(clean)
        ordered.insert(0, clean)
    elif clean:
        ordered.insert(0, clean)
    return ordered



def install_application_local_ai_configuration(
    controller: LocalAIConfigurationController,
) -> None:
    """Install one explicit QApplication-scoped Local AI configuration owner."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before Local AI configuration setup.")
    setattr(app, _APP_ATTRIBUTE, controller)


def application_local_ai_configuration() -> LocalAIConfigurationController:
    """Return the QApplication-scoped owner, creating a test-safe owner if needed."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication must exist before Local AI configuration use.")
    controller = getattr(app, _APP_ATTRIBUTE, None)
    if not isinstance(controller, LocalAIConfigurationController):
        controller = LocalAIConfigurationController(app)
        setattr(app, _APP_ATTRIBUTE, controller)
    return controller
