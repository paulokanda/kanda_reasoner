"""Behavior tests for Workbench stage, state, and correction boundaries."""
from __future__ import annotations

import hashlib
import sys
import types
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest import mock

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


def _install_qt_stubs_if_needed() -> None:
    """Install inert import-only Qt stubs when PySide6 is unavailable."""
    try:
        __import__("PySide6")
        return
    except ModuleNotFoundError:
        pass

    class _QtStubMeta(type):
        def __getattr__(cls, _name: str):
            return cls

        def __or__(cls, _other: object):
            return cls

    class _QtStub(metaclass=_QtStubMeta):
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            pass

        def __getattr__(self, _name: str):
            return type(self)

        def __call__(self, *_args: object, **_kwargs: object):
            return type(self)()

        def __or__(self, _other: object):
            return self

        def __bool__(self) -> bool:
            return False

    package = types.ModuleType("PySide6")
    package.__path__ = []
    sys.modules["PySide6"] = package
    for suffix in ("QtCore", "QtGui", "QtWidgets"):
        module = types.ModuleType("PySide6." + suffix)
        module.__getattr__ = lambda _name, stub=_QtStub: stub
        sys.modules[module.__name__] = module
        setattr(package, suffix, module)


_install_qt_stubs_if_needed()

import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_stage_adapters as stage_adapters
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.main_workbench_state_store as state_store
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.planner_bounded_refinement as bounded_refinement
import kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_stage_correction_service as correction_service
from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.models import (
    DocstringProposal,
)


class _TextOutput:
    def __init__(self) -> None:
        self.text = ""

    def setPlainText(self, value: str) -> None:
        self.text = value


class WorkbenchStageAndStateBoundaryTests(unittest.TestCase):
    """Verify state mutations are evidence-driven and persistence is integrity-checked."""

    def test_stage_adapters_project_only_result_backed_states(self) -> None:
        window = SimpleNamespace(
            _large_file_refactor_workbench_dependency_output=_TextOutput(),
            _large_file_refactor_workbench_real_preview_output=_TextOutput(),
            _large_file_refactor_workbench_validation_output=_TextOutput(),
            _large_file_refactor_workbench_preflight_output=_TextOutput(),
        )
        synced: list[object] = []

        with (
            mock.patch.object(
                stage_adapters,
                "format_workbench_dependency_readiness",
                return_value="dependency-ready",
            ),
            mock.patch.object(
                stage_adapters,
                "format_real_preview_result",
                return_value="preview-ready",
            ),
            mock.patch.object(
                stage_adapters,
                "preview_validation_guidance",
                return_value="validate-preview",
            ),
            mock.patch.object(
                stage_adapters,
                "format_real_preview_structural_validation",
                return_value="structural-pass",
            ),
            mock.patch.object(
                stage_adapters,
                "format_preflight_gate_reason",
                return_value="preflight-open",
            ),
        ):
            dependency = SimpleNamespace(
                ready_for_real_preview_writer=True,
                status="ready",
            )
            stage_adapters.apply_dependency_stage_result(
                window,
                dependency,
                synced.append,
            )
            self.assertEqual(
                window._large_file_refactor_workbench_state,
                "DEPENDENCY_READY",
            )

            preview = SimpleNamespace(status="real_preview_written")
            stage_adapters.apply_preview_stage_result(
                window,
                preview,
                synced.append,
            )
            self.assertEqual(
                window._large_file_refactor_workbench_state,
                "REAL_PREVIEW_READY",
            )

            structural = SimpleNamespace(status="passed_full")
            stage_adapters.apply_structural_stage_result(
                window,
                structural,
                synced.append,
            )
            self.assertEqual(
                window._large_file_refactor_workbench_state,
                "STRUCTURAL_PREVIEW_VALIDATED",
            )

        self.assertEqual(len(synced), 3)
        self.assertEqual(
            window._large_file_refactor_workbench_validation_output.text,
            "structural-pass",
        )

    def test_terminal_seal_round_trip_detects_source_drift(self) -> None:
        with TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "project"
            support_root = Path(temp_dir) / "support"
            project_root.mkdir()
            target = project_root / "module.py"
            target.write_text("VALUE = 1\n", encoding="utf-8")
            source_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            snapshot = SimpleNamespace(
                target_file=str(target),
                source_content_hash=source_hash,
                snapshot_hash="snapshot-hash",
            )
            preview = SimpleNamespace(
                files=(
                    SimpleNamespace(
                        relative_path="module.py",
                        content_hash="preview-hash",
                    ),
                )
            )
            window = SimpleNamespace(
                _large_file_refactor_workbench_plan_snapshot=snapshot,
                _large_file_refactor_workbench_real_preview=preview,
                _large_file_refactor_workbench_structural_validation={"ok": True},
                _large_file_refactor_workbench_advanced_quality_review={"ok": True},
            )

            with mock.patch.object(
                state_store,
                "workbench_support_root",
                return_value=support_root,
            ):
                seal = state_store.build_main_workbench_terminal_seal(
                    window,
                    active_project_root=str(project_root),
                    generation=3,
                    terminal_status="READY",
                    blockers=(),
                )
                path = state_store.write_main_workbench_terminal_seal(seal)
                self.assertTrue(path.is_file())
                loaded = state_store.load_main_workbench_terminal_seal(project_root)
                self.assertEqual(loaded, seal)
                self.assertTrue(
                    state_store.terminal_seal_matches_evidence(
                        seal=loaded,
                        active_project_root=project_root,
                        snapshot=snapshot,
                        preview=preview,
                        structural={"ok": True},
                        aqr={"ok": True},
                    )
                )

                target.write_text("VALUE = 2\n", encoding="utf-8")
                self.assertFalse(
                    state_store.terminal_seal_matches_evidence(
                        seal=loaded,
                        active_project_root=project_root,
                        snapshot=snapshot,
                        preview=preview,
                        structural={"ok": True},
                        aqr={"ok": True},
                    )
                )

    def test_bounded_docstring_updates_reject_unknown_targets(self) -> None:
        proposal = DocstringProposal(
            schema_version="1.0",
            feature_id="test",
            target_file="module.py",
            target_kind="function",
            target_name="run",
            proposed_docstring='"""Original."""',
            provenance="heuristic",
            confidence="low",
            reason="Missing docstring.",
        )
        updated = bounded_refinement.apply_bounded_docstring_updates(
            [proposal],
            [
                {
                    "target_kind": "function",
                    "target_name": "run",
                    "proposed_docstring": '"""Run the bounded operation."""',
                }
            ],
            provenance="local_ai",
        )
        self.assertEqual(updated[0].provenance, "local_ai")
        self.assertEqual(updated[0].confidence, "medium")
        self.assertIn("Run the bounded operation", updated[0].proposed_docstring)

        with self.assertRaisesRegex(ValueError, "not in the deterministic proposal set"):
            bounded_refinement.apply_bounded_docstring_updates(
                [proposal],
                [
                    {
                        "target_kind": "function",
                        "target_name": "unknown",
                        "proposed_docstring": '"""Not allowed."""',
                    }
                ],
                provenance="local_ai",
            )

    def test_heuristic_correction_applies_only_passing_replay(self) -> None:
        window = SimpleNamespace()
        context = SimpleNamespace(
            stage="REAL_PREVIEW",
            active_project_root="C:\\fixture",
        )
        replay = SimpleNamespace(
            passed=True,
            reached_stage="REAL_PREVIEW",
            dependency_readiness="dependency",
            real_preview="preview",
            structural_validation=None,
            preflight_backup=None,
            source_payload=None,
            completion_evidence=None,
        )
        candidate = correction_service.HeuristicWorkbenchCorrectionCandidate(
            ok=True,
            message="candidate-ready",
            report="report",
            corrected_plan="corrected-plan",
            proposals=("proposal",),
            replay=replay,
            strategy="bounded",
            settings_label="safe",
        )
        intake = SimpleNamespace(ready_for_real_preview=True)

        with (
            mock.patch.object(correction_service, "store_heuristic_version") as store,
            mock.patch.object(correction_service, "select_planner_version") as select,
            mock.patch.object(
                correction_service,
                "load_latest_snapshot_into_workbench",
                return_value=(intake, "loaded"),
            ),
        ):
            result = correction_service.apply_heuristic_workbench_correction(
                window,
                context,
                candidate,
            )

        self.assertTrue(result.ok)
        self.assertEqual(
            window._large_file_refactor_workbench_state,
            "REAL_PREVIEW_READY",
        )
        self.assertEqual(window._large_file_refactor_workbench_real_preview, "preview")
        store.assert_called_once()
        select.assert_called_once()

        blocked = correction_service.HeuristicWorkbenchCorrectionCandidate(
            ok=False,
            message="blocked",
        )
        blocked_result = correction_service.apply_heuristic_workbench_correction(
            SimpleNamespace(),
            context,
            blocked,
        )
        self.assertFalse(blocked_result.ok)
        self.assertEqual(blocked_result.message, "blocked")


if __name__ == "__main__":
    unittest.main()
