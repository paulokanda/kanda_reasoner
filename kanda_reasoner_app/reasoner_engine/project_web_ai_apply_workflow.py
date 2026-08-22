# project-path: kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py
"""Integrate explicit human review into Project Web AI proposal evidence."""

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
from kanda_reasoner_app.reasoner_engine.project_web_ai_write_broker import (
    ProjectWebAIApplyError,
    execute_project_web_ai_apply,
)

__all__ = ["ProjectWebAIApplyWorkflowMixin"]


class ProjectWebAIApplyWorkflowMixin:
    """Own explicit human review and proposal-receipt recording."""

    def _initialize_apply_workflow(self) -> None:
        """Create empty Project-scoped terminal receipt state."""
        self._apply_receipt: ProjectWebAIApplyReceipt | None = None

    def _authorize_and_apply_current_preview(self) -> None:
        """Require exact human confirmation and record proposal evidence."""
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
                "Proposal unavailable",
                "The current Project, operation, or Shadow Preview is stale.",
            )
            return
        if self._apply_receipt is not None:
            QMessageBox.information(
                self,
                "Proposal already recorded",
                "This Preview already has a terminal proposal receipt.",
            )
            return
        phrase = required_confirmation_phrase(operation, preview)
        operation_class = (
            "SELF-HOSTING KANDA TOOL PROPOSAL"
            if context.self_hosting_mode
            else "EXTERNAL PROJECT PROPOSAL"
        )
        prompt = (
            "This action records the reviewed Shadow Preview as governed "
            "proposal evidence. It does not update Project source.\n\n"
            + "Operation class: "
            + operation_class
            + "\nProject: "
            + context.project_slug
            + "\nTarget files:\n- "
            + "\n- ".join(item.relative_path for item in preview.targets)
            + "\n\nNo Project source backup, source mutation, or rollback will run. "
            + "A durable support-side proposal receipt will be created.\n\n"
            + "Type exactly:\n"
            + phrase
        )
        typed, accepted = QInputDialog.getText(
            self,
            "Record reviewed proposal",
            prompt,
            QLineEdit.EchoMode.Normal,
            "",
        )
        if not accepted:
            self.status_value.setText("Proposal recording cancelled.")
            return
        try:
            authorization = build_apply_authorization(
                operation=operation,
                preview=preview,
                session_identity=session_identity,
                context=context,
                typed_phrase=typed,
            )
            receipt = execute_project_web_ai_apply(
                operation=operation,
                preview=preview,
                authorization=authorization,
                session_identity=session_identity,
                context=context,
            )
        except ProjectWebAIApplyContractError as exc:
            QMessageBox.warning(self, "Proposal rejected", str(exc))
            self.status_value.setText("Proposal rejected: " + str(exc))
            return
        except ProjectWebAIApplyError as exc:
            self._apply_receipt = exc.receipt
            QMessageBox.critical(
                self,
                "Proposal receipt did not complete",
                str(exc)
                + "\n\nStatus: "
                + exc.status
                + "\nReceipt: "
                + (
                    exc.receipt.receipt_path
                    if exc.receipt is not None
                    else "unavailable"
                ),
            )
            self.status_value.setText("Proposal receipt status: " + exc.status)
            self._update_send_state()
            return
        except Exception as exc:
            QMessageBox.critical(self, "Proposal recording failed", str(exc))
            self.status_value.setText("Proposal recording failed: " + str(exc))
            self._update_send_state()
            return

        self._apply_receipt = receipt
        self.status_value.setText(
            "Reviewed proposal recorded. Active Project source is unchanged."
        )
        QMessageBox.information(
            self,
            "Reviewed proposal recorded",
            "Status: "
            + receipt.status
            + "\nOperation class: "
            + receipt.operation_class
            + "\nReceipt: "
            + receipt.receipt_path
            + "\n\nProject source was not changed. The current handoff remains "
            + "source-current because this action recorded evidence only.",
        )
        self._update_send_state()

    def _apply_authority_available(self) -> bool:
        """Return whether the current Preview can record one review receipt."""
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
        """Preserve compatibility with historical rolled-back receipt cleanup."""
        if not receipt_allows_retry_after_shadow_delete(self._apply_receipt):
            return False
        self._apply_receipt = None
        return True

    def _retire_successful_apply_after_context_refresh(self, snapshot) -> bool:
        """Retire only historical verified source-write receipts after refresh."""
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
