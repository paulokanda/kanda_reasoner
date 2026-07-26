# project-path: kanda_reasoner_app/freeze_after_update_gui/_freeze_formulary_ai_runtime.py
"""Provider-mode runtime for one Freeze formulary dialog."""

from __future__ import annotations

import queue
import threading
import uuid
from pathlib import Path
from typing import Any, Callable, Mapping

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMessageBox

from kanda_reasoner_app.freeze_after_update_gui._ai_formulary_response_parser import (
    parse_ai_formulary_response,
)
from kanda_reasoner_app.freeze_after_update_gui._freeze_formulary_contracts import (
    FreezeFormularyIdentity,
    build_freeze_formulary_identity,
    form_payload_size_bytes,
    form_snapshot_hash,
)
from kanda_reasoner_app.freeze_after_update_gui._local_ai_formulary import (
    LocalFreezeAIFormularyRunner,
    local_ai_response_looks_like_prompt_echo,
    validate_local_ai_form_against_heuristic,
)
from kanda_reasoner_app.freeze_after_update_gui._web_ai_formulary import (
    WebFreezeAIFormularyRunner,
)
from kanda_reasoner_app.project_support_boundary import (
    resolve_project_tool_boundary_identity,
)
from kanda_reasoner_app.local_ai_configuration import (
    LocalAIConfigurationController,
    application_local_ai_configuration,
)
from kanda_reasoner_app.web_ai_configuration import (
    WebAIConfigurationController,
    application_web_ai_configuration,
)

__all__ = [
    "FreezeFormularyAIController",
    "HEURISTIC_MODE",
    "LOCAL_AI_MODE",
    "WEB_AI_MODE",
]

HEURISTIC_MODE = "heuristic"
LOCAL_AI_MODE = "local"
WEB_AI_MODE = "web"


def _mode_label(mode: str) -> str:
    return {
        HEURISTIC_MODE: "Heuristic",
        LOCAL_AI_MODE: "Local AI",
        WEB_AI_MODE: "Web AI",
    }.get(mode, "Heuristic")


class FreezeFormularyAIController:
    """Own provider selection and asynchronous draft improvement only."""

    def __init__(
        self,
        *,
        owner: Any,
        dialog: Any,
        widgets: Any,
        project_root: Path,
        action_state: Any,
        collect_inputs: Callable[[], dict[str, str]],
        apply_inputs: Callable[[Mapping[str, Any]], None],
        preview_callback: Callable[[], None],
    ) -> None:
        self.owner = owner
        self.dialog = dialog
        self.widgets = widgets
        self.project_root = Path(project_root)
        self.action_state = action_state
        self.collect_inputs = collect_inputs
        self.apply_inputs = apply_inputs
        self.preview_callback = preview_callback
        controller = getattr(owner, "_freeze_web_ai_configuration", None)
        if not isinstance(controller, WebAIConfigurationController):
            controller = application_web_ai_configuration()
            owner._freeze_web_ai_configuration = controller
        self.controller = controller
        local_controller = getattr(owner, "_freeze_local_ai_configuration", None)
        if not isinstance(local_controller, LocalAIConfigurationController):
            local_controller = application_local_ai_configuration()
            owner._freeze_local_ai_configuration = local_controller
        self.local_controller = local_controller
        self._closed = False

    def selected_mode(self) -> str:
        if self.widgets.web_ai_radio.isChecked():
            return WEB_AI_MODE
        if self.widgets.local_ai_radio.isChecked():
            return LOCAL_AI_MODE
        return HEURISTIC_MODE

    def wire(self) -> None:
        for radio in (
            self.widgets.heuristic_radio,
            self.widgets.local_ai_radio,
            self.widgets.web_ai_radio,
        ):
            radio.toggled.connect(self.sync_visible_state)
        self.widgets.open_config_web_ai_button.clicked.connect(
            self._open_selected_configuration
        )
        self.controller.configuration_changed.connect(self._configuration_changed)
        self.controller.catalog_changed.connect(self.sync_visible_state)
        self.local_controller.configuration_changed.connect(
            self._local_configuration_changed
        )
        self.local_controller.catalog_changed.connect(self.sync_visible_state)
        self.widgets.autofill_button.clicked.connect(self.fill_selected)
        self.dialog.finished.connect(self.close)
        self.dialog.destroyed.connect(self.close)
        self.sync_visible_state()

    def sync_visible_state(self, *_args: object) -> None:
        mode = self.selected_mode()
        if mode == HEURISTIC_MODE:
            status = "Heuristic selected. Deterministic intake and validation remain authoritative."
        elif mode == LOCAL_AI_MODE:
            status = (
                "Local AI selected. Global settings: "
                + self.local_controller.summary()
            )
        else:
            status = "Web AI selected. Web settings come only from Config AI."
        self.widgets.mode_status_label.setText(status)
        self.widgets.autofill_button.setText("Fill with " + _mode_label(mode))
        summary = (
            "Local AI: " + self.local_controller.summary()
            if mode == LOCAL_AI_MODE
            else "Web AI: " + self.controller.summary()
        )
        self.widgets.web_config_summary_label.setText(summary)

    def _open_selected_configuration(self) -> None:
        if self.selected_mode() == LOCAL_AI_MODE:
            self.local_controller.request_open_configuration()
        else:
            self.controller.request_open_configuration()

    def _local_configuration_changed(self, *_args: object) -> None:
        self.sync_visible_state()
        if self.selected_mode() == LOCAL_AI_MODE:
            self.invalidate(
                "Central Local AI configuration changed; pending result discarded."
            )

    def _configuration_changed(self, *_args: object) -> None:
        self.sync_visible_state()
        if self.selected_mode() == WEB_AI_MODE:
            self.invalidate(
                "Central Web AI configuration changed; pending result discarded."
            )

    def _set_busy(self, busy: bool) -> None:
        for widget in (
            self.widgets.autofill_button,
            self.widgets.preview_button,
            self.widgets.copy_to_ai_button,
            self.widgets.receive_from_ai_button,
            self.widgets.open_config_web_ai_button,
            self.widgets.heuristic_radio,
            self.widgets.local_ai_radio,
            self.widgets.web_ai_radio,
        ):
            widget.setEnabled(not busy)
        if busy:
            self.action_state.disable("AI formulary fill is still running.")

    def close(self, *_args: object) -> None:
        """Disconnect application-scoped signals and invalidate pending work."""
        if self._closed:
            return
        self._closed = True
        self.stop()
        for signal, callback in (
            (self.controller.configuration_changed, self._configuration_changed),
            (self.controller.catalog_changed, self.sync_visible_state),
            (self.local_controller.configuration_changed, self._local_configuration_changed),
            (self.local_controller.catalog_changed, self.sync_visible_state),
        ):
            try:
                signal.disconnect(callback)
            except (RuntimeError, TypeError):
                pass

    def stop(self, *_args: object) -> None:
        self.owner._local_freeze_ai_request_id = None
        self.owner._local_freeze_ai_identity = None
        timer = self.owner._local_freeze_ai_poll_timer
        if timer is not None:
            timer.stop()
            timer.deleteLater()
            self.owner._local_freeze_ai_poll_timer = None
        self.owner._local_freeze_ai_result_queue = None

    def invalidate(self, reason: str) -> None:
        if self.owner._local_freeze_ai_request_id is None:
            return
        self.stop()
        self.owner._local_freeze_ai_thread = None
        self._set_busy(False)
        self.widgets.mode_status_label.setText(reason)
        self.owner._append_log("Freeze formulary AI result invalidated: " + reason)

    def fill_selected(self) -> None:
        mode = self.selected_mode()
        if mode == HEURISTIC_MODE:
            self._fill_heuristic()
            return
        self._start_provider(mode)

    def _fill_heuristic(self, reason: str = "") -> dict[str, str]:
        self.action_state.disable("No writable freeze preview has been generated yet.")
        self.owner._local_freeze_preview = None
        baseline = self.owner._build_heuristic_local_freeze_inputs(self.project_root)
        self.apply_inputs(baseline)
        if reason:
            self.owner._append_log(reason)
        self.owner._append_log(
            "Freeze fields filled from project-local hint intake or a safe starter. No files were written."
        )
        self.preview_callback()
        return self.collect_inputs()

    def _approval(self, inputs: Mapping[str, Any]) -> str:
        snapshot = self.controller.snapshot()
        if self.controller.selected_model() is None or not self.controller.ready_for_chat():
            QMessageBox.warning(
                self.dialog,
                "Web AI not configured",
                "Open Config Web AI, refresh models, and select a usable model first.",
            )
            self.controller.request_open_configuration()
            return ""
        if not snapshot.structured_output_supported:
            QMessageBox.warning(
                self.dialog,
                "Web AI model unsupported",
                "Freeze Web AI requires strict response_format support.",
            )
            self.controller.request_open_configuration()
            return ""
        project = resolve_project_tool_boundary_identity(self.project_root)
        details = (
            "Approve one read-only Freeze formulary Web AI request?\n\n"
            f"Project: {project.active_project_slug}\n"
            f"Project root: {project.active_project_root}\n"
            f"Project Support: {project.active_project_support_root}\n"
            f"Gateway: {snapshot.gateway_id}\n"
            f"Model: {snapshot.model_id}\n"
            f"Payload bytes: {form_payload_size_bytes(inputs)}\n"
            f"Form SHA-256: {form_snapshot_hash(inputs)}\n"
            f"Privacy: {snapshot.privacy_summary}\n\n"
            "The model can improve draft text only. It cannot validate, Preview, Confirm, Write, consume hints, or refresh startup context."
        )
        answer = QMessageBox.question(
            self.dialog,
            "Approve Freeze Formulary Web AI",
            details,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        return uuid.uuid4().hex if answer == QMessageBox.StandardButton.Yes else ""

    def _start_provider(self, mode: str) -> None:
        baseline = self._fill_heuristic(
            _mode_label(mode)
            + " starts from the deterministic heuristic draft and may improve it only after quality gates."
        )
        web_snapshot = self.controller.snapshot()
        local_snapshot = self.local_controller.snapshot()
        approval_id = self._approval(baseline) if mode == WEB_AI_MODE else ""
        if mode == WEB_AI_MODE and not approval_id:
            return
        self.owner._local_freeze_ai_generation += 1
        if mode == WEB_AI_MODE:
            identity, project = build_freeze_formulary_identity(
                project_root=self.project_root,
                generation=self.owner._local_freeze_ai_generation,
                inputs=baseline,
                assistant_mode=mode,
                approval_id=approval_id,
                gateway_id=web_snapshot.gateway_id,
                model_id=web_snapshot.model_id,
                configuration_revision=web_snapshot.revision,
            )
            runner: Any = WebFreezeAIFormularyRunner(
                inputs=baseline,
                project_root=project.active_project_root,
                gateway_id=web_snapshot.gateway_id,
                model_id=web_snapshot.model_id,
                api_key=self.controller.api_key(),
                request_id=identity.request_id,
            )
        else:
            if not self.local_controller.ready_for_chat():
                QMessageBox.warning(
                    self.dialog,
                    "Local AI not configured",
                    "Open Config AI > Config Local AI and select a model first.",
                )
                self.local_controller.request_open_configuration()
                return
            identity, project = build_freeze_formulary_identity(
                project_root=self.project_root,
                generation=self.owner._local_freeze_ai_generation,
                inputs=baseline,
                assistant_mode=mode,
                model_id=local_snapshot.model_id,
                configuration_revision=local_snapshot.revision,
            )
            runner = LocalFreezeAIFormularyRunner(
                inputs=baseline,
                project_root=project.active_project_root,
                model_name=local_snapshot.model_id,
            )
        self.stop()
        self._set_busy(True)
        result_queue: queue.Queue = queue.Queue(maxsize=1)
        self.owner._local_freeze_ai_request_id = identity.request_id
        self.owner._local_freeze_ai_identity = identity
        self.owner._local_freeze_ai_result_queue = result_queue
        self.widgets.mode_status_label.setText(
            _mode_label(mode) + " is filling the form outside the GUI thread."
        )
        self.owner._append_log(
            _mode_label(mode) + " formulary fill requested. No files will be written by the provider."
        )

        def run_request() -> None:
            ok, payload, model_name = runner.run()
            try:
                result_queue.put_nowait(
                    (identity.request_id, ok, payload, model_name, baseline, mode)
                )
            except Exception:
                pass

        self.owner._local_freeze_ai_thread = threading.Thread(
            target=run_request,
            name="kanda-freeze-formulary-" + mode,
            daemon=True,
        )
        self.owner._local_freeze_ai_thread.start()
        timer = QTimer(self.dialog)
        timer.setInterval(200)
        timer.timeout.connect(self._poll)
        self.owner._local_freeze_ai_poll_timer = timer
        timer.start()

    def _identity_current(self, identity: FreezeFormularyIdentity) -> bool:
        if not self.dialog.isVisible():
            return False
        if identity.request_id != self.owner._local_freeze_ai_request_id:
            return False
        if identity.generation != self.owner._local_freeze_ai_generation:
            return False
        if identity.assistant_mode != self.selected_mode():
            return False
        if identity.form_snapshot_hash != form_snapshot_hash(self.collect_inputs()):
            return False
        current_root = self.owner._project_root()
        if current_root is None:
            return False
        try:
            project = resolve_project_tool_boundary_identity(current_root)
        except Exception:
            return False
        if (
            project.active_project_id != identity.active_project_id
            or project.active_project_root_fingerprint
            != identity.active_project_root_fingerprint
            or str(project.active_project_support_root)
            != identity.active_project_support_root
        ):
            return False
        if identity.assistant_mode == LOCAL_AI_MODE:
            snapshot = self.local_controller.snapshot()
            return (
                snapshot.revision == identity.configuration_revision
                and snapshot.model_id == identity.model_id
            )
        if identity.assistant_mode == WEB_AI_MODE:
            snapshot = self.controller.snapshot()
            return (
                bool(identity.privacy_approval_id)
                and snapshot.revision == identity.configuration_revision
                and snapshot.gateway_id == identity.gateway_id
                and snapshot.model_id == identity.model_id
            )
        return True

    def _poll(self) -> None:
        result_queue = self.owner._local_freeze_ai_result_queue
        identity = self.owner._local_freeze_ai_identity
        if result_queue is None or not isinstance(identity, FreezeFormularyIdentity):
            return
        try:
            request_id, ok, payload, model_name, baseline, mode = result_queue.get_nowait()
        except queue.Empty:
            return
        is_current = request_id == identity.request_id and self._identity_current(identity)
        self.stop()
        self.owner._local_freeze_ai_thread = None
        self._set_busy(False)
        if not is_current:
            self.widgets.mode_status_label.setText(
                "Project, form, mode, or central AI configuration changed. Stale result discarded."
            )
            self.owner._append_log("Stale Freeze formulary AI result discarded.")
            return
        if not ok:
            self.widgets.mode_status_label.setText(
                _mode_label(mode) + " unavailable; heuristic draft kept."
            )
            self.owner._append_log(
                _mode_label(mode) + " fill unavailable. Error: " + str(payload)
            )
            self.preview_callback()
            return
        self._apply_result(str(payload), str(model_name), dict(baseline), str(mode))

    def _apply_result(
        self,
        response_text: str,
        model_name: str,
        baseline: dict[str, str],
        mode: str,
    ) -> None:
        if local_ai_response_looks_like_prompt_echo(response_text):
            self.widgets.mode_status_label.setText(
                _mode_label(mode) + " echoed instructions; heuristic draft kept."
            )
            QMessageBox.warning(
                self.dialog,
                "AI fill rejected",
                "The provider echoed instructions. The heuristic draft was kept.",
            )
            self.preview_callback()
            return
        try:
            candidate = parse_ai_formulary_response(response_text, baseline).inputs
        except Exception as exc:
            self.owner._append_log(_mode_label(mode) + " parse error: " + str(exc))
            self.widgets.mode_status_label.setText(
                _mode_label(mode) + " answer could not be parsed; heuristic draft kept."
            )
            self.preview_callback()
            return
        ok, reasons = validate_local_ai_form_against_heuristic(candidate, baseline)
        if not ok:
            for reason in reasons:
                self.owner._append_log("- " + reason)
            self.widgets.mode_status_label.setText(
                _mode_label(mode) + " weakened the baseline; heuristic draft kept."
            )
            self.preview_callback()
            return
        self.action_state.disable(
            _mode_label(mode) + " changed the form. Preview and validation must run again."
        )
        self.owner._local_freeze_preview = None
        self.apply_inputs(candidate)
        self.owner._append_log(
            _mode_label(mode)
            + " filled the formulary using model: "
            + model_name
            + ". Quality gates passed. No files were written."
        )
        self.widgets.mode_status_label.setText(
            _mode_label(mode) + " fill applied with model: " + model_name
        )
        self.preview_callback()
