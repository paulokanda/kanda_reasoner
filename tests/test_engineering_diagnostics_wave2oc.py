# project-path: tests/test_engineering_diagnostics_wave2oc.py
"""Focused public-contract tests for Engineering Diagnostics Wave 2O-C."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from threading import Event
import time
import unittest
from unittest.mock import patch
from uuid import uuid4

from kanda_reasoner_app.engineering_diagnostics import (
    BOM_PRODUCER_ID,
    RUFF_PRODUCER_ID,
    DiagnosticFindingInput,
    DiagnosticRunInput,
    EngineeringDiagnosticsStore,
    RuffCollectionError,
    RuffCollectionResult,
    build_ruff_diagnostic_run,
    collect_ruff_json,
    issue_fingerprint,
    ruff_rule_profile,
    scan_identity,
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
            (isolation.project_root / "ruff.toml").write_text(
                'required-version = "==0.15.21"\n'
                'target-version = "py310"\n'
                "line-length = 88\n"
                "fix = false\n",
                encoding="utf-8",
            )
            with patch.dict("os.environ", isolation.environment, clear=True):
                boundary = resolve_explicit_project_tool_boundary_identity(
                    isolation.project_root,
                    selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
                    stable_project_id="wave2oc-" + uuid4().hex,
                    tool_source_root=isolation.app_root,
                )
                yield boundary


def _raw(
    root: Path,
    relative: str,
    *,
    code: str = "F821",
    message: str = "Undefined name `missing`",
    row: int = 2,
    column: int = 9,
    fix: object = None,
) -> dict[str, object]:
    return {
        "code": code,
        "message": message,
        "filename": str(root / relative),
        "location": {"row": row, "column": column},
        "end_location": {"row": row, "column": column + 7},
        "fix": fix,
    }


def _collection(
    root: Path,
    findings: list[dict[str, object]],
    *,
    version: str = "ruff 0.15.21",
) -> RuffCollectionResult:
    config = root / "ruff.toml"
    return RuffCollectionResult(
        project_root=str(root),
        ruff_version=version,
        command_source="fixture",
        config_relative_path="ruff.toml",
        config_sha256=hashlib.sha256(config.read_bytes()).hexdigest(),
        started_at_utc="2026-08-06T00:00:00+00:00",
        completed_at_utc="2026-08-06T00:00:01+00:00",
        raw_findings=tuple(findings),
        stdout_sha256="fixture-output",
    )


def _ruff_run(boundary, collection, attempt: str = "ruff-attempt"):
    return build_ruff_diagnostic_run(
        collection,
        boundary=boundary,
        attempt_id=attempt,
        source_fingerprint="source-v1",
        operation_generation=1,
    )


def _record(store, boundary, run):
    return store.record_completed_run(
        boundary,
        run,
        current_source_fingerprint=run.source_fingerprint,
        current_scope_fingerprint=run.scope_fingerprint,
        current_configuration_fingerprint=run.configuration_fingerprint,
        current_generation=run.operation_generation,
    )


def _fake_ruff(root: Path, payload: str, version: str = "ruff 0.15.21") -> Path:
    script = root / "fake_ruff.py"
    script.write_text(
        "import sys\n"
        + "if '--version' in sys.argv:\n"
        + "    print(" + repr(version) + ")\n"
        + "    raise SystemExit(0)\n"
        + "print(" + repr(payload) + ")\n",
        encoding="utf-8",
    )
    return script


class EngineeringDiagnosticsWave2OCTests(unittest.TestCase):
    def test_malformed_ruff_json_is_rejected(self) -> None:
        with _boundary_fixture() as boundary:
            script = _fake_ruff(boundary.active_project_root, "not-json")
            with self.assertRaises(RuffCollectionError):
                collect_ruff_json(
                    boundary.active_project_root,
                    argv_prefix=(sys.executable, str(script)),
                )

    def test_missing_ruff_executable_is_rejected(self) -> None:
        with _boundary_fixture() as boundary:
            missing = boundary.active_project_root / "missing-ruff.exe"
            with self.assertRaises(RuffCollectionError):
                collect_ruff_json(
                    boundary.active_project_root,
                    argv_prefix=(str(missing),),
                )

    def test_native_json_command_is_read_only(self) -> None:
        with _boundary_fixture() as boundary:
            log = boundary.active_project_root / "argv.json"
            script = boundary.active_project_root / "fake_ruff.py"
            script.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "if '--version' in sys.argv:\n"
                "    print('ruff 0.15.21')\n"
                "    raise SystemExit(0)\n"
                "Path(" + repr(str(log)) + ").write_text(json.dumps(sys.argv))\n"
                "print('[]')\n",
                encoding="utf-8",
            )
            collect_ruff_json(
                boundary.active_project_root,
                argv_prefix=(sys.executable, str(script)),
            )
            argv = json.loads(log.read_text(encoding="utf-8"))
            self.assertIn("--output-format", argv)
            self.assertIn("json", argv)
            self.assertIn("--no-fix", argv)
            self.assertNotIn("--fix", argv)

    def test_version_change_updates_scan_not_issue_identity(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            (root / "sample.py").write_text("def f():\n    return missing\n")
            raw = [_raw(root, "sample.py")]
            first = _ruff_run(boundary, _collection(root, raw, version="ruff 0.15.21"))
            second = _ruff_run(boundary, _collection(root, raw, version="ruff 0.16.0"))
            self.assertNotEqual(first.configuration_fingerprint, second.configuration_fingerprint)
            self.assertNotEqual(scan_identity(first), scan_identity(second))
            self.assertEqual(
                issue_fingerprint(first.producer_id, first.findings[0]),
                issue_fingerprint(second.producer_id, second.findings[0]),
            )

    def test_line_insertion_and_whitespace_preserve_identity(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            path = root / "sample.py"
            path.write_text("def f():\n    return missing\n")
            first = _ruff_run(boundary, _collection(root, [_raw(root, "sample.py")]))
            path.write_text("# inserted\n\ndef f():\n    return    missing\n")
            second = _ruff_run(
                boundary,
                _collection(root, [_raw(root, "sample.py", row=4)]),
            )
            self.assertEqual(
                issue_fingerprint(first.producer_id, first.findings[0]),
                issue_fingerprint(second.producer_id, second.findings[0]),
            )

    def test_function_rename_changes_identity(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            path = root / "sample.py"
            path.write_text("def alpha():\n    return missing\n")
            first = _ruff_run(boundary, _collection(root, [_raw(root, "sample.py")]))
            path.write_text("def beta():\n    return missing\n")
            second = _ruff_run(boundary, _collection(root, [_raw(root, "sample.py")]))
            self.assertNotEqual(
                issue_fingerprint(first.producer_id, first.findings[0]),
                issue_fingerprint(second.producer_id, second.findings[0]),
            )

    def test_file_rename_changes_identity(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            (root / "first.py").write_text("def f():\n    return missing\n")
            first = _ruff_run(boundary, _collection(root, [_raw(root, "first.py")]))
            (root / "second.py").write_text("def f():\n    return missing\n")
            second = _ruff_run(boundary, _collection(root, [_raw(root, "second.py")]))
            self.assertNotEqual(
                issue_fingerprint(first.producer_id, first.findings[0]),
                issue_fingerprint(second.producer_id, second.findings[0]),
            )

    def test_duplicate_findings_are_deduplicated(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            (root / "sample.py").write_text("def f():\n    return missing\n")
            item = _raw(root, "sample.py")
            run = _ruff_run(boundary, _collection(root, [item, dict(item)]))
            self.assertEqual(len(run.findings), 1)
            self.assertEqual(run.provenance["duplicate_raw_findings_dropped"], 1)

    def test_safe_and_unsafe_fix_metadata_is_preserved(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            (root / "sample.py").write_text("x = missing\ny = missing\n")
            safe = {
                "applicability": "safe",
                "message": "Add import",
                "edits": [{"content": "from x import missing"}],
            }
            unsafe = {
                "applicability": "unsafe",
                "message": "Rewrite expression",
                "edits": [{"content": "0"}],
            }
            run = _ruff_run(
                boundary,
                _collection(
                    root,
                    [
                        _raw(root, "sample.py", row=1, fix=safe),
                        _raw(root, "sample.py", row=2, fix=unsafe),
                    ],
                ),
            )
            applicability = {
                item.evidence["fix_applicability"] for item in run.findings
            }
            self.assertEqual(applicability, {"safe", "unsafe"})
            self.assertTrue(all(not item.evidence["fix_executed"] for item in run.findings))

    def test_priority_defaults_are_deterministic(self) -> None:
        self.assertEqual(ruff_rule_profile("F821").priority, "high")
        self.assertEqual(ruff_rule_profile("F401").priority, "medium_low")
        self.assertEqual(ruff_rule_profile("E501").severity, "info")

    def test_high_volume_persistence_and_baseline_diff_are_stable(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            payload = [
                _raw(root, f"src/file_{index:05d}.py", row=1)
                for index in range(25000)
            ]
            first_run = _ruff_run(boundary, _collection(root, payload), "ruff-high-1")
            store = EngineeringDiagnosticsStore(boundary)
            started = time.perf_counter()
            first = _record(store, boundary, first_run)
            elapsed = time.perf_counter() - started
            self.assertEqual(first.finding_count, 25000)
            self.assertLess(elapsed, 20.0)
            draft = store.create_draft_baseline(boundary, first.run_id, label="Ruff")
            store.activate_baseline(
                boundary,
                draft.baseline_id,
                expected_generation=draft.generation,
            )
            second = _record(
                store,
                boundary,
                _ruff_run(boundary, _collection(root, payload), "ruff-high-2"),
            )
            comparison = store.compare_run_to_active_baseline(boundary, second.run_id)
            self.assertEqual(len(comparison.persistent_issue_fingerprints), 25000)
            self.assertEqual(comparison.new_issue_fingerprints, ())
            self.assertEqual(comparison.resolved_issue_fingerprints, ())
            fingerprints = {
                item.issue_fingerprint for item in store.list_findings(boundary, second.run_id)
            }
            self.assertEqual(len(fingerprints), 25000)
            self.assertEqual(second.producer_version, "ruff 0.15.21")

    def test_ruff_failure_does_not_erase_bom_history(self) -> None:
        with _boundary_fixture() as boundary:
            store = EngineeringDiagnosticsStore(boundary)
            bom = DiagnosticRunInput(
                attempt_id="bom-existing",
                project_id=boundary.active_project_id,
                project_root_fingerprint=boundary.active_project_root_fingerprint,
                producer_id=BOM_PRODUCER_ID,
                producer_version="1.0",
                source_fingerprint="source-v1",
                scope_fingerprint="bom-scope",
                configuration_fingerprint="bom-config",
                operation_generation=1,
                findings=(
                    DiagnosticFindingInput(
                        code="UTF8_BOM_DETECTED",
                        relative_path="sample.py",
                        message="BOM found",
                    ),
                ),
            )
            _record(store, boundary, bom)
            missing = boundary.active_project_root / "missing-ruff.exe"
            with self.assertRaises(RuffCollectionError):
                collect_ruff_json(
                    boundary.active_project_root,
                    argv_prefix=(str(missing),),
                )
            self.assertEqual(
                len(store.list_runs(boundary, producer_id=BOM_PRODUCER_ID)),
                1,
            )
            self.assertEqual(
                store.list_runs(boundary, producer_id=RUFF_PRODUCER_ID),
                (),
            )

    def test_gui_controller_collects_and_commits_ruff_publicly(self) -> None:
        with _boundary_fixture() as boundary:
            root = boundary.active_project_root
            (root / "sample.py").write_text("def f():\n    return missing\n")
            payload = json.dumps([_raw(root, "sample.py")])
            script = _fake_ruff(root, payload)
            controller = EngineeringDiagnosticsController(
                tool_root=boundary.tool_source_root,
                boundary_resolver=lambda _root: boundary,
                ruff_argv_prefix=(sys.executable, str(script)),
            )
            candidate = controller.collect_ruff_candidate(root, 1, Event())
            record = controller.commit_candidate(root, candidate, current_generation=1)
            self.assertEqual(record.producer_id, RUFF_PRODUCER_ID)
            self.assertEqual(record.finding_count, 1)
            self.assertEqual(
                len(controller.list_runs(root, producer_id=RUFF_PRODUCER_ID)),
                1,
            )


if __name__ == "__main__":
    unittest.main()
