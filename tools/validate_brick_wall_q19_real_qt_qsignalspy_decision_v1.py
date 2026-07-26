"""Validate Brick Wall Q19 real Qt and QSignalSpy decision routing."""

from __future__ import annotations

__all__: list[str] = []

import argparse
import json
import re
from pathlib import Path
from typing import Callable, Sequence

from brick_wall_q19_real_qt_decision_contract import (
    mutated_record,
    valid_not_applicable_record,
    valid_required_record,
    validate_record,
)

FEATURE_ID = "brick-wall-q19-real-qt-qsignalspy-validation-decision-enforcement-v1"
PLIB = Path("kanda_prompt_workspace/prompt_library")
BRICK_REL = PLIB / (
    "ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
    "brick_wall_comprehensive_quality_gate.md"
)
BRICK_META_REL = PLIB / "METADATA/brick_wall_comprehensive_quality_gate.meta.json"
BRIDGE_REL = PLIB / (
    "ACTIVE_PROMPTS/05_patch_delivery_and_validation/"
    "router_bridge_governed_implementation.md"
)
BRIDGE_META_REL = PLIB / "METADATA/router_bridge_governed_implementation.meta.json"
Q18_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q18_stale_async_result_rejection_v1.py"
)
Q19_CONTRACT_REL = Path("tools/brick_wall_q19_real_qt_decision_contract.py")
Q19_VALIDATOR_REL = Path(
    "tools/validate_brick_wall_q19_real_qt_qsignalspy_decision_v1.py"
)
QSIGNALSPY_FIXTURE_REL = Path(
    "tools/validate_brick_wall_q19_qsignalspy_runtime_fixture_v1.py"
)
REAL_WIDGET_REL = Path(
    "tools/validate_large_file_refactor_workbench_real_widget_attemptability_v1.py"
)
HEURISTIC_QT_REL = Path(
    "tools/validate_workbench_heuristic_correction_qthread_runtime_v2.py"
)
LOCAL_AI_SETTLEMENT_REL = Path(
    "tools/validate_workbench_local_ai_correction_ui_settlement_real_widget_v1.py"
)
AQR_SESSION_REL = Path("tools/validate_aqr_correction_session_real_widget_v1.py")
OBSERVABILITY_REL = Path(
    "tools/validate_real_widget_observability_transient_fixture_v1.py"
)

BRICK_MARKERS = (
    "### Real Qt/QSignalSpy validation decision (Q19)",
    "REAL QT/QSIGNALSPY VALIDATION DECISION RECORD",
    "mode REAL_QT_QSIGNALSPY/REAL_QT_WIDGET/STATIC_SUFFICIENT",
    "QSignalSpy for material signal delivery/count/order/payload or thread affinity",
    "real widgets for click/enable/visibility/ancestor projection",
    "proceed to Q20 isolated filesystem fixtures YES/NO",
    "Missing PySide6 may define a user-local requirement",
)
BRIDGE_MARKERS = (
    "## Real Qt/QSignalSpy validation decision gate (Q19)",
    "Q19 decision complete and material Qt modes correct: YES / NO / N/A",
    "May proceed to Q20 shared isolated filesystem fixtures gate: YES / NO",
    "## Real Qt/QSignalSpy validation decision bridge",
    "REAL_QT_QSIGNALSPY/REAL_QT_WIDGET/STATIC_SUFFICIENT",
    "static evidence cannot satisfy material Qt behavior",
)
QSIGNALSPY_MARKERS = (
    "from PySide6.QtTest import QSignalSpy",
    "Qt.ConnectionType.QueuedConnection",
    "result_spy = QSignalSpy(receiver.received)",
    "finished_spy = QSignalSpy(thread.finished)",
    "Q19_REAL_QT_QUEUED_SIGNAL_DELIVERY: PASS",
    "Q19_RECEIVER_MAIN_THREAD_AFFINITY: PASS",
    "Q19_QTHREAD_SETTLEMENT: PASS",
    "Q19_QSIGNALSPY_WATCHDOG: PASS",
)
REAL_WIDGET_MARKERS = (
    "QApplication.instance() or QApplication([])",
    "real-widget-validator-watchdog",
    ".click()",
    ".isEnabled()",
    ".isEnabledTo(page)",
)
HEURISTIC_MARKERS = (
    "from PySide6.QtCore import QEventLoop, QTimer",
    "QApplication.instance() or QApplication([])",
    "heartbeat = QTimer()",
    "button.click()",
    "worker.finished.connect(thread.quit)",
)
LOCAL_AI_MARKERS = (
    "QApplication.instance() or QApplication([])",
    "local_button.click()",
    "app.processEvents()",
    "dependency_button.isEnabled()",
)
AQR_MARKERS = (
    "QApplication.instance() or QApplication([])",
    "app.processEvents()",
    ".isEnabled()",
)
OBSERVABILITY_MARKERS = (
    "REAL_WIDGET_VALIDATOR_WATCHDOG_PRESENT",
    "CONTROLLED_VALIDATION_FIXTURES_UNDER_TRANSIENT_GARBAGE_ROOT",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _gate(label: str, ok: bool, detail: str = "") -> None:
    if not ok:
        suffix = " - " + detail if detail else ""
        raise AssertionError(label + ": FAIL" + suffix)
    print(label + ": PASS")


def _require(text: str, markers: Sequence[str], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    _gate(label, not missing, ", ".join(missing))


def _parse_version(value: object) -> tuple[int, ...]:
    if not isinstance(value, str):
        return ()
    try:
        return tuple(int(part) for part in value.split("."))
    except ValueError:
        return ()


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _precode_gate_at_least(text: str, minimum_gate: int) -> bool:
    match = re.search(
        r"After Q(\d+), all applicable pre-code items.*?Q01-Q(\d+) complete YES/NO",
        text,
        re.DOTALL,
    )
    return bool(match and match.group(1) == match.group(2) and int(match.group(1)) >= minimum_gate)


def validate_source(root: Path) -> None:
    brick = _read(root / BRICK_REL)
    bridge = _read(root / BRIDGE_REL)
    brick_meta = _load(root / BRICK_META_REL)
    bridge_meta = _load(root / BRIDGE_META_REL)
    _require(brick, BRICK_MARKERS, "Q19_BRICK_WALL_CONTRACT")
    _gate(
        "Q19_FORWARD_COMPATIBLE_Q20_PRECODE_PROGRESSION",
        _precode_gate_at_least(brick, 19),
    )
    _require(bridge, BRIDGE_MARKERS, "Q19_ROUTER_BRIDGE_CONTRACT")
    _require(
        _read(root / QSIGNALSPY_FIXTURE_REL),
        QSIGNALSPY_MARKERS,
        "Q19_QSIGNALSPY_FIXTURE_STATIC_CONTRACT",
    )
    _require(
        _read(root / REAL_WIDGET_REL),
        REAL_WIDGET_MARKERS,
        "Q19_REAL_WIDGET_CLICK_PROJECTION_CONTRACT",
    )
    _require(
        _read(root / HEURISTIC_QT_REL),
        HEURISTIC_MARKERS,
        "Q19_REAL_QT_THREAD_EVENT_LOOP_CONTRACT",
    )
    _require(
        _read(root / LOCAL_AI_SETTLEMENT_REL),
        LOCAL_AI_MARKERS,
        "Q19_REAL_WIDGET_SETTLEMENT_CONTRACT",
    )
    _require(
        _read(root / AQR_SESSION_REL),
        AQR_MARKERS,
        "Q19_AQR_REAL_WIDGET_CONTROL_CONTRACT",
    )
    _require(
        _read(root / OBSERVABILITY_REL),
        OBSERVABILITY_MARKERS,
        "Q19_REAL_WIDGET_OBSERVABILITY_CONTRACT",
    )
    _gate("Q19_BRICK_VERSION", _parse_version(brick_meta.get("version")) >= (2, 9))
    _gate("Q19_BRIDGE_VERSION", _parse_version(bridge_meta.get("version")) >= (3, 3))
    for label, meta in (("brick", brick_meta), ("bridge", bridge_meta)):
        stage = meta.get("source_stage")
        updated = meta.get("updated_for")
        _gate("Q19_METADATA_ALIGNMENT", _nonempty(stage) and stage == updated, label)
    q18 = _read(root / Q18_VALIDATOR_REL)
    _gate(
        "Q18_FORWARD_COMPATIBLE_Q19_PROGRESSION",
        "proceed to Q19 real Qt/QSignalSpy decision YES/NO" in q18
        and "Q18_FORWARD_COMPATIBLE_Q19_PRECODE_PROGRESSION" in q18
        and '_parse_version(brick_meta.get("version")) >= (2, 8)' in q18
        and '_parse_version(bridge_meta.get("version")) >= (3, 2)' in q18,
    )
    for rel in (
        BRICK_REL,
        BRIDGE_REL,
        Q18_VALIDATOR_REL,
        Q19_CONTRACT_REL,
        Q19_VALIDATOR_REL,
        QSIGNALSPY_FIXTURE_REL,
        REAL_WIDGET_REL,
        HEURISTIC_QT_REL,
        LOCAL_AI_SETTLEMENT_REL,
        AQR_SESSION_REL,
        OBSERVABILITY_REL,
    ):
        lines = len(_read(root / rel).splitlines())
        _gate("Q19_MODULE_SIZE", lines <= 500, f"{rel}={lines}")


def _reject(label: str, mutate: Callable[[dict[str, object]], None]) -> None:
    record = mutated_record()
    mutate(record)
    try:
        validate_record(record)
    except AssertionError:
        _gate(label, True)
        return
    _gate(label, False, "invalid record was accepted")


def validate_semantics() -> None:
    validate_record(valid_required_record())
    _gate("Q19_REQUIRED_QT_DECISION_ACCEPTED", True)
    validate_record(valid_not_applicable_record())
    _gate("Q19_NOT_APPLICABLE_RECORD_ACCEPTED", True)
    cases = (
        (
            "Q19_NEGATIVE_DUPLICATE_CASE",
            lambda record: record["cases"].append(dict(record["cases"][0])),
        ),
        (
            "Q19_NEGATIVE_QSIGNALSPY_MODE_MISSING",
            lambda record: record["cases"][0].update(
                validation_mode="REAL_QT_WIDGET"
            ),
        ),
        (
            "Q19_NEGATIVE_QUEUED_SIGNAL_LIST_MISSING",
            lambda record: record["cases"][0].update(signals=[]),
        ),
        (
            "Q19_NEGATIVE_SIGNAL_ASSERTIONS_MISSING",
            lambda record: record["cases"][0].update(signal_assertions=[]),
        ),
        (
            "Q19_NEGATIVE_THREAD_ASSERTIONS_MISSING",
            lambda record: record["cases"][0].update(thread_assertions=[]),
        ),
        (
            "Q19_NEGATIVE_STATIC_FOR_THREAD_AFFINITY",
            lambda record: record["cases"][0].update(
                validation_mode="STATIC_SUFFICIENT"
            ),
        ),
        (
            "Q19_NEGATIVE_WIDGET_REAL_MODE_MISSING",
            lambda record: record["cases"][1].update(
                validation_mode="STATIC_SUFFICIENT"
            ),
        ),
        (
            "Q19_NEGATIVE_WIDGET_ASSERTIONS_MISSING",
            lambda record: record["cases"][1].update(widget_assertions=[]),
        ),
        (
            "Q19_NEGATIVE_REAL_SUBJECTS_MISSING",
            lambda record: record["cases"][1].update(real_subjects=[]),
        ),
        (
            "Q19_NEGATIVE_WATCHDOG_MISSING",
            lambda record: record["cases"][0].update(
                event_loop_and_watchdog=""
            ),
        ),
        (
            "Q19_NEGATIVE_VALIDATOR_PATH_MISSING",
            lambda record: record["cases"][0].update(validator_path=""),
        ),
        (
            "Q19_NEGATIVE_EXPECTED_MARKERS_MISSING",
            lambda record: record["cases"][0].update(expected_markers=[]),
        ),
        (
            "Q19_NEGATIVE_PYSIDE_REQUIREMENT_MISSING",
            lambda record: record["cases"][0].update(
                environment_requirement="NOT_REQUIRED"
            ),
        ),
        (
            "Q19_NEGATIVE_STATIC_CASE_CARRIES_SIGNAL",
            lambda record: record["cases"][2].update(signals=["unexpected"]),
        ),
        (
            "Q19_NEGATIVE_Q20_PROGRESSION",
            lambda record: record.update(may_proceed_to_q20=False),
        ),
        (
            "Q19_NEGATIVE_CODING_AUTHORIZATION",
            lambda record: record.update(may_begin_coding=True),
        ),
        (
            "Q19_NEGATIVE_SOURCE_WRITE_AUTHORIZATION",
            lambda record: record.update(may_write_source=True),
        ),
    )
    for label, mutate in cases:
        _reject(label, mutate)
    invalid = valid_not_applicable_record()
    invalid["no_qt_evidence"] = []
    try:
        validate_record(invalid)
    except AssertionError:
        _gate("Q19_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", True)
    else:
        _gate("Q19_NEGATIVE_EMPTY_NOT_APPLICABLE_EVIDENCE", False)
    _gate("Q19_REAL_QT_QSIGNALSPY_DECISION_REGRESSION_SET", True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.expanduser().resolve()
    validate_source(root)
    validate_semantics()
    print("VALIDATION OK: " + FEATURE_ID)
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
