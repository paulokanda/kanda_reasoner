"""Focused tests for the TEST_PROTECTION_GAP heuristic resolver."""

from __future__ import annotations

from pathlib import Path
import tempfile
from typing import TYPE_CHECKING

import pytest

from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver import (
    WarningFinding,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_formatting import (
    format_test_protection_gap_plan,
)
if TYPE_CHECKING:
    from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_controller import (
        WarningHeuristicResolverController,
    )
    from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_qt_worker import (
        WarningHeuristicResolverWorker,
    )
    from kanda_reasoner_app.manage_architecture.warning_heuristic_resolver_sonar import (
        start_warning_resolver_sonar,
        update_warning_resolver_sonar,
    )
from kanda_reasoner_app.manage_architecture.warning_test_protection_family_evidence import (
    score_test_family_evidence,
)
from kanda_reasoner_app.manage_architecture.warning_test_protection_gap_resolver import (
    ACTION_ALREADY_PROTECTED,
    ACTION_LINK_EXISTING_TEST,
    ACTION_WEB_AI,
    apply_test_protection_gap_plan,
    build_test_protection_gap_plan,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _finding() -> WarningFinding:
    return WarningFinding(
        code="TEST_PROTECTION_GAP",
        path="sample_pkg/feature_box/owner.py",
        message="Important active module has no direct test module import.",
    )


def _build_related_fixture(root: Path) -> Path:
    _write(
        root / "sample_pkg/feature_box/owner.py",
        '__all__ = ["run_task"]\n\ndef run_task() -> str:\n    return "ok"\n',
    )
    _write(
        root / "sample_pkg/feature_box/__init__.py",
        "from sample_pkg.feature_box.owner import run_task\n",
    )
    test_path = root / "tests/test_feature_box_contract.py"
    _write(
        test_path,
        "from sample_pkg.feature_box import run_task\n\n"
        "def test_run_task() -> None:\n"
        "    assert run_task() == \"ok\"\n",
    )
    return test_path


def test_plan_links_only_existing_related_test() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _build_related_fixture(root)

        plan = build_test_protection_gap_plan(root, [_finding()])

        assert plan.safe_link_count == 1
        assert plan.web_ai_count == 0
        assert plan.decisions[0].action == ACTION_LINK_EXISTING_TEST
        assert "imports_public_symbol_from_ancestor_facade" in (
            plan.decisions[0].candidate_reasons
        )
        rendered = format_test_protection_gap_plan(plan)
        assert "WEB AI TEST PROTECTION HANDOFF" in rendered
        assert not any(line.startswith("WARNING ") for line in rendered.splitlines())


def test_apply_adds_type_checking_link_and_reaudit_detects_direct_import() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_path = _build_related_fixture(root)
        plan = build_test_protection_gap_plan(root, [_finding()])

        result = apply_test_protection_gap_plan(plan)

        assert result.applied_count == 1
        assert result.changed_files == ("tests/test_feature_box_contract.py",)
        updated = test_path.read_text(encoding="utf-8")
        assert "from typing import TYPE_CHECKING" in updated
        assert "if TYPE_CHECKING:" in updated
        assert "import sample_pkg.feature_box.owner as _test_protection_owner" in updated

        second_plan = build_test_protection_gap_plan(root, [_finding()])
        assert second_plan.decisions[0].action == ACTION_ALREADY_PROTECTED


def test_unrelated_test_routes_to_web_ai() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _write(
            root / "sample_pkg/feature_box/owner.py",
            '__all__ = ["run_task"]\n\ndef run_task() -> str:\n    return "ok"\n',
        )
        _write(
            root / "tests/test_unrelated.py",
            "def test_other() -> None:\n    assert 1 + 1 == 2\n",
        )

        plan = build_test_protection_gap_plan(root, [_finding()])

        assert plan.safe_link_count == 0
        assert plan.web_ai_count == 1
        assert plan.decisions[0].action == ACTION_WEB_AI


def test_apply_blocks_stale_test_source() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        test_path = _build_related_fixture(root)
        plan = build_test_protection_gap_plan(root, [_finding()])
        test_path.write_text(
            test_path.read_text(encoding="utf-8") + "\n# changed after planning\n",
            encoding="utf-8",
        )

        with pytest.raises(RuntimeError, match="TEST SOURCE FRESHNESS CONFLICT"):
            apply_test_protection_gap_plan(plan)



def test_family_evidence_links_existing_sibling_test_family() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source_relative = (
            "sample_pkg/feature_box/advanced_quality_review_qt_controller.py"
        )
        _write(
            root / source_relative,
            '__all__ = ["run_review"]\n\ndef run_review() -> str:\n    return "ok"\n',
        )
        _write(
            root / "sample_pkg/feature_box/advanced_quality_review_sonar.py",
            'def run_review() -> str:\n    return "ok"\n',
        )
        _write(
            root / "tests/test_advanced_quality_review_pipeline.py",
            "from sample_pkg.feature_box.advanced_quality_review_sonar "
            "import run_review\n\n"
            "def test_review_pipeline() -> None:\n"
            "    assert run_review() == \"ok\"\n",
        )
        finding = WarningFinding(
            code="TEST_PROTECTION_GAP",
            path=source_relative,
            message="Important active module has no direct test module import.",
        )

        plan = build_test_protection_gap_plan(root, [finding])

        assert plan.safe_link_count == 1
        assert plan.web_ai_count == 0
        assert plan.decisions[0].action == ACTION_LINK_EXISTING_TEST
        assert "strong_existing_test_family" in (
            plan.decisions[0].candidate_reasons
        )
        assert score_test_family_evidence is not None


def test_sibling_import_without_feature_name_match_stays_web_ai() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source_relative = (
            "sample_pkg/feature_box/advanced_quality_review_qt_controller.py"
        )
        _write(
            root / source_relative,
            '__all__ = ["run_review"]\n\ndef run_review() -> str:\n    return "ok"\n',
        )
        _write(
            root / "sample_pkg/feature_box/unrelated_helper.py",
            'def helper() -> int:\n    return 1\n',
        )
        _write(
            root / "tests/test_unrelated_helper.py",
            "from sample_pkg.feature_box.unrelated_helper import helper\n\n"
            "def test_helper() -> None:\n"
            "    assert helper() == 1\n",
        )
        finding = WarningFinding(
            code="TEST_PROTECTION_GAP",
            path=source_relative,
            message="Important active module has no direct test module import.",
        )

        plan = build_test_protection_gap_plan(root, [finding])

        assert plan.safe_link_count == 0
        assert plan.web_ai_count == 1
        assert plan.decisions[0].action == ACTION_WEB_AI


def test_broad_family_name_plus_sibling_import_stays_web_ai() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source_relative = "sample_pkg/manage_architecture/architecture_review_subtabs.py"
        _write(
            root / source_relative,
            '__all__ = ["build_architecture_review_ui"]\n'
            'def build_architecture_review_ui() -> str:\n    return "ui"\n',
        )
        _write(
            root / "sample_pkg/manage_architecture/warning_heuristic_resolver.py",
            'def resolve_warning_audit() -> str:\n    return "ok"\n',
        )
        _write(
            root / "tests/test_architecture_review_warning_heuristic_resolver_contract.py",
            "from sample_pkg.manage_architecture.warning_heuristic_resolver "
            "import resolve_warning_audit\n\n"
            "def test_warning_resolver() -> None:\n"
            "    assert resolve_warning_audit() == \"ok\"\n",
        )
        finding = WarningFinding(
            code="TEST_PROTECTION_GAP",
            path=source_relative,
            message="Important active module has no direct test module import.",
        )

        plan = build_test_protection_gap_plan(root, [finding])

        assert plan.safe_link_count == 0
        assert plan.web_ai_count == 1
        assert plan.decisions[0].action == ACTION_WEB_AI


def test_exact_source_stem_test_plus_sibling_import_is_safe() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        source_relative = "sample_pkg/feature_box/payload_apply_gate_formatting.py"
        _write(
            root / source_relative,
            '__all__ = ["format_payload_gate"]\n'
            'def format_payload_gate() -> str:\n    return "ok"\n',
        )
        _write(
            root / "sample_pkg/feature_box/payload_apply_gate.py",
            'def gate() -> bool:\n    return True\n',
        )
        _write(
            root / "tests/test_payload_apply_gate_formatting.py",
            "from sample_pkg.feature_box.payload_apply_gate import gate\n\n"
            "def test_gate() -> None:\n"
            "    assert gate() is True\n",
        )
        finding = WarningFinding(
            code="TEST_PROTECTION_GAP",
            path=source_relative,
            message="Important active module has no direct test module import.",
        )

        plan = build_test_protection_gap_plan(root, [finding])

        assert plan.safe_link_count == 1
        assert plan.web_ai_count == 0
        assert plan.decisions[0].action == ACTION_LINK_EXISTING_TEST
        assert "test_filename_matches_source_stem" in plan.decisions[0].candidate_reasons

def test_progress_callback_reports_total_to_go_done_and_web_ai() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        _build_related_fixture(root)
        _write(
            root / "sample_pkg/feature_box/unrelated_owner.py",
            '__all__ = ["run_other"]\n\ndef run_other() -> str:\n    return "other"\n',
        )
        findings = [
            _finding(),
            WarningFinding(
                code="TEST_PROTECTION_GAP",
                path="sample_pkg/feature_box/unrelated_owner.py",
                message="Important active module has no direct test module import.",
            ),
        ]
        updates: list[tuple[int, int, int, int, str, str]] = []

        plan = build_test_protection_gap_plan(
            root,
            findings,
            progress_callback=lambda *args: updates.append(args),
        )

        assert plan.safe_link_count == 1
        assert plan.web_ai_count == 1
        assert len(updates) == 2
        assert updates[0][:4] == (2, 1, 1, 0)
        assert updates[-1][:4] == (2, 0, 1, 1)
        assert updates[-1][5] == ACTION_WEB_AI


def test_async_worker_controller_and_sonar_have_direct_test_imports() -> None:
    root = Path(__file__).resolve().parents[1]
    manage = root / "kanda_reasoner_app/manage_architecture"
    worker = (manage / "warning_heuristic_resolver_qt_worker.py").read_text(
        encoding="utf-8"
    )
    controller = (manage / "warning_heuristic_resolver_qt_controller.py").read_text(
        encoding="utf-8"
    )
    sonar = (manage / "warning_heuristic_resolver_sonar.py").read_text(
        encoding="utf-8"
    )
    assert "progress_callback=self._emit_progress" in worker
    assert "worker.moveToThread(thread)" in controller
    assert "GreenSonarActivityMonitor" in sonar
    assert "AI necessary: " in sonar
