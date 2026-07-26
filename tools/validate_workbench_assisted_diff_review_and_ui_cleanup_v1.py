"""Validate Workbench assisted diff review and legacy GUI cleanup."""
from __future__ import annotations

import json
from pathlib import Path
import sys
from types import SimpleNamespace

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PKG = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "manage_architecture"
    / "large_file_refactor_planner"
)
sys.path.insert(0, str(PROJECT_ROOT))

FEATURE_ID = "architecture-review-workbench-assisted-diff-review-and-legacy-ui-cleanup-v1"


def run_validation() -> None:
    """Run static and service-level regression checks."""

    gui = (PKG / "workbench_gui.py").read_text(encoding="utf-8")
    completion = (PKG / "workbench_completion_gui.py").read_text(encoding="utf-8")
    service = (PKG / "workbench_diff_review_assistant.py").read_text(encoding="utf-8")
    assistant_gui = (PKG / "workbench_diff_review_assistant_gui.py").read_text(
        encoding="utf-8"
    )
    real_widget_validator = (
        PROJECT_ROOT
        / "tools"
        / "validate_large_file_refactor_workbench_real_widget_attemptability_v1.py"
    ).read_text(encoding="utf-8")

    _validate_legacy_controls_removed(gui)
    print("LEGACY_UNUSED_APPLY_CONTROLS_REMOVED: PASS")

    _validate_review_routes(completion, assistant_gui)
    print("ASSISTED_DIFF_REVIEW_ROUTES_PRESENT: PASS")

    _validate_local_ai_thread_contract(assistant_gui)
    print("LOCAL_AI_DIFF_REVIEW_QTHREAD_AND_STALE_GUARD: PASS")

    _validate_web_ai_receive_contract(service, assistant_gui)
    print("WEB_AI_DIFF_REVIEW_RECEIVE_CONTRACT: PASS")

    _validate_human_gate_separation(assistant_gui)
    print("ASSISTED_REVIEW_DOES_NOT_AUTO_CONFIRM_HUMAN_GATES: PASS")

    _validate_real_widget_fontdir_preflight(real_widget_validator)
    print("REAL_WIDGET_OFFSCREEN_FONTDIR_PREFLIGHT: PASS")

    _validate_native_stderr_probe()
    print("NATIVE_STDERR_EXITCODE_PROBE_PRESENT: PASS")

    _validate_service_runtime()
    print("DIFF_REVIEW_SERVICE_RUNTIME_CONTRACT: PASS")

    _validate_sizes()
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")

    print("WORKBENCH_ASSISTED_DIFF_REVIEW_AND_UI_CLEANUP: PASS")
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")


def _validate_legacy_controls_removed(gui: str) -> None:
    forbidden = (
        'QPushButton("Legacy Apply Source Changes (Disabled)")',
        'QPushButton("Rollback Last Apply")',
        "Exact apply token:",
        "Exact rollback token:",
        "_large_file_refactor_workbench_apply_token_edit",
        "_large_file_refactor_workbench_rollback_token_edit",
    )
    for marker in forbidden:
        assert marker not in gui, "LEGACY_CONTROL_STILL_PRESENT:" + marker
    assert "Next governed stage: Completion Review and Refactor Authorization." in gui


def _validate_review_routes(completion: str, assistant_gui: str) -> None:
    assert "build_diff_review_assistant_box" in completion
    for label in (
        'QPushButton("Heuristic")',
        'QPushButton("Local AI")',
        'QPushButton("Web AI")',
        'QPushButton("Receive From Web AI")',
    ):
        assert label in assistant_gui, "REVIEW_ROUTE_MISSING:" + label
    assert "sync_diff_review_assistant_controls(window)" in completion


def _validate_local_ai_thread_contract(assistant_gui: str) -> None:
    for marker in (
        "class _LocalDiffReviewReceiver(QObject)",
        "class _LocalDiffReviewWorker(QObject)",
        "thread = QThread()",
        "worker.moveToThread(thread)",
        "thread.started.connect(worker.run)",
        "worker.result_ready.connect(receiver.on_result)",
        "_evidence_identity(evidence)",
        "The stale result was discarded.",
    ):
        assert marker in assistant_gui, "LOCAL_AI_THREAD_MARKER_MISSING:" + marker


def _validate_web_ai_receive_contract(service: str, assistant_gui: str) -> None:
    for marker in (
        "KANDA_WORKBENCH_DIFF_REVIEW_BEGIN",
        "KANDA_WORKBENCH_DIFF_REVIEW_END",
        "parse_web_ai_diff_review_response",
    ):
        assert marker in service, "WEB_AI_SERVICE_MARKER_MISSING:" + marker
    for marker in (
        'QPushButton("Validate Response")',
        'QPushButton("Implement Review")',
        'QPushButton("Clear")',
        'QPushButton("Close")',
        "parse_web_ai_diff_review_response(input_edit.toPlainText())",
        "appendPlainText",
    ):
        assert marker in assistant_gui, "WEB_AI_RECEIVE_MARKER_MISSING:" + marker


def _validate_human_gate_separation(assistant_gui: str) -> None:
    assert ".setChecked(True)" not in assistant_gui
    assert "semantic_review_check" not in assistant_gui
    assert "warning_ack_check" not in assistant_gui
    assert "transaction_confirm_check" not in assistant_gui
    assert "mutates project source" in assistant_gui


def _validate_real_widget_fontdir_preflight(validator: str) -> None:
    required = (
        'os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")',
        "def _configure_offscreen_font_directory() -> str:",
        'os.environ.get("QT_QPA_FONTDIR", "").strip()',
        '("WINDIR", "SystemRoot")',
        'os.environ["QT_QPA_FONTDIR"] = str(candidate)',
        'print("QT_OFFSCREEN_FONTDIR_READY: PASS")',
    )
    for marker in required:
        assert marker in validator, "OFFSCREEN_FONTDIR_MARKER_MISSING:" + marker
    configure_index = validator.index("QT_OFFSCREEN_FONTDIR =")
    pyside_index = validator.index("from PySide6.QtWidgets import")
    assert configure_index < pyside_index, "OFFSCREEN_FONTDIR_CONFIGURED_AFTER_PYSIDE_IMPORT"


def _validate_native_stderr_probe() -> None:
    probe = PROJECT_ROOT / "tools" / "validate_native_stderr_exitcode_classification_v1.py"
    text = probe.read_text(encoding="utf-8")
    required = (
        "BENIGN_NATIVE_STDERR_PROBE",
        "NATIVE_STDERR_EXITCODE_CLASSIFICATION: PASS",
        "file=sys.stderr",
    )
    for value in required:
        assert value in text, "NATIVE_STDERR_PROBE_MARKER_MISSING:" + value


def _validate_service_runtime() -> None:
    from kanda_reasoner_app.manage_architecture.large_file_refactor_planner.workbench_diff_review_assistant import (
        WEB_AI_DIFF_REVIEW_BEGIN,
        WEB_AI_DIFF_REVIEW_END,
        build_heuristic_diff_review,
        build_web_ai_diff_review_prompt,
        format_assistant_panel_appendix,
        parse_web_ai_diff_review_response,
    )

    class Semantic:
        blockers = ()
        warnings = ("W1",)
        public_api_before = ("public_api",)
        public_api_after = ("public_api",)
        size_after = (("facade.py", 250), ("helper.py", 420))
        symbol_movements = (("symbol", "helper.py"),)
        contract_hash = "contract-hash"
        payload_hash = "payload-hash"

        def to_dict(self) -> dict[str, object]:
            return {"warnings": ["W1"], "blockers": []}

    row = SimpleNamespace(
        kind="add",
        old_lineno=None,
        new_lineno=1,
        text="value = 1",
    )
    text_diff = SimpleNamespace(
        status="ready",
        source_label="source.py",
        target_label="preview.py",
        counts={"add": 1, "remove": 0, "hunk": 1},
        warnings=(),
        blockers=(),
        rows=[row],
    )
    evidence = SimpleNamespace(
        semantic_review=Semantic(),
        text_diff=text_diff,
        contract=SimpleNamespace(contract_id="contract-id"),
        dynamic_risks=SimpleNamespace(status="ready", warnings=(), blockers=()),
        shadow_validation=SimpleNamespace(
            status="shadow_validation_pass",
            warnings=(),
            blockers=(),
        ),
    )

    heuristic = build_heuristic_diff_review(evidence)
    assert heuristic.route == "Heuristic"
    assert heuristic.verdict == "review_ready"
    assert "Public API preserved: YES" in heuristic.semantic_review

    prompt = build_web_ai_diff_review_prompt(evidence, r"E:\demo")
    assert prompt.count(WEB_AI_DIFF_REVIEW_BEGIN) == 1
    assert prompt.count(WEB_AI_DIFF_REVIEW_END) == 1

    payload = {
        "schema_version": "1.0",
        "verdict": "review_ready",
        "semantic_review": "semantic ok",
        "text_review": "text ok",
        "correction_plan": ["no change"],
        "warnings": [],
    }
    raw = (
        WEB_AI_DIFF_REVIEW_BEGIN
        + "\n"
        + json.dumps(payload)
        + "\n"
        + WEB_AI_DIFF_REVIEW_END
    )
    imported = parse_web_ai_diff_review_response(raw)
    assert imported.route == "Web AI"
    assert "semantic ok" in format_assistant_panel_appendix(
        imported,
        panel="semantic",
    )

    duplicate = raw + "\n" + raw
    try:
        parse_web_ai_diff_review_response(duplicate)
    except ValueError:
        pass
    else:
        raise AssertionError("DUPLICATE_WEB_AI_MARKERS_NOT_REJECTED")


def _validate_sizes() -> None:
    names = (
        "workbench_gui.py",
        "workbench_completion_gui.py",
        "workbench_diff_review_assistant.py",
        "workbench_diff_review_assistant_gui.py",
        "final_complete_workbench_freeze.py",
    )
    for name in names:
        path = PKG / name
        lines = len(path.read_text(encoding="utf-8").splitlines())
        assert lines <= 500, "MODULE_SIZE_POLICY_FAILED:" + name + ":" + str(lines)


if __name__ == "__main__":
    run_validation()
