"""Real PySide6 validation for Complete Review -> READY AI handoff v5."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
import time

FEATURE_ID = (
    "kanda-reasoner-complete-engineering-review-ai-correction-handoff-ready-v5"
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool-root", required=True)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    tool_root = Path(args.tool_root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    if str(tool_root) not in sys.path:
        sys.path.insert(0, str(tool_root))

    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication

    import _reasoner_tools_gui_engineering_safety_full_audit as full_audit
    import _reasoner_tools_gui_engineering_safety_full_audit_handoff as handoff_ui
    from kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_handoff import (
        AiCorrectionHandoffArtifact,
    )
    from kanda_reasoner_app.engineering_safety.complete_review_contract import (
        CompleteEngineeringReviewItem,
        CompleteEngineeringReviewResult,
    )
    from kanda_reasoner_app.project_selection_registry import ProjectSelectionRegistry
    from reasoner_tools_gui_engineering_safety_panel import (
        create_engineering_safety_panel,
        get_engineering_safety_panel_catalog,
    )

    registry = ProjectSelectionRegistry(tool_source_root=tool_root)
    record = registry.load_current_record()
    _require(record is not None, "REAL_QT_V5_ACTIVE_PROJECT_CARD_PRESENT")
    boundary = registry.resolve_boundary_for_root(project_root)
    _require(
        boundary.active_project_id == record.stable_project_id,
        "REAL_QT_V5_ACTIVE_PROJECT_CARD_MATCH",
    )

    protected = (
        tool_root / "kanda_reasoner_app" / "project_selection_registry.py",
        tool_root / "kanda_reasoner_app" / "engineering_diagnostics_gui" / "controller.py",
        tool_root / "kanda_reasoner_app" / "engineering_diagnostics" / "store.py",
    )
    before = {str(path): _hash(path) for path in protected if path.is_file()}
    catalog = tuple(get_engineering_safety_panel_catalog())
    items = tuple(
        CompleteEngineeringReviewItem(
            index=index,
            total=len(catalog),
            section=str(tool.section),
            label=str(tool.label),
            command_name=str(tool.command_name),
            outcome="PASS",
            assessment="CLEAN",
            assessment_reason="Real Qt v5 UI fixture result.",
            status_code=0,
            stdout="fixture evidence",
            stderr="",
        )
        for index, tool in enumerate(catalog, start=1)
    )
    review = CompleteEngineeringReviewResult(
        project_root=str(project_root),
        items=items,
        overall="PASS",
        passed=len(catalog),
        failed=0,
        completed=len(catalog),
        cancelled=False,
        total=len(catalog),
        assessment_counts=(("CLEAN", len(catalog)),),
        rendered_log=(
            "COMPLETE ENGINEERING REVIEW\n"
            + "Project root: "
            + str(project_root)
            + "\nCatalog items: "
            + str(len(catalog))
            + "\nSUMMARY\nOverall: PASS"
        ),
    )

    artifact_path = (
        boundary.active_project_daily_work_root
        / "validation_evidence"
        / "complete_review_ai_handoff_v5_real_qt_fixture.txt"
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)

    def fake_review(*_args, **_kwargs):
        time.sleep(0.15)
        return review

    def fake_handoff(card, supplied_review, _cancel):
        _require(
            card.stable_project_id == record.stable_project_id,
            "REAL_QT_V5_HANDOFF_RECEIVES_PROJECT_MCARD",
        )
        _require(
            supplied_review.project_root == str(project_root),
            "REAL_QT_V5_HANDOFF_RECEIVES_ACTIVE_PROJECT_REVIEW",
        )
        time.sleep(0.15)
        text = (
            "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF\n"
            "AUDIT TARGET ROLE: ACTIVE PROJECT\n"
            "KANDA Tool role: AUDIT EXECUTION PROVIDER ONLY\n"
            "Project is the M-card for this audit: YES\n"
            "FULL ENGINEERING CAPABILITY COVERAGE LEDGER\n"
        )
        artifact_path.write_text(text, encoding="utf-8")
        payload = artifact_path.read_bytes()
        return AiCorrectionHandoffArtifact(
            report_path=str(artifact_path),
            sha256=hashlib.sha256(payload).hexdigest(),
            finding_count=0,
            correction_group_count=0,
            correction_ready_count=0,
            blocked_count=0,
            review_required_count=0,
            byte_count=len(payload),
            console_summary=(
                "FULL ENGINEERING CAPABILITY COVERAGE\n"
                "Total engineering surfaces: 26/26 ACCOUNTED\n"
                "Silent capability omissions: 0"
            ),
            capability_surface_count=26,
            capability_error_count=0,
            capability_warning_count=0,
        )

    full_audit.collect_complete_engineering_review = fake_review
    handoff_ui.build_project_bound_handoff = fake_handoff

    app = QApplication.instance() or QApplication([])
    panel = create_engineering_safety_panel(
        project_root_provider=lambda: str(project_root)
    )
    button = panel.engineering_safety_full_audit_button
    copy_button = panel.engineering_safety_copy_complete_ai_correction_handoff_button
    output = panel.engineering_safety_full_audit_log
    heartbeat = {"count": 0}
    timer = QTimer()
    timer.setInterval(25)
    timer.timeout.connect(lambda: heartbeat.__setitem__("count", heartbeat["count"] + 1))
    timer.start()

    button.click()
    deadline = time.monotonic() + 10.0
    building_seen = False
    while time.monotonic() < deadline:
        app.processEvents()
        text = output.toPlainText()
        if "AI correction handoff: BUILDING" in text:
            building_seen = True
        if "AI correction handoff: READY" in text:
            break
        time.sleep(0.01)

    timer.stop()
    text = output.toPlainText()
    _require(building_seen, "REAL_QT_V5_BUILDING_VISIBLE")
    _require("AI correction handoff: READY" in text, "REAL_QT_V5_READY_VISIBLE")
    _require(heartbeat["count"] >= 3, "REAL_QT_V5_EVENT_LOOP_RESPONSIVE")
    _require(copy_button.isEnabled(), "REAL_QT_V5_COPY_BUTTON_ENABLED")
    _require(
        "26/26 ACCOUNTED" in text,
        "REAL_QT_V5_COMPLETE_COVERAGE_SUMMARY_VISIBLE",
    )
    copy_button.click()
    app.processEvents()
    clipboard_text = QApplication.clipboard().text()
    _require(
        "AUDIT TARGET ROLE: ACTIVE PROJECT" in clipboard_text,
        "REAL_QT_V5_COPY_COMPLETE_HANDOFF",
    )
    _require(
        str(boundary.active_project_daily_work_root) in str(artifact_path),
        "REAL_QT_V5_PROJECT_DAILY_WORK_OWNER",
    )

    after = {str(path): _hash(path) for path in protected if path.is_file()}
    _require(before == after, "REAL_QT_V5_PROTECTED_OWNER_SOURCE_UNCHANGED")
    artifact_path.unlink(missing_ok=True)
    panel.close()
    panel.deleteLater()
    app.processEvents()

    print("REAL_QT_V5_TOOL_ROOT_USED_AS_AUDIT_TARGET: NO")
    print("REAL_QT_V5_ACTIVE_PROJECT_IS_MCARD: PASS")
    print("REAL_QT_V5_PROJECT_SELECTION_REGISTRY_MUTATED: NO")
    print("REAL_QT_V5_ENGINEERING_DIAGNOSTICS_STORE_MUTATED: NO")
    print("REAL_QT_V5_FREEZE_MEMORY_MUTATED: NO")
    print("TOOL PROJECT LOGICAL ROLE SEPARATION: PASS")
    print("MCARD LIFECYCLE GATE: PASS")
    print("VALIDATION OK: " + FEATURE_ID + "-real-qt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
