"""Focused tests for reader AI workflow contract detectors."""

from __future__ import annotations

import atexit
import shutil
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_context import (  # noqa: E501
    WorkflowDetectorContext,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_detector_registry import (  # noqa: E501
    run_workflow_detectors,
)
from kanda_reasoner_app.manage_workflows.manage_workflows_help.workflow_reader_ai_contract_detectors import (  # noqa: E501
    detect_workflow_reader_ai_contract_issues,
)


_TEMP_ROOTS: list[Path] = []


def _cleanup_temp_roots() -> None:
    for root in list(_TEMP_ROOTS):
        shutil.rmtree(root, ignore_errors=True)


atexit.register(_cleanup_temp_roots)


SAFE_SOURCE = """
class AskSessionService:
    pass

class ReaderWindow:
    def build(self):
        self.ask_local_ai_button.clicked.connect(self.ask_local_ai)

    def ask_local_ai(self):
        session_service = AskSessionService()
        json_track = "developer_tools__complete_local_AI.json"
        canonical_track = "developer_tools__complete.json"
        return session_service, json_track, canonical_track
"""


def _context(source_text: str) -> WorkflowDetectorContext:
    root = Path(tempfile.mkdtemp(prefix="workflow_reader_ai_contract_"))
    _TEMP_ROOTS.append(root)

    package_dir = "_".join(("ask", "ai", "project", "reasoner"))
    source_dir = root / package_dir / "project_reasoner_v10"
    source_dir.mkdir(parents=True, exist_ok=True)
    source_path = source_dir / "reader_ai_sample.py"
    source_path.write_text(source_text, encoding="utf-8")

    return WorkflowDetectorContext(
        project_root=root,
        workflow_manifest={"workflows": {}},
        workflows_doc="",
    )


class WorkflowReaderAiContractDetectorTests(unittest.TestCase):
    """Protect reader AI workflow contract detection."""

    def test_project_without_reader_ai_feature_has_no_issue(self) -> None:
        context = _context("def unrelated():\n    return 'ok'\n")

        issues = detect_workflow_reader_ai_contract_issues(context)

        self.assertEqual(issues, [])

    def test_safe_reader_ai_flow_has_no_issue(self) -> None:
        context = _context(SAFE_SOURCE)

        issues = detect_workflow_reader_ai_contract_issues(context)

        self.assertEqual(issues, [])

    def test_missing_ask_wiring_is_error(self) -> None:
        source = SAFE_SOURCE.replace(
            "self.ask_local_ai_button.clicked.connect(self.ask_local_ai)",
            "self.ask_local_ai_label = 'Ask Local AI'",
        )
        context = _context(source)

        issues = detect_workflow_reader_ai_contract_issues(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_READER_AI_ASK_BUTTON_NOT_WIRED", issue_ids)

    def test_missing_session_boundary_is_error(self) -> None:
        source = SAFE_SOURCE.replace("class AskSessionService:\n    pass\n\n", "")
        source = source.replace(
            "session_service = AskSessionService()",
            "session = object()",
        )
        source = source.replace(
            "return session_service, json_track, canonical_track",
            "return session, json_track, canonical_track",
        )
        context = _context(source)

        issues = detect_workflow_reader_ai_contract_issues(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_READER_AI_ASK_SESSION_SERVICE_BYPASSED", issue_ids)

    def test_missing_json_track_classifier_is_error(self) -> None:
        source = SAFE_SOURCE.replace(
            'json_track = "developer_tools__complete_local_AI.json"',
            'json_blob = "developer_tools__complete.json"',
        )
        source = source.replace(
            'canonical_track = "developer_tools__complete.json"',
            'canonical_blob = "developer_tools__complete.json"',
        )
        source = source.replace(
            "return session_service, json_track, canonical_track",
            "return session_service, json_blob, canonical_blob",
        )
        context = _context(source)

        issues = detect_workflow_reader_ai_contract_issues(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_READER_AI_JSON_TRACK_CLASSIFIER_MISSING", issue_ids)

    def test_default_registry_runs_detector(self) -> None:
        source = SAFE_SOURCE.replace(
            "self.ask_local_ai_button.clicked.connect(self.ask_local_ai)",
            "self.ask_local_ai_label = 'Ask Local AI'",
        )
        context = _context(source)

        issues = run_workflow_detectors(context)

        issue_ids = {issue.issue_id for issue in issues}
        self.assertIn("WORKFLOW_READER_AI_ASK_BUTTON_NOT_WIRED", issue_ids)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
