# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_workers.py
"""Qt worker shells for Project Web AI catalog and chat requests.

The workers delegate all networking to the shared provider runtime. They own
only background execution, progress signals, cooperative cancellation, and
immutable request identity delivery back to the GUI thread.
"""

from __future__ import annotations

from threading import Event
from typing import Mapping, Sequence

from PySide6.QtCore import QObject, Signal, Slot

from kanda_reasoner_app.reasoner_engine.project_web_ai_agent_runtime import (
    run_project_agent_completion,
)
from kanda_reasoner_app.web_ai_model_catalog import fetch_gateway_models
from kanda_reasoner_app.web_ai_provider_contracts import (
    GatewayProfile,
    ProjectWebAIRequestIdentity,
    ProviderCancelledError,
)
from kanda_reasoner_app.web_ai_provider_runtime import stream_chat_completion

__all__ = [
    "ProjectWebAIChatWorker",
    "ProjectWebAIModelCatalogWorker",
]


class ProjectWebAIModelCatalogWorker(QObject):
    """Fetch one web-gateway model catalog off the GUI thread."""

    completed = Signal(str, object)
    failed = Signal(str, str)
    finished = Signal()

    def __init__(
        self,
        profile: GatewayProfile,
        api_key: str,
        operation_id: str,
    ) -> None:
        """Store the immutable catalog request."""
        super().__init__()
        self._profile = profile
        self._api_key = str(api_key or "")
        self._operation_id = str(operation_id)

    @Slot()
    def run(self) -> None:
        """Fetch the catalog and emit a typed result or explicit failure."""
        try:
            models = fetch_gateway_models(self._profile, self._api_key)
        except Exception as exc:
            self.failed.emit(
                self._operation_id,
                exc.__class__.__name__ + ": " + str(exc),
            )
        else:
            self.completed.emit(self._operation_id, models)
        finally:
            self.finished.emit()


class ProjectWebAIChatWorker(QObject):
    """Stream one project-aware web AI response off the GUI thread."""

    started = Signal(object)
    token_ready = Signal(object, str)
    completed = Signal(object, object)
    failed = Signal(object, str)
    cancelled = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        profile: GatewayProfile,
        model_id: str,
        api_key: str,
        messages: Sequence[Mapping[str, str]],
        request_identity: ProjectWebAIRequestIdentity,
        project_root: str = "",
    ) -> None:
        """Store one immutable request and create its cancellation event."""
        super().__init__()
        self._profile = profile
        self._model_id = str(model_id or "")
        self._api_key = str(api_key or "")
        self._messages = tuple(dict(message) for message in messages)
        self._request_identity = request_identity
        self._project_root = str(project_root or "").strip()
        self._cancel_event = Event()

    @Slot()
    def run(self) -> None:
        """Execute the stream and emit request-card-bound events."""
        identity = self._request_identity
        self.started.emit(identity)
        try:
            if self._project_root:
                result = run_project_agent_completion(
                    self._profile,
                    self._model_id,
                    self._messages,
                    self._api_key,
                    project_root=self._project_root,
                    request_identity=identity,
                    cancel_event=self._cancel_event,
                )
            else:
                result = stream_chat_completion(
                    self._profile,
                    self._model_id,
                    self._messages,
                    self._api_key,
                    request_id=identity.request_id,
                    cancel_event=self._cancel_event,
                    on_token=self._emit_token,
                )
        except ProviderCancelledError:
            self.cancelled.emit(identity)
        except Exception as exc:
            self.failed.emit(
                identity,
                exc.__class__.__name__ + ": " + str(exc),
            )
        else:
            if self._cancel_event.is_set():
                self.cancelled.emit(identity)
            else:
                self.completed.emit(identity, result)
        finally:
            self.finished.emit()

    def _emit_token(self, token: str) -> None:
        """Emit one token with the complete immutable request identity."""
        if not self._cancel_event.is_set():
            self.token_ready.emit(self._request_identity, str(token))

    @Slot()
    def cancel(self) -> None:
        """Request cooperative cancellation of the active HTTP stream."""
        self._cancel_event.set()
