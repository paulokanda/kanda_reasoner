# project-path: kanda_reasoner_app/manage_architecture/large_file_refactor_planner/workbench_behavior_gui_bridge.py
"""GUI bridge for optional Workbench behavior/test validation."""
from __future__ import annotations

from collections.abc import Callable

from PySide6.QtWidgets import QGroupBox, QLabel, QLineEdit, QPlainTextEdit, QPushButton, QVBoxLayout

from .workbench_behavior_formatting import format_workbench_behavior_validation
from .workbench_behavior_validation import run_workbench_behavior_validation

__all__ = [
    "build_behavior_validation_section",
    "sync_behavior_validation_buttons",
]


def build_behavior_validation_section(
    window: object,
    root_getter: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> QGroupBox:
    """Create the optional behavior/test validation panel."""
    box = QGroupBox("Legacy Compatibility - Optional Behavior Validation (Non-sequential)")
    layout = QVBoxLayout(box)
    layout.addWidget(QLabel(
        "Legacy compatibility panel only. It is not part of the numbered Refactor Large "
        "Module workflow. The governed completion path performs Shadow and post-apply "
        "validation through the journaled transaction flow."
    ))
    command = QLineEdit()
    command.setPlaceholderText("Example: python -m unittest discover")
    window._large_file_refactor_workbench_behavior_command_edit = command
    layout.addWidget(command)
    button = QPushButton("Run Optional Behavior Validation")
    button.setEnabled(False)
    button.clicked.connect(lambda: _run_behavior_validation(window, root_getter, sync_callback))
    window._large_file_refactor_workbench_behavior_button = button
    layout.addWidget(button)
    status = QLabel(
        "Unavailable unless a legacy guarded-apply result and successful legacy post-apply "
        "structural validation already exist."
    )
    window._large_file_refactor_workbench_behavior_gate_label = status
    layout.addWidget(status)
    output = QPlainTextEdit()
    output.setReadOnly(True)
    output.setPlainText(
        "Optional. Requires exact-token apply and post-apply structural validation. "
        "Allowed command forms include python -m unittest, python -m pytest, and pytest."
    )
    window._large_file_refactor_workbench_behavior_output = output
    layout.addWidget(output, 1)
    return box


def sync_behavior_validation_buttons(window: object) -> None:
    """Enable behavior validation only after structural post-apply success."""
    button = getattr(window, "_large_file_refactor_workbench_behavior_button", None)
    if button is None:
        return
    apply_result = getattr(window, "_large_file_refactor_workbench_guarded_apply", None)
    post_apply = getattr(window, "_large_file_refactor_workbench_post_apply_validation", None)
    enabled = bool(
        apply_result
        and apply_result.status == "applied"
        and post_apply
        and post_apply.status == "post_apply_validated"
    )
    button.setEnabled(enabled)
    label = getattr(window, "_large_file_refactor_workbench_behavior_gate_label", None)
    if label is not None:
        if enabled:
            label.setText("Legacy behavior validation is available for the recorded legacy apply state.")
        else:
            label.setText(
                "Non-sequential legacy panel. Use Completion Review and Refactor Large Module "
                "for the governed current workflow."
            )


def _run_behavior_validation(
    window: object,
    root_getter: Callable[[object], str],
    sync_callback: Callable[[object], None],
) -> None:
    """Run optional behavior validation and render the result."""
    edit = getattr(window, "_large_file_refactor_workbench_behavior_command_edit", None)
    command = edit.text().strip() if edit is not None else ""
    result = run_workbench_behavior_validation(
        apply_result=getattr(window, "_large_file_refactor_workbench_guarded_apply", None),
        post_apply_validation=getattr(window, "_large_file_refactor_workbench_post_apply_validation", None),
        source_payload=getattr(window, "_large_file_refactor_workbench_source_payload", None),
        active_project_root=root_getter(window),
        test_command=command,
    )
    window._large_file_refactor_workbench_behavior_validation = result
    output = getattr(window, "_large_file_refactor_workbench_behavior_output", None)
    if output is not None:
        output.setPlainText(format_workbench_behavior_validation(result))
    if result.status == "behavior_validated_pass":
        window._large_file_refactor_workbench_state = "BEHAVIOR_VALIDATED_PASS"
    elif result.status == "behavior_validation_not_run":
        window._large_file_refactor_workbench_state = "APPLY_SUCCESS_STRUCTURAL"
    else:
        window._large_file_refactor_workbench_state = "BLOCKED"
    sync_callback(window)
