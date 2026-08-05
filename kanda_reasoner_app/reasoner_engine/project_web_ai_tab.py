# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py
"""Project Web AI tab using the application-scoped Config Web AI owner."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import QThread, QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox, QWidget

from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_workflow import (
    ProjectWebAIApplyWorkflowMixin,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_bridge import load_project_web_ai_context
from kanda_reasoner_app.reasoner_engine.project_web_ai_change_preparation import (
    ProjectWebAIChangePreparationMixin,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_complete_json_router import (
    SmartProjectContextError,
    build_remote_approval_text,
    route_complete_json_context,
)
from kanda_reasoner_app.reasoner_engine import (
    project_web_ai_configuration_selector as web_selector,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_conversations import (
    ProjectWebAIChatHistoryMixin,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
    ProjectWebAISessionLifecycle,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_switch_guard import request_guarded_project_switch
from kanda_reasoner_app.reasoner_engine.project_web_ai_tab_ui import (
    build_project_web_ai_ui,
    create_project_web_ai_controls,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_workers import ProjectWebAIChatWorker
from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    application_web_ai_configuration,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ContextSnapshot,
    GatewayProfile,
    ModelDescriptor,
    ProjectWebAIRequestIdentity,
)
from kanda_reasoner_app.web_ai_provider_runtime import build_project_messages

__all__ = ["ProjectWebAITab"]


class ProjectWebAITab(
    ProjectWebAIApplyWorkflowMixin,
    ProjectWebAIChangePreparationMixin,
    ProjectWebAIChatHistoryMixin,
    QWidget,
):
    """Provide one web-only, project-aware advisory chat surface."""

    def __init__(self) -> None:
        """Build the tab and bind the single central Web AI configuration."""
        super().__init__()
        self._context: ContextSnapshot | None = None
        self._history: list[dict[str, str]] = []
        self._active_request_identity: ProjectWebAIRequestIdentity | None = None
        self._active_config_revision = ""
        self._active_question = ""
        self._chat_thread: QThread | None = None
        self._chat_worker: ProjectWebAIChatWorker | None = None
        self._project_session = ProjectWebAISessionLifecycle()
        self._scheduled_reload_epoch = 0
        self._close_pending = False
        self._project_reload_timer = QTimer(self)
        self._project_reload_timer.setSingleShot(True)
        self._switch_wait_timer = QTimer(self)
        self._switch_wait_timer.setSingleShot(True)
        self._web_config: WebAIConfigurationController = (
            application_web_ai_configuration()
        )

        create_project_web_ai_controls(self)
        build_project_web_ai_ui(self)
        self._initialize_chat_history()
        self._initialize_apply_workflow()
        self._initialize_change_preparation()
        self._connect_signals()
        self._connect_web_configuration()
        web_selector.connect(self)
        self._render_web_configuration()
        self._update_send_state()
    def _connect_signals(self) -> None:
        """Connect user commands and Project state changes."""
        self.pick_project_button.clicked.connect(self._pick_project)
        self.reload_context_button.clicked.connect(self.reload_context)
        self.project_root_edit.textChanged.connect(self._on_project_root_changed)
        self.open_web_config_button.clicked.connect(
            self._web_config.request_open_configuration
        )
        self.question_edit.textChanged.connect(self._update_send_state)
        self.send_button.clicked.connect(self.send_question)
        self.stop_button.clicked.connect(self.stop_request)
        self._project_reload_timer.timeout.connect(self._reload_if_current_epoch)
        self._switch_wait_timer.timeout.connect(self._warn_if_switch_still_waiting)
        self._connect_chat_history_signals()
        self._connect_change_preparation_signals()
    def _connect_web_configuration(self) -> None:
        """Invalidate active work whenever the central configuration changes."""
        self._web_config.configuration_changed.connect(
            self._on_web_configuration_changed
        )
        self._web_config.catalog_changed.connect(self._on_web_catalog_changed)
        self._web_config.status_changed.connect(self._on_web_status_changed)
    def _pick_project(self) -> None:
        """Let the user select a real Project source root."""
        start = self.project_root_edit.text().strip() or str(Path.cwd())
        selected = QFileDialog.getExistingDirectory(
            self, "Select project source root", start
        )
        if selected:
            self.project_root_edit.setText(selected)
    def _on_project_root_changed(self, text: str) -> None:
        """Clear old Project state and schedule only a safe current reload."""
        decision = request_guarded_project_switch(self, text)
        if decision is None:
            return
        self.stop_request()
        self._invalidate_active_request()
        self._clear_project_session_ui()
        if decision.wait_for_worker:
            self.status_value.setText(
                "Project switch waiting for the previous request to stop. "
                "No new Project context has been loaded."
            )
            self._project_reload_timer.stop()
            self._switch_wait_timer.start(5000)
        elif decision.reload_allowed:
            self._switch_wait_timer.stop()
            self._schedule_project_reload(decision.project_epoch)
        else:
            self._project_reload_timer.stop()
            self._switch_wait_timer.stop()
            self.status_value.setText("Select a project and load context.")
        self._update_send_state()

    def _clear_project_session_ui(self) -> None:
        """Clear only transient Project Web AI state for the old Project."""
        self._context = None
        self._clear_change_preparation_for_project()
        self._reset_chat_history_for_project()
        self.support_root_value.setText("Not resolved")
        self.collector_status_value.setText("Not loaded")
        self.snapshot_value.setText("Not loaded")
        self.context_size_value.setText("0 bytes")
        self.context_details.clear()

    def _schedule_project_reload(self, project_epoch: int) -> None:
        """Schedule one quiet reload bound to the newest Project epoch."""
        self._scheduled_reload_epoch = project_epoch
        self._project_reload_timer.start(80)

    def _reload_if_current_epoch(self) -> None:
        """Load context only for the newest settled root-change event."""
        root_text = self.project_root_edit.text().strip()
        if not self._project_session.reload_is_current(
            self._scheduled_reload_epoch,
            root_text,
        ):
            return
        path = Path(root_text).expanduser()
        if path.is_dir():
            self.reload_context(quiet=True)

    def _warn_if_switch_still_waiting(self) -> None:
        """Expose a blocking worker without forcing unsafe thread teardown."""
        if self._project_session.waiting_for_worker:
            self.status_value.setText(
                "Project switch is blocked until the previous request settles. "
                "The old result cannot update the new Project session."
            )

    def reload_context(self, _checked: bool = False, *, quiet: bool = False) -> None:
        """Load a bounded immutable snapshot from Project Support."""
        if self._project_session.waiting_for_worker or self._chat_thread is not None:
            self.status_value.setText(
                "Context reload is blocked until the previous request settles."
            )
            self._update_send_state()
            return
        try:
            snapshot = load_project_web_ai_context(
                self.project_root_edit.text().strip()
            )
            session_identity = self._project_session.bind_snapshot(snapshot)
        except Exception as exc:
            self.status_value.setText(exc.__class__.__name__ + ": " + str(exc))
            if not quiet:
                QMessageBox.warning(self, "Context load failed", str(exc))
            self._context = None
            self._update_send_state()
            return
        self._context = snapshot
        retired_apply = self._retire_change_cycle_after_context_refresh(snapshot)
        self.support_root_value.setText(snapshot.support_root)
        self.collector_status_value.setText(snapshot.collector_status)
        self.snapshot_value.setText(snapshot.short_hash())
        estimate = max(1, snapshot.context_bytes // 4)
        self.context_size_value.setText(
            f"{snapshot.context_bytes:,} bytes (~{estimate:,} tokens)"
        )
        self.context_details.setPlainText(
            "Tool: " + snapshot.tool_project_slug
            + "\nTool source: " + snapshot.tool_source_root
            + "\nActive Project: " + snapshot.project_slug
            + "\nProject ID: " + snapshot.project_id
            + "\nProject root: " + snapshot.project_root
            + "\nProject epoch: " + str(session_identity.project_epoch)
            + "\nProject Support: " + snapshot.support_root
            + "\nDaily work: " + snapshot.daily_work_root
            + "\nSelf-hosting: " + ("YES" if snapshot.self_hosting_mode else "NO")
            + "\nSupport identity: " + snapshot.support_identity_status
            + "\nGenerated: " + (snapshot.generated_at_utc or "unknown")
            + "\nLoaded artifacts:\n- " + "\n- ".join(snapshot.artifacts_loaded)
            + "\n\nOmitted by default:\n- " + "\n- ".join(snapshot.omitted_sections)
        )
        if retired_apply:
            self.status_value.setText(
                "Fresh handoff loaded after verified source update. The previous "
                "Apply cycle was retired; start a new chat before preparing changes."
            )
        else:
            self.status_value.setText(
                "Compact project handoff loaded. Smart complete-JSON routing is "
                "evaluated for each approved question."
            )
        self._update_send_state()

    def _current_profile(self) -> GatewayProfile:
        """Return the central immutable gateway profile."""
        return self._web_config.profile()

    def _selected_model(self) -> ModelDescriptor | None:
        """Return the exact central selected model."""
        return self._web_config.selected_model()

    def _on_web_configuration_changed(self, _snapshot: object) -> None:
        """Reject active results and refresh the compact configuration summary."""
        self.stop_request()
        self._invalidate_active_request()
        self._render_web_configuration()
        self._update_send_state()

    def _on_web_catalog_changed(self, _models: object) -> None:
        """Refresh the catalog summary through an owned Qt receiver."""
        self._render_web_configuration()

    def _on_web_status_changed(self, message: str) -> None:
        """Show central catalog or credential status without exposing secrets."""
        self.web_config_status_value.setText(str(message))
        self._render_web_configuration()

    def _render_web_configuration(self) -> None:
        """Render the central Web configuration as read-only summary text."""
        self.web_config_summary_value.setText(self._web_config.summary())
        self.web_config_status_value.setText(self._web_config.catalog_status())
        self.web_config_privacy_value.setText(
            self._web_config.profile().privacy_summary
        )
        web_selector.render(self)

    def send_question(self) -> None:
        """Confirm remote transmission and start one request-bound stream."""
        if self._chat_thread is not None or self._context is None:
            return
        model = self._selected_model()
        if model is None:
            QMessageBox.warning(
                self,
                "Web AI not configured",
                "Open Config Web AI, refresh models, and select a model first.",
            )
            return
        profile = self._current_profile()
        api_key = self._web_config.api_key()
        if not self._web_config.ready_for_chat():
            QMessageBox.warning(
                self,
                "Web AI not ready",
                "Open Config Web AI and complete the provider, credential, "
                "and model setup.",
            )
            return
        question = self.question_edit.toPlainText().strip()
        if not question:
            return
        try:
            routed_context = route_complete_json_context(
                self._context.project_root, question, self._context.context_text
            )
        except SmartProjectContextError as exc:
            self.status_value.setText(str(exc))
            QMessageBox.warning(self, "Smart context failed", str(exc))
            return
        approved = QMessageBox.question(
            self,
            "Approve remote project-context transmission",
            build_remote_approval_text(
                profile,
                model,
                self._context,
                routed_context,
                api_key_provided=bool(api_key),
                read_tools_enabled=self.inspect_project_checkbox.isChecked(),
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if approved != QMessageBox.StandardButton.Yes:
            self.status_value.setText(
                "Remote transmission cancelled. No request was sent."
            )
            return

        context = self._context
        session_identity = self._project_session.identity
        if session_identity is None:
            self.status_value.setText(
                "Project session is not ready. Reload the selected Project context."
            )
            self._update_send_state()
            return
        config_snapshot = self._web_config.snapshot()
        identity = ProjectWebAIRequestIdentity(
            request_id=uuid.uuid4().hex,
            session_id=self._active_chat().session_id,
            project_id=context.project_id,
            project_slug=context.project_slug,
            project_root_fingerprint=context.project_root_fingerprint,
            support_root=context.support_root,
            snapshot_id=context.snapshot_id,
            context_hash=context.context_hash,
            gateway_id=profile.gateway_id,
            model_id=model.model_id,
            privacy_approval_id=uuid.uuid4().hex,
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            project_epoch=session_identity.project_epoch,
            evidence_context_hash=routed_context.evidence_context_hash,
        )
        messages = build_project_messages(
            question,
            routed_context.context_text,
            self._history,
            trusted_boundary_text=context.trusted_boundary_text,
        )
        agent_root = context.project_root if self.inspect_project_checkbox.isChecked() else ""
        thread = QThread(self)
        worker = ProjectWebAIChatWorker(
            profile=profile,
            model_id=model.model_id,
            api_key=api_key,
            messages=messages,
            request_identity=identity,
            project_root=agent_root,
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.started.connect(self._on_chat_started)
        worker.token_ready.connect(self._on_chat_token)
        worker.completed.connect(self._on_chat_completed)
        worker.failed.connect(self._on_chat_failed)
        worker.cancelled.connect(self._on_chat_cancelled)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._chat_thread_finished)
        self._request_mode = "chat"
        self._active_request_identity = identity
        self._active_config_revision = config_snapshot.revision
        self._active_question = question
        self._chat_thread = thread
        self._chat_worker = worker
        self._begin_chat_turn(question)
        self.provenance_box.clear()
        route_label = "Smart complete-JSON" if routed_context.smart_context_used else "Compact"
        self.status_value.setText("Starting remote request with " + route_label + " context...")
        self._update_send_state()
        thread.start()

    def _event_is_current(self, identity: object) -> bool:
        """Accept events only for the exact Project and central config snapshot."""
        if not isinstance(identity, ProjectWebAIRequestIdentity):
            return False
        context = self._context
        model = self._selected_model()
        return bool(
            context is not None
            and model is not None
            and identity == self._active_request_identity
            and self._request_mode == "chat"
            and self._active_config_revision == self._web_config.snapshot().revision
            and identity.session_id == self._active_chat().session_id
            and self._project_session.request_is_current(identity, context)
            and identity.gateway_id == self._current_profile().gateway_id
            and identity.model_id == model.model_id
            and bool(identity.evidence_context_hash)
        )

    def _chat_thread_finished(self) -> None:
        """Release the worker and resume only the newest pending switch."""
        self._chat_thread = None
        self._chat_worker = None
        self._settle_change_request()
        self._request_mode = ""
        self._invalidate_active_request()
        decision = self._project_session.worker_settled()
        self._switch_wait_timer.stop()
        if self._close_pending:
            self._close_pending = False
            QTimer.singleShot(0, self.close)
            return
        if decision.reload_allowed:
            self.status_value.setText(
                "Previous request settled. Loading the newly selected Project."
            )
            self._schedule_project_reload(decision.project_epoch)
        self._update_send_state()

    def _invalidate_active_request(self) -> None:
        """Reject later events from the previous request."""
        self._active_request_identity = None
        self._active_config_revision = ""
        self._active_question = ""

    def _protected_export_roots(self) -> tuple[Path, ...]:
        """Return all Tool, Project, support, and transient write barriers."""
        if self._context is None:
            project_text = self.project_root_edit.text().strip()
            return (Path(project_text).expanduser(),) if project_text else ()
        return tuple(
            Path(value).expanduser()
            for value in (
                self._context.tool_source_root,
                self._context.project_root,
                self._context.support_root,
                self._context.daily_work_root,
            )
        )

    def stop_request(self) -> None:
        """Request cooperative cancellation of the active stream."""
        if self._chat_worker is not None:
            self.status_value.setText("Cancelling request...")
            self._chat_worker.cancel()

    def clear_session(self) -> None:
        """Preserve the public command by creating a new memory-only chat."""
        self.new_chat()

    def _update_send_state(self) -> None:
        """Apply fail-closed command availability."""
        running = self._chat_thread is not None
        switching = self._project_session.waiting_for_worker
        transaction_locked = self._project_session.transaction_blocks_project_switch
        locked = running or switching or transaction_locked
        ready = bool(
            self._context is not None
            and self._project_session.identity is not None
            and self._web_config.ready_for_chat()
            and self.question_edit.toPlainText().strip()
            and not locked
        )
        self.send_button.setEnabled(ready)
        self.stop_button.setEnabled(running)
        self.question_edit.setEnabled(not locked)
        self.pick_project_button.setEnabled(not locked)
        self.reload_context_button.setEnabled(not locked)
        self.project_root_edit.setEnabled(not locked)
        self.open_web_config_button.setEnabled(not locked)
        self.inspect_project_checkbox.setEnabled(not locked)
        self._update_chat_history_action_state(locked)
        self._update_change_preparation_state(locked)

    def closeEvent(self, event) -> None:
        """Settle active work before destroying Project-scoped Qt owners."""
        self._project_reload_timer.stop()
        self._switch_wait_timer.stop()
        self.stop_request()
        self._invalidate_active_request()
        self._project_session.invalidate_for_disposal()
        self._dispose_change_preparation()
        if self._chat_thread is not None:
            self._close_pending = True
            self.status_value.setText(
                "Closing is waiting for the active Web AI request to settle."
            )
            event.ignore()
            return
        super().closeEvent(event)
