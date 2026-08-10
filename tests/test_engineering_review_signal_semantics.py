# project-path: tests/test_engineering_review_signal_semantics.py
"""Regression tests for Engineering Review decision-quality semantics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tempfile
import unittest

from _reasoner_tools_gui_engineering_safety_full_audit import (
    run_complete_engineering_review,
)
from _reasoner_tools_gui_engineering_safety_review_signals import (
    ASSESSMENT_CLEAN,
    ASSESSMENT_DEGRADED,
    ASSESSMENT_DRAFT,
    ASSESSMENT_INVALID_COVERAGE,
    ASSESSMENT_MANUAL_REVIEW_REQUIRED,
    ASSESSMENT_MISSING_EVIDENCE,
    ASSESSMENT_NOT_RUN,
    ASSESSMENT_PASS_WITH_FINDINGS,
    classify_engineering_review_signal,
)
from kanda_reasoner_app.source_hygiene.bom_scanner import (
    scan_project_for_bom,
)
from kanda_reasoner_app.source_hygiene.shadow_audit import (
    audit_project_for_shadow_conflicts,
    iter_shadow_audit_files,
)
from kanda_reasoner_app.source_hygiene.shadow_fixer import (
    build_safe_facade_fix_plan,
)


@dataclass(frozen=True)
class _Tool:
    section: str
    label: str
    command_name: str


@dataclass(frozen=True)
class _Result:
    status_code: int
    stdout: str
    stderr: str = ""


class EngineeringReviewSignalSemanticsTests(unittest.TestCase):
    """Protect signal separation, coverage, and active-source boundaries."""

    def test_classifier_separates_execution_from_decision_quality(self) -> None:
        cases = (
            (
                "bom-scan",
                "Summary: files_scanned=0; findings=0.\nFinding count: 0",
                ASSESSMENT_INVALID_COVERAGE,
            ),
            (
                "ruff-quality",
                (
                    "Summary: lint_status=0; format_status=1; findings=19874.\n"
                    "Finding count: 19874"
                ),
                ASSESSMENT_PASS_WITH_FINDINGS,
            ),
            (
                "release-notes",
                "Status: draft",
                ASSESSMENT_DRAFT,
            ),
            (
                "push-plan",
                "Overall status: unknown\n- No check results were supplied.",
                ASSESSMENT_NOT_RUN,
            ),
            (
                "evidence-freshness",
                "Evidence freshness status=missing_evidence; checked_files=0",
                ASSESSMENT_MISSING_EVIDENCE,
            ),
            (
                "find-owner",
                "status=needs_owner_review; confidence=medium",
                ASSESSMENT_MANUAL_REVIEW_REQUIRED,
            ),
            (
                "find-symbol",
                (
                    "inactive_reference_paths_filtered=true\n"
                    "owner_path=.project_reference/archive/owner.py\n"
                    "status=needs_owner_review; missing_evidence"
                ),
                ASSESSMENT_DEGRADED,
            ),
            (
                "pre-patch-gate",
                (
                    "status=needs_owner_review; "
                    "pre_patch_status=facade_patch_risk; "
                    "missing_evidence"
                ),
                ASSESSMENT_MANUAL_REVIEW_REQUIRED,
            ),
            (
                "list-tools",
                "bom-scan\nruff-quality\nshadow-audit",
                ASSESSMENT_CLEAN,
            ),
        )
        for command, output, expected in cases:
            with self.subTest(command=command):
                signal = classify_engineering_review_signal(
                    command,
                    0,
                    output,
                )
                self.assertEqual(expected, signal.assessment)

    def test_complete_review_reports_execution_and_assessment_counts(self) -> None:
        tools = (
            _Tool("Source Hygiene", "Scan BOM", "bom-scan"),
            _Tool("Source Hygiene", "Ruff Quality", "ruff-quality"),
            _Tool("Source Hygiene", "Ruff Corrections", "ruff-correction-dialog"),
            _Tool("Governance", "Release Notes", "release-notes"),
            _Tool("Governance", "Push Plan", "push-plan"),
            _Tool("Atlas", "Evidence Freshness", "evidence-freshness"),
            _Tool("Utilities", "List Tools", "list-tools"),
        )
        outputs = {
            "bom-scan": "Summary: files_scanned=0; findings=0.\nFinding count: 0",
            "ruff-quality": (
                "Summary: lint_status=0; format_status=1; findings=8.\n"
                "Finding count: 8"
            ),
            "release-notes": "Status: draft",
            "push-plan": "Overall status: unknown\nNo check results were supplied.",
            "evidence-freshness": (
                "Evidence freshness status=missing_evidence; checked_files=0"
            ),
            "list-tools": "bom-scan\nruff-quality",
        }

        def runner(command_name: str, project_root: str) -> _Result:
            self.assertEqual("C:/project", project_root)
            return _Result(0, outputs[command_name])

        report = run_complete_engineering_review(
            tools,
            "C:/project",
            runner,
        )
        self.assertIn("Outcome: PASS", report)
        self.assertIn("Execution: PASS", report)
        self.assertIn("Assessment: INVALID_COVERAGE", report)
        self.assertIn("Assessment: PASS_WITH_FINDINGS", report)
        self.assertIn("Assessment: MANUAL_REVIEW_REQUIRED", report)
        self.assertIn("Overall: INVALID REVIEW", report)
        self.assertIn("Commands succeeded: 6", report)
        self.assertIn("Commands failed: 0", report)
        self.assertIn("Clean checks: 1", report)
        self.assertIn("Checks with findings: 1", report)
        self.assertIn("Invalid coverage checks: 1", report)
        self.assertIn("Missing evidence checks: 1", report)
        self.assertIn("Draft checks: 1", report)
        self.assertIn("Not-run checks: 1", report)
        self.assertIn("Manual review required: 1", report)
        self.assertTrue(report.rstrip().endswith("Total catalog items: 7"))

    def test_bom_empty_suffix_override_uses_active_default_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "active.py").write_text("value = 1\n", encoding="utf-8")
            (root / "active.md").write_bytes(
                b"\xef\xbb\xbfactive documentation\n"
            )

            excluded_files = (
                root / "_bundle_temp" / "bundle.md",
                root / "snippets" / "example.py",
                root / "workbench" / "report.md",
                root / "feature_deprecated" / "old.py",
                root / "tests" / "fixtures" / "sample.md",
                root / ".project_reference" / "archive" / "old.py",
                root / "project_freeze_ledger" / "tool.py",
            )
            for path in excluded_files:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"\xef\xbb\xbfexcluded\n")

            report = scan_project_for_bom(root, suffixes=())

        self.assertIn("files_scanned=2", report.summary)
        self.assertEqual(1, len(report.findings))
        self.assertEqual("active.md", report.findings[0].path)

    def test_shadow_and_facade_plans_exclude_inactive_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            active_package = root / "active_package"
            active_package.mkdir()
            (active_package / "__init__.py").write_bytes(b"")
            (root / "owner_a.py").write_text(
                "def shared_symbol():\n    return 'a'\n",
                encoding="utf-8",
            )

            excluded_roots = (
                root / ".project_reference" / "archive",
                root / "_bundle_temp" / "generated",
                root / "snippets" / "example",
                root / "workbench" / "reports",
                root / "feature_deprecated",
                root / "tests" / "fixtures" / "sample",
                root / "tests" / "unit",
            )
            for excluded in excluded_roots:
                excluded.mkdir(parents=True)
                (excluded / "__init__.py").write_bytes(b"")
                (excluded / "owner_b.py").write_text(
                    "def shared_symbol():\n    return 'b'\n",
                    encoding="utf-8",
                )

            scanned = iter_shadow_audit_files(root)
            audit = audit_project_for_shadow_conflicts(root)
            fix_plan = build_safe_facade_fix_plan(root)

        scanned_paths = {path.relative_to(root).as_posix() for path in scanned}
        self.assertEqual(
            {"active_package/__init__.py", "owner_a.py"},
            scanned_paths,
        )
        serialized_audit = str(audit.to_dict())
        serialized_fix_plan = str(fix_plan.to_dict())
        for inactive_marker in (
            ".project_reference",
            "_bundle_temp",
            "snippets",
            "workbench",
            "feature_deprecated",
            "tests/fixtures",
            "tests/unit",
        ):
            self.assertNotIn(inactive_marker, serialized_audit)
            self.assertNotIn(inactive_marker, serialized_fix_plan)
        self.assertIn("active_package/__init__.py", serialized_fix_plan)



if __name__ == "__main__":
    unittest.main(verbosity=2)
