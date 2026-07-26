# project-path: kanda_reasoner_app/tab3_manual_review_runtime/ai_docstring_async_runtime.py
"""Asynchronous AI draft jobs with Project-bound stale-result guards."""

from __future__ import annotations

from pathlib import Path
from threading import Event

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.project_support_boundary import ProjectSupportBoundaryError
from kanda_reasoner_app.tab3_manual_review_runtime import (
    ai_docstring_row_bridge_runtime,
    ai_openai_compatible_provider_runtime,
    ai_web_controls_runtime,
    ai_web_docstring_provider_runtime,
    inline_preview_runtime,
    review_status_visibility,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    ProviderCallable,
    generate_ai_docstring_with_fallback,
)
from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_task_contracts import (
    DocstringTaskIdentity,
    DocstringTaskItem,
    DocstringTaskOutcome,
    build_identity,
    build_items,
    current_project_identity,
    job_input_hash,
    payload_bytes,
    row_snapshot_hash,
    text_hash,
)
from kanda_reasoner_app.tab3_manual_review_runtime.review_support import (
    _save_manual_review_state,
)

__all__ = ["cancel_ai_draft_job", "start_ai_draft_job", "wire_ai_draft_events"]


class DocstringAIDraftWorker(QObject):
    """Generate one or more docstring drafts outside the GUI thread."""

    progress = Signal(object, int, int)
    completed = Signal(object, object)
    failed = Signal(object, str)
    cancelled = Signal(object)
    finished = Signal()

    def __init__(
        self,
        *,
        identity: DocstringTaskIdentity,
        items: tuple[DocstringTaskItem, ...],
        provider: ProviderCallable,
    ) -> None:
        """Store one immutable job and cancellation event."""
        super().__init__()
        self._identity = identity
        self._items = items
        self._provider = provider
        self._cancel_event = Event()

    @Slot()
    def run(self) -> None:
        """Generate drafts and emit immutable task-bound outcomes."""
        outcomes: list[DocstringTaskOutcome] = []
        try:
            total = len(self._items)
            for index, item in enumerate(self._items, start=1):
                if self._cancel_event.is_set():
                    self.cancelled.emit(self._identity)
                    return
                result = generate_ai_docstring_with_fallback(
                    item.request,
                    self._provider,
                )
                outcomes.append(
                    DocstringTaskOutcome(item_id=item.item_id, result=result)
                )
                self.progress.emit(self._identity, index, total)
            if self._cancel_event.is_set():
                self.cancelled.emit(self._identity)
            else:
                self.completed.emit(self._identity, tuple(outcomes))
        except Exception as exc:
            self.failed.emit(
                self._identity,
                exc.__class__.__name__ + ": " + str(exc),
            )
        finally:
            self.finished.emit()

    @Slot()
    def cancel(self) -> None:
        """Request cancellation after the current provider call."""
        self._cancel_event.set()


class _DocstringDraftReceiver(QObject):
    """Apply terminal results on the GUI thread after freshness checks."""

    def __init__(self, owner: object) -> None:
        super().__init__(owner)
        self._owner = owner

    @Slot(object, int, int)
    def on_progress(self, identity: object, completed: int, total: int) -> None:
        """Display progress only for the current request."""
        if _identity_is_current(self._owner, identity):
            _status(
                self._owner,
                "Generating AI docstrings: " + str(completed) + "/" + str(total),
            )

    @Slot(object, object)
    def on_completed(self, identity: object, outcomes: object) -> None:
        """Restore controls before applying fresh preview results."""
        _restore_action_state(self._owner)
        if not _identity_is_current(self._owner, identity):
            _append_output(
                self._owner,
                "[review] stale AI result rejected after Project or settings change.\n",
            )
            return
        accepted = _apply_outcomes(self._owner, tuple(outcomes or ()))
        _append_output(
            self._owner,
            "[review] AI draft job complete | accepted=" + str(accepted) + "\n",
        )
        _refresh_visible_state(self._owner)

    @Slot(object, str)
    def on_failed(self, identity: object, message: str) -> None:
        """Restore controls and display a current safe failure."""
        _restore_action_state(self._owner)
        if _identity_is_current(self._owner, identity):
            _append_output(
                self._owner,
                "[review] AI draft job failed: " + str(message) + "\n",
            )
        else:
            _append_output(self._owner, "[review] stale AI failure ignored.\n")

    @Slot(object)
    def on_cancelled(self, identity: object) -> None:
        """Restore controls and report cooperative cancellation."""
        _restore_action_state(self._owner)
        if _identity_is_current(self._owner, identity):
            _append_output(self._owner, "[review] AI draft job cancelled.\n")


def wire_ai_draft_events(owner: object) -> None:
    """Connect the optional Stop AI Drafts button."""
    button = getattr(owner, "_review_stop_ai_drafts_button", None)
    signal = getattr(button, "clicked", None)
    connect = getattr(signal, "connect", None)
    if callable(connect):
        connect(lambda *args: cancel_ai_draft_job(owner))


def start_ai_draft_job(owner: object, scope: str) -> bool:
    """Start a selected, visible, or all-row AI job."""
    if getattr(owner, "_docstring_ai_thread", None) is not None:
        _warn(owner, "AI work running", "Wait for or stop the current AI job.")
        return False
    rows = [
        row
        for row in _rows_for_scope(owner, scope)
        if inline_preview_runtime.is_reviewable_docstring_row(row)
    ]
    if not rows:
        _append_output(owner, "[review] no reviewable rows for AI generation.\n")
        return False
    if _normalize_scope(scope) == "all" and not _confirm_all(owner, len(rows)):
        return False
    try:
        project = current_project_identity(owner)
        items, row_map, snapshot = build_items(owner, project, rows)
    except (OSError, ValueError, ProjectSupportBoundaryError) as exc:
        _warn(owner, "AI draft boundary", str(exc))
        return False
    provider, gateway_id, approval_id = _resolve_provider(owner, scope, items)
    if provider is None:
        return False
    identity = build_identity(
        owner,
        project,
        operation_id="docstring_" + _normalize_scope(scope),
        input_hash=job_input_hash(items),
        gateway_id=gateway_id,
        approval_id=approval_id,
    )
    _start_worker(owner, identity, items, row_map, snapshot, provider)
    return True


def cancel_ai_draft_job(owner: object) -> None:
    """Invalidate and cooperatively cancel the current draft job."""
    worker = getattr(owner, "_docstring_ai_worker", None)
    if worker is None:
        _append_output(owner, "[review] no active AI draft job.\n")
        return
    owner._docstring_ai_active_identity = None
    worker.cancel()
    _restore_action_state(owner)
    _status(owner, "Stopping AI drafts after the current request...")


def _resolve_provider(
    owner: object,
    scope: str,
    items: tuple[DocstringTaskItem, ...],
) -> tuple[ProviderCallable | None, str, str]:
    """Resolve local or approved Web AI provider configuration."""
    mode = ai_web_controls_runtime.provider_mode_from_owner(owner)
    if mode != "web":
        provider = (
            ai_openai_compatible_provider_runtime.local_openai_compatible_provider_from_owner(
                owner
            )
        )
        if provider is None:
            _warn(
                owner,
                "Local AI",
                "Open Config AI > Config Local AI and select a model first.",
            )
        return provider, "local", "local-no-cloud-approval"
    model = ai_web_controls_runtime.selected_model_descriptor(owner)
    if model is None or "response_format" not in set(model.supported_parameters):
        _warn(
            owner,
            "Structured model required",
            "Refresh models and select one that advertises response_format support.",
        )
        return None, "", ""
    input_hash = job_input_hash(items)
    approval_id = ai_web_controls_runtime.request_cloud_approval(
        owner,
        operation="Docstring Assistant " + _normalize_scope(scope) + " drafts",
        item_count=len(items),
        payload_bytes=payload_bytes(items),
        input_fingerprint=input_hash,
    )
    if not approval_id:
        _append_output(owner, "[review] Web AI request cancelled before transmission.\n")
        return None, "", ""
    provider = ai_web_docstring_provider_runtime.web_provider_from_owner(owner)
    if provider is None:
        _warn(owner, "Web AI", "The selected Web AI provider is unavailable.")
        return None, "", ""
    return provider, ai_web_controls_runtime.gateway_id_from_owner(owner), approval_id


def _start_worker(
    owner: object,
    identity: DocstringTaskIdentity,
    items: tuple[DocstringTaskItem, ...],
    row_map: dict[str, dict],
    snapshot: list[dict],
    provider: ProviderCallable,
) -> None:
    """Create worker, receiver, thread, and current job registry."""
    thread = QThread(owner)
    worker = DocstringAIDraftWorker(identity=identity, items=items, provider=provider)
    receiver = _DocstringDraftReceiver(owner)
    worker.moveToThread(thread)
    owner._docstring_ai_active_identity = identity
    owner._docstring_ai_row_map = row_map
    owner._docstring_ai_items = {item.item_id: item for item in items}
    owner._docstring_ai_thread = thread
    owner._docstring_ai_worker = worker
    owner._docstring_ai_receiver = receiver
    owner._last_bulk_draft_snapshot = snapshot
    _set_action_state(owner, running=True)
    thread.started.connect(worker.run)
    worker.progress.connect(receiver.on_progress)
    worker.completed.connect(receiver.on_completed)
    worker.failed.connect(receiver.on_failed)
    worker.cancelled.connect(receiver.on_cancelled)
    worker.finished.connect(thread.quit)
    thread.finished.connect(lambda: _cleanup_job(owner))
    thread.start()
    _status(owner, "AI generation started for " + str(len(items)) + " item(s).")


def _cleanup_job(owner: object) -> None:
    """Release QObject references after terminal GUI state restoration."""
    worker = getattr(owner, "_docstring_ai_worker", None)
    if worker is not None:
        worker.deleteLater()
    thread = getattr(owner, "_docstring_ai_thread", None)
    if thread is not None:
        thread.deleteLater()
    owner._docstring_ai_worker = None
    owner._docstring_ai_thread = None
    owner._docstring_ai_receiver = None
    owner._docstring_ai_active_identity = None
    owner._docstring_ai_items = {}
    owner._docstring_ai_row_map = {}
    _restore_action_state(owner)


def _apply_outcomes(owner: object, outcomes: tuple[DocstringTaskOutcome, ...]) -> int:
    """Apply fresh source-bound outcomes to GUI-owned rows."""
    accepted = 0
    row_map = dict(getattr(owner, "_docstring_ai_row_map", {}) or {})
    item_map = dict(getattr(owner, "_docstring_ai_items", {}) or {})
    for outcome in outcomes:
        row = row_map.get(outcome.item_id)
        item = item_map.get(outcome.item_id)
        if not isinstance(row, dict) or not isinstance(item, DocstringTaskItem):
            continue
        try:
            module_text = Path(item.source_path).read_text(
                encoding="utf-8", errors="replace"
            )
        except OSError:
            continue
        if text_hash(module_text) != item.source_hash:
            _append_output(owner, "[review] source changed; one draft was rejected.\n")
            continue
        current_request = ai_docstring_row_bridge_runtime.build_review_row_ai_request(
            owner,
            row,
            module_text,
        )
        if row_snapshot_hash(row, current_request) != item.row_snapshot_hash:
            _append_output(owner, "[review] row changed; one draft was rejected.\n")
            continue
        ai_docstring_row_bridge_runtime.apply_ai_result_to_review_row(
            row,
            outcome.result,
            current_request,
            owner,
        )
        _save_manual_review_state(owner, row, str(row.get("draft_docstring") or ""))
        review_status_visibility.append_draft_generation_output(owner, row, "ai")
        accepted += 1
    return accepted


def _identity_is_current(owner: object, identity: object) -> bool:
    """Return whether a result matches current Project and provider state."""
    active = getattr(owner, "_docstring_ai_active_identity", None)
    if not isinstance(identity, DocstringTaskIdentity) or active != identity:
        return False
    try:
        project = current_project_identity(owner)
    except (ProjectSupportBoundaryError, OSError, ValueError):
        return False
    if project.active_project_id != identity.active_project_id:
        return False
    if project.active_project_root_fingerprint != identity.active_project_root_fingerprint:
        return False
    mode = ai_web_controls_runtime.provider_mode_from_owner(owner)
    if mode != identity.assistant_mode:
        return False
    if mode in {"local", "web"}:
        if ai_web_controls_runtime.configuration_revision(owner) != identity.configuration_revision:
            return False
    if mode == "web":
        if ai_web_controls_runtime.gateway_id_from_owner(owner) != identity.gateway_id:
            return False
        if ai_web_controls_runtime.selected_model_id(owner) != identity.model_id:
            return False
        if str(getattr(owner, "_docstring_web_approval_id", "")) != identity.privacy_approval_id:
            return False
    return True


def _rows_for_scope(owner: object, scope: str) -> list[dict]:
    """Return mutable rows for selected, visible, or all scope."""
    normalized = _normalize_scope(scope)
    if normalized == "selected":
        row = _current_review_row(owner)
        return [row] if row else []
    rows = [row for row in getattr(owner, "_report_rows", ()) if isinstance(row, dict)]
    if normalized == "visible":
        matcher = getattr(owner, "_matches_review_filter", None)
        return [row for row in rows if not callable(matcher) or matcher(row)]
    return rows


def _current_review_row(owner: object) -> dict | None:
    """Return the current review row from the list item data."""
    review_list = getattr(owner, "_review_list", None)
    current = getattr(review_list, "currentItem", None)
    item = current() if callable(current) else None
    if item is None:
        return None
    method = getattr(item, "data", None)
    if not callable(method):
        return None
    for role in (256, None):
        try:
            value = method() if role is None else method(role)
        except (TypeError, RuntimeError):
            continue
        if isinstance(value, dict):
            return value
    return None


def _normalize_scope(scope: str) -> str:
    value = str(scope or "").strip().lower().replace(" ", "_")
    if value in {"selected", "selected_row", "current"}:
        return "selected"
    if value in {"visible", "visible_rows", "filtered"}:
        return "visible"
    return "all"


def _confirm_all(owner: object, count: int) -> bool:
    result = QMessageBox.question(
        owner,
        "Generate All AI Drafts",
        "Generate AI drafts for " + str(count) + " rows? Source files remain unchanged.",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    return result == QMessageBox.Yes


def _set_action_state(owner: object, *, running: bool) -> None:
    for name in (
        "_review_generate_draft_button",
        "_review_generate_visible_drafts_button",
        "_review_generate_all_drafts_button",
    ):
        button = getattr(owner, name, None)
        setter = getattr(button, "setEnabled", None)
        if callable(setter):
            setter(not running)
    stop = getattr(owner, "_review_stop_ai_drafts_button", None)
    setter = getattr(stop, "setEnabled", None)
    if callable(setter):
        setter(running)


def _restore_action_state(owner: object) -> None:
    _set_action_state(owner, running=False)
    _status(owner, "Ready")


def _refresh_visible_state(owner: object) -> None:
    from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime

    inline_corrector_runtime.refresh_inline_corrector_for_selection(
        owner,
        _current_review_row(owner),
    )
    refresh = getattr(owner, "_refresh_review_summary", None)
    if callable(refresh):
        refresh()


def _append_output(owner: object, text: str) -> None:
    method = getattr(owner, "_append_text", None)
    if callable(method):
        method(str(text))


def _status(owner: object, text: str) -> None:
    method = getattr(owner, "statusBar", None)
    if callable(method):
        method().showMessage(str(text))


def _warn(owner: object, title: str, message: str) -> None:
    QMessageBox.warning(owner, str(title), str(message))
