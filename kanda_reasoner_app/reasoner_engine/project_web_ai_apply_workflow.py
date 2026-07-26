# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py
"""Integrate explicit one-use Project source authorization into Project Web AI."""

from __future__ import annotations

from PySide6.QtWidgets import QInputDialog, QLineEdit, QMessageBox

from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_contracts import (
    ProjectWebAIApplyContractError,
    build_apply_authorization,
    required_confirmation_phrase,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_apply_receipts import (
    ProjectWebAIApplyReceipt,
    apply_preview_caption,
    receipt_allows_retry_after_shadow_delete,
    receipt_matches_fresh_project_context,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_session import (
    ProjectWebAISessionStateError,
)
from kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker import (
    ProjectWebAIApplyError,
    execute_project_web_ai_apply,
)

__all__ = ["ProjectWebAIApplyWorkflowMixin"]


class ProjectWebAIApplyWorkflowMixin:
    """Own the human authorization and local broker invocation boundary."""

    def _initialize_apply_workflow(self) -> None:
        """Create empty Project-scoped apply state."""
        self._apply_receipt: ProjectWebAIApplyReceipt | None = None

    def _authorize_and_apply_current_preview(self) -> None:
        """Require exact human confirmation and invoke the local write broker."""
        operation = self._change_operation
        preview = self._change_preview
        context = self._context
        session_identity = self._project_session.identity
        if (
            operation is None
            or preview is None
            or context is None
            or session_identity is None
        ):
            QMessageBox.warning(
                self,
                "Apply unavailable",
                "The current Project, operation, or Shadow Preview is stale.",
            )
            return
        if self._apply_receipt is not None:
            QMessageBox.information(
                self,
                "Apply already settled",
                "This Preview already has a terminal apply receipt.",
            )
            return
        phrase = required_confirmation_phrase(operation, preview)
        operation_class = (
            "SELF-HOSTING KANDA TOOL CHANGE"
            if context.self_hosting_mode
            else "EXTERNAL PROJECT CHANGE"
        )
        prompt = (
            "This action will update the active Project source through the local "
            "governed write broker. The remote AI cannot execute this action.\n\n"
            + "Operation class: "
            + operation_class
            + "\nProject: "
            + context.project_slug
            + "\nTarget files:\n- "
            + "\n- ".join(item.relative_path for item in preview.targets)
            + "\n\nRollback backups and a durable receipt will be created. "
            + "For self-hosting changes, restart KANDA after success.\n\n"
            + "Type exactly:\n"
            + phrase
        )
        typed, accepted = QInputDialog.getText(
            self,
            "Authorize Project source update",
            prompt,
            QLineEdit.EchoMode.Normal,
            "",
        )
        if not accepted:
            self.status_value.setText("Project source authorization cancelled.")
            return
        try:
            authorization = build_apply_authorization(
                operation=operation,
                preview=preview,
                session_identity=session_identity,
                context=context,
                typed_phrase=typed,
            )
            self._project_session.begin_write_transaction(
                authorization.transaction_id
            )
            receipt = execute_project_web_ai_apply(
                operation=operation,
                preview=preview,
                authorization=authorization,
                session_identity=session_identity,
                context=context,
            )
        except (
            ProjectWebAIApplyContractError,
            ProjectWebAISessionStateError,
        ) as exc:
            QMessageBox.warning(self, "Authorization rejected", str(exc))
            self.status_value.setText("Authorization rejected: " + str(exc))
            return
        except ProjectWebAIApplyError as exc:
            self._project_session.finish_write_transaction(
                getattr(locals().get("authorization"), "transaction_id", ""),
                exc.status,
            )
            self._apply_receipt = exc.receipt
            QMessageBox.critical(
                self,
                "Project source update did not complete",
                str(exc)
                + "\n\nStatus: "
                + exc.status
                + "\nReceipt: "
                + (exc.receipt.receipt_path if exc.receipt is not None else "unavailable"),
            )
            self.status_value.setText(
                "Project source update status: " + exc.status
            )
            self._update_send_state()
            return
        except Exception as exc:
            transaction_id = getattr(locals().get("authorization"), "transaction_id", "")
            if transaction_id:
                self._project_session.finish_write_transaction(
                    transaction_id,
                    "UNRESOLVED",
                )
            QMessageBox.critical(self, "Project source update failed", str(exc))
            self.status_value.setText("Project source update unresolved: " + str(exc))
            self._update_send_state()
            return

        self._project_session.finish_write_transaction(
            authorization.transaction_id,
            receipt.status,
        )
        self._apply_receipt = receipt
        self._project_session.mark_source_mutated(
            context.project_root,
            receipt.completed_at_utc,
        )
        self._context = None
        self._invalidate_active_request()
        if self._change_preview_dialog is not None:
            self._change_preview_dialog.close()
            self._change_preview_dialog = None
        self.status_value.setText(
            "Project source updated and verified. Regenerate Show Project to AI, "
            "reload context, and restart KANDA when self-hosting."
        )
        QMessageBox.information(
            self,
            "Project source update verified",
            "Status: "
            + receipt.status
            + "\nOperation class: "
            + receipt.operation_class
            + "\nReceipt: "
            + receipt.receipt_path
            + "\n\nThe compact handoff is now stale. Run Show Project to AI "
            + "again before using Project Web AI with the changed source. "
            + "Run the governed Project validators before Freeze.",
        )
        self._update_send_state()

    def _apply_authority_available(self) -> bool:
        """Return whether the current Preview can request one human authorization."""
        return bool(
            self._apply_receipt is None
            and self._context is not None
            and self._project_session.identity is not None
            and not self._project_session.transaction_blocks_project_switch
        )

    def _apply_preview_caption(self) -> str:
        """Return the current terminal Preview caption without overstating success."""
        return apply_preview_caption(self._apply_receipt)

    def _release_rolled_back_apply_receipt(self) -> bool:
        """Release retry authority only after the rolled-back Shadow is deleted."""
        if not receipt_allows_retry_after_shadow_delete(self._apply_receipt):
            return False
        self._apply_receipt = None
        return True

    def _retire_successful_apply_after_context_refresh(self, snapshot) -> bool:
        """Retire one verified apply only after a fresh context was accepted."""
        if not receipt_matches_fresh_project_context(
            self._apply_receipt,
            project_id=snapshot.project_id,
            project_root_fingerprint=snapshot.project_root_fingerprint,
        ):
            return False
        self._apply_receipt = None
        return True

    def _clear_apply_workflow_for_project(self) -> None:
        """Clear terminal in-memory receipt state during safe Project Eject."""
        self._apply_receipt = None
