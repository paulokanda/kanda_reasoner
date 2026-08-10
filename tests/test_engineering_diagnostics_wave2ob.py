# project-path: tests/test_engineering_diagnostics_wave2ob.py
"""Public-contract tests for Engineering Diagnostics GUI Wave 2O-B."""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Event
import unittest
from unittest.mock import patch
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import EngineeringDiagnosticsStore
from kanda_reasoner_app.engineering_diagnostics_gui import (
    EngineeringDiagnosticsController,
    EngineeringDiagnosticsGuiCancelled,
)
from kanda_reasoner_app.project_support_boundary import (
    ProjectSelectionMode,
    resolve_explicit_project_tool_boundary_identity,
)
from portable.models import BuildPaths
from portable.smoke_isolation import prepared_smoke_isolation


class _FixtureProvider:
    def __init__(self, payload: dict[str, object], *, cancel: bool = False) -> None:
        self.payload = payload
        self.cancel = cancel

    def collect(self, project_root: Path, cancellation: Event):
        if self.cancel:
            cancellation.set()
            raise EngineeringDiagnosticsGuiCancelled("cancelled")
        return dict(self.payload)


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
    """Yield one public token-bound fixture with canonical support storage."""
    with TemporaryDirectory() as temporary:
        base = Path(temporary)
        paths = _fixture_paths(base)
        with prepared_smoke_isolation(paths, "KandaReasoner") as isolation:
            isolation.app_root.mkdir(parents=True, exist_ok=True)
            with patch.dict("os.environ", isolation.environment, clear=True):
                boundary = resolve_explicit_project_tool_boundary_identity(
                    isolation.project_root,
                    selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
                    stable_project_id="fixture-project-id-" + uuid4().hex,
                    tool_source_root=isolation.app_root,
                )
                (isolation.project_root / "sample.py").write_text(
                    "print('ok')\n",
                    encoding="utf-8",
                )
                yield isolation.project_root, boundary


def _report(root: Path) -> dict[str, object]:
    return {
        "report_id": "fixture-report",
        "report_type": "bom_scan",
        "created_at": "2026-08-06T01:00:00+00:00",
        "project_root": str(root),
        "input_sources": ["project_root"],
        "summary": "One finding.",
        "findings": [
            {
                "code": "UTF8_BOM_DETECTED",
                "path": "sample.py",
                "line": 1,
                "severity": "warning",
                "confidence": "high",
                "message": "File starts with a UTF-8 BOM.",
                "evidence": {"bom_hex": "efbbbf"},
                "suggested_action": "Review before correction.",
            }
        ],
    }


class EngineeringDiagnosticsWave2OBTests(unittest.TestCase):
    """Protect GUI ownership, stale-result, and baseline boundaries."""

    def test_completed_candidate_persists_only_through_store_owner(self) -> None:
        with _boundary_fixture() as (root, boundary):
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root)),
                boundary_resolver=lambda _root: boundary,
            )
            candidate = controller.collect_bom_candidate(root, 1, Event())
            record = controller.commit_candidate(
                root,
                candidate,
                current_generation=1,
            )
            store = EngineeringDiagnosticsStore(boundary)
            self.assertEqual(len(store.list_runs(boundary)), 1)
            self.assertEqual(record.finding_count, 1)

    def test_stale_worker_generation_is_rejected_before_commit(self) -> None:
        with _boundary_fixture() as (root, boundary):
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root)),
                boundary_resolver=lambda _root: boundary,
            )
            candidate = controller.collect_bom_candidate(root, 3, Event())
            with self.assertRaisesRegex(RuntimeError, "STALE_WORKER_COMPLETION"):
                controller.commit_candidate(
                    root,
                    candidate,
                    current_generation=4,
                )
            self.assertEqual(
                EngineeringDiagnosticsStore(boundary).list_runs(boundary),
                (),
            )

    def test_selected_project_change_is_rejected_before_commit(self) -> None:
        with _boundary_fixture() as (root, boundary):
            other = root.parent / "other_project"
            other.mkdir()
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root)),
                boundary_resolver=lambda _root: boundary,
            )
            candidate = controller.collect_bom_candidate(root, 1, Event())
            with self.assertRaisesRegex(RuntimeError, "SELECTED_PROJECT_CHANGED"):
                controller.commit_candidate(other, candidate, current_generation=1)

    def test_cancelled_provider_creates_no_run(self) -> None:
        with _boundary_fixture() as (root, boundary):
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root), cancel=True),
                boundary_resolver=lambda _root: boundary,
            )
            with self.assertRaises(EngineeringDiagnosticsGuiCancelled):
                controller.collect_bom_candidate(root, 1, Event())
            self.assertEqual(
                EngineeringDiagnosticsStore(boundary).list_runs(boundary),
                (),
            )

    def test_explicit_baseline_activation_uses_public_store_contract(self) -> None:
        with _boundary_fixture() as (root, boundary):
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root)),
                boundary_resolver=lambda _root: boundary,
            )
            candidate = controller.collect_bom_candidate(root, 1, Event())
            run = controller.commit_candidate(root, candidate, current_generation=1)
            baseline = controller.activate_run_as_baseline(
                root,
                run.run_id,
                label="Approved fixture baseline",
            )
            self.assertEqual(baseline.state, "ACTIVE")
            view = controller.load_run_view(root, run.run_id)
            self.assertEqual(view.comparison.status, "COMPARED")

    def test_source_excerpt_is_read_only_and_project_contained(self) -> None:
        with _boundary_fixture() as (root, boundary):
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                report_provider=_FixtureProvider(_report(root)),
                boundary_resolver=lambda _root: boundary,
            )
            candidate = controller.collect_bom_candidate(root, 1, Event())
            run = controller.commit_candidate(root, candidate, current_generation=1)
            view = controller.load_run_view(root, run.run_id)
            excerpt = controller.source_excerpt(root, view.findings[0].record)
            self.assertIn("print('ok')", excerpt)

    def test_gui_box_uses_public_backend_and_no_sqlite(self) -> None:
        package = (
            Path(__file__).parents[1]
            / "kanda_reasoner_app"
            / "engineering_diagnostics_gui"
        )
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(package.glob("*.py"))
        )
        self.assertIn(
            "from kanda_reasoner_app.engineering_diagnostics import",
            source,
        )
        self.assertNotIn("engineering_diagnostics._store", source)
        self.assertNotIn("import sqlite3", source)
        self.assertNotIn("kanda_reasoner_app.source_hygiene", source)

    def test_audit_project_host_uses_public_gui_factory(self) -> None:
        root = Path(__file__).parents[1]
        helper = (
            root
            / "kanda_reasoner_app"
            / "manage_architecture"
            / "audit_project_sibling_tabs.py"
        )
        source = helper.read_text(encoding="utf-8")
        self.assertIn('"kanda_reasoner_app.engineering_diagnostics_gui"', source)
        self.assertIn('"create_engineering_diagnostics_panel"', source)
        self.assertNotIn("engineering_diagnostics_gui.", source)


if __name__ == "__main__":
    unittest.main()
