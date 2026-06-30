# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_interaction_contract_detectors.py
"""Detect Tab 2 workflow interface button/action and state-label mismatches."""

from __future__ import annotations

import re
from pathlib import Path

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_interaction_contract_issues",
]

_interface_WINDOW_RELATIVE_PATH = (
    "/".join(("ask", "ai", "project", "reasoner")) + "/"
    "manage_workflows/"
    "manage_workflows_interface_help/"
    "workflow_interface_window.py"
)

_BUTTON_ACTION_SNIPPETS = (
    (
        "Run toolbar action",
        "run_action.triggered.connect(self.run_selected_mode)",
        "Toolbar Run action should call run_selected_mode.",
    ),
    (
        "Run Selected Mode button",
        "self._run_button.clicked.connect(self.run_selected_mode)",
        "Run Selected Mode button should call run_selected_mode.",
    ),
    (
        "Immediate mode buttons",
        "btn.clicked.connect(lambda _=False, m=mode: self.run_mode(m))",
        "Immediate mode buttons should call run_mode with their own mode.",
    ),
    (
        "Mode Help button",
        "help_btn.clicked.connect(self.show_mode_help)",
        "Mode help button should call show_mode_help.",
    ),
)

_MODE_LOOP_SNIPPETS = (
    'for mode in ("validate", "diff", "scan", "write"):',
    'for mode in ("validate","diff","scan","write"):',
    "for mode in ['validate', 'diff', 'scan', 'write']:",
    "for mode in ['validate','diff','scan','write']:",
)

_SUCCESS_REQUIRED_SNIPPETS = (
    "setEnabled(True)",
    "OK Finished",
    "exit_code=0",
    "completed successfully",
)

_ERROR_REQUIRED_SNIPPETS = (
    "setEnabled(True)",
    "ERROR Finished",
    "exit_code=1",
    "{details}",
    "Finished with issues",
)

_RUNNING_REQUIRED_SNIPPETS = (
    "setEnabled(False)",
    "Running {mode}",
)


def _relative_display(root: Path, path: Path) -> str:
    """Return a stable project-relative display path."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _normalize_source(text: str) -> str:
    """Collapse whitespace so source checks tolerate formatting changes."""
    return " ".join(text.split())


def _line_number(text: str, needle: str) -> int:
    """Return the first source line containing needle, or 1 if not found."""
    for index, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return index
    return 1


def _function_block(source: str, function_name: str) -> str:
    """Return the textual block for a method/function name."""
    pattern = re.compile(
        r"^\s+def\s+"
        + re.escape(function_name)
        + r"\s*\(.*?(?=^\s+def\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(source)
    if match:
        return match.group(0)
    return ""


def _issue(
    *,
    issue_id: str,
    workflow_step: str,
    file_path: str,
    evidence: str,
    expected: str,
    actual: str,
    line_number: int,
) -> WorkflowIssue:
    """Build a workflow interface contract issue."""
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_detectors",
        severity="error",
        workflow_step=workflow_step,
        file_path=file_path,
        evidence=evidence,
        expected=expected,
        actual=actual,
        owning_box="workflow_governance",
        suggested_action=(
            "Align the interface label, connected slot, status text, and output footer "
            "so Tab 2 exposes the real workflow action and result."
        ),
        correction_allowed=False,
        details={
            "line_number": line_number,
            "detector": "workflow_interaction_contract_detectors",
        },
    )


def _read_interface_window_source(context: WorkflowDetectorContext) -> tuple[Path, str] | None:
    """Return the workflow interface window source when it exists in this project."""
    root = context.resolved_root()
    path = root / _interface_WINDOW_RELATIVE_PATH
    if not path.exists():
        return None
    return path, path.read_text(encoding="utf-8", errors="replace")


def _detect_button_action_mismatches(
    *,
    root: Path,
    source_path: Path,
    source: str,
) -> list[WorkflowIssue]:
    """Detect labels/buttons that do not call the intended action."""
    issues: list[WorkflowIssue] = []
    normalized = _normalize_source(source)
    rel = _relative_display(root, source_path)

    for label, snippet, expected in _BUTTON_ACTION_SNIPPETS:
        if snippet in source:
            continue
        issues.append(
            _issue(
                issue_id="WORKFLOW_INTERFACE_BUTTON_ACTION_MISMATCH",
                workflow_step=label,
                file_path=rel,
                evidence=(
                    "interface control contract is missing expected action binding: "
                    + snippet
                ),
                expected=expected,
                actual="Expected binding not found in workflow_interface_window.py.",
                line_number=_line_number(source, label.split()[0]),
            )
        )

    if not any(_normalize_source(snippet) in normalized for snippet in _MODE_LOOP_SNIPPETS):
        issues.append(
            _issue(
                issue_id="WORKFLOW_INTERFACE_BUTTON_ACTION_MISMATCH",
                workflow_step="Immediate mode buttons",
                file_path=rel,
                evidence=(
                    "interface immediate-mode buttons do not expose the canonical "
                    "validate/diff/scan/write mode set."
                ),
                expected="Mode buttons should expose validate, diff, scan, and write.",
                actual="Canonical mode loop not found.",
                line_number=_line_number(source, "for mode"),
            )
        )

    return issues


def _detect_state_label_mismatches(
    *,
    root: Path,
    source_path: Path,
    source: str,
) -> list[WorkflowIssue]:
    """Detect status/output labels that do not expose the real workflow result."""
    issues: list[WorkflowIssue] = []
    rel = _relative_display(root, source_path)

    success_block = _function_block(source, "_handle_worker_success")
    if not success_block:
        issues.append(
            _issue(
                issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                workflow_step="_handle_worker_success",
                file_path=rel,
                evidence="interface success handler is missing.",
                expected="Success handler should re-enable controls and expose exit_code=0.",
                actual="No _handle_worker_success block found.",
                line_number=1,
            )
        )
    else:
        for snippet in _SUCCESS_REQUIRED_SNIPPETS:
            if snippet in success_block:
                continue
            issues.append(
                _issue(
                    issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                    workflow_step="_handle_worker_success",
                    file_path=rel,
                    evidence="interface success state is missing required label/output: " + snippet,
                    expected=(
                        "Success state should re-enable Run, show OK status, "
                        "and append an exit_code=0 footer."
                    ),
                    actual="Missing snippet: " + snippet,
                    line_number=_line_number(source, "_handle_worker_success"),
                )
            )

    error_block = _function_block(source, "_handle_worker_error")
    if not error_block:
        issues.append(
            _issue(
                issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                workflow_step="_handle_worker_error",
                file_path=rel,
                evidence="interface error handler is missing.",
                expected="Error handler should re-enable controls and expose details.",
                actual="No _handle_worker_error block found.",
                line_number=1,
            )
        )
    else:
        for snippet in _ERROR_REQUIRED_SNIPPETS:
            if snippet in error_block:
                continue
            issues.append(
                _issue(
                    issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                    workflow_step="_handle_worker_error",
                    file_path=rel,
                    evidence="interface error state is missing required label/output: " + snippet,
                    expected=(
                        "Error state should re-enable Run, show ERROR status, "
                        "append exit_code=1, and expose failure details."
                    ),
                    actual="Missing snippet: " + snippet,
                    line_number=_line_number(source, "_handle_worker_error"),
                )
            )

    run_block = _function_block(source, "run_mode")
    if not run_block:
        issues.append(
            _issue(
                issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                workflow_step="run_mode",
                file_path=rel,
                evidence="interface run handler is missing.",
                expected="Run handler should disable Run and show Running status.",
                actual="No run_mode block found.",
                line_number=1,
            )
        )
    else:
        for snippet in _RUNNING_REQUIRED_SNIPPETS:
            if snippet in run_block:
                continue
            issues.append(
                _issue(
                    issue_id="WORKFLOW_INTERFACE_STATE_LABEL_MISMATCH",
                    workflow_step="run_mode",
                    file_path=rel,
                    evidence="interface running state is missing required label/output: " + snippet,
                    expected="Running state should disable Run and show the active mode.",
                    actual="Missing snippet: " + snippet,
                    line_number=_line_number(source, "run_mode"),
                )
            )

    return issues


def detect_workflow_interaction_contract_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect Tab 2 interface button/action and state-label contract problems."""
    loaded = _read_interface_window_source(context)
    if loaded is None:
        return []

    source_path, source = loaded
    root = context.resolved_root()
    issues: list[WorkflowIssue] = []
    issues.extend(
        _detect_button_action_mismatches(
            root=root,
            source_path=source_path,
            source=source,
        )
    )
    issues.extend(
        _detect_state_label_mismatches(
            root=root,
            source_path=source_path,
            source=source,
        )
    )
    return issues
