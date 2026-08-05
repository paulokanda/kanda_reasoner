# project-path: _reasoner_tools_gui_engineering_safety_full_audit.py
"""Private complete-audit orchestration for the Engineering Safety panel."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from threading import Event

from _reasoner_tools_gui_engineering_safety_review_signals import (
    ASSESSMENT_DEGRADED,
    ASSESSMENT_DRAFT,
    ASSESSMENT_FAILED,
    ASSESSMENT_INVALID_COVERAGE,
    ASSESSMENT_MANUAL_REVIEW_REQUIRED,
    ASSESSMENT_MISSING_EVIDENCE,
    ASSESSMENT_NOT_RUN,
    ASSESSMENT_PASS_WITH_FINDINGS,
    classify_engineering_review_signal,
)
from _reasoner_tools_gui_engineering_safety_sonar import (
    create_engineering_safety_sonar,
)

__all__: list[str] = []

_MANUAL_COMMANDS = frozenset({"ruff-correction-dialog"})
_COMPLETE_REVIEW_COMMAND = "complete-engineering-review"


@dataclass(frozen=True)
class _EngineeringReviewItemResult:
    """Typed outcome for one complete-review catalog command."""

    status_code: int
    stdout: str
    stderr: str
    outcome: str
    assessment: str
    assessment_reason: str


def _run_catalog_item(
    command_name: str,
    project_root: str,
    command_runner: Callable[[str, str], object],
) -> _EngineeringReviewItemResult:
    """Run one catalog command and surface exceptions as explicit failures."""
    try:
        result = command_runner(command_name, project_root)
    except Exception as exc:  # noqa: BLE001 - orchestration boundary result.
        return _EngineeringReviewItemResult(
            status_code=1,
            stdout="",
            stderr=f"{type(exc).__name__}: {exc}",
            outcome="FAIL",
            assessment=ASSESSMENT_FAILED,
            assessment_reason="Command runner raised an exception.",
        )

    status_code = _result_status_code(result)
    stdout_text = _result_text(result, "stdout")
    stderr_text = _result_text(result, "stderr")
    signal = classify_engineering_review_signal(
        command_name,
        status_code,
        stdout_text,
        stderr_text,
    )
    return _EngineeringReviewItemResult(
        status_code=status_code,
        stdout=stdout_text,
        stderr=stderr_text,
        outcome="PASS" if status_code == 0 else "FAIL",
        assessment=signal.assessment,
        assessment_reason=signal.reason,
    )


def _result_status_code(result: object) -> int:
    """Return a numeric status code from a panel command result."""
    for name in ("status_code", "status"):
        value = getattr(result, name, None)
        if isinstance(value, int):
            return value
    return 0


def _result_text(result: object, name: str) -> str:
    """Return one normalized text field from a panel command result."""
    value = getattr(result, name, "")
    return str(value or "").strip()


def _format_item_result(
    index: int,
    total: int,
    tool: object,
    outcome: str,
    assessment: str,
    assessment_reason: str,
    status_code: int | None,
    stdout_text: str,
    stderr_text: str,
) -> list[str]:
    """Format one discriminated Engineering Safety audit result block."""
    section = str(getattr(tool, "section", "Engineering Safety"))
    label = str(getattr(tool, "label", "Unnamed tool"))
    command_name = str(getattr(tool, "command_name", ""))
    lines = [
        f"[{index:02d}/{total:02d}] {section} - {label}",
        f"Command: {command_name}",
        f"Outcome: {outcome}",
        f"Execution: {outcome}",
        f"Assessment: {assessment}",
        f"Assessment reason: {assessment_reason}",
    ]
    if status_code is not None:
        lines.append(f"Status: {status_code}")
    if stdout_text:
        lines.extend(("STDOUT:", stdout_text))
    if stderr_text:
        lines.extend(("STDERR:", stderr_text))
    lines.append("-" * 72)
    return lines


def run_complete_engineering_review(
    tools: Iterable[object],
    project_root: str,
    command_runner: Callable[[str, str], object],
    cancel_requested: Callable[[], bool] | None = None,
) -> str:
    """Run every safe catalog item and return one complete audit log.

    Interactive actions are represented in the report but are not opened or
    applied automatically. A failed command does not stop later checks.
    Cancellation is cooperative and is observed between catalog items.
    """
    catalog = tuple(tools)
    total = len(catalog)
    lines = [
        "COMPLETE ENGINEERING REVIEW",
        f"Project root: {project_root}",
        f"Catalog items: {total}",
        "",
    ]
    passed = 0
    failed = 0
    completed = 0
    cancelled = False
    assessment_counts = {
        "CLEAN": 0,
        ASSESSMENT_PASS_WITH_FINDINGS: 0,
        ASSESSMENT_DEGRADED: 0,
        ASSESSMENT_INVALID_COVERAGE: 0,
        ASSESSMENT_MISSING_EVIDENCE: 0,
        ASSESSMENT_DRAFT: 0,
        ASSESSMENT_NOT_RUN: 0,
        ASSESSMENT_MANUAL_REVIEW_REQUIRED: 0,
        ASSESSMENT_FAILED: 0,
    }

    for index, tool in enumerate(catalog, start=1):
        if cancel_requested is not None and cancel_requested():
            cancelled = True
            label = str(getattr(tool, "label", "next catalog item"))
            lines.extend(
                (
                    "CANCELLATION",
                    f"Stopped before item {index:02d}/{total:02d}: {label}",
                    "The active command, if any, was allowed to settle safely.",
                    "-" * 72,
                )
            )
            break

        command_name = str(getattr(tool, "command_name", ""))
        if command_name in _MANUAL_COMMANDS:
            assessment_counts[ASSESSMENT_MANUAL_REVIEW_REQUIRED] += 1
            completed += 1
            lines.extend(
                _format_item_result(
                    index,
                    total,
                    tool,
                    "MANUAL REVIEW REQUIRED",
                    ASSESSMENT_MANUAL_REVIEW_REQUIRED,
                    "Interactive correction requires explicit human review.",
                    None,
                    "",
                    (
                        "This interactive correction workflow is intentionally "
                        "not opened or applied by Complete Engineering Review."
                    ),
                )
            )
            continue

        item_result = _run_catalog_item(
            command_name,
            project_root,
            command_runner,
        )
        if item_result.status_code == 0:
            passed += 1
        else:
            failed += 1

        assessment_counts[item_result.assessment] += 1
        completed += 1
        lines.extend(
            _format_item_result(
                index,
                total,
                tool,
                item_result.outcome,
                item_result.assessment,
                item_result.assessment_reason,
                item_result.status_code,
                item_result.stdout,
                item_result.stderr,
            )
        )

    if not cancelled and cancel_requested is not None and cancel_requested():
        cancelled = completed < total

    overall = "PASS"
    if cancelled:
        overall = "CANCELLED"
    elif failed or assessment_counts[ASSESSMENT_FAILED]:
        overall = "ATTENTION REQUIRED"
    elif assessment_counts[ASSESSMENT_INVALID_COVERAGE]:
        overall = "INVALID REVIEW"
    elif (
        assessment_counts[ASSESSMENT_MISSING_EVIDENCE]
        or assessment_counts[ASSESSMENT_DEGRADED]
        or assessment_counts[ASSESSMENT_NOT_RUN]
    ):
        overall = "DEGRADED REVIEW"
    elif (
        assessment_counts[ASSESSMENT_PASS_WITH_FINDINGS]
        or assessment_counts[ASSESSMENT_DRAFT]
        or assessment_counts[ASSESSMENT_MANUAL_REVIEW_REQUIRED]
    ):
        overall = "PASS WITH REVIEW ITEMS"
    lines.extend(
        (
            "SUMMARY",
            f"Overall: {overall}",
            f"Passed: {passed}",
            f"Failed: {failed}",
            f"Commands succeeded: {passed}",
            f"Commands failed: {failed}",
            f"Clean checks: {assessment_counts['CLEAN']}",
            (
                "Checks with findings: "
                + str(assessment_counts[ASSESSMENT_PASS_WITH_FINDINGS])
            ),
            f"Degraded checks: {assessment_counts[ASSESSMENT_DEGRADED]}",
            (
                "Invalid coverage checks: "
                + str(assessment_counts[ASSESSMENT_INVALID_COVERAGE])
            ),
            (
                "Missing evidence checks: "
                + str(assessment_counts[ASSESSMENT_MISSING_EVIDENCE])
            ),
            f"Draft checks: {assessment_counts[ASSESSMENT_DRAFT]}",
            f"Not-run checks: {assessment_counts[ASSESSMENT_NOT_RUN]}",
            (
                "Manual review required: "
                + str(assessment_counts[ASSESSMENT_MANUAL_REVIEW_REQUIRED])
            ),
            f"Failed assessments: {assessment_counts[ASSESSMENT_FAILED]}",
            f"Completed catalog items: {completed}",
            f"Cancelled: {'YES' if cancelled else 'NO'}",
            f"Total catalog items: {total}",
        )
    )
    return "\n".join(lines)


def _install_complete_engineering_review(
    panel: object,
    audit_tabs: object,
    command_executor: object,
    running_commands: set[str],
    set_buttons_enabled: Callable[[bool], None],
    current_project_root: Callable[[], str],
    catalog_provider: Callable[[], tuple[object, ...]],
    command_runner: Callable[[str, str], object],
    status_label: object,
) -> None:
    """Create and bind the Full Audit page without owning panel state."""
    from PySide6.QtCore import QTimer  # type: ignore[import-not-found]
    from PySide6.QtWidgets import (  # type: ignore[import-not-found]
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
    start_button.setToolTip(
        "Run every safe Engineering Safety catalog item in order and build one report"
    )
    cancel_button = QPushButton("Cancel Review")
    cancel_button.setObjectName("engineering_safety_cancel_review_button")
    cancel_button.setToolTip(
        "Request cooperative cancellation. The current catalog command is allowed "
        "to settle before the review stops."
    )
    cancel_button.setEnabled(False)
    controls.addWidget(start_button)
    controls.addWidget(cancel_button)
    controls.addStretch(1)

    sonar = create_engineering_safety_sonar(full_page)
    output = QTextEdit()
    output.setObjectName("engineering_safety_full_audit_log")
    output.setReadOnly(True)
    output.setPlainText(
        "Run Complete Enginneering Review to audit every Engineering Safety item."
    )
    layout.addLayout(controls)
    layout.addWidget(output, 1)
    audit_tabs.insertTab(0, full_page, "Full Audit")

    cancel_event = Event()
    panel.engineering_safety_full_audit_page = full_page
    panel.engineering_safety_full_audit_button = start_button
    panel.engineering_safety_cancel_review_button = cancel_button
    panel.engineering_safety_full_audit_sonar = sonar
    panel.engineering_safety_full_audit_sonar_widget = sonar.widget()
    panel.engineering_safety_full_audit_log = output
    panel.engineering_safety_full_audit_cancel_event = cancel_event

    def finish(future: object) -> None:
        try:
            output.setPlainText(str(future.result()))  # type: ignore[attr-defined]
            if cancel_event.is_set():
                status_label.setText("Cancelled: complete-engineering-review")
            else:
                status_label.setText("Finished: complete-engineering-review")
        except Exception as exc:  # noqa: BLE001
            output.setPlainText(f"{type(exc).__name__}: {exc}")
            status_label.setText(f"Failed: complete-engineering-review: {exc}")
        finally:
            sonar.stop()  # type: ignore[attr-defined]
            running_commands.discard(_COMPLETE_REVIEW_COMMAND)
            set_buttons_enabled(True)
            cancel_button.setEnabled(False)
            start_button.setEnabled(True)

    def poll(future: object) -> None:
        if future.done():  # type: ignore[attr-defined]
            finish(future)
            return
        QTimer.singleShot(150, lambda: poll(future))

    def cancel() -> None:
        if _COMPLETE_REVIEW_COMMAND not in running_commands:
            status_label.setText("No complete Engineering review is running.")
            return
        if cancel_event.is_set():
            return
        cancel_event.set()
        sonar.stop()  # Visual feedback stops immediately on user cancellation.
        cancel_button.setEnabled(False)
        status_label.setText("Cancellation requested: complete-engineering-review")
        output.append(
            "\nCancellation requested. Sonar stopped immediately. The active "
            "catalog command will settle before the review stops."
        )

    def start() -> None:
        if running_commands:
            active = sorted(running_commands)[0]
            status_label.setText(f"Still running: {active}")
            return
        cancel_event.clear()
        running_commands.add(_COMPLETE_REVIEW_COMMAND)
        set_buttons_enabled(False)
        start_button.setEnabled(False)
        cancel_button.setEnabled(True)
        sonar.start()  # type: ignore[attr-defined]
        output.setPlainText(
            "Running Complete Enginneering Review.\n"
            "Every catalog item will receive a separate result block.\n"
            "Cancel Review stops cooperatively between catalog items."
        )
        future = command_executor.submit(
            run_complete_engineering_review,
            catalog_provider(),
            current_project_root(),
            command_runner,
            cancel_event.is_set,
        )
        QTimer.singleShot(150, lambda: poll(future))

    start_button.clicked.connect(start)
    cancel_button.clicked.connect(cancel)
