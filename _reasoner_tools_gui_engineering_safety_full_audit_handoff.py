# project-path: _reasoner_tools_gui_engineering_safety_full_audit_handoff.py
"""Project-card guarded AI handoff integration for Complete Engineering Review."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from threading import Event
import time

from _reasoner_tools_gui_engineering_safety_sonar import (
    create_engineering_safety_sonar,
)
from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_handoff import (
    AiCorrectionHandoffArtifact,
)
from kanda_reasoner_app.engineering_diagnostics_gui.review_handoff import (
    build_complete_review_ai_correction_handoff,
)
from kanda_reasoner_app.engineering_safety.complete_review_contract import (
    CompleteEngineeringReviewResult,
)
from kanda_reasoner_app.project_selection_registry import (
    ProjectSelectionRecord,
    ProjectSelectionRegistry,
)

__all__: list[str] = []


def _tool_root() -> Path:
    """Return this KANDA Tool installation root, never the audit target."""
    return Path(__file__).resolve().parent


def capture_active_project_card(project_root: str) -> ProjectSelectionRecord:
    """Capture the canonical selected-Project M-card for one review run."""
    tool_root = _tool_root()
    registry = ProjectSelectionRegistry(tool_source_root=tool_root)
    record = registry.load_current_record()
    if record is None:
        raise RuntimeError("ACTIVE_PROJECT_SELECTION_REQUIRED")
    boundary = registry.resolve_boundary_for_root(project_root)
    if boundary.active_project_id != record.stable_project_id:
        raise RuntimeError("ACTIVE_PROJECT_CARD_ID_MISMATCH")
    if boundary.active_project_root_fingerprint != record.project_root_fingerprint:
        raise RuntimeError("ACTIVE_PROJECT_CARD_ROOT_FINGERPRINT_MISMATCH")
    return record


def project_card_is_current(card: ProjectSelectionRecord) -> bool:
    """Return whether the exact selection snapshot still owns the active card."""
    registry = ProjectSelectionRegistry(tool_source_root=_tool_root())
    current = registry.load_current_record()
    if current is None:
        return False
    return current.as_json() == card.as_json()


def build_project_bound_handoff(
    card: ProjectSelectionRecord,
    review: CompleteEngineeringReviewResult,
    cancellation: Event,
    performance_lines: tuple[str, ...] = (),
):
    """Invoke the public Diagnostics handoff for only the captured Project card."""
    if not project_card_is_current(card):
        raise RuntimeError("ACTIVE_PROJECT_MCARD_CHANGED")
    return build_complete_review_ai_correction_handoff(
        _tool_root(),
        card,
        review,
        cancellation,
        performance_lines=performance_lines,
    )


def install_review_handoff(
    panel: object,
    audit_tabs: object,
    command_executor: object,
    running_commands: set[str],
    set_buttons_enabled: Callable[[bool], None],
    current_project_root: Callable[[], str],
    catalog_provider: Callable[[], tuple[object, ...]],
    command_runner: Callable[[str, str], object],
    status_label: object,
    review_collector: Callable[..., CompleteEngineeringReviewResult],
    complete_review_command: str,
) -> None:
    """Create Full Audit and publish one Project-bound AI handoff on completion."""
    from PySide6.QtCore import QTimer  # type: ignore[import-not-found]
    from PySide6.QtWidgets import (  # type: ignore[import-not-found]
        QApplication,
        QHBoxLayout,
        QPushButton,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )

    full_page = QWidget(audit_tabs)
    full_page.setObjectName("engineering_safety_full_audit_page")
    layout = QVBoxLayout(full_page)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(8)
    controls = QHBoxLayout()
    controls.setContentsMargins(0, 0, 0, 0)
    controls.setSpacing(8)

    start_button = QPushButton("Complete Enginneering Review")
    start_button.setObjectName(
        "engineering_safety_complete_engineering_review_button"
    )
    cancel_button = QPushButton("Cancel Review")
    cancel_button.setObjectName("engineering_safety_cancel_review_button")
    cancel_button.setEnabled(False)
    copy_button = QPushButton("Copy Complete AI Correction Handoff")
    copy_button.setObjectName(
        "engineering_safety_copy_complete_ai_correction_handoff_button"
    )
    copy_button.setEnabled(False)
    controls.addWidget(start_button)
    controls.addWidget(cancel_button)
    controls.addWidget(copy_button)
    controls.addStretch(1)

    sonar = create_engineering_safety_sonar(full_page)
    output = QTextEdit()
    output.setObjectName("engineering_safety_full_audit_log")
    output.setReadOnly(True)
    output.setPlainText(
        "Run Complete Enginneering Review to audit the active Project and build "
        "one AI correction handoff."
    )
    layout.addLayout(controls)
    layout.addWidget(output, 1)
    audit_tabs.insertTab(0, full_page, "Full Audit")

    cancel_event = Event()
    state: dict[str, object | None] = {
        "project_card": None,
        "review_future": None,
        "handoff_future": None,
        "artifact": None,
        "review_started_at": None,
        "review_command_timings": None,
    }
    panel.engineering_safety_full_audit_page = full_page
    panel.engineering_safety_full_audit_button = start_button
    panel.engineering_safety_cancel_review_button = cancel_button
    panel.engineering_safety_copy_complete_ai_correction_handoff_button = copy_button
    panel.engineering_safety_full_audit_sonar = sonar
    panel.engineering_safety_full_audit_sonar_widget = sonar.widget()
    panel.engineering_safety_full_audit_log = output
    panel.engineering_safety_full_audit_cancel_event = cancel_event

    def finalize() -> None:
        sonar.stop()  # type: ignore[attr-defined]
        running_commands.discard(complete_review_command)
        set_buttons_enabled(True)
        cancel_button.setEnabled(False)
        start_button.setEnabled(True)
        copy_button.setEnabled(
            isinstance(state.get("artifact"), AiCorrectionHandoffArtifact)
        )

    def finish_handoff(future: object) -> None:
        state["handoff_future"] = None
        try:
            artifact = future.result()  # type: ignore[attr-defined]
            card = state.get("project_card")
            if card is None or not project_card_is_current(card):
                raise RuntimeError("ACTIVE_PROJECT_MCARD_CHANGED")
            if not isinstance(artifact, AiCorrectionHandoffArtifact):
                raise RuntimeError("AI_CORRECTION_HANDOFF_ARTIFACT_INVALID")
            state["artifact"] = artifact
            copy_button.setEnabled(True)
            output.append(
                "\nAI correction handoff: READY\n"
                + artifact.console_summary
                + "\nPath: "
                + artifact.report_path
                + "\nSHA256: "
                + artifact.sha256
                + "\nFindings: "
                + str(artifact.finding_count)
                + "\nCorrection groups: "
                + str(artifact.correction_group_count)
                + "\nEngineering capability surfaces: "
                + str(artifact.capability_surface_count)
                + "\nCapability errors: "
                + str(artifact.capability_error_count)
                + "\nCapability warnings: "
                + str(artifact.capability_warning_count)
                + "\nBytes: "
                + str(artifact.byte_count)
            )
            status_label.setText(
                "Complete Engineering Review finished. AI correction handoff READY."
            )
        except Exception as exc:  # noqa: BLE001
            state["artifact"] = None
            copy_button.setEnabled(False)
            marker = "FAILED"
            if "ACTIVE_PROJECT_MCARD_CHANGED" in str(exc):
                marker = "REJECTED_STALE_PROJECT"
            output.append(
                "\nAI correction handoff: "
                + marker
                + "\n"
                + type(exc).__name__
                + ": "
                + str(exc)
            )
            status_label.setText(
                "Complete Review finished, but AI correction handoff was not published."
            )
        finally:
            finalize()

    def poll_handoff(future: object) -> None:
        if future.done():  # type: ignore[attr-defined]
            finish_handoff(future)
            return
        QTimer.singleShot(150, lambda: poll_handoff(future))

    def finish_review(future: object) -> None:
        state["review_future"] = None
        try:
            review = future.result()  # type: ignore[attr-defined]
            if not isinstance(review, CompleteEngineeringReviewResult):
                raise RuntimeError("COMPLETE_ENGINEERING_REVIEW_RESULT_INVALID")
            render_started = time.perf_counter()
            output.setPlainText(review.rendered_log)
            render_elapsed = time.perf_counter() - render_started
            if review.cancelled or cancel_event.is_set():
                status_label.setText("Cancelled: complete-engineering-review")
                finalize()
                return
            card = state.get("project_card")
            if card is None or not project_card_is_current(card):
                output.append(
                    "\nAI correction handoff: REJECTED_STALE_PROJECT\n"
                    "The selected Project changed after Complete Engineering Review."
                )
                status_label.setText("Review result rejected: active Project changed.")
                finalize()
                return
            output.append(
                "\nAI correction handoff: BUILDING\n"
                "Audit target role: ACTIVE PROJECT\n"
                "Project is the M-card for this audit: YES\n"
                "KANDA Tool role: AUDIT EXECUTION PROVIDER ONLY\n"
                "Complete Review 23-tool evidence will be consumed, not rerun.\n"
                "Diagnostics will add its canonical structured collectors and "
                "Architecture-grade correction dossiers."
            )
            status_label.setText(
                "Complete Review finished. Building AI correction handoff..."
            )
            started_at = state.get("review_started_at")
            review_elapsed = (
                time.perf_counter() - float(started_at)
                if isinstance(started_at, (int, float))
                else 0.0
            )
            performance_lines = [
                "Complete Review total: " + f"{review_elapsed:.3f}s",
                "Complete Review GUI render: " + f"{render_elapsed:.3f}s",
            ]
            command_timings = state.get("review_command_timings")
            if isinstance(command_timings, list):
                for command_name, elapsed in command_timings:
                    performance_lines.append(
                        "Complete Review command "
                        + str(command_name)
                        + ": "
                        + f"{float(elapsed):.3f}s"
                    )
            handoff_future = command_executor.submit(
                build_project_bound_handoff,
                card,
                review,
                cancel_event,
                tuple(performance_lines),
            )
            state["handoff_future"] = handoff_future
            QTimer.singleShot(150, lambda: poll_handoff(handoff_future))
        except Exception as exc:  # noqa: BLE001
            output.setPlainText(type(exc).__name__ + ": " + str(exc))
            status_label.setText("Failed: complete-engineering-review: " + str(exc))
            finalize()

    def poll_review(future: object) -> None:
        if future.done():  # type: ignore[attr-defined]
            finish_review(future)
            return
        QTimer.singleShot(150, lambda: poll_review(future))

    def cancel() -> None:
        if complete_review_command not in running_commands:
            status_label.setText("No complete Engineering review is running.")
            return
        if cancel_event.is_set():
            return
        cancel_event.set()
        sonar.stop()
        cancel_button.setEnabled(False)
        status_label.setText("Cancellation requested: complete-engineering-review")
        output.append(
            "\nCancellation requested. Active work will settle safely before stop."
        )

    def copy_handoff() -> None:
        artifact = state.get("artifact")
        if not isinstance(artifact, AiCorrectionHandoffArtifact):
            status_label.setText("No complete AI correction handoff is ready yet.")
            return
        from pathlib import Path

        path = Path(artifact.report_path)
        if not path.is_file():
            copy_button.setEnabled(False)
            status_label.setText("AI correction handoff file is no longer available.")
            return
        if artifact.byte_count <= 2_000_000:
            QApplication.clipboard().setText(
                path.read_text(encoding="utf-8", errors="replace")
            )
            status_label.setText("Complete AI correction handoff copied.")
            return
        QApplication.clipboard().setText(
            "\n".join(
                (
                    "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF",
                    "Path: " + artifact.report_path,
                    "SHA256: " + artifact.sha256,
                    "Bytes: " + str(artifact.byte_count),
                    "Instruction: Send this report to the engineering AI.",
                )
            )
        )
        status_label.setText("Large handoff: path and SHA256 copied.")

    def start() -> None:
        if running_commands:
            active = sorted(running_commands)[0]
            status_label.setText("Still running: " + active)
            return
        cancel_event.clear()
        state["artifact"] = None
        copy_button.setEnabled(False)
        project_root = current_project_root()
        try:
            project_card = capture_active_project_card(project_root)
        except Exception as exc:  # noqa: BLE001
            output.setPlainText(
                "BRICK WALL: ACTIVE PROJECT CARD REQUIRED\n"
                + type(exc).__name__
                + ": "
                + str(exc)
            )
            status_label.setText(
                "Complete Review blocked: active Project card invalid."
            )
            return
        state["project_card"] = project_card
        review_command_timings: list[tuple[str, float]] = []
        state["review_command_timings"] = review_command_timings
        state["review_started_at"] = time.perf_counter()

        def timed_command_runner(command_name: str, root: str) -> object:
            started = time.perf_counter()
            try:
                expected_root = Path(project_card.project_root).resolve(
                    strict=False
                )
                command_root = Path(root).resolve(strict=False)
                if command_root != expected_root:
                    raise RuntimeError("COMPLETE_REVIEW_PROJECT_ROOT_MISMATCH")
                if not project_card_is_current(project_card):
                    raise RuntimeError("ACTIVE_PROJECT_MCARD_CHANGED")
                return command_runner(command_name, root)
            finally:
                review_command_timings.append(
                    (command_name, time.perf_counter() - started)
                )

        operation_id = (
            "complete-engineering-review-" + str(time.monotonic_ns())
        )

        def collect_project_review() -> CompleteEngineeringReviewResult:
            from kanda_reasoner_app.reasoner_symbol_atlas import (
                reasoner_symbol_atlas_review_session,
            )

            if not project_card_is_current(project_card):
                raise RuntimeError("ACTIVE_PROJECT_MCARD_CHANGED")
            with reasoner_symbol_atlas_review_session(
                project_root=project_card.project_root,
                stable_project_id=project_card.stable_project_id,
                project_root_fingerprint=(
                    project_card.project_root_fingerprint
                ),
                operation_id=operation_id,
            ):
                return review_collector(
                    catalog_provider(),
                    project_card.project_root,
                    timed_command_runner,
                    cancel_event.is_set,
                )

        running_commands.add(complete_review_command)
        set_buttons_enabled(False)
        start_button.setEnabled(False)
        cancel_button.setEnabled(True)
        sonar.start()  # type: ignore[attr-defined]
        output.setPlainText(
            "Running Complete Enginneering Review.\n"
            "Audit target role: ACTIVE PROJECT\n"
            "Project root: "
            + project_card.project_root
            + "\nProject stable ID: "
            + project_card.stable_project_id
            + "\nProject is the M-card for this audit: YES\n"
            "KANDA Tool role: AUDIT EXECUTION PROVIDER ONLY\n"
            "Tool and Project roles remain logically separate even if their "
            "physical roots match."
        )
        review_future = command_executor.submit(collect_project_review)
        state["review_future"] = review_future
        QTimer.singleShot(150, lambda: poll_review(review_future))

    start_button.clicked.connect(start)
    cancel_button.clicked.connect(cancel)
    copy_button.clicked.connect(copy_handoff)
