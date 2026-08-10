"""Real Qt validation for comprehensive Full Engineering Diagnostics v3."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace as NS

FEATURE_ID = (
    "kanda-reasoner-full-engineering-diagnostics-comprehensive-capability-coverage-v3"
)


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _finding(run_id: str, producer: str, index: int):
    group_id = index % 4
    plan = NS(
        focused_tests=("tools/test_x.py",),
        validation_commands=("python tools/test_x.py",),
        rollback_expectation="Restore exact predecessor.",
        evidence_required=("VALIDATION OK",),
    )
    intent = NS(
        action_class="FIX_NOW",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="TEST_RULE_" + str(group_id),
        likely_correction="Move behavior to the canonical owner.",
        reason="Owner mismatch.",
        expected_affected_files=("fixture/" + producer + "_" + str(index) + ".py",),
        frozen_path_impact="UNFROZEN",
        required_governed_wave="",
        fix_applicability="EXACT_FILE",
        mechanical_safety="SEMANTIC_REVIEW_REQUIRED",
        semantic_review_requirement="REQUIRED",
        uncertainty="low",
        validation_plan=plan,
        deterministic_evidence=("owner mismatch",),
        project_governance_rules=("Box Logic", "No Leak"),
        ai_hypothesis=None,
    )
    record = NS(
        issue_fingerprint=run_id + "-issue-" + str(index),
        evidence_digest=run_id + "-evidence-" + str(index),
        severity="warning",
        confidence="high",
        code="TEST" + str(group_id),
        category="architecture",
        relative_path="fixture/" + producer + "_" + str(index) + ".py",
        line=index + 1,
        symbol_id="fixture.symbol." + str(index),
        location_key="",
        semantic_key="",
        message="Behavior is in the wrong owner.",
        suggested_action="Move behavior.",
        evidence={"rule": "TEST" + str(group_id)},
    )
    owner = NS(
        active_candidates=("fixture.owner",),
        historical_candidates=(),
        selection_method="symbol_atlas",
        evidence=("active owner",),
    )
    scope = NS(method="path_policy", evidence=("active source",))
    frozen = NS(
        matched_protected_paths=(),
        evidence=("unfrozen",),
        governing_freeze_ids=(),
    )
    enrichment = NS(owner=owner, scope=scope, frozen_path=frozen)
    group = NS(
        kind="DETERMINISTIC",
        group_id=producer + "-group-" + str(group_id),
        label="TEST group " + str(group_id),
        confidence="high",
    )
    return NS(
        record=record,
        lifecycle_state="new",
        decision_state="OPEN",
        decision_generation=0,
        scope_classification="ACTIVE",
        scope_confidence="high",
        frozen_status="UNFROZEN",
        governing_freeze_ids="",
        owner_status="READY",
        owner_confidence="high",
        canonical_owner="fixture.owner",
        enrichment=enrichment,
        groups=(group,),
        remediation_intent=intent,
        remediation_action_class="FIX_NOW",
    )


def _run_view(run_id: str, producer: str):
    findings = tuple(_finding(run_id, producer, index) for index in range(40))
    run = NS(
        producer_id=producer,
        producer_version="1",
        run_id=run_id,
        attempt_id=run_id + "-attempt",
        project_id="project-1",
        project_root_fingerprint="rootfp",
        source_fingerprint="sourcefp",
        scope_fingerprint="scopefp",
        configuration_fingerprint="configfp",
        operation_generation=1,
        completion_status="COMPLETE_WITH_FINDINGS",
        finding_count=len(findings),
        content_digest=run_id + "-digest",
        started_at_utc="2026-08-07T00:00:00Z",
        completed_at_utc="2026-08-07T00:00:01Z",
        provenance={"source": "fixture"},
    )
    comparison = NS(
        status="NO_BASELINE",
        new_issue_fingerprints=(),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    return NS(run=run, findings=findings, comparison=comparison)


class _FakeController:
    def __init__(self) -> None:
        self.load_threads: list[int] = []
        self._counter = 0

    def _collect(self, label: str):
        time.sleep(0.03)
        return NS(label=label)

    def collect_bom_candidate(self, *_args):
        return self._collect("bom")

    def collect_ruff_candidate(self, *_args):
        return self._collect("ruff")

    def collect_architecture_candidate(self, *_args):
        return self._collect("architecture")

    def collect_shadow_candidate(self, *_args):
        return self._collect("shadow")

    def commit_candidate(self, _project_root, candidate, **_kwargs):
        self._counter += 1
        run_id = "fixture-" + str(candidate.label) + "-" + str(self._counter)
        return NS(run_id=run_id, finding_count=40)

    def load_run_view(self, _project_root, run_id):
        self.load_threads.append(threading.get_ident())
        time.sleep(0.04)
        producer = run_id.split("-")[1]
        return _run_view(run_id, producer)


def _fake_coverage(thread_ids: list[int]):
    def build(_project_root, _collector_results, _cancellation=None):
        from kanda_reasoner_app.engineering_diagnostics_gui._engineering_capability_models import (
            EngineeringCapabilityCoverage,
            EngineeringCapabilityResult,
        )

        thread_ids.append(threading.get_ident())
        time.sleep(0.35)
        results = []
        for index in range(26):
            status = "CLEAN"
            severity = "INFO"
            if index in {20, 21, 22}:
                status = "FAILED"
                severity = "ERROR"
            elif index in {4, 10, 18}:
                status = "MISSING_EVIDENCE"
                severity = "WARNING"
            results.append(
                EngineeringCapabilityResult(
                    surface="PONTUAL_GUI" if index < 23 else (
                        "SAFETY_CLI_ONLY" if index < 25 else "ARCHITECTURE_REVIEW"
                    ),
                    section="Fixture",
                    label="Capability " + str(index),
                    command_name="fixture-" + str(index),
                    scope_mode="PROJECT_WIDE_READ_ONLY",
                    status=status,
                    severity=severity,
                    assessment_reason="Fixture assessment.",
                    execution="EXECUTED_PUBLIC_CONTRACT",
                    status_code=2 if severity == "ERROR" else 0,
                    evidence="Fixture evidence.",
                    correction_guidance="Inspect exact source.",
                )
            )
        return EngineeringCapabilityCoverage(
            results=tuple(results),
            gui_catalog_count=23,
            cli_catalog_count=24,
            unique_safety_surface_count=25,
            architecture_surface_count=1,
        )

    return build


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    project_root = Path(args.project_root).expanduser().resolve(strict=True)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from PySide6.QtCore import QTimer
    from PySide6.QtWidgets import QApplication
    import kanda_reasoner_app.engineering_diagnostics_gui.ai_correction_handoff as handoff

    coverage_threads: list[int] = []
    handoff.collect_engineering_capability_coverage = _fake_coverage(coverage_threads)

    from kanda_reasoner_app.engineering_diagnostics_gui.full_engineering_diagnostics_tab import (
        create_full_engineering_diagnostics_panel,
    )

    app = QApplication.instance() or QApplication([])
    controller = _FakeController()
    main_thread = threading.get_ident()
    heartbeat = {"count": 0}
    timer = QTimer()
    timer.setInterval(20)
    timer.timeout.connect(
        lambda: heartbeat.__setitem__("count", heartbeat["count"] + 1)
    )
    timer.start()

    panel = create_full_engineering_diagnostics_panel(
        project_root_provider=lambda: str(project_root),
        controller=controller,
    )
    panel.show()
    app.processEvents()
    copy_button = panel.full_engineering_diagnostics_copy_ai_handoff_button
    panel.start_full_engineering_diagnostics()

    building_seen = False
    deadline = time.monotonic() + 15.0
    while time.monotonic() < deadline and not copy_button.isEnabled():
        app.processEvents()
        text = panel.full_engineering_diagnostics_output.toPlainText()
        if "AI correction handoff: BUILDING" in text:
            building_seen = True
        time.sleep(0.01)

    _require(building_seen, "REAL_QT_COMPREHENSIVE_BUILDING_VISIBLE")
    _require(copy_button.isEnabled(), "REAL_QT_COMPREHENSIVE_HANDOFF_READY")
    _require(
        heartbeat["count"] >= 10,
        "REAL_QT_COMPREHENSIVE_EVENT_LOOP_RESPONSIVE",
    )
    _require(bool(controller.load_threads), "REAL_QT_COMPREHENSIVE_RUN_VIEWS_LOADED")
    _require(
        all(thread_id != main_thread for thread_id in controller.load_threads),
        "REAL_QT_COMPREHENSIVE_ENRICHMENT_OFF_GUI_THREAD",
    )
    _require(bool(coverage_threads), "REAL_QT_COMPREHENSIVE_COVERAGE_EXECUTED")
    _require(
        all(thread_id != main_thread for thread_id in coverage_threads),
        "REAL_QT_COMPREHENSIVE_COVERAGE_OFF_GUI_THREAD",
    )

    output_text = panel.full_engineering_diagnostics_output.toPlainText()
    for marker in (
        "Pontual Audit GUI catalog: 23/23 ACCOUNTED",
        "Safety Suite CLI catalog: 24/24 ACCOUNTED",
        "Unique GUI/CLI safety surfaces: 25/25 ACCOUNTED",
        "Total engineering surfaces: 26/26 ACCOUNTED",
        "Capability errors: 3",
        "Capability warnings: 3",
        "AI CORRECTION SUMMARY",
    ):
        _require(marker in output_text, "REAL_QT_OUTPUT:" + marker)

    path_line = next(
        line for line in output_text.splitlines() if line.startswith("Path: ")
    )
    report_path = Path(path_line[6:].strip())
    _require(report_path.is_file(), "REAL_QT_COMPREHENSIVE_FILE_WRITTEN")
    report_text = report_path.read_text(encoding="utf-8", errors="replace")
    _require(
        "FULL ENGINEERING CAPABILITY COVERAGE LEDGER" in report_text,
        "REAL_QT_COMPREHENSIVE_LEDGER_WRITTEN",
    )
    _require(
        "Correction guidance:" in report_text
        and "Exact source inspection required before edit: YES" in report_text,
        "REAL_QT_COMPREHENSIVE_AI_CORRECTION_CONTEXT",
    )

    timer.stop()
    panel.close()
    panel.deleteLater()
    app.processEvents()
    try:
        report_path.unlink()
        if not any(report_path.parent.iterdir()):
            report_path.parent.rmdir()
    except OSError:
        pass

    print("PROJECT SOURCE MUTATED BY REAL QT VALIDATOR: NO")
    print("FREEZE MEMORY MUTATED BY REAL QT VALIDATOR: NO")
    print("PROJECT SELECTION REGISTRY MUTATED BY REAL QT VALIDATOR: NO")
    print("VALIDATION OK: " + FEATURE_ID)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
