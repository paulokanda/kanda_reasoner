# project-path: kanda_reasoner_app/manage_architecture/architecture_audit_actions_gui.py
"""Clipboard and protocol actions for the Architecture Review GUI."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox

from kanda_reasoner_app.refactor_report_evidence import (
    build_refactor_report_evidence_text,
)
from kanda_reasoner_app.templates.floating_windows import show_error_copy_close_window
from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    format_warning_resolution_report,
    resolve_warning_audit,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_formatting import (
    format_test_protection_apply_result,
    format_test_protection_gap_plan,
)

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_controller import (
    WarningHeuristicResolverController,
)
from kanda_reasoner_app.manage_architecture.warning_resolver_cancel_gui import (
    bind_warning_resolver_cancel_controller,
)
from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_sonar import (
    finish_warning_resolver_sonar_error,
    finish_warning_resolver_sonar_success,
    start_warning_resolver_sonar,
    update_warning_resolver_sonar,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    TestProtectionGapPlan,
    apply_test_protection_gap_plan,
)
from kanda_reasoner_app.manage_architecture.warning_model_resolver_sonar import (
    finish_warning_model_sonar_error,
    finish_warning_model_sonar_success,
    start_warning_model_sonar,
    update_warning_model_sonar,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_formatting import (
    format_model_apply_verification_result,
    format_model_test_protection_plan,
)
from kanda_reasoner_app.manage_architecture.warning_model_live_audit import (
    ModelApplyVerificationResult,
)
from kanda_reasoner_app.manage_architecture.warning_model_test_protection_resolver import (
    ModelTestProtectionPlan,
)

__all__ = ["ArchitectureAuditActionsMixin"]

LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH = (
    "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/"
    "06_refactor_and_architecture_hardening/large_module_refactor_protocol.md"
)


class ArchitectureAuditActionsMixin:
    """Provide Project Audit Results clipboard actions."""

    def showEvent(self, event) -> None:
        """Apply the protocol-button visual contract when the window is shown."""
        self._apply_large_module_protocol_button_style()
        super().showEvent(event)

    def _apply_large_module_protocol_button_style(self) -> None:
        """Keep the button background inherited while emphasizing its text."""
        self._copy_large_module_protocol_btn.setStyleSheet(
            "color: #FF8C00; font-weight: bold;"
        )

    def copy_audit_to_clipboard(self) -> None:
        """Copy project audit results, optionally with refactor evidence."""
        audit_text = self._output.toPlainText()
        if self._include_refactor_report_checkbox.isChecked():
            root_path = Path(self._root_path_edit.text().strip())
            self.statusBar().showMessage(
                "Running Refactor Report before copying Project Audit Results..."
            )
            QApplication.processEvents()
            try:
                audit_text += build_refactor_report_evidence_text(root_path)
            except Exception as exc:
                audit_text += (
                    "\n\n---\n"
                    "Refactor Report Evidence\n"
                    f"Unable to auto-generate compact evidence for {root_path}:\n"
                    f"{exc}\n"
                )
                show_error_copy_close_window(
                    self,
                    title="Refactor Report evidence failed",
                    message=(
                        "Project Audit Results will still be copied, but "
                        f"Refactor Report evidence failed:\n{exc}"
                    ),
                )
        QApplication.clipboard().setText(audit_text)
        if self._include_refactor_report_checkbox.isChecked():
            self.statusBar().showMessage(
                "Copied Project Audit Results with compact Refactor Report evidence"
            )
        else:
            self.statusBar().showMessage("Copied Project Audit Results to clipboard")

    def run_warning_heuristic_resolver(self) -> None:
        """Run warning routing and specialist analysis without blocking the GUI."""
        audit_text = self._output.toPlainText()
        report = resolve_warning_audit(audit_text)
        if report.total_findings == 0:
            self.statusBar().showMessage(
                "Warning Heuristic Resolver found no WARNING lines in Project Audit Results"
            )
            return

        self._output.appendPlainText(
            "\n" + format_warning_resolution_report(report)
        )
        test_gap_findings = tuple(
            item.finding
            for item in report.decisions
            if item.finding.code == "TEST_PROTECTION_GAP"
            and item.finding.path != "."
        )
        if not test_gap_findings:
            self.statusBar().showMessage(
                "Warning Heuristic Resolver: "
                + str(report.heuristic_count)
                + " heuristic, "
                + str(report.web_ai_count)
                + " Web AI"
            )
            return

        if self._warning_resolver_route_busy():
            self.statusBar().showMessage("A warning resolver route is already running")
            return
        controller = self._warning_resolver_controller()
        root_path = Path(self._root_path_edit.text().strip())
        started = controller.start(root_path, test_gap_findings)
        if not started:
            self.statusBar().showMessage(
                "Warning Heuristic Resolver is already running"
            )
            return
        start_warning_resolver_sonar(self, len(test_gap_findings))
        self.statusBar().showMessage(
            "Warning Heuristic Resolver running in background"
        )
    def _warning_resolver_controller(self) -> WarningHeuristicResolverController:
        """Return the window-child controller without caching feature state on host."""
        object_name = "warningHeuristicResolverController"
        controller = self.findChild(WarningHeuristicResolverController, object_name)
        if controller is not None:
            return controller
        controller = WarningHeuristicResolverController(self)
        controller.setObjectName(object_name)
        controller.progress.connect(self._on_warning_resolver_progress)
        controller.result_ready.connect(self._on_warning_resolver_result)
        controller.failed.connect(self._on_warning_resolver_failure)
        controller.model_progress.connect(self._on_warning_model_progress)
        controller.model_result_ready.connect(self._on_warning_model_result)
        controller.model_failed.connect(self._on_warning_model_failure)
        controller.model_apply_progress.connect(self._on_warning_model_apply_progress)
        controller.model_apply_result_ready.connect(self._on_warning_model_apply_result)
        controller.model_apply_failed.connect(self._on_warning_model_apply_failure)
        bind_warning_resolver_cancel_controller(self, controller)
        return controller
    def _on_warning_resolver_progress(
        self,
        total: int,
        to_go: int,
        done: int,
        web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        """Update sonar counters from real worker progress on the GUI thread."""
        update_warning_resolver_sonar(
            self, total, to_go, done, web_ai, source_path, action
        )
        self.statusBar().showMessage(
            "Resolver: total "
            + str(total)
            + ", to go "
            + str(to_go)
            + ", done "
            + str(done)
            + ", Web AI "
            + str(web_ai)
        )
    def _on_warning_resolver_result(self, result: object) -> None:
        """Render the completed plan and keep writes behind human confirmation."""
        if not isinstance(result, TestProtectionGapPlan):
            self._on_warning_resolver_failure(
                "Warning resolver worker returned an invalid result type."
            )
            return
        plan = result
        self._output.appendPlainText(
            "\n" + format_test_protection_gap_plan(plan)
        )
        done = plan.safe_link_count + plan.already_protected_count
        finish_warning_resolver_sonar_success(
            self,
            total=len(plan.decisions),
            done=done,
            web_ai=plan.web_ai_count,
        )

        if plan.safe_link_count:
            answer = QMessageBox.question(
                self,
                "Apply safe TEST_PROTECTION_GAP corrections?",
                (
                    "The resolver found "
                    + str(plan.safe_link_count)
                    + " existing-test links with strong structural evidence.\n\n"
                    "Apply only these TYPE_CHECKING direct-module links now? "
                    "Unresolved findings will remain in the Web AI handoff."
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer == QMessageBox.Yes:
                try:
                    apply_result = apply_test_protection_gap_plan(plan)
                except Exception as exc:
                    show_error_copy_close_window(
                        self,
                        title="Warning heuristic correction failed",
                        message=str(exc),
                    )
                else:
                    self._output.appendPlainText(
                        "\n" + format_test_protection_apply_result(apply_result)
                    )

        self.statusBar().showMessage(
            "Warning Heuristic Resolver: "
            + str(plan.safe_link_count)
            + " safe test links, "
            + str(plan.web_ai_count)
            + " test gaps for Web AI"
        )
    def _on_warning_resolver_failure(self, diagnostic: str) -> None:
        """Surface one background resolver failure without freezing the GUI."""
        finish_warning_resolver_sonar_error(self, diagnostic)
        self.statusBar().showMessage("Warning Heuristic Resolver failed")
        show_error_copy_close_window(
            self,
            title="Warning heuristic resolver failed",
            message=str(diagnostic),
        )

    def _warning_resolver_route_busy(self) -> bool:
        """Return True while the shared warning resolver controller owns work."""
        controller = self.findChild(
            WarningHeuristicResolverController,
            "warningHeuristicResolverController",
        )
        return bool(controller is not None and controller.running)

    def run_warning_web_ai_resolver(self) -> None:
        """Reuse the governed Audit Project Web AI advisory review route."""
        if self._warning_resolver_route_busy():
            self.statusBar().showMessage("A warning resolver route is already running")
            return
        web_radio = getattr(self, "_ai_review_web_radio", None)
        review_button = getattr(self, "_ai_review_button", None)
        if web_radio is None or review_button is None:
            self.statusBar().showMessage("Web AI Resolver is unavailable")
            return
        web_radio.setChecked(True)
        self.statusBar().showMessage(
            "Web AI Resolver uses Config AI > Config Web AI and remains read-only"
        )
        review_button.click()


    def run_warning_model_resolver(self) -> None:
        """Run Local AI from a fresh background Architecture Review queue."""
        if self._warning_resolver_route_busy():
            self.statusBar().showMessage("A warning resolver route is already running")
            return
        model_selection = ""
        controller = self._warning_resolver_controller()
        root_path = Path(self._root_path_edit.text().strip())
        started = controller.start(
            root_path,
            (),
            route="model",
            model_selection=model_selection,
        )
        if not started:
            self.statusBar().showMessage("Warning Local AI Resolver is already running")
            return
        start_warning_model_sonar(self, 0, model_selection)
        self.statusBar().showMessage(
            "Warning Local AI Resolver running fresh Architecture Review before model analysis"
        )


    def _on_warning_model_progress(
        self,
        total: int,
        to_go: int,
        done: int,
        web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        """Project Local AI worker progress on the GUI thread."""
        update_warning_model_sonar(
            self, total, to_go, done, web_ai, source_path, action
        )
        self.statusBar().showMessage(
            "Local AI Resolver: total "
            + str(total)
            + ", to go "
            + str(to_go)
            + ", done "
            + str(done)
            + ", Web AI "
            + str(web_ai)
        )

    def _on_warning_model_result(self, result: object) -> None:
        """Render Local AI decisions and keep all writes behind confirmation."""
        if not isinstance(result, ModelTestProtectionPlan):
            self._on_warning_model_failure(
                "Warning Local AI Resolver returned an invalid result type."
            )
            return
        plan = result
        self._output.appendPlainText(
            "\n" + format_model_test_protection_plan(plan)
        )
        done = (
            plan.safe_link_count
            + plan.model_test_change_count
            + plan.already_protected_count
        )
        finish_warning_model_sonar_success(
            self,
            total=len(plan.decisions),
            done=done,
            web_ai=plan.web_ai_count,
            model_name=plan.model_name,
        )
        if plan.safe_change_count:
            answer = QMessageBox.question(
                self,
                "Apply safe Local AI TEST_PROTECTION_GAP corrections?",
                (
                    "Model: "
                    + plan.model_name
                    + "\n\nHeuristic safe links: "
                    + str(plan.heuristic_safe_count)
                    + "\nLocal AI existing-test links: "
                    + str(plan.model_safe_count)
                    + "\nValidated Local AI test changes: "
                    + str(plan.model_test_change_count)
                    + "\nWeb AI still required: "
                    + str(plan.web_ai_count)
                    + "\n\nApply the guarded links and sandbox-validated test-only changes now?"
                ),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if answer == QMessageBox.Yes:
                controller = self._warning_resolver_controller()
                queued = controller.queue_model_apply_verify(plan)
                if not queued:
                    show_error_copy_close_window(
                        self,
                        title="Warning Local AI apply verification busy",
                        message="A confirmed apply verification is already queued.",
                    )
                else:
                    self.statusBar().showMessage(
                        "Warning Local AI apply + fresh re-audit queued in background"
                    )
        self.statusBar().showMessage(
            "Warning Local AI Resolver v2: "
            + str(plan.safe_link_count)
            + " safe links, "
            + str(plan.model_test_change_count)
            + " validated test changes, "
            + str(plan.web_ai_count)
            + " test gaps still require Web AI"
        )


    def _on_warning_model_apply_progress(
        self,
        total: int,
        to_go: int,
        done: int,
        web_ai: int,
        source_path: str,
        action: str,
    ) -> None:
        """Project background apply and fresh re-audit progress on the GUI thread."""
        update_warning_model_sonar(
            self, total, to_go, done, web_ai, source_path, action
        )
        self.statusBar().showMessage(
            "Local AI verified apply: " + action + " | " + source_path
        )

    def _on_warning_model_apply_result(self, result: object) -> None:
        """Render actual writes and exact-path fresh-audit verification."""
        if not isinstance(result, ModelApplyVerificationResult):
            self._on_warning_model_apply_failure(
                "Warning Local AI apply worker returned an invalid result type."
            )
            return
        self._output.appendPlainText(
            "\n" + format_model_apply_verification_result(result)
        )
        finish_warning_model_sonar_success(
            self,
            total=len(result.requested_source_paths),
            done=result.verified_resolved_count,
            web_ai=len(result.still_present_source_paths),
            model_name="verified live apply",
        )
        self.statusBar().showMessage(
            "Warning Local AI verified apply: "
            + str(len(result.apply_result.changed_files))
            + " files changed, "
            + str(result.verified_resolved_count)
            + " exact gaps resolved"
        )

    def _on_warning_model_apply_failure(self, diagnostic: str) -> None:
        """Surface background apply or fresh re-audit failure."""
        finish_warning_model_sonar_error(self, diagnostic)
        self.statusBar().showMessage("Warning Local AI verified apply failed")
        show_error_copy_close_window(
            self,
            title="Warning Local AI verified apply failed",
            message=str(diagnostic),
        )

    def _on_warning_model_failure(self, diagnostic: str) -> None:
        """Surface a Local AI resolver failure without blocking the GUI."""
        finish_warning_model_sonar_error(self, diagnostic)
        self.statusBar().showMessage("Warning Local AI Resolver failed")
        show_error_copy_close_window(
            self,
            title="Warning Local AI Resolver failed",
            message=str(diagnostic),
        )

    def copy_large_module_protocol_to_clipboard(self) -> None:
        """Copy the canonical large-module protocol to the clipboard."""
        prompt_path = self._large_module_protocol_path()
        if prompt_path is None or not prompt_path.exists():
            show_error_copy_close_window(
                self,
                title="Large Module Creation/Refactor Protocol not found",
                message=(
                    "Could not find the canonical Large Module Creation/"
                    "Refactor Protocol at:\n"
                    + LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH
                    + "\n\nSelect the active KANDA project root and try again."
                ),
            )
            return
        QApplication.clipboard().setText(prompt_path.read_text(encoding="utf-8"))
        self.statusBar().showMessage(
            "Copied Large Module Creation/Refactor Protocol to clipboard"
        )

    def _large_module_protocol_path(self) -> Path | None:
        """Return the first available large-module protocol path."""
        candidates: list[Path] = []
        root_text = self._root_path_edit.text().strip()
        if root_text:
            candidates.append(Path(root_text) / LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH)
        candidates.append(
            Path(__file__).resolve().parents[2]
            / LARGE_MODULE_REFACTOR_PROTOCOL_RELATIVE_PATH
        )
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0] if candidates else None
