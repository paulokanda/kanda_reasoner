# project-path: kanda_reasoner_app/manage_workflows/manage_workflows_help/workflow_reader_ai_contract_detectors.py
"""Detect reader AI ask-flow and JSON-track workflow contract issues."""

from __future__ import annotations

from pathlib import Path

from .workflow_detector_context import WorkflowDetectorContext
from .workflow_issue_models import WorkflowIssue

__all__ = [
    "detect_workflow_reader_ai_contract_issues",
]


def _issue(
    *,
    issue_id: str,
    workflow_step: str,
    evidence: str,
    expected: str,
    actual: str,
) -> WorkflowIssue:
    """Support issue behavior.
    
    Parameters
    ----------
    issue_id : str
        The issue id value.
    workflow_step : str
        The workflow step value.
    evidence : str
        The evidence value.
    expected : str
        The expected value.
    actual : str
        The actual value.
    
    Returns
    -------
    WorkflowIssue
        The workflow issue result.
    """
    
    return WorkflowIssue(
        issue_id=issue_id,
        category="workflow_reader_ai_contract",
        severity="error",
        workflow_step=workflow_step,
        evidence=evidence,
        expected=expected,
        actual=actual,
    )


def _read_text(path: Path) -> str:
    """Support read text behavior.
    
    Parameters
    ----------
    path : Path
        The file or folder path.
    
    Returns
    -------
    str
        The string result.
    """
    
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _candidate_source_roots(project_root: Path) -> list[Path]:
    """Support candidate source roots behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    list[Path]
        The list of values.
    """
    
    package_root = project_root / "_".join(("ask", "ai", "project", "reasoner"))
    return [
        package_root / "project_reasoner_v10",
        package_root / "manage_workflows",
    ]


def _combined_source_text(project_root: Path) -> str:
    """Support combined source text behavior.
    
    Parameters
    ----------
    project_root : Path
        The project root path.
    
    Returns
    -------
    str
        The string result.
    """
    
    chunks: list[str] = []
    for source_root in _candidate_source_roots(project_root):
        if not source_root.exists():
            continue
        for path in sorted(source_root.rglob("*.py")):
            chunks.append(_read_text(path))
    return "\n".join(chunks).lower()


def _reader_runtime_markers() -> tuple[str, ...]:
    """Support reader runtime markers behavior.
    
    Returns
    -------
    tuple[str, ...]
        The tuple of values.
    """
    
    local_token = "local"
    ai_token = "ai"
    return (
        local_token + " " + ai_token,
        local_token + "_" + ai_token,
        local_token + "-" + ai_token,
        "ask " + local_token + " " + ai_token,
        "ask_" + local_token + "_" + ai_token,
        "complete_" + local_token + "_" + ai_token,
        "developer_tools__complete_" + local_token + "_" + ai_token,
        "reader ai",
        "reader_ai",
    )


def _has_reader_feature(text: str) -> bool:
    """Support has reader feature behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    return any(marker in text for marker in _reader_runtime_markers())


def _ask_control_is_wired(text: str) -> bool:
    """Support ask control is wired behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    ask_markers = (
        "ask_" + "local" + "_" + "ai",
        "ask " + "local" + " " + "ai",
        "reader_ai",
        "reader ai",
    )
    has_ask_marker = any(marker in text for marker in ask_markers)
    if not has_ask_marker:
        return False

    wiring_markers = (
        "clicked.connect",
        ".connect(",
        "triggered.connect",
        "button",
        "action",
    )
    return any(marker in text for marker in wiring_markers)


def _session_boundary_is_preserved(text: str) -> bool:
    """Support session boundary is preserved behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    strong_markers = (
        "session_service",
        "ask_session_service",
        "asksessionservice",
        "session service",
    )
    if any(marker in text for marker in strong_markers):
        return True

    return "session" in text and "service" in text and "ask" in text


def _json_track_classifier_is_present(text: str) -> bool:
    """Support json track classifier is present behavior.
    
    Parameters
    ----------
    text : str
        The text value.
    
    Returns
    -------
    bool
        True if the condition is met; otherwise, False.
    """
    
    local_token = "local"
    ai_token = "ai"

    strong_markers = (
        "complete_" + local_token + "_" + ai_token,
        "developer_tools__complete_" + local_token + "_" + ai_token,
        "json_track",
        "track_classifier",
    )
    if any(marker in text for marker in strong_markers):
        return True

    has_dual_json_terms = (
        "canonical" in text
        and local_token + "_" + ai_token in text
        and "json" in text
    )
    has_classifier_terms = "classif" in text or "track" in text or "route" in text
    return has_dual_json_terms and has_classifier_terms


def detect_workflow_reader_ai_contract_issues(
    context: WorkflowDetectorContext,
) -> list[WorkflowIssue]:
    """Detect reader AI ask-flow and dual-JSON workflow regressions."""
    text = _combined_source_text(context.project_root)
    if not text.strip():
        return []

    if not _has_reader_feature(text):
        return []

    issues: list[WorkflowIssue] = []

    if not _ask_control_is_wired(text):
        issues.append(
            _issue(
                issue_id="WORKFLOW_READER_AI_ASK_BUTTON_NOT_WIRED",
                workflow_step="reader_ai::ask_control",
                evidence="reader AI ask feature markers exist without a visible button/action wiring marker.",
                expected="The reader AI ask control should be wired to an executable ask action.",
                actual="No clicked/connect/action wiring marker was found near the reader AI ask feature.",
            )
        )

    if not _session_boundary_is_preserved(text):
        issues.append(
            _issue(
                issue_id="WORKFLOW_READER_AI_ASK_SESSION_SERVICE_BYPASSED",
                workflow_step="reader_ai::session_boundary",
                evidence="reader AI ask feature markers exist without a visible session-service boundary marker.",
                expected="The reader AI ask flow should preserve the session-service boundary.",
                actual="No session-service marker was found for the reader AI ask feature.",
            )
        )

    if not _json_track_classifier_is_present(text):
        issues.append(
            _issue(
                issue_id="WORKFLOW_READER_AI_JSON_TRACK_CLASSIFIER_MISSING",
                workflow_step="reader_ai::json_track_classifier",
                evidence="reader AI feature markers exist without a visible dual-JSON classifier marker.",
                expected="The workflow should distinguish canonical JSON from reader AI JSON.",
                actual="No dual-JSON track classifier marker was found.",
            )
        )

    return issues
