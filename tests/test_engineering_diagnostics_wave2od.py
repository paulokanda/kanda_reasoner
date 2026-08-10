# project-path: tests/test_engineering_diagnostics_wave2od.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2O-D."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
import unittest
from unittest.mock import patch
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import (
    ARCHITECTURE_PRODUCER_ID,
    ArchitectureCollectionCancelled,
    ArchitectureCollectionResult,
    ArchitectureIssueEvidence,
    EngineeringDiagnosticsStore,
    architecture_rule_profile,
    build_architecture_diagnostic_run,
    collect_architecture_findings,
    issue_fingerprint,
)
from kanda_reasoner_app.engineering_diagnostics_gui import (
    EngineeringDiagnosticsController,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    resolve_explicit_project_tool_boundary_identity,
)
from portable.models import BuildPaths
from portable.smoke_isolation import prepared_smoke_isolation


@dataclass
class _FakeModule:
    module_id: str
    path: str


@dataclass
class _FakeIssue:
    level: str
    code: str
    path: str
    message: str


def _fixture_paths(base: Path) -> BuildPaths:
    run_root = base / "run"
    run_root.mkdir(parents=True)
    dummy = base / "dummy"
    return BuildPaths(
        project_root=dummy,
        drive_root=base,
        project_support_root=dummy,
        transient_root=base,
        run_root=run_root,
        pyinstaller_work=dummy,
        pyinstaller_dist=dummy,
        pyinstaller_config=dummy,
        temporary_root=dummy,
        stage_parent=dummy,
        candidate_zip=dummy,
        clean_extract_root=dummy,
        final_zip=dummy,
        spec_path=dummy,
        governed_python=Path(__file__),
        zip_helper=dummy,
        registry_boundary=None,
    )


@contextmanager
def _boundary_fixture():
    with TemporaryDirectory() as temporary:
        base = Path(temporary)
        with prepared_smoke_isolation(
            _fixture_paths(base),
            "KandaReasoner",
        ) as isolation:
            isolation.app_root.mkdir(parents=True, exist_ok=True)
            isolation.project_root.mkdir(parents=True, exist_ok=True)
            (isolation.project_root / "sample.py").write_text(
                "VALUE = 1\n", encoding="utf-8"
            )
            with patch.dict("os.environ", isolation.environment, clear=True):
                boundary = resolve_explicit_project_tool_boundary_identity(
                    isolation.project_root,
                    selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
                    stable_project_id="wave2od-" + uuid4().hex,
                    tool_source_root=isolation.app_root,
                )
                yield boundary


def _scanner(issues):
    def scan(_root: Path):
        modules = {
            "sample": _FakeModule(
                "sample",
                "sample.py",
            )
        }
        return modules, list(issues), {"coverage": "fixture"}, {}

    return scan


def _boundary(_module: _FakeModule) -> str:
    return "sample_box"


def _collection(root: Path, issues) -> ArchitectureCollectionResult:
    return collect_architecture_findings(
        root,
        scanner=_scanner(issues),
        boundary_resolver=_boundary,
        validation_source_path=Path(__file__),
    )


class EngineeringDiagnosticsWave2ODTests(unittest.TestCase):
    def test_warning_only_collection_is_clean_with_valid_coverage(self) -> None:
        with _boundary_fixture() as boundary:
            result = _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "TEST_PROTECTION_GAP", "sample.py", "gap")],
            )
            self.assertEqual(result.assessment, "CLEAN")
            self.assertEqual(result.canonical_issue_count, 0)
            self.assertTrue(result.coverage_valid)
            self.assertEqual(len(result.issues), 1)

    def test_error_collection_is_not_clean(self) -> None:
        with _boundary_fixture() as boundary:
            result = _collection(
                boundary.active_project_root,
                [_FakeIssue("error", "DUPLICATE_PUBLIC_SYMBOL", "sample.py", "Symbol 'x' owned by multiple modules: ['a', 'b']")],
            )
            self.assertEqual(result.assessment, "ISSUES")
            self.assertEqual(result.canonical_issue_count, 1)

    def test_architecture_evidence_retains_governance_fields(self) -> None:
        with _boundary_fixture() as boundary:
            result = _collection(
                boundary.active_project_root,
                [_FakeIssue("error", "DUPLICATE_PUBLIC_SYMBOL", "sample.py", "Symbol 'x' owned by multiple modules: ['a', 'b']")],
            )
            run = build_architecture_diagnostic_run(
                result,
                boundary=boundary,
                attempt_id="architecture-1",
                source_fingerprint="source-v1",
                operation_generation=1,
            )
            finding = run.findings[0]
            self.assertEqual(run.producer_id, ARCHITECTURE_PRODUCER_ID)
            self.assertEqual(finding.symbol_id, "x")
            self.assertEqual(finding.evidence["boundary"], "sample_box")
            self.assertEqual(finding.evidence["validation_source"], result.validation_source)
            self.assertEqual(finding.evidence["governance_impact"], "high")

    def test_message_wording_does_not_change_issue_identity(self) -> None:
        with _boundary_fixture() as boundary:
            first = _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "TEST_PROTECTION_GAP", "sample.py", "first wording")],
            )
            second = _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "TEST_PROTECTION_GAP", "sample.py", "second wording")],
            )
            first_run = build_architecture_diagnostic_run(
                first,
                boundary=boundary,
                attempt_id="first",
                source_fingerprint="source-v1",
                operation_generation=1,
            )
            second_run = build_architecture_diagnostic_run(
                second,
                boundary=boundary,
                attempt_id="second",
                source_fingerprint="source-v1",
                operation_generation=1,
            )
            self.assertEqual(
                issue_fingerprint(first_run.producer_id, first_run.findings[0]),
                issue_fingerprint(second_run.producer_id, second_run.findings[0]),
            )

    def test_symbol_change_changes_issue_identity(self) -> None:
        with _boundary_fixture() as boundary:
            one = _collection(
                boundary.active_project_root,
                [_FakeIssue("error", "DUPLICATE_PUBLIC_SYMBOL", "sample.py", "Symbol 'one' owned by multiple modules: ['a', 'b']")],
            )
            two = _collection(
                boundary.active_project_root,
                [_FakeIssue("error", "DUPLICATE_PUBLIC_SYMBOL", "sample.py", "Symbol 'two' owned by multiple modules: ['a', 'b']")],
            )
            run_one = build_architecture_diagnostic_run(
                one, boundary=boundary, attempt_id="one", source_fingerprint="source-v1", operation_generation=1
            )
            run_two = build_architecture_diagnostic_run(
                two, boundary=boundary, attempt_id="two", source_fingerprint="source-v1", operation_generation=1
            )
            self.assertNotEqual(
                issue_fingerprint(run_one.producer_id, run_one.findings[0]),
                issue_fingerprint(run_two.producer_id, run_two.findings[0]),
            )

    def test_duplicate_public_findings_are_deduplicated(self) -> None:
        with _boundary_fixture() as boundary:
            item = _FakeIssue("warning", "TEST_PROTECTION_GAP", "sample.py", "gap")
            result = _collection(boundary.active_project_root, [item, item])
            self.assertEqual(len(result.issues), 1)
            self.assertEqual(result.metadata["raw_issue_count"], 2)

    def test_collection_is_read_only(self) -> None:
        with _boundary_fixture() as boundary:
            path = boundary.active_project_root / "sample.py"
            before = path.read_bytes()
            _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "DEAD_CODE_UNREACHABLE_FILE", "sample.py", "dead")],
            )
            self.assertEqual(path.read_bytes(), before)

    def test_cancelled_collection_is_rejected_before_scan(self) -> None:
        with _boundary_fixture() as boundary:
            cancellation = Event()
            cancellation.set()
            with self.assertRaises(ArchitectureCollectionCancelled):
                collect_architecture_findings(
                    boundary.active_project_root,
                    cancellation=cancellation,
                    scanner=_scanner([]),
                    boundary_resolver=_boundary,
                    validation_source_path=Path(__file__),
                )

    def test_controller_commits_architecture_only_through_store(self) -> None:
        with _boundary_fixture() as boundary:
            collection = _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "TEST_PROTECTION_GAP", "sample.py", "gap")],
            )
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda _root: boundary,
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics_gui.controller.collect_architecture_findings",
                return_value=collection,
            ):
                candidate = controller.collect_architecture_candidate(
                    boundary.active_project_root,
                    1,
                    Event(),
                )
            record = controller.commit_candidate(
                boundary.active_project_root,
                candidate,
                current_generation=1,
            )
            self.assertEqual(record.producer_id, ARCHITECTURE_PRODUCER_ID)
            self.assertEqual(
                len(EngineeringDiagnosticsStore(boundary).list_findings(boundary, record.run_id)),
                1,
            )

    def test_architecture_rule_defaults_have_elevated_governance(self) -> None:
        error = architecture_rule_profile("DUPLICATE_PUBLIC_SYMBOL", "error")
        warning = architecture_rule_profile("TEST_PROTECTION_GAP", "warning")
        self.assertEqual(error.governance_impact, "high")
        self.assertEqual(warning.governance_impact, "medium_high")

    def test_project_level_issue_uses_safe_relative_anchor(self) -> None:
        with _boundary_fixture() as boundary:
            result = _collection(
                boundary.active_project_root,
                [_FakeIssue("warning", "DEAD_CODE_UNREACHABLE_FILE", ".", "suppressed")],
            )
            self.assertEqual(result.issues[0].relative_path, "ARCHITECTURE.md")

    def test_gui_source_declares_architecture_public_producer(self) -> None:
        root = Path(__file__).resolve().parents[1]
        tab = (
            root
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
            / "engineering_diagnostics_tab.py"
        ).read_text(encoding="utf-8")
        controller = (
            root
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
            / "controller.py"
        ).read_text(encoding="utf-8")
        self.assertIn("ARCHITECTURE_PRODUCER_ID", tab)
        self.assertIn("collect_architecture_candidate", controller)
        self.assertNotIn("manage_architecture_help", controller)


if __name__ == "__main__":
    unittest.main()
