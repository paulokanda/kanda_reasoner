# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py
"""Add exact-source Prepare Changes workflow to Project Web AI.

The workflow creates a remote advisory proposal and a local transient Shadow
Preview. It has no active Project source-write or execution authority.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog, QMessageBox

from kanda_reasoner_app.reasoner_engine.project_web_ai_change_contracts import (
    ChangeProposalError,
    ProjectWebAIChangeOperation,
    build_project_change_messages,
    new_change_operation,
    parse_project_change_proposal,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_change_preview import (
    ProjectWebAIChangePreviewDialog,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_shadow import (
    ProjectWebAIShadowError,
    ProjectWebAIShadowPreview,
    build_shadow_preview,
    delete_shadow_preview,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_source_reader import (
    ProjectSourceReadError,
    read_exact_project_sources,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_workers import (
    ProjectWebAIChatWorker,
)
from kanda_reasoner_app.web_ai_provider_contracts import (
    ChatResult,
    ProjectWebAIRequestIdentity,
)

__all__ = ["ProjectWebAIChangePreparationMixin"]

_SOURCE_FILTER = (
    "Text source files (*.py *.ps1 *.md *.json *.txt *.toml *.yaml *.yml "
    "*.ini *.cfg *.css *.html *.js *.jsx *.ts *.tsx);;All files (*)"
)


class ProjectWebAIChangePreparationMixin:
    """Provide Phase 2 exact-source proposal and Shadow Preview behavior."""

    def _initialize_change_preparation(self) -> None:
        """Create empty Project-scoped preparation state."""
        self._change_operation: ProjectWebAIChangeOperation | None = None
        self._change_preview: ProjectWebAIShadowPreview | None = None
        self._change_preview_dialog: ProjectWebAIChangePreviewDialog | None = None
        self._request_mode = ""

    def _connect_change_preparation_signals(self) -> None:
        """Connect the explicit Prepare Changes command."""
        self.prepare_changes_button.clicked.connect(self.prepare_changes)

    def prepare_changes(self) -> None:
        """Send exact selected source for proposal-only remote review."""
        if self._chat_thread is not None or self._context is None:
            return
        if self._change_preview is not None:
            self._open_change_preview()
            return
        exchange = self._latest_completed_exchange()
        if exchange is None:
            QMessageBox.warning(
                self,
                "Prepare Changes unavailable",
                "Complete one Project Web AI question and answer first.",
            )
            return
        model = self._selected_model()
        if model is None or not self._web_config.ready_for_chat():
            QMessageBox.warning(
                self,
                "Web AI not ready",
                "Complete the central Web AI gateway, credential, and model setup.",
            )
            return
        session_identity = self._project_session.identity
        context = self._context
        if session_identity is None:
            self.status_value.setText(
                "Project session is not ready. Reload the selected Project context."
            )
            return
        selected_paths, _filter = QFileDialog.getOpenFileNames(
            self,
            "Select exact Project source for Shadow proposal",
            context.project_root,
            _SOURCE_FILTER,
        )
        if not selected_paths:
            return
        try:
            sources = read_exact_project_sources(
                context.project_root,
                selected_paths,
            )
        except ProjectSourceReadError as exc:
            QMessageBox.warning(self, "Source selection rejected", str(exc))
            return
        approved = QMessageBox.question(
            self,
            "Approve exact-source transmission",
            self._change_approval_text(sources),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if approved != QMessageBox.StandardButton.Yes:
            self.status_value.setText(
                "Prepare Changes cancelled. Exact source was not transmitted."
            )
            return

        profile = self._current_profile()
        config_snapshot = self._web_config.snapshot()
        request_identity = ProjectWebAIRequestIdentity(
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
        )
        question, advisory_answer = exchange
        try:
            operation = new_change_operation(
                request_identity=request_identity,
                session_identity=session_identity,
                context=context,
                question=question,
                advisory_answer=advisory_answer,
                source_files=sources,
            )
            messages = build_project_change_messages(
                operation,
                context.context_text,
                trusted_boundary_text=context.trusted_boundary_text,
            )
        except ChangeProposalError as exc:
            QMessageBox.warning(self, "Prepare Changes rejected", str(exc))
            return

        self._delete_current_shadow_preview()
        self._change_operation = operation
        self._request_mode = "prepare_changes"
        thread = QThread(self)
        worker = ProjectWebAIChatWorker(
            profile=profile,
            model_id=model.model_id,
            api_key=self._web_config.api_key(),
            messages=messages,
            request_identity=request_identity,
        )
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.started.connect(self._on_change_started)
        worker.token_ready.connect(self._on_change_token)
        worker.completed.connect(self._on_change_completed)
        worker.failed.connect(self._on_change_failed)
        worker.cancelled.connect(self._on_change_cancelled)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.finished.connect(self._chat_thread_finished)
        self._active_request_identity = request_identity
        self._active_config_revision = config_snapshot.revision
        self._active_question = question
        self._chat_thread = thread
        self._chat_worker = worker
        self.status_value.setText(
            "Preparing a proposal-only Shadow correction from exact selected source..."
        )
        self._update_send_state()
        thread.start()

    def _latest_completed_exchange(self) -> tuple[str, str] | None:
        """Return the newest complete user and assistant pair from model history."""
        assistant_index = -1
        advisory_answer = ""
        for index in range(len(self._history) - 1, -1, -1):
            item = self._history[index]
            if str(item.get("role") or "") != "assistant":
                continue
            advisory_answer = str(item.get("content") or "").strip()
            if advisory_answer:
                assistant_index = index
                break
        if assistant_index < 0:
            return None
        for index in range(assistant_index - 1, -1, -1):
            item = self._history[index]
            if str(item.get("role") or "") != "user":
                continue
            question = str(item.get("content") or "").strip()
            if question:
                return question, advisory_answer
        return None

    def _change_approval_text(self, sources: tuple[Any, ...]) -> str:
        """Return the explicit per-request exact-source privacy approval text."""
        context = self._context
        model = self._selected_model()
        assert context is not None and model is not None
        file_lines = "\n".join(
            "- " + item.relative_path + " (" + str(item.size_bytes) + " bytes)"
            for item in sources
        )
        total_bytes = sum(item.size_bytes for item in sources)
        return (
            "You are about to send exact selected Project source to a remote AI.\n\n"
            + "Gateway: "
            + self._current_profile().display_name
            + "\nModel: "
            + model.model_id
            + "\nProject: "
            + context.project_slug
            + "\nSnapshot: "
            + context.short_hash()
            + "\nExact source files: "
            + str(len(sources))
            + "\nExact source bytes: "
            + str(total_bytes)
            + "\n\n"
            + file_lines
            + "\n\nThe response will be parsed as a strict proposal and applied only "
            + "to a transient Shadow under the Project daily-work root. "
            + "Active Project source will remain unchanged.\n\nApprove this request?"
        )

    def _on_change_started(self, identity: object) -> None:
        """Show current proposal-request status only for the exact operation."""
        if self._change_event_is_current(identity):
            self.status_value.setText(
                "Project Web AI is preparing a strict Shadow proposal..."
            )

    def _on_change_token(self, identity: object, _token: str) -> None:
        """Ignore streamed JSON fragments while preserving request identity checks."""
        if not self._change_event_is_current(identity):
            return

    def _on_change_completed(self, identity: object, result: object) -> None:
        """Parse the strict proposal and build a validated Shadow Preview."""
        if not self._change_event_is_current(identity):
            return
        operation = self._change_operation
        if operation is None or not isinstance(result, ChatResult):
            self.status_value.setText("Prepare Changes returned an invalid result.")
            return
        try:
            proposal = parse_project_change_proposal(result.content, operation)
            preview = build_shadow_preview(operation, proposal)
        except (ChangeProposalError, ProjectWebAIShadowError, OSError) as exc:
            self.status_value.setText(
                "Prepare Changes rejected: "
                + exc.__class__.__name__
                + ": "
                + str(exc)
            )
            QMessageBox.warning(self, "Shadow proposal rejected", str(exc))
            return
        self._change_preview = preview
        self.status_value.setText(
            "Validated Shadow Preview ready. Active Project source is unchanged."
        )
        self._open_change_preview()

    def _on_change_failed(self, identity: object, message: str) -> None:
        """Show one current provider or proposal failure."""
        if self._change_event_is_current(identity):
            self.status_value.setText("Prepare Changes failed: " + str(message))

    def _on_change_cancelled(self, identity: object) -> None:
        """Show current cooperative cancellation without creating a Preview."""
        if self._change_event_is_current(identity):
            self.status_value.setText("Prepare Changes cancelled.")

    def _change_event_is_current(self, identity: object) -> bool:
        """Accept events only for the exact operation and current Project session."""
        operation = self._change_operation
        context = self._context
        model = self._selected_model()
        return bool(
            operation is not None
            and context is not None
            and model is not None
            and isinstance(identity, ProjectWebAIRequestIdentity)
            and identity == operation.request_identity
            and identity == self._active_request_identity
            and self._request_mode == "prepare_changes"
            and self._active_config_revision == self._web_config.snapshot().revision
            and self._project_session.request_is_current(identity, context)
            and identity.gateway_id == self._current_profile().gateway_id
            and identity.model_id == model.model_id
        )

    def _open_change_preview(self) -> None:
        """Open one read-only dialog for the current validated Shadow Preview."""
        preview = self._change_preview
        if preview is None:
            return
        if self._change_preview_dialog is not None:
            self._change_preview_dialog.close()
        apply_callback = (
            self._authorize_and_apply_current_preview
            if self._apply_authority_available()
            else None
        )
        dialog = ProjectWebAIChangePreviewDialog(
            preview,
            delete_callback=self._delete_current_shadow_preview,
            apply_callback=apply_callback,
            parent=self,
        )
        dialog.finished.connect(self._on_change_preview_dialog_closed)
        self._change_preview_dialog = dialog
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _on_change_preview_dialog_closed(self, _result: int) -> None:
        """Release only the dialog wrapper; keep the transient Preview available."""
        self._change_preview_dialog = None

    def _delete_current_shadow_preview(self) -> None:
        """Delete the current transient Shadow and clear proposal state."""
        if self._project_session.transaction_blocks_project_switch:
            self.status_value.setText(
                "Shadow deletion is blocked by an open or unresolved transaction."
            )
            return
        delete_shadow_preview(self._change_preview)
        self._change_preview = None
        self._change_operation = None
        self._release_rolled_back_apply_receipt()
        if self._change_preview_dialog is not None:
            self._change_preview_dialog.close()
            self._change_preview_dialog = None
        self.status_value.setText(
            "Transient Shadow Preview deleted. Active Project source was unchanged."
        )
        self._update_send_state()

    def _clear_change_preparation_for_project(self) -> None:
        """Eject all old-Project proposal and Shadow state on Project switch."""
        delete_shadow_preview(self._change_preview)
        self._change_preview = None
        self._change_operation = None
        self._request_mode = ""
        if self._change_preview_dialog is not None:
            self._change_preview_dialog.close()
            self._change_preview_dialog = None
        self._clear_apply_workflow_for_project()

    def _settle_change_request(self) -> None:
        """Release request-only state while retaining a completed Shadow Preview."""
        if self._request_mode == "prepare_changes":
            self._request_mode = ""
            if self._change_preview is None:
                self._change_operation = None

    def _update_change_preparation_state(self, locked: bool) -> None:
        """Enable Prepare Changes only for a completed current advisory exchange."""
        has_preview = self._change_preview is not None
        ready = bool(
            not locked
            and (
                has_preview
                or (
                    self._context is not None
                    and self._project_session.identity is not None
                    and self._web_config.ready_for_chat()
                    and self._latest_completed_exchange() is not None
                )
            )
        )
        if has_preview:
            label = self._apply_preview_caption()
        else:
            label = "Prepare Changes"
        self.prepare_changes_button.setText(label)
        self.prepare_changes_button.setEnabled(ready)

    def _retire_change_cycle_after_context_refresh(self, snapshot) -> bool:
        """Start a clean advisory cycle after a verified apply and fresh handoff."""
        if not self._retire_successful_apply_after_context_refresh(snapshot):
            return False
        delete_shadow_preview(self._change_preview)
        self._change_preview = None
        self._change_operation = None
        if self._change_preview_dialog is not None:
            self._change_preview_dialog.close()
            self._change_preview_dialog = None
        self.new_chat()
        return True

    def _dispose_change_preparation(self) -> None:
        """Delete transient Shadow state before final widget disposal."""
        self._clear_change_preparation_for_project()
