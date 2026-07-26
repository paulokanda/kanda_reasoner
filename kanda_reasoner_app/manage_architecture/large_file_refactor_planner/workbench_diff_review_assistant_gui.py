"""Qt controls for assisted Workbench Semantic Diff and Text Diff review."""
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .workbench_diff_review_assistant import (
    DiffReviewAssistantResult,
    build_heuristic_diff_review,
    build_local_ai_diff_review,
    build_web_ai_diff_review_prompt,
    format_assistant_panel_appendix,
    parse_web_ai_diff_review_response,
)

__all__ = [
    "build_diff_review_assistant_box",
    "sync_diff_review_assistant_controls",
]

RootTextCallback = Callable[[object], str]


class _LocalDiffReviewReceiver(QObject):
    """Receive Local AI results on the GUI thread through Qt signal delivery."""

    def __init__(self, window: object, thread: QThread) -> None:
        super().__init__()
        self._window = window
        self._thread = thread

    @Slot(object)
    def on_result(self, payload: object) -> None:
        _on_local_ai_result(self._window, payload)

    @Slot()
    def on_thread_finished(self) -> None:
        _on_local_ai_thread_finished(self._window, self._thread)


class _LocalDiffReviewWorker(QObject):
    """Run Local AI review outside the GUI thread."""

    result_ready = Signal(object)
    finished = Signal()

    def __init__(self, evidence: Any, evidence_identity: str) -> None:
        super().__init__()
        self._evidence = evidence
        self._evidence_identity = evidence_identity

    @Slot()
    def run(self) -> None:
        """Build one bounded Local AI review and always terminate the worker."""

        try:
            result = build_local_ai_diff_review(self._evidence)
        except Exception as exc:
            result = DiffReviewAssistantResult(
                route="Local AI",
                status="blocked",
                verdict="error",
                semantic_review="Local AI review failed: " + str(exc),
                text_review="No Local AI text-diff review was produced.",
                correction_plan=(),
                warnings=("LOCAL_AI_REVIEW_FAILED",),
            )
        self.result_ready.emit((self._evidence_identity, result))
        self.finished.emit()


def build_diff_review_assistant_box(
    window: object,
    root_text_callback: RootTextCallback,
) -> QGroupBox:
    """Build one review-assistance row shared by Semantic Diff and Text Diff."""

    box = QGroupBox("Assisted Diff Review")
    layout = QVBoxLayout(box)
    layout.addWidget(
        QLabel(
            "Review with: Heuristic performs deterministic checks; Local AI reviews the "
            "immutable evidence with the configured local model; Web AI copies a bounded "
            "context package; Receive From Web AI validates pasted review JSON before it "
            "can be inserted into the two review panels. None of these routes confirms "
            "the human review checkboxes or mutates project source."
        )
    )

    row = QHBoxLayout()
    heuristic_btn = QPushButton("Heuristic")
    heuristic_btn.setToolTip(
        "Runs deterministic checks for API drift, module-size violations, blockers, warnings, and diff counts."
    )
    heuristic_btn.clicked.connect(lambda: _run_heuristic(window))
    window._large_file_refactor_workbench_diff_review_heuristic_button = heuristic_btn
    row.addWidget(heuristic_btn)

    local_ai_btn = QPushButton("Local AI")
    local_ai_btn.setToolTip(
        "Runs a schema-bounded review through the shared Local AI service on a Qt worker thread."
    )
    local_ai_btn.clicked.connect(lambda: _start_local_ai(window))
    window._large_file_refactor_workbench_diff_review_local_ai_button = local_ai_btn
    row.addWidget(local_ai_btn)

    web_ai_btn = QPushButton("Web AI")
    web_ai_btn.setToolTip(
        "Copies a contextualized external-review package with an exact marker-wrapped JSON response contract."
    )
    web_ai_btn.clicked.connect(
        lambda: _copy_web_ai(window, root_text_callback)
    )
    window._large_file_refactor_workbench_diff_review_web_ai_button = web_ai_btn
    row.addWidget(web_ai_btn)

    receive_btn = QPushButton("Receive From Web AI")
    receive_btn.setToolTip(
        "Opens a paste window. Validate the external response, then Implement Review to append it to the correct diff panels."
    )
    receive_btn.clicked.connect(lambda: _open_receive_dialog(window))
    window._large_file_refactor_workbench_diff_review_receive_button = receive_btn
    row.addWidget(receive_btn)
    row.addStretch(1)
    layout.addLayout(row)

    status = QPlainTextEdit()
    status.setReadOnly(True)
    status.setPlainText(
        "Prepare Completion Evidence first. Assisted review is advisory and does not replace human review confirmation."
    )
    window._large_file_refactor_workbench_diff_review_status_output = status
    layout.addWidget(status)

    sync_diff_review_assistant_controls(window)
    return box


def sync_diff_review_assistant_controls(window: object) -> None:
    """Enable review routes only when immutable completion evidence exists."""

    evidence_ready = _evidence(window) is not None
    local_running = bool(
        getattr(window, "_large_file_refactor_workbench_diff_review_local_ai_running", False)
    )
    for attribute in (
        "_large_file_refactor_workbench_diff_review_heuristic_button",
        "_large_file_refactor_workbench_diff_review_web_ai_button",
        "_large_file_refactor_workbench_diff_review_receive_button",
    ):
        button = getattr(window, attribute, None)
        if button is not None:
            button.setEnabled(evidence_ready)
    local_button = getattr(
        window,
        "_large_file_refactor_workbench_diff_review_local_ai_button",
        None,
    )
    if local_button is not None:
        local_button.setEnabled(evidence_ready and not local_running)
        local_button.setText("Local AI - Running" if local_running else "Local AI")


def _run_heuristic(window: object) -> None:
    evidence = _evidence(window)
    if evidence is None:
        _set_status(window, "HEURISTIC REVIEW BLOCKED\nPrepare Completion Evidence first.")
        return
    result = build_heuristic_diff_review(evidence)
    _apply_result(window, result)
    _set_status(
        window,
        "HEURISTIC REVIEW APPLIED\nDeterministic findings were appended to Semantic Diff and Text Diff. Human review remains manual.",
    )


def _start_local_ai(window: object) -> None:
    evidence = _evidence(window)
    if evidence is None:
        _set_status(window, "LOCAL AI REVIEW BLOCKED\nPrepare Completion Evidence first.")
        return
    if bool(getattr(window, "_large_file_refactor_workbench_diff_review_local_ai_running", False)):
        return

    evidence_identity = _evidence_identity(evidence)
    thread = QThread()
    worker = _LocalDiffReviewWorker(evidence, evidence_identity)
    receiver = _LocalDiffReviewReceiver(window, thread)
    worker.moveToThread(thread)

    window._large_file_refactor_workbench_diff_review_local_ai_running = True
    window._large_file_refactor_workbench_diff_review_local_ai_thread = thread
    window._large_file_refactor_workbench_diff_review_local_ai_worker = worker
    window._large_file_refactor_workbench_diff_review_local_ai_receiver = receiver

    thread.started.connect(worker.run)
    worker.result_ready.connect(receiver.on_result)
    worker.finished.connect(thread.quit)
    worker.finished.connect(worker.deleteLater)
    thread.finished.connect(receiver.on_thread_finished)

    _set_status(
        window,
        "LOCAL AI REVIEW STARTED\nImmutable completion evidence is being reviewed off the GUI thread.",
    )
    sync_diff_review_assistant_controls(window)
    thread.start()


def _on_local_ai_result(window: object, payload: object) -> None:
    try:
        evidence_identity, result = payload
    except (TypeError, ValueError):
        _set_status(window, "LOCAL AI REVIEW FAILED\nWorker returned an invalid result envelope.")
        return
    evidence = _evidence(window)
    if evidence is None or _evidence_identity(evidence) != str(evidence_identity):
        _set_status(
            window,
            "LOCAL AI REVIEW STALE\nCompletion Evidence changed while the model was running. The stale result was discarded.",
        )
        return
    if not isinstance(result, DiffReviewAssistantResult):
        _set_status(window, "LOCAL AI REVIEW FAILED\nWorker returned an unsupported result object.")
        return
    _apply_result(window, result)
    _set_status(
        window,
        "LOCAL AI REVIEW APPLIED\nThe validated model response was appended to Semantic Diff and Text Diff. Human review remains manual.",
    )


def _on_local_ai_thread_finished(window: object, thread: QThread) -> None:
    window._large_file_refactor_workbench_diff_review_local_ai_running = False
    if getattr(window, "_large_file_refactor_workbench_diff_review_local_ai_thread", None) is thread:
        window._large_file_refactor_workbench_diff_review_local_ai_thread = None
        window._large_file_refactor_workbench_diff_review_local_ai_worker = None
        receiver = getattr(
            window,
            "_large_file_refactor_workbench_diff_review_local_ai_receiver",
            None,
        )
        window._large_file_refactor_workbench_diff_review_local_ai_receiver = None
        if receiver is not None:
            receiver.deleteLater()
    thread.deleteLater()
    sync_diff_review_assistant_controls(window)


def _copy_web_ai(window: object, root_text_callback: RootTextCallback) -> None:
    evidence = _evidence(window)
    if evidence is None:
        _set_status(window, "WEB AI REVIEW BLOCKED\nPrepare Completion Evidence first.")
        return
    prompt = build_web_ai_diff_review_prompt(
        evidence,
        str(root_text_callback(window)),
    )
    QApplication.clipboard().setText(prompt)
    _set_status(
        window,
        "WEB AI REVIEW PACKAGE COPIED\nSend the clipboard package to Web AI. Paste the marker-wrapped JSON response into Receive From Web AI. A separate governed patch ZIP may also be returned when the external AI finds a KANDA Tool defect.",
    )


def _open_receive_dialog(window: object) -> None:
    if _evidence(window) is None:
        _set_status(window, "WEB AI RECEIVE BLOCKED\nPrepare Completion Evidence first.")
        return

    parent = window if isinstance(window, QWidget) else None
    dialog = QDialog(parent)
    dialog.setWindowTitle("Receive Workbench Diff Review From Web AI")
    dialog.resize(1000, 760)
    layout = QVBoxLayout(dialog)
    layout.addWidget(
        QLabel(
            "Paste the complete Web AI marker-wrapped response. Validate checks the response contract. Implement Review appends the validated semantic and text review sections to their respective panels; it does not edit project source."
        )
    )
    input_edit = QPlainTextEdit()
    input_edit.setPlaceholderText(
        "Paste KANDA_WORKBENCH_DIFF_REVIEW_BEGIN ... KANDA_WORKBENCH_DIFF_REVIEW_END here"
    )
    layout.addWidget(input_edit, 1)
    status = QLabel("Not validated.")
    layout.addWidget(status)

    buttons = QHBoxLayout()
    validate_btn = QPushButton("Validate Response")
    implement_btn = QPushButton("Implement Review")
    implement_btn.setEnabled(False)
    clear_btn = QPushButton("Clear")
    close_btn = QPushButton("Close")
    buttons.addWidget(validate_btn)
    buttons.addWidget(implement_btn)
    buttons.addWidget(clear_btn)
    buttons.addStretch(1)
    buttons.addWidget(close_btn)
    layout.addLayout(buttons)

    state: dict[str, DiffReviewAssistantResult | None] = {"result": None}

    def validate_response() -> None:
        try:
            result = parse_web_ai_diff_review_response(input_edit.toPlainText())
        except ValueError as exc:
            state["result"] = None
            implement_btn.setEnabled(False)
            status.setText("Validation failed: " + str(exc))
            return
        state["result"] = result
        implement_btn.setEnabled(True)
        status.setText("Response contract valid. Review can be implemented into the two panels.")

    def implement_review() -> None:
        result = state.get("result")
        if result is None:
            status.setText("Validate the response before implementation.")
            return
        _apply_result(window, result)
        _set_status(
            window,
            "WEB AI REVIEW APPLIED\nValidated external review text was appended to Semantic Diff and Text Diff. No source mutation occurred.",
        )
        dialog.accept()

    validate_btn.clicked.connect(validate_response)
    implement_btn.clicked.connect(implement_review)
    clear_btn.clicked.connect(lambda: _clear_receive_dialog(input_edit, status, implement_btn, state))
    close_btn.clicked.connect(dialog.reject)
    dialog.exec()


def _clear_receive_dialog(
    input_edit: QPlainTextEdit,
    status: QLabel,
    implement_btn: QPushButton,
    state: dict[str, DiffReviewAssistantResult | None],
) -> None:
    input_edit.clear()
    state["result"] = None
    implement_btn.setEnabled(False)
    status.setText("Not validated.")


def _apply_result(window: object, result: DiffReviewAssistantResult) -> None:
    semantic_output = getattr(window, "_large_file_refactor_workbench_semantic_diff_output", None)
    text_output = getattr(window, "_large_file_refactor_workbench_text_diff_output", None)
    if semantic_output is not None:
        semantic_output.appendPlainText(
            format_assistant_panel_appendix(result, panel="semantic")
        )
    if text_output is not None:
        text_output.appendPlainText(
            format_assistant_panel_appendix(result, panel="text")
        )
    window._large_file_refactor_workbench_last_diff_review_assistant_result = result


def _evidence(window: object) -> Any:
    return getattr(window, "_large_file_refactor_workbench_completion_evidence", None)


def _evidence_identity(evidence: Any) -> str:
    semantic = evidence.semantic_review
    return str(getattr(semantic, "contract_hash", "")) + ":" + str(
        getattr(semantic, "payload_hash", "")
    )


def _set_status(window: object, text: str) -> None:
    output = getattr(window, "_large_file_refactor_workbench_diff_review_status_output", None)
    if output is not None:
        output.setPlainText(str(text))
