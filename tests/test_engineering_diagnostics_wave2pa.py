# project-path: tests/test_engineering_diagnostics_wave2pa.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2P-A."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import unittest
from unittest.mock import patch
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import (
    DiagnosticFindingInput,
    DiagnosticFindingRecord,
    DiagnosticRunInput,
    EngineeringDiagnosticsEnricher,
    EngineeringDiagnosticsStore,
    SCOPE_CLASSIFICATIONS,
    build_diagnostic_freeze_snapshot,
    classify_diagnostic_frozen_path,
    issue_fingerprint,
)
from kanda_reasoner_app.engineering_diagnostics.scope_enrichment import (
    build_diagnostic_scope_policy,
    classify_diagnostic_scope,
)
from kanda_reasoner_app.engineering_diagnostics_gui import (
    EngineeringDiagnosticsController,
)
from kanda_reasoner_app.freeze_after_update import (
    FreezeAfterUpdateResult,
    FreezeAfterUpdateStatus,
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
    with TemporaryDirectory() as temporary:
        base = Path(temporary)
        with prepared_smoke_isolation(
            _fixture_paths(base),
            "KandaReasoner",
        ) as isolation:
            isolation.app_root.mkdir(parents=True, exist_ok=True)
            isolation.project_root.mkdir(parents=True, exist_ok=True)
            with patch.dict("os.environ", isolation.environment, clear=True):
                boundary = resolve_explicit_project_tool_boundary_identity(
                    isolation.project_root,
                    selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
                    stable_project_id="wave2pa-" + uuid4().hex,
                    tool_source_root=isolation.app_root,
                )
                yield isolation, boundary


def _finding(
    relative_path: str,
    *,
    evidence: dict[str, object] | None = None,
) -> DiagnosticFindingRecord:
    return DiagnosticFindingRecord(
        run_id="run",
        issue_fingerprint="issue-" + hashlib.sha256(
            relative_path.encode("utf-8")
        ).hexdigest(),
        evidence_digest="evidence",
        code="TEST_RULE",
        relative_path=relative_path,
        message="Fixture finding.",
        severity="warning",
        confidence="high",
        semantic_key="fixture",
        symbol_id="",
        location_key="",
        category="fixture",
        line=1,
        evidence=evidence or {},
        suggested_action="Review evidence.",
    )


def _freeze_box(
    root: Path,
    freezes: list[dict[str, object]],
) -> FreezeAfterUpdateResult:
    box = root / "project_freeze_after_update"
    index = box / "frozen_features_memory" / "freeze_index.json"
    index.parent.mkdir(parents=True)
    index.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_by": "fixture",
                "freezes": freezes,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return FreezeAfterUpdateResult(
        status=FreezeAfterUpdateStatus.VALID,
        project_root=root,
        box_root=box,
        freeze_count=len(freezes),
    )


def _record_run(store, boundary, relative_path: str):
    finding = DiagnosticFindingInput(
        code="TEST_RULE",
        relative_path=relative_path,
        message="Fixture finding.",
        severity="warning",
        confidence="high",
        semantic_key="fixture",
        category="fixture",
        line=1,
    )
    run = DiagnosticRunInput(
        attempt_id="attempt-" + uuid4().hex,
        project_id=boundary.active_project_id,
        project_root_fingerprint=boundary.active_project_root_fingerprint,
        producer_id="fixture.scope",
        producer_version="1.0",
        source_fingerprint="source-v1",
        scope_fingerprint="scope-v1",
        configuration_fingerprint="config-v1",
        operation_generation=1,
        findings=(finding,),
    )
    return store.record_completed_run(
        boundary,
        run,
        current_source_fingerprint="source-v1",
        current_scope_fingerprint="scope-v1",
        current_configuration_fingerprint="config-v1",
        current_generation=1,
    )


class EngineeringDiagnosticsWave2PATests(unittest.TestCase):
    def test_scope_classifications_cover_declared_taxonomy(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            paths = {
                "src/app.py": "ACTIVE",
                "tests/test_app.py": "TEST",
                "fixtures/sample.py": "FIXTURE",
                "prototypes/demo.py": "PROTOTYPE",
                "generated/model.py": "GENERATED",
                ".project_reference/old.py": "REFERENCE",
                "legacy_deprecated/old.py": "DEPRECATED",
                "workbench/try.py": "WORKBENCH",
                "snippets/example.py": "SNIPPET",
                "temp/scratch.py": "TEMPORARY",
            }
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("value = 1\n", encoding="utf-8")
            policy = build_diagnostic_scope_policy(root)
            observed = {
                relative: classify_diagnostic_scope(
                    policy,
                    relative,
                ).classification
                for relative in paths
            }
            self.assertEqual(observed, paths)
            self.assertTrue(set(observed.values()).issubset(SCOPE_CLASSIFICATIONS))

    def test_explicit_scope_marker_has_highest_precedence(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "tests" / "generated_test.py"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# kanda:scope=active\nvalue = 1\n",
                encoding="utf-8",
            )
            result = classify_diagnostic_scope(
                build_diagnostic_scope_policy(root),
                "tests/generated_test.py",
            )
            self.assertEqual(result.classification, "ACTIVE")
            self.assertEqual(result.method, "explicit_scope_marker")
            self.assertEqual(result.confidence, "high")

    def test_excluded_unclassified_path_fails_to_unknown(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "notes.log"
            path.write_text("log\n", encoding="utf-8")
            result = classify_diagnostic_scope(
                build_diagnostic_scope_policy(root),
                "notes.log",
            )
            self.assertEqual(result.classification, "UNKNOWN")
            self.assertEqual(result.method, "project_exclusion_policy")

    def test_active_and_historical_freeze_paths_are_distinguished(self) -> None:
        with TemporaryDirectory() as temporary:
            support = Path(temporary)
            result = _freeze_box(
                support,
                [
                    {
                        "freeze_id": "freeze-active",
                        "status": "frozen",
                        "superseded_by": None,
                        "protected_paths": ["src/active_box"],
                    },
                    {
                        "freeze_id": "freeze-old",
                        "status": "frozen",
                        "superseded_by": "freeze-new",
                        "protected_paths": ["src/historical.py"],
                    },
                ],
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=result,
            ):
                snapshot = build_diagnostic_freeze_snapshot(support)
            active = classify_diagnostic_frozen_path(
                snapshot,
                "src/active_box/module.py",
            )
            historical = classify_diagnostic_frozen_path(
                snapshot,
                "src/historical.py",
            )
            self.assertEqual(active.status, "FROZEN")
            self.assertEqual(active.governing_freeze_ids, ("freeze-active",))
            self.assertEqual(historical.status, "HISTORICAL_FROZEN")
            self.assertEqual(historical.governing_freeze_ids, ("freeze-old",))

    def test_related_evidence_can_touch_frozen_path(self) -> None:
        with TemporaryDirectory() as temporary:
            support = Path(temporary)
            result = _freeze_box(
                support,
                [
                    {
                        "freeze_id": "freeze-owner",
                        "status": "frozen",
                        "superseded_by": None,
                        "protected_paths": ["owners/canonical.py"],
                    }
                ],
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=result,
            ):
                enricher = EngineeringDiagnosticsEnricher(support)
            enriched = enricher.enrich(
                _finding(
                    "src/caller.py",
                    evidence={"owner_path": "owners/canonical.py"},
                )
            )
            self.assertEqual(enriched.frozen_path.status, "TOUCHES_FROZEN")
            self.assertEqual(
                enriched.frozen_path.governing_freeze_ids,
                ("freeze-owner",),
            )

    def test_missing_freeze_index_fails_closed_without_writing(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            box = root / "project_freeze_after_update"
            box.mkdir()
            result = FreezeAfterUpdateResult(
                status=FreezeAfterUpdateStatus.VALID,
                project_root=root,
                box_root=box,
            )
            before = tuple(sorted(path.as_posix() for path in root.rglob("*")))
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=result,
            ):
                snapshot = build_diagnostic_freeze_snapshot(root)
            after = tuple(sorted(path.as_posix() for path in root.rglob("*")))
            self.assertEqual(snapshot.state, "UNKNOWN")
            self.assertEqual(before, after)

    def test_enrichment_does_not_change_finding_identity(self) -> None:
        finding = DiagnosticFindingInput(
            code="F821",
            relative_path="src/app.py",
            message="Undefined name.",
            semantic_key="F821|Undefined name.",
        )
        before = issue_fingerprint("ruff.check", finding)
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            (root / "src" / "app.py").write_text("value = missing\n")
            result = _freeze_box(root / "support", [])
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=result,
            ):
                EngineeringDiagnosticsEnricher(root).enrich(
                    _finding("src/app.py")
                )
        after = issue_fingerprint("ruff.check", finding)
        self.assertEqual(before, after)

    def test_controller_loads_scope_and_freeze_context_read_only(self) -> None:
        with _boundary_fixture() as (isolation, boundary):
            root = isolation.project_root
            path = root / "src" / "frozen.py"
            path.parent.mkdir(parents=True)
            path.write_text("value = 1\n", encoding="utf-8")
            freeze_result = _freeze_box(
                isolation.project_support_root,
                [
                    {
                        "freeze_id": "freeze-fixture",
                        "status": "frozen",
                        "superseded_by": None,
                        "protected_paths": ["src/frozen.py"],
                    }
                ],
            )
            store = EngineeringDiagnosticsStore(boundary)
            run = _record_run(store, boundary, "src/frozen.py")
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda _root: boundary,
            )
            index = (
                freeze_result.box_root
                / "frozen_features_memory"
                / "freeze_index.json"
            )
            before = index.read_bytes()
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=freeze_result,
            ):
                view = controller.load_run_view(root, run.run_id)
            self.assertEqual(view.findings[0].scope_classification, "ACTIVE")
            self.assertEqual(view.findings[0].frozen_status, "FROZEN")
            self.assertEqual(before, index.read_bytes())

    def test_batch_enrichment_handles_25000_rows_without_persistence(self) -> None:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "src").mkdir()
            freeze_result = _freeze_box(root / "support", [])
            findings = tuple(
                _finding("src/file_" + str(index).zfill(5) + ".py")
                for index in range(25000)
            )
            with patch(
                "kanda_reasoner_app.engineering_diagnostics."
                "frozen_path_enrichment.inspect_freeze_after_update_box",
                return_value=freeze_result,
            ):
                enricher = EngineeringDiagnosticsEnricher(root)
                started = time.perf_counter()
                enriched = enricher.enrich_many(findings)
                elapsed = time.perf_counter() - started
            self.assertEqual(len(enriched), 25000)
            self.assertTrue(all(item.scope.classification == "ACTIVE" for item in enriched))
            self.assertLess(elapsed, 5.0)

    def test_gui_uses_public_enrichment_and_no_freeze_private_imports(self) -> None:
        root = Path(__file__).parents[1]
        gui = root / "kanda_reasoner_app" / "engineering_diagnostics_gui"
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(gui.glob("*.py"))
        )
        self.assertIn("scope_classification", source)
        self.assertIn("frozen_status", source)
        self.assertNotIn("freeze_after_update.freeze_state", source)
        self.assertNotIn("freeze_after_update.paths", source)
        self.assertNotIn("import sqlite3", source)


if __name__ == "__main__":
    unittest.main()
