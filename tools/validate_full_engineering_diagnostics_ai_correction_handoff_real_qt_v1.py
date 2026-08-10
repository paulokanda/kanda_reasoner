"""Real Qt validation for Full Engineering Diagnostics AI correction handoff v1."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace as NS

FEATURE_ID = "kanda-reasoner-full-engineering-diagnostics-ai-correction-handoff-v1"


def _require(condition: bool, marker: str) -> None:
    if not condition:
        raise RuntimeError(marker)
    print(marker + ": PASS")


def _finding_view(run_id: str, path: str):
    plan = NS(
        focused_tests=("tools/test_x.py",),
        validation_commands=("python tools/test_x.py",),
        rollback_expectation="Restore exact predecessor.",
        evidence_required=("VALIDATION OK",),
    )
    intent = NS(
        action_class="FIX_NOW",
        primary_trust_source="KANDA_RULE_TEMPLATE",
        rule_template_id="TEST_RULE",
        likely_correction="Move behavior to the canonical owner.",
        reason="Owner mismatch.",
        expected_affected_files=(path,),
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
        issue_fingerprint=run_id + "-issue",
        evidence_digest=run_id + "-evidence",
        severity="warning",
        confidence="high",
        code="TEST001",
        category="architecture",
        relative_path=path,
        line=10,
        symbol_id="fixture.symbol",
        location_key=path + ":fixture.symbol",
        semantic_key="TEST001:fixture.symbol",
        message="Behavior is in the wrong owner.",
        suggested_action="Move behavior.",
        evidence={"rule": "TEST001"},
    )
    owner = NS(
        active_candidates=("fixture.owner",),
        historical_candidates=(),
        selection_method="symbol_atlas",
        evidence=("active owner",),
    )
    scope = NS(method="path_policy", evidence=("active source",))
    frozen = NS(matched_protected_paths=(), evidence=("unfrozen",))
    enrichment = NS(owner=owner, scope=scope, frozen_path=frozen)
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
        group_count=1,
        group_kind="DETERMINISTIC",
        group_label="TEST001 " + path,
        group_confidence="high",
        enrichment=enrichment,
        remediation_intent=intent,
        remediation_action_class="FIX_NOW",
    )


def _run_view(run_id: str, producer: str):
    finding = _finding_view(run_id, "fixture/" + producer + ".py")
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
        finding_count=1,
        content_digest=run_id + "-digest",
        started_at_utc="2026-08-07T00:00:00Z",
        completed_at_utc="2026-08-07T00:00:01Z",
        provenance={"source": "fixture"},
    )
    comparison = NS(
        status="NO_BASELINE",
        new_issue_fingerprints=(finding.record.issue_fingerprint,),
        persistent_issue_fingerprints=(),
        resolved_issue_fingerprints=(),
    )
    return NS(run=run, findings=(finding,), comparison=comparison)


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
        return NS(run_id=run_id, finding_count=1)

    def load_run_view(self, _project_root, run_id):
        self.load_threads.append(threading.get_ident())
        time.sleep(0.15)
        producer = run_id.split("-")[1]
        return _run_view(run_id, producer)


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
    _require(copy_button.isEnabled() is False, "REAL_QT_AI_HANDOFF_IDLE_DISABLED")
    panel.start_full_engineering_diagnostics()

    deadline = time.monotonic() + 12.0
    while time.monotonic() < deadline and not copy_button.isEnabled():
        app.processEvents()
        time.sleep(0.01)

    _require(copy_button.isEnabled(), "REAL_QT_AI_HANDOFF_READY")
    _require(heartbeat["count"] >= 10, "REAL_QT_AI_HANDOFF_EVENT_LOOP_RESPONSIVE")
    _require(bool(controller.load_threads), "REAL_QT_AI_HANDOFF_RUN_VIEWS_LOADED")
    _require(
        all(thread_id != main_thread for thread_id in controller.load_threads),
        "REAL_QT_AI_HANDOFF_ENRICHMENT_OFF_GUI_THREAD",
    )

    output_text = panel.full_engineering_diagnostics_output.toPlainText()
    _require("AI correction handoff: READY" in output_text, "REAL_QT_AI_HANDOFF_STATUS")
    path_line = next(
        line for line in output_text.splitlines() if line.startswith("Path: ")
    )
    report_path = Path(path_line[6:].strip())
    _require(report_path.is_file(), "REAL_QT_AI_HANDOFF_FILE_WRITTEN")
    report_text = report_path.read_text(encoding="utf-8", errors="replace")
    _require(
        "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF" in report_text,
        "REAL_QT_AI_HANDOFF_REPORT_HEADER",
    )
    _require(
        "Likely correction: Move behavior to the canonical owner." in report_text,
        "REAL_QT_AI_HANDOFF_CORRECTION_CONTEXT",
    )
    _require(
        "Source inspection required before edit: YES" in report_text,
        "REAL_QT_AI_HANDOFF_SOURCE_INSPECTION_GATE",
    )

    copy_button.click()
    app.processEvents()
    clipboard_text = QApplication.clipboard().text()
    _require(
        "FULL ENGINEERING DIAGNOSTICS AI CORRECTION HANDOFF" in clipboard_text,
        "REAL_QT_AI_HANDOFF_CLIPBOARD",
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
