# project-path: kanda_reasoner_app/manage_architecture/large_module_split_audit_gui.py
"""GUI actions for Large Module AST Split Audit."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from kanda_reasoner_app.manage_architecture.large_module_split_audit import (
    run_large_module_split_audit,
)
from kanda_reasoner_app.manage_architecture.large_module_target_queue import (
    LargeModuleTarget,
    count_python_lines,
    format_target_counter,
    parse_module_too_large_findings,
)
from kanda_reasoner_app.templates.floating_windows import (
    show_auto_close_action_window,
    show_error_copy_close_window,
)

__all__ = ["LargeModuleSplitAuditGuiMixin"]


def _target_signature(
    targets: list[LargeModuleTarget],
) -> tuple[tuple[str, int], ...]:
    """Return a stable identity for one sorted oversized-module result set."""
    return tuple((target.path, target.line_count) for target in targets)


class LargeModuleSplitAuditGuiMixin:
    """Provide target queue and AST split audit GUI actions."""

    def _reset_large_module_target_state_for_new_project_audit_run(
        self,
        mode: str,
    ) -> None:
        """Clear stale AST target data before replacing audit results."""
        self._large_module_targets = []
        self._large_module_target_index = -1
        self._large_module_target_source = "pending" if mode == "validate" else "none"
        self._large_module_audit_target_signature = ()
        self._last_large_module_split_handoff = ""
        if hasattr(self, "_large_module_target_edit"):
            self._large_module_target_edit.clear()
            if mode == "validate":
                self._large_module_target_edit.setPlaceholderText(
                    "Validate running - AST target queue will refresh from new results"
                )
            else:
                self._large_module_target_edit.setPlaceholderText(
                    "Run Validate to populate oversized module targets"
                )
        self._clear_large_module_split_output()
        self._sync_large_module_target_controls()

    def _refresh_large_module_targets_from_audit_results(self) -> None:
        """Populate the AST target selector from MODULE_TOO_LARGE findings."""
        targets = parse_module_too_large_findings(self._output.toPlainText())
        self._large_module_audit_target_signature = _target_signature(targets)
        self._large_module_targets = targets
        self._large_module_target_source = "audit" if targets else "none"
        self._large_module_target_index = 0 if targets else -1
        self._last_large_module_split_handoff = ""
        if targets:
            self._large_module_target_edit.setText(targets[0].path)
            self.statusBar().showMessage(
                f"Loaded {len(targets)} oversized module target(s) "
                "from Project Audit Results"
            )
        else:
            self._large_module_target_edit.clear()
            self._large_module_target_edit.setPlaceholderText(
                "No MODULE_TOO_LARGE findings in latest Validate output"
            )
            self.statusBar().showMessage(
                "No oversized modules found in latest Project Audit Results"
            )
        self._clear_large_module_split_output()
        self._sync_large_module_target_controls()


    def _sync_largest_module_target_from_latest_run_results(self) -> bool:
        """Load the largest module from the latest Run Selected Mode results.

        The audit queue is already sorted from largest to smallest. This handoff
        runs when the AST Split Audit subtab opens, so the machine inserts the
        first project-owned card from the latest result set even when the run
        mode did not use the validate completion hook. A manual target selected
        after the same result set was loaded remains authoritative until a new
        run resets the result signature.
        """
        targets = parse_module_too_large_findings(self._output.toPlainText())
        if not targets:
            return False
        signature = _target_signature(targets)
        loaded_signature = tuple(
            getattr(self, "_large_module_audit_target_signature", ()) or ()
        )
        if loaded_signature == signature:
            if (
                getattr(self, "_large_module_target_source", "") == "audit"
                and not self._large_module_target_edit.text().strip()
            ):
                self._large_module_targets = targets
                self._select_large_module_target(0)
                return True
            return False
        self._large_module_audit_target_signature = signature
        self._large_module_targets = targets
        self._large_module_target_source = "audit"
        self._large_module_target_index = 0
        self._last_large_module_split_handoff = ""
        self._large_module_target_edit.setText(targets[0].path)
        self._clear_large_module_split_output()
        self._sync_large_module_target_controls()
        self.statusBar().showMessage(
            "Loaded largest module from latest Run Selected Mode results: "
            f"{targets[0].path} ({targets[0].line_count} lines)"
        )
        return True

    def _sync_large_module_target_controls(self) -> None:
        """Enable AST controls only when an oversized target is selected."""
        has_targets = bool(self._large_module_targets) and 0 <= self._large_module_target_index < len(self._large_module_targets)
        if hasattr(self, "_large_module_target_count_label"):
            self._large_module_target_count_label.setText(
                format_target_counter(
                    self._large_module_targets,
                    self._large_module_target_index,
                )
            )
        if hasattr(self, "_prev_large_module_target_btn"):
            navigation_enabled = len(self._large_module_targets) > 1
            self._prev_large_module_target_btn.setEnabled(navigation_enabled)
            self._next_large_module_target_btn.setEnabled(navigation_enabled)
        if hasattr(self, "_run_large_module_split_btn"):
            self._run_large_module_split_btn.setEnabled(has_targets)
        if hasattr(self, "_copy_large_module_split_btn"):
            self._copy_large_module_split_btn.setEnabled(
                bool(self._last_large_module_split_handoff)
            )
        if hasattr(self, "_copy_large_module_target_path_btn"):
            target_text = ""
            if hasattr(self, "_large_module_target_edit"):
                target_text = self._large_module_target_edit.text().strip()
            self._copy_large_module_target_path_btn.setEnabled(bool(target_text))
        if hasattr(self, "_large_module_split_label"):
            if has_targets:
                self._large_module_split_label.setText(
                    "Large Module AST Split Audit"
                )
                self._large_module_split_label.setToolTip(
                    "Active: oversized module target selected from audit "
                    "findings or manual browse."
                )
            else:
                self._large_module_split_label.setText(
                    "Large Module AST Split Audit - inactive"
                )
                self._large_module_split_label.setToolTip(
                    "Run Validate to populate MODULE_TOO_LARGE targets before "
                    "running AST split audit."
                )

    def _select_large_module_target(self, index: int) -> None:
        """Select an oversized module target by index."""
        if not self._large_module_targets:
            self._large_module_target_index = -1
            self._large_module_target_edit.clear()
            self._sync_large_module_target_controls()
            return
        self._large_module_target_index = max(
            0,
            min(index, len(self._large_module_targets) - 1),
        )
        current = self._large_module_targets[self._large_module_target_index]
        self._large_module_target_edit.setText(current.path)
        self._sync_large_module_target_controls()

    def _move_large_module_target(self, step: int) -> None:
        """Move through the audit-derived oversized-module queue."""
        self._prune_current_large_module_target_if_resolved()
        if not self._large_module_targets:
            return
        next_index = (
            self._large_module_target_index + step
        ) % len(self._large_module_targets)
        self._select_large_module_target(next_index)

    def _prune_current_large_module_target_if_resolved(self) -> None:
        """Remove the current target when it has dropped below 501 lines."""
        if not self._large_module_targets or not (
            0 <= self._large_module_target_index < len(self._large_module_targets)
        ):
            self._sync_large_module_target_controls()
            return
        root_text = self._root_path_edit.text().strip() or str(Path.cwd())
        current = self._large_module_targets[self._large_module_target_index]
        current_lines = count_python_lines(root_text, current.path)
        if current_lines <= 0:
            self._sync_large_module_target_controls()
            return
        if current_lines <= 500:
            removed_path = current.path
            del self._large_module_targets[self._large_module_target_index]
            if self._large_module_targets:
                self._large_module_target_index = min(
                    self._large_module_target_index,
                    len(self._large_module_targets) - 1,
                )
                self._select_large_module_target(self._large_module_target_index)
            else:
                self._large_module_target_index = -1
                self._large_module_target_edit.clear()
                self._large_module_target_edit.setPlaceholderText(
                    "No oversized module targets remain"
                )
                self._sync_large_module_target_controls()
            self.statusBar().showMessage(
                f"Removed resolved module from AST queue: {removed_path}"
            )
            return
        if current_lines != current.line_count:
            self._large_module_targets[self._large_module_target_index] = (
                LargeModuleTarget(current.path, current_lines)
            )
            self._large_module_targets.sort(
                key=lambda item: (-item.line_count, item.path.lower())
            )
            self._large_module_target_index = next(
                (
                    idx for idx, target in enumerate(self._large_module_targets)
                    if target.path == current.path
                ),
                0,
            )
            self._sync_large_module_target_controls()

    def browse_large_module_target(self) -> None:
        """Browse for a manual large-module target."""
        root_text = self._root_path_edit.text().strip() or str(Path.cwd())
        start = str(Path(root_text)) if Path(root_text).exists() else str(Path.cwd())
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select large module target",
            start,
            "Python files (*.py)",
        )
        if path:
            self._set_manual_large_module_target(root_text, path)

    def _set_manual_large_module_target(self, root_text: str, path: str) -> None:
        """Set a manually browsed large-module target inside the active project."""
        root = Path(root_text).resolve()
        selected = Path(path).resolve()
        try:
            target_text = str(selected.relative_to(root)).replace("\\", "/")
        except ValueError:
            QMessageBox.warning(
                self,
                "AST target blocked",
                "The selected module is outside the active Project Root. "
                "Architecture Review accepts project-owned cards only.",
            )
            return
        line_count = count_python_lines(root_text, target_text)
        self._last_large_module_split_handoff = ""
        self._clear_large_module_split_output()
        if line_count <= 500:
            self._large_module_targets = []
            self._large_module_target_index = -1
            self._large_module_target_source = "manual"
            self._large_module_target_edit.setText(target_text)
            self._large_module_target_edit.setPlaceholderText(
                "Selected module is not above 500 lines"
            )
            self._sync_large_module_target_controls()
            QMessageBox.information(
                self,
                "AST target inactive",
                f"Selected module has {line_count} lines. AST Split Audit "
                "activates only for modules above 500 lines.",
            )
            return
        self._large_module_targets = [LargeModuleTarget(target_text, line_count)]
        self._large_module_target_index = 0
        self._large_module_target_source = "manual"
        self._large_module_target_edit.setText(target_text)
        self._sync_large_module_target_controls()
        self.statusBar().showMessage(
            f"Manual oversized AST target selected: {line_count} lines"
        )

    def run_large_module_split_audit_from_gui(self) -> None:
        """Run the read-only large-module split audit."""
        root_path = Path(self._root_path_edit.text().strip())
        self._prune_current_large_module_target_if_resolved()
        target_text = self._large_module_target_edit.text().strip()
        if not root_path.exists():
            show_error_copy_close_window(
                self,
                title="Invalid project root",
                message=f"Project root not found:\n{root_path}",
            )
            return
        if not self._large_module_targets or not target_text:
            show_error_copy_close_window(
                self,
                title="AST Split Audit inactive",
                message=(
                    "Run Validate first and select a MODULE_TOO_LARGE target, "
                    "or Browse Target to choose a .py file above 500 lines."
                ),
            )
            return
        if self._worker_thread is not None or self._ai_review_thread is not None:
            QMessageBox.warning(
                self,
                "Work running",
                "Wait for the current work to finish first.",
            )
            return
        classifier_mode = self._large_module_split_classifier_mode()
        try:
            result = run_large_module_split_audit(
                root_path,
                target_text,
                classifier_mode=classifier_mode,
            )
        except Exception as exc:
            show_error_copy_close_window(
                self,
                title="AST Split Audit failed",
                message=str(exc),
            )
            return
        self._last_large_module_split_handoff = result.markdown
        self._update_large_module_refactor_safety_label(
            result.data.get("refactor_safety_classification", {})
        )
        self._large_module_split_output.clear()
        self._large_module_split_output.appendPlainText(result.markdown)
        self._large_module_split_output.appendPlainText(
            f"\n[report] markdown={result.markdown_path}\n"
            f"[report] json={result.json_path}\n"
        )
        self._sync_large_module_target_controls()
        self.statusBar().showMessage("Large Module AST Split Audit completed")
        show_auto_close_action_window(
            self,
            title="AST Split Audit done",
            message=(
                "Read-only split audit completed. Use Copy Split Handoff for "
                "AI to paste the report into chat."
            ),
        )

    def _large_module_split_classifier_mode(self) -> str:
        """Return the selected split-audit safety classifier mode."""
        tool_radio = getattr(
            self,
            "_large_module_split_classifier_tool_radio",
            None,
        )
        if tool_radio is not None and tool_radio.isChecked():
            return "static_tools"
        return "heuristic"

    def _update_large_module_refactor_safety_label(
        self,
        classification: dict[str, object],
    ) -> None:
        """Update the bold green/red refactor safety label."""
        label = getattr(self, "_large_module_refactor_safety_label", None)
        if label is None:
            return
        result_label = str(classification.get("label") or "not audited")
        engine = str(classification.get("engine") or "")
        if result_label == "SAFE REFACTORING":
            label.setText("SAFE REFACTORING")
            label.setStyleSheet(
                "color: #008000; font-weight: bold; padding: 4px 8px;"
            )
            label.setToolTip(engine or "AST heuristic safety classifier")
            return
        if result_label == "RISK REFACTORING":
            label.setText("RISK REFACTORING")
            label.setStyleSheet(
                "color: #B00020; font-weight: bold; padding: 4px 8px;"
            )
            blockers = classification.get("hard_blockers") or []
            if isinstance(blockers, list) and blockers:
                label.setToolTip(engine + ": " + "; ".join(map(str, blockers)))
            else:
                label.setToolTip(engine or "Risk refactoring classifier")
            return
        label.setText("Refactor safety: not audited")
        label.setStyleSheet(
            "color: #555555; font-weight: bold; padding: 4px 8px;"
        )
        label.setToolTip("Run AST Split Audit to classify refactor safety.")

    def copy_large_module_target_path_to_clipboard(self) -> None:
        """Copy the selected Large Module AST Audit target path."""
        target_text = self._large_module_target_edit.text().strip()
        if not target_text:
            self.statusBar().showMessage(
                "No Large Module AST Audit target path to copy"
            )
            return
        target_path = Path(target_text)
        if not target_path.is_absolute():
            root_text = self._root_path_edit.text().strip() or str(Path.cwd())
            target_path = Path(root_text) / target_path
        QApplication.clipboard().setText(str(target_path))
        self.statusBar().showMessage(
            "Copied Large Module AST Audit target .py path to clipboard"
        )

    def copy_large_module_split_handoff(self) -> None:
        """Copy the latest Large Module Split Handoff for AI."""
        handoff = self._last_large_module_split_handoff
        if not handoff and hasattr(self, "_large_module_split_output"):
            handoff = self._large_module_split_output.toPlainText()
        QApplication.clipboard().setText(handoff)
        self.statusBar().showMessage(
            "Copied Large Module Split Handoff for AI to clipboard"
        )

    def _clear_large_module_split_output(self) -> None:
        """Clear AST split output when target state is reset."""
        if hasattr(self, "_large_module_split_output"):
            self._large_module_split_output.clear()
        self._update_large_module_refactor_safety_label({})
