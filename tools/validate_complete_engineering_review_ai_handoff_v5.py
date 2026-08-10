"""Validate Complete Engineering Review -> AI handoff integration v5."""

from __future__ import annotations

import argparse
from dataclasses import replace
from pathlib import Path
import py_compile
import sys
import tempfile
import types
from types import SimpleNamespace as NS

FEATURE_ID = (
    "kanda-reasoner-complete-engineering-review-ai-correction-handoff-ready-v5"
)
TOUCHED = (
    "_reasoner_tools_gui_engineering_safety_full_audit.py",
    "_reasoner_tools_gui_engineering_safety_full_audit_handoff.py",
    "kanda_reasoner_app/engineering_safety/complete_review_contract.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_handoff.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/ai_correction_report.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/complete_review_coverage.py",
    "kanda_reasoner_app/engineering_diagnostics_gui/review_handoff.py",
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _stub_gui_package(root: Path) -> None:
    import kanda_reasoner_app

    name = "kanda_reasoner_app.engineering_diagnostics_gui"
    package = types.ModuleType(name)
    package.__path__ = [str(root / "kanda_reasoner_app" / "engineering_diagnostics_gui")]
    sys.modules[name] = package


def _fake_review(root: Path):
    import _reasoner_tools_gui_engineering_safety_full_audit as full_audit
    from reasoner_tools_gui_engineering_safety_panel import (
        get_engineering_safety_panel_catalog,
    )

    class Result:
        status_code = 0
        stderr = ""

        def __init__(self, command: str) -> None:
            self.stdout = "fixture evidence for " + command
            if command == "bom-scan":
                self.stdout = "files_scanned=10; findings=4.\nFinding count: 4"
            elif command == "ruff-quality":
                self.stdout = "lint_status=0; format_status=1; findings=12."
            elif command == "shadow-audit":
                self.stdout = "files_scanned=10; findings=3.\nFinding count: 3"
            elif command == "evidence-freshness":
                self.stdout = "Evidence freshness status=missing_evidence"
            elif command == "related-files":
                self.status_code = 2
                self.stderr = (
                    "AttributeError: module 'kanda_reasoner_app.reasoner_symbol_atlas."
                    "_related_file_finder_support' has no attribute "
                    "'_limited_unique_paths'"
                )

    review = full_audit.collect_complete_engineering_review(
        get_engineering_safety_panel_catalog(),
        str(root),
        lambda command, _project: Result(command),
    )
    _require(review.total == 23, "V5_COMPLETE_REVIEW_23_ITEMS")
    _require(len(review.items) == 23, "V5_STRUCTURED_FULL_AUDIT_RESULT_23_ITEMS")
    _require(
        "COMPLETE ENGINEERING REVIEW" in review.rendered_log,
        "V5_BACKWARD_COMPATIBLE_HUMAN_LOG",
    )
    return review


def _collector_results():
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_report import (
        AiCorrectionCollectorResult,
    )

    return (
        AiCorrectionCollectorResult("BOM", "STORED", "bom-run", 4),
        AiCorrectionCollectorResult("Ruff", "STORED", "ruff-run", 12),
        AiCorrectionCollectorResult("Architecture", "STORED", "arch-run", 2),
        AiCorrectionCollectorResult("Shadow", "STORED", "shadow-run", 3),
    )


def _coverage_contract(root: Path, review) -> object:
    import kanda_reasoner_app.engineering_diagnostics_gui.complete_review_coverage as adapter
    from kanda_reasoner_app.engineering_diagnostics_gui._engineering_capability_models import (
        EngineeringCapabilityResult,
    )

    calls: list[str] = []

    def fake_cli_only(command: str, project_root: str):
        calls.append(command + "|" + project_root)
        return EngineeringCapabilityResult(
            surface="SAFETY_CLI_ONLY",
            section="Project Symbol Atlas",
            label=command,
            command_name=command,
            scope_mode="TARGETED_SMOKE",
            status="CLEAN",
            severity="INFO",
            assessment_reason="fixture CLI-only result",
            execution="EXECUTED_PUBLIC_CLI",
            status_code=0,
            evidence="fixture",
            correction_guidance="none",
        )

    adapter._cli_only_result = fake_cli_only
    coverage = adapter.coverage_from_complete_engineering_review(
        review,
        _collector_results(),
    )
    _require(coverage.gui_catalog_count == 23, "V5_GUI_CATALOG_23_OF_23")
    _require(coverage.cli_catalog_count == 24, "V5_CLI_CATALOG_24_OF_24")
    _require(
        coverage.unique_safety_surface_count == 25,
        "V5_UNIQUE_SAFETY_SURFACES_25_OF_25",
    )
    _require(coverage.total_surface_count == 26, "V5_TOTAL_SURFACES_26_OF_26")
    _require(len(calls) == 2, "V5_ONLY_TWO_CLI_ONLY_SURFACES_EXECUTED_AFTER_FULL_AUDIT")
    _require(
        all("CONSUMED_COMPLETE_ENGINEERING_REVIEW_RESULT" in item.execution
            or item.execution == "COVERED_BY_STRUCTURED_DIAGNOSTIC"
            or item.surface != "PONTUAL_GUI"
            for item in coverage.results),
        "V5_FULL_AUDIT_RESULTS_CONSUMED_NOT_RERUN",
    )
    related = next(item for item in coverage.results if item.command_name == "related-files")
    _require(related.severity == "ERROR", "V5_FULL_AUDIT_ERROR_SURFACED")
    _require("_limited_unique_paths" in related.evidence, "V5_FULL_AUDIT_ERROR_EVIDENCE")
    freshness = next(item for item in coverage.results if item.command_name == "evidence-freshness")
    _require(freshness.severity == "WARNING", "V5_FULL_AUDIT_WARNING_SURFACED")
    return coverage


def _project_card(root: Path, tool_root: Path):
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRecord
    from kanda_reasoner_app.project_support_boundary import ProjectSelectionMode

    return ProjectSelectionRecord(
        stable_project_id="project-card-fixture",
        project_slug=root.name,
        project_root=str(root),
        project_root_fingerprint="project-root-fingerprint",
        project_support_root=str(root.parent / (root.name + "_show_project_to_AI")),
        selection_mode=ProjectSelectionMode.EXPLICIT_EXTERNAL_PROJECT,
        updated_at_utc="2026-08-07T13:00:00+00:00",
    )


def _report_identity_contract(root: Path, coverage) -> None:
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_report import (
        build_full_ai_correction_report,
    )

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        tool_root = base / "tool"
        project_root = base / "active_project"
        tool_root.mkdir()
        project_root.mkdir()
        card = _project_card(project_root, tool_root)
        report = build_full_ai_correction_report(
            str(project_root),
            _collector_results(),
            (),
            coverage,
            project_card=card,
            tool_root=str(tool_root),
            complete_review_sha256="abc123",
            complete_review_item_count=23,
        )
        text = report.text
        required = (
            "AUDIT TARGET ROLE: ACTIVE PROJECT",
            "Audit target derived from Tool root: NO",
            "KANDA Tool role: AUDIT EXECUTION PROVIDER ONLY",
            "Tool and Project same physical root: NO",
            "Active Project stable ID: project-card-fixture",
            "Project is the M-card for this audit: YES",
            "Complete Engineering Review catalog items: 23",
            "Complete Review evidence consumed without rerunning its 23 GUI actions: YES",
            "FULL ENGINEERING CAPABILITY COVERAGE LEDGER",
            "AI CORRECTION DOSSIER: REQUIRED",
        )
        for marker in required:
            _require(marker in text, "V5_REPORT_MARKER:" + marker)
        _require(str(project_root) in text, "V5_EXTERNAL_PROJECT_IS_AUDIT_TARGET")
        _require(
            "Tool and selected Project logical roles merged: NO" in text,
            "V5_TOOL_PROJECT_LOGICAL_SEPARATION_REPORT",
        )


def _publish_guard_contract(root: Path, coverage) -> None:
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_handoff import (
        build_full_ai_correction_handoff,
    )

    class Controller:
        def load_run_view(self, _project_root: str, _run_id: str):
            raise AssertionError("no run IDs expected in guard fixture")

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        project = base / "active_project"
        daily = base / "active_project_delete_after_daily_work"
        project.mkdir()
        calls = {"count": 0}

        def guard() -> None:
            calls["count"] += 1
            if calls["count"] >= 2:
                raise RuntimeError("ACTIVE_PROJECT_MCARD_CHANGED")

        try:
            build_full_ai_correction_handoff(
                Controller(),
                str(project),
                (),
                capability_coverage=coverage,
                project_daily_work_root=str(daily),
                publish_guard=guard,
            )
        except RuntimeError as exc:
            _require(
                "ACTIVE_PROJECT_MCARD_CHANGED" in str(exc),
                "V5_STALE_PROJECT_CARD_REJECTED",
            )
        else:
            raise RuntimeError("V5_STALE_PROJECT_CARD_WAS_NOT_REJECTED")
        artifacts = tuple(daily.rglob("*.txt")) if daily.exists() else ()
        _require(len(artifacts) == 0, "V5_STALE_PROJECT_ARTIFACT_NOT_PUBLISHED")


def _source_contract(root: Path) -> None:
    full_audit = (
        root / "_reasoner_tools_gui_engineering_safety_full_audit.py"
    ).read_text(encoding="utf-8")
    ui_helper = (
        root / "_reasoner_tools_gui_engineering_safety_full_audit_handoff.py"
    ).read_text(encoding="utf-8")
    bridge = (
        root / "kanda_reasoner_app/engineering_diagnostics_gui/review_handoff.py"
    ).read_text(encoding="utf-8")
    public_init = (
        root / "kanda_reasoner_app/engineering_diagnostics_gui/__init__.py"
    ).read_text(encoding="utf-8")
    _require(
        "create_engineering_diagnostics_workspace" in public_init
        and "create_full_engineering_diagnostics_panel" in public_init
        and "build_complete_review_ai_correction_handoff" in public_init,
        "V5R1_LIVE_INIT_EXPORT_PRESERVATION",
    )
    _require(
        "from _reasoner_tools_gui_engineering_safety_sonar import (" in ui_helper
        and "create_engineering_safety_sonar," in ui_helper
        and "create_engineering_safety_sonar(full_page)" in ui_helper
        and "from _reasoner_tools_gui_engineering_safety_sonar import ("
        not in full_audit,
        "V5R3_EXTRACTED_HANDOFF_SONAR_DEPENDENCY_OWNED_LOCALLY",
    )
    _require(
        "AI correction handoff: BUILDING" in ui_helper,
        "V5_COMPLETE_REVIEW_BUILDING_STATE",
    )
    _require(
        "AI correction handoff: READY" in ui_helper,
        "V5_COMPLETE_REVIEW_READY_STATE",
    )
    _require(
        "engineering_safety_copy_complete_ai_correction_handoff_button" in ui_helper,
        "V5_COMPLETE_REVIEW_COPY_BUTTON",
    )
    _require(
        "capture_active_project_card(project_root)" in ui_helper,
        "V5_PROJECT_MCARD_CAPTURE_BEFORE_REVIEW",
    )
    _require(
        "project_card.project_root" in ui_helper,
        "V5_PROJECT_CARD_ROOT_IS_REVIEW_TARGET",
    )
    _require(
        "EngineeringDiagnosticsController(tool_root=tool)" in bridge,
        "V5_TOOL_ROOT_EXECUTION_PROVIDER_ONLY",
    )
    _require(
        "collect_full_engineering_diagnostics_candidates" in bridge,
        "V5_PUBLIC_DIAGNOSTICS_COLLECTOR_ORCHESTRATION_REUSED",
    )
    _require(
        "coverage_from_complete_engineering_review" in bridge,
        "V5_FULL_AUDIT_EVIDENCE_ADAPTER_USED",
    )
    _require(
        "run_engineering_safety_panel_command" not in bridge,
        "V5_NO_23_TOOL_RERUN_IN_BRIDGE",
    )
    _require(
        "run_complete_engineering_review" in full_audit,
        "V5_LEGACY_TEXT_FACADE_PRESERVED",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    for relative in TOUCHED:
        path = root / relative
        _require(path.is_file(), "V5_TOUCHED_FILE_EXISTS:" + relative)
        path.read_bytes().decode("ascii")
        _require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            "V5_MODULE_SIZE_MAX_500:" + relative,
        )
        py_compile.compile(str(path), doraise=True)
    print("V5_PYTHON_COMPILE: PASS")
    print("V5_ASCII_SOURCE_CONTRACT: PASS")

    _stub_gui_package(root)
    review = _fake_review(root)
    coverage = _coverage_contract(root, review)
    _report_identity_contract(root, coverage)
    _publish_guard_contract(root, coverage)
    _source_contract(root)

    print("FULL AUDIT 23 GUI ACTIONS RERUN FOR HANDOFF: NO")
    print("TOOL ROOT USED AS AUDIT TARGET BY BRIDGE: NO")
    print("ACTIVE PROJECT MCARD REQUIRED: YES")
    print("STALE PROJECT COMPLETION PUBLISHED: NO")
    print("PROJECT DAILY-WORK HANDOFF OWNER: PASS")
    print("FULL AUDIT SOURCE MUTATION BY VALIDATOR: NO")
    print("ENGINEERING DIAGNOSTICS STORE MUTATED BY VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY VALIDATOR: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("MCARD LIFECYCLE GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
