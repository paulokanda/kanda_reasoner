# project-path: tests/test_engineering_diagnostics_wave2oa.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2O-A."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import replace
import gc
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from uuid import uuid4
import warnings

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    DiagnosticBoundaryError,
    DiagnosticConflictError,
    DiagnosticFindingInput,
    DiagnosticRunInput,
    EngineeringDiagnosticsStore,
    build_bom_diagnostic_run,
    engineering_diagnostics_database_path,
    issue_fingerprint,
    normalize_relative_path,
    scan_identity,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    resolve_explicit_project_tool_boundary_identity,
)
from portable.models import BuildPaths
from portable.smoke_isolation import prepared_smoke_isolation


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
    """Yield one token-bound Project with fully isolated support state."""
    with TemporaryDirectory() as temporary:
        base = Path(temporary)
        paths = _fixture_paths(base)
        with prepared_smoke_isolation(paths, "KandaReasoner") as isolation:
            isolation.app_root.mkdir(parents=True, exist_ok=True)
            with patch.dict("os.environ", isolation.environment, clear=True):
                token = uuid4().hex
                boundary = resolve_explicit_project_tool_boundary_identity(
                    isolation.project_root,
                    selection_mode=(
                        ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT
                    ),
                    stable_project_id="project-stable-id-" + token,
                    tool_source_root=isolation.app_root,
                )
                yield boundary


def _finding(path: str = "src/example.py", message: str = "BOM found"):
    return DiagnosticFindingInput(
        code="UTF8_BOM_DETECTED",
        relative_path=path,
        message=message,
        severity="warning",
        confidence="high",
        semantic_key="UTF8_BOM_DETECTED",
        category="source_hygiene_bom",
        evidence={"bom_hex": "efbbbf"},
    )


def _run(boundary, attempt_id: str, findings=()):
    return DiagnosticRunInput(
        attempt_id=attempt_id,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id=BOM_PRODUCER_ID,
        producer_version="1.0",
        source_fingerprint="source-v1",
        scope_fingerprint="scope-v1",
        configuration_fingerprint="config-v1",
        operation_generation=1,
        findings=tuple(findings),
        completion_status="COMPLETED",
        started_at_utc="2026-08-05T20:00:00+00:00",
        completed_at_utc="2026-08-05T20:01:00+00:00",
        provenance={"fixture": "wave2oa"},
    )


def _record(store, boundary, run):
    return store.record_completed_run(
        boundary,
        run,
        current_source_fingerprint="source-v1",
        current_scope_fingerprint="scope-v1",
        current_configuration_fingerprint="config-v1",
        current_generation=1,
    )


class EngineeringDiagnosticsWave2OATests(unittest.TestCase):
    """Protect persistence, identity, baseline, and BOM boundaries."""

    def test_database_is_external_project_support_state(self) -> None:
        with _boundary_fixture() as boundary:
            path = engineering_diagnostics_database_path(boundary)
            self.assertEqual(
                path.parent.name,
                "project_engineering_diagnostics",
            )
            with self.assertRaises(ValueError):
                path.relative_to(boundary.active_project_root)

    def test_canonical_support_state_isolated_per_project_fixture(self) -> None:
        with _boundary_fixture() as first_boundary:
            first_support = first_boundary.active_project_support_root
            first_store = EngineeringDiagnosticsStore(first_boundary)
            _record(
                first_store,
                first_boundary,
                _run(first_boundary, "attempt-1", (_finding(),)),
            )
            self.assertEqual(len(first_store.list_runs(first_boundary)), 1)
        with _boundary_fixture() as second_boundary:
            second_support = second_boundary.active_project_support_root
            second_store = EngineeringDiagnosticsStore(second_boundary)
            self.assertNotEqual(first_support, second_support)
            self.assertEqual(second_store.list_runs(second_boundary), ())

    def test_issue_and_scan_identity_are_deterministic(self) -> None:
        with _boundary_fixture() as boundary:
            first = _finding(path="src\\example.py", message="first wording")
            second = _finding(path="src/example.py", message="second wording")
            self.assertEqual(
                issue_fingerprint(BOM_PRODUCER_ID, first),
                issue_fingerprint(BOM_PRODUCER_ID, second),
            )
            run = _run(boundary, "attempt-1", (first,))
            self.assertEqual(scan_identity(run), scan_identity(replace(run)))
            changed = replace(run, source_fingerprint="source-v2")
            self.assertNotEqual(scan_identity(run), scan_identity(changed))

    def test_absolute_and_parent_paths_fail_closed(self) -> None:
        with self.assertRaises(Exception):
            normalize_relative_path("C:\\secret\\file.py")
        with self.assertRaises(Exception):
            normalize_relative_path("../outside.py")

    def test_completed_run_is_atomic_and_idempotent(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = _run(boundary, "attempt-1", (_finding(),))
            first = _record(store, boundary, run)
            second = _record(store, boundary, run)
            self.assertEqual(first.run_id, second.run_id)
            self.assertEqual(first.content_digest, second.content_digest)
            self.assertEqual(len(store.list_runs(boundary)), 1)
            self.assertEqual(len(store.list_findings(boundary, first.run_id)), 1)

    def test_conflicting_attempt_id_is_rejected_without_partial_write(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            _record(store, boundary, _run(boundary, "attempt-1", (_finding(),)))
            conflicting = _run(
                boundary,
                "attempt-1",
                (_finding(path="src/other.py"),),
            )
            with self.assertRaises(DiagnosticConflictError):
                _record(store, boundary, conflicting)
            self.assertEqual(len(store.list_runs(boundary)), 1)

    def test_stale_source_scope_configuration_and_generation_are_rejected(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = _run(boundary, "attempt-1", (_finding(),))
            cases = (
                {"current_source_fingerprint": "source-v2"},
                {"current_scope_fingerprint": "scope-v2"},
                {"current_configuration_fingerprint": "config-v2"},
                {"current_generation": 2},
            )
            defaults = {
                "current_source_fingerprint": "source-v1",
                "current_scope_fingerprint": "scope-v1",
                "current_configuration_fingerprint": "config-v1",
                "current_generation": 1,
            }
            for changed in cases:
                arguments = dict(defaults)
                arguments.update(changed)
                with self.assertRaises(DiagnosticBoundaryError):
                    store.record_completed_run(boundary, run, **arguments)
            self.assertEqual(store.list_runs(boundary), ())

    def test_project_identity_change_is_rejected(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            other = replace(
                boundary,
                active_project_id="other-project-id",
            )
            with self.assertRaises(DiagnosticBoundaryError):
                store.list_runs(other)

    def test_baseline_activation_requires_compare_and_swap_generation(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            run = _record(
                store,
                boundary,
                _run(boundary, "attempt-1", (_finding(),)),
            )
            draft = store.create_draft_baseline(
                boundary,
                run.run_id,
                label="Initial BOM baseline",
            )
            with self.assertRaises(DiagnosticConflictError):
                store.activate_baseline(
                    boundary,
                    draft.baseline_id,
                    expected_generation=1,
                )
            active = store.activate_baseline(
                boundary,
                draft.baseline_id,
                expected_generation=0,
            )
            self.assertEqual(active.state, "ACTIVE")
            self.assertEqual(active.generation, 1)

    def test_baseline_comparison_reports_new_persistent_and_resolved(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            first_run = _record(
                store,
                boundary,
                _run(
                    boundary,
                    "attempt-1",
                    (_finding("a.py"), _finding("b.py")),
                ),
            )
            draft = store.create_draft_baseline(
                boundary,
                first_run.run_id,
                label="BOM baseline",
            )
            store.activate_baseline(
                boundary,
                draft.baseline_id,
                expected_generation=0,
            )
            second_run = _record(
                store,
                boundary,
                _run(
                    boundary,
                    "attempt-2",
                    (_finding("b.py"), _finding("c.py")),
                ),
            )
            comparison = store.compare_run_to_active_baseline(
                boundary,
                second_run.run_id,
            )
            self.assertEqual(comparison.status, "COMPARED")
            self.assertEqual(len(comparison.new_issue_fingerprints), 1)
            self.assertEqual(len(comparison.persistent_issue_fingerprints), 1)
            self.assertEqual(len(comparison.resolved_issue_fingerprints), 1)

    def test_bom_adapter_consumes_public_data_without_scanning_source(self) -> None:
        with _boundary_fixture() as boundary:
            payload = {
                "report_id": "bom_scan_fixture",
                "report_type": "bom_scan",
                "created_at": "2026-08-05T20:00:00+00:00",
                "project_root": str(boundary.active_project_root),
                "input_sources": ["project_root"],
                "summary": "One finding.",
                "findings": [
                    {
                        "code": "UTF8_BOM_DETECTED",
                        "path": "src/example.py",
                        "line": None,
                        "severity": "warning",
                        "confidence": "high",
                        "message": "File starts with a UTF-8 byte order mark.",
                        "evidence": {"bom_hex": "efbbbf"},
                        "suggested_action": "Review before correction.",
                    }
                ],
            }
            run = build_bom_diagnostic_run(
                payload,
                boundary=boundary,
                attempt_id="attempt-bom",
                source_fingerprint="source-v1",
                scope_fingerprint="scope-v1",
                configuration_fingerprint="config-v1",
                operation_generation=1,
            )
            self.assertEqual(run.producer_id, BOM_PRODUCER_ID)
            self.assertEqual(len(run.findings), 1)

    def test_bom_adapter_rejects_another_project(self) -> None:
        with _boundary_fixture() as boundary:
            payload = {
                "report_type": "bom_scan",
                "project_root": str(
                    boundary.active_project_root.parent / "wrong_project"
                ),
                "findings": [],
            }
            with self.assertRaises(Exception):
                build_bom_diagnostic_run(
                    payload,
                    boundary=boundary,
                    attempt_id="attempt-bom",
                    source_fingerprint="source-v1",
                    scope_fingerprint="scope-v1",
                    configuration_fingerprint="config-v1",
                    operation_generation=1,
                )

    def test_sqlite_connections_close_without_resource_warnings(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("error", ResourceWarning)
            with _boundary_fixture() as boundary:
                store = EngineeringDiagnosticsStore(boundary)
                record = _record(
                    store,
                    boundary,
                    _run(boundary, "attempt-1", (_finding(),)),
                )
                store.list_findings(boundary, record.run_id)
                store.list_runs(boundary)
                del store
                gc.collect()


if __name__ == "__main__":
    unittest.main()
