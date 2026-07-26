"""Semantic contract for Brick Wall Q19 real Qt validation decisions."""

from __future__ import annotations

from copy import deepcopy
from typing import Mapping, Sequence

__all__: list[str] = []

RECORD_FIELDS = (
    "identity_basis",
    "primary_box",
    "qt_behavior_affected",
    "no_qt_evidence",
    "cases",
    "unresolved_cases",
    "blockers",
    "tests",
    "decision",
    "may_proceed_to_q20",
    "may_begin_coding",
    "may_write_source",
)
CASE_FIELDS = (
    "case_id",
    "owner_box",
    "public_facade",
    "behaviors",
    "queued_signal_material",
    "thread_affinity_material",
    "widget_projection_material",
    "static_or_mock_limitations",
    "validation_mode",
    "real_subjects",
    "trigger_path",
    "signals",
    "signal_assertions",
    "thread_assertions",
    "widget_assertions",
    "cancel_timeout_late_scenario",
    "event_loop_and_watchdog",
    "validator_path",
    "expected_markers",
    "environment_requirement",
)
MODES = {
    "REAL_QT_QSIGNALSPY",
    "REAL_QT_WIDGET",
    "STATIC_SUFFICIENT",
}
BEHAVIORS = {
    "queued_signal_delivery",
    "signal_count_order_payload",
    "thread_affinity",
    "thread_settlement",
    "widget_click_path",
    "widget_enabled_projection",
    "widget_visibility_projection",
    "ancestor_enabled_or_visible_projection",
    "pure_source_contract",
}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _text_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _fields(record: Mapping[str, object], fields: Sequence[str]) -> None:
    missing = [field for field in fields if field not in record]
    if missing:
        raise AssertionError("missing fields: " + ", ".join(missing))


def _require_real_common(case: Mapping[str, object]) -> None:
    for field in (
        "owner_box",
        "public_facade",
        "trigger_path",
        "event_loop_and_watchdog",
        "validator_path",
        "environment_requirement",
    ):
        if not _nonempty(case[field]):
            raise AssertionError("missing real Qt field: " + field)
    for field in (
        "real_subjects",
        "static_or_mock_limitations",
        "expected_markers",
    ):
        if not _text_list(case[field]):
            raise AssertionError("missing real Qt list: " + field)
    if case["environment_requirement"] not in {
        "PYSIDE6_AVAILABLE",
        "USER_LOCAL_PYSIDE6_REQUIRED",
    }:
        raise AssertionError("invalid PySide6 environment requirement")


def _validate_case(case: Mapping[str, object]) -> str:
    _fields(case, CASE_FIELDS)
    if not _nonempty(case["case_id"]):
        raise AssertionError("case id missing")
    behaviors = set(_text_list(case["behaviors"]))
    if not behaviors or not behaviors.issubset(BEHAVIORS):
        raise AssertionError("invalid Qt behavior set")
    for field in (
        "queued_signal_material",
        "thread_affinity_material",
        "widget_projection_material",
    ):
        if not isinstance(case[field], bool):
            raise AssertionError("materiality field must be boolean: " + field)
    mode = case["validation_mode"]
    if mode not in MODES:
        raise AssertionError("unknown Qt validation mode")
    queued_or_thread = bool(
        case["queued_signal_material"] or case["thread_affinity_material"]
    )
    widget = bool(case["widget_projection_material"])
    if queued_or_thread:
        if mode != "REAL_QT_QSIGNALSPY":
            raise AssertionError("material queued/thread behavior requires QSignalSpy")
        _require_real_common(case)
        if not _text_list(case["signals"]):
            raise AssertionError("QSignalSpy signals missing")
        if not _text_list(case["signal_assertions"]):
            raise AssertionError("QSignalSpy assertions missing")
        if not _text_list(case["thread_assertions"]):
            raise AssertionError("thread assertions missing")
    elif widget:
        if mode not in {"REAL_QT_WIDGET", "REAL_QT_QSIGNALSPY"}:
            raise AssertionError("material widget projection requires a real widget")
        _require_real_common(case)
        if not _text_list(case["widget_assertions"]):
            raise AssertionError("widget assertions missing")
    else:
        if mode != "STATIC_SUFFICIENT":
            raise AssertionError("non-material Qt case should use static sufficiency")
        if not _text_list(case["static_or_mock_limitations"]):
            raise AssertionError("static sufficiency evidence missing")
        if case["real_subjects"] not in ([], None):
            raise AssertionError("static case carries real subjects")
        if case["signals"] not in ([], None):
            raise AssertionError("static case carries signals")
        if case["environment_requirement"] != "NOT_REQUIRED":
            raise AssertionError("static case requires a Qt environment")
    if queued_or_thread or widget:
        if not _text_list(case["cancel_timeout_late_scenario"]):
            raise AssertionError("real Qt lifecycle scenario missing")
    return str(case["case_id"])


def validate_record(record: Mapping[str, object]) -> None:
    """Validate one complete Q19 decision record."""
    _fields(record, RECORD_FIELDS)
    if not _nonempty(record["identity_basis"]):
        raise AssertionError("identity basis missing")
    if not _nonempty(record["primary_box"]):
        raise AssertionError("primary box missing")
    if not isinstance(record["qt_behavior_affected"], bool):
        raise AssertionError("qt_behavior_affected must be boolean")
    if record["may_begin_coding"] is not False:
        raise AssertionError("Q19 cannot authorize coding")
    if record["may_write_source"] is not False:
        raise AssertionError("Q19 cannot authorize source writes")
    if _text_list(record["unresolved_cases"]):
        raise AssertionError("unresolved Qt cases remain")
    if _text_list(record["blockers"]):
        raise AssertionError("Qt validation blockers remain")
    if not _text_list(record["tests"]):
        raise AssertionError("Q19 tests are missing")
    if record["qt_behavior_affected"] is False:
        if not _text_list(record["no_qt_evidence"]):
            raise AssertionError("not-applicable Qt evidence missing")
        if record["cases"] not in ([], None):
            raise AssertionError("not-applicable record carries cases")
        if record["decision"] != "NOT_APPLICABLE":
            raise AssertionError("not-applicable decision invalid")
        if record["may_proceed_to_q20"] is not True:
            raise AssertionError("not-applicable record cannot progress")
        return
    cases = record["cases"]
    if not isinstance(cases, list) or not cases:
        raise AssertionError("required Qt cases are missing")
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, Mapping):
            raise AssertionError("Qt case is not a mapping")
        case_id = _validate_case(case)
        if case_id in seen:
            raise AssertionError("duplicate Qt case")
        seen.add(case_id)
    if record["decision"] != "COMPLETE":
        raise AssertionError("required Qt decision is not COMPLETE")
    if record["may_proceed_to_q20"] is not True:
        raise AssertionError("Q20 progression missing")


def _base_case(case_id: str) -> dict[str, object]:
    return {
        "case_id": case_id,
        "owner_box": "architecture_review_workbench",
        "public_facade": "canonical_workbench_gui_facade",
        "behaviors": [],
        "queued_signal_material": False,
        "thread_affinity_material": False,
        "widget_projection_material": False,
        "static_or_mock_limitations": [],
        "validation_mode": "STATIC_SUFFICIENT",
        "real_subjects": [],
        "trigger_path": "",
        "signals": [],
        "signal_assertions": [],
        "thread_assertions": [],
        "widget_assertions": [],
        "cancel_timeout_late_scenario": [],
        "event_loop_and_watchdog": "",
        "validator_path": "",
        "expected_markers": [],
        "environment_requirement": "NOT_REQUIRED",
    }


def valid_required_record() -> dict[str, object]:
    """Return a complete required Q19 fixture."""
    signal_case = _base_case("queued_worker_result")
    signal_case.update(
        behaviors=[
            "queued_signal_delivery",
            "signal_count_order_payload",
            "thread_affinity",
            "thread_settlement",
        ],
        queued_signal_material=True,
        thread_affinity_material=True,
        static_or_mock_limitations=[
            "source inspection cannot prove queued delivery or receiver thread",
        ],
        validation_mode="REAL_QT_QSIGNALSPY",
        real_subjects=["QObject worker", "QThread", "main-thread receiver"],
        trigger_path="start worker and deliver queued result",
        signals=["result_ready", "thread.finished"],
        signal_assertions=["exact count", "order", "payload"],
        thread_assertions=["worker thread", "receiver main thread", "settled"],
        cancel_timeout_late_scenario=["late signal has no authority"],
        event_loop_and_watchdog="QCoreApplication event loop with bounded watchdog",
        validator_path="tools/validate_brick_wall_q19_qsignalspy_runtime_fixture_v1.py",
        expected_markers=["Q19_REAL_QT_QUEUED_SIGNAL_DELIVERY: PASS"],
        environment_requirement="USER_LOCAL_PYSIDE6_REQUIRED",
    )
    widget_case = _base_case("workbench_button_projection")
    widget_case.update(
        behaviors=[
            "widget_click_path",
            "widget_enabled_projection",
            "ancestor_enabled_or_visible_projection",
        ],
        widget_projection_material=True,
        static_or_mock_limitations=[
            "pure state tests cannot prove real button or ancestor projection",
        ],
        validation_mode="REAL_QT_WIDGET",
        real_subjects=["real Workbench window", "real QPushButton"],
        trigger_path="click production button after production synchronization",
        widget_assertions=["enabled", "enabledTo", "click reaches handler"],
        cancel_timeout_late_scenario=["terminal settlement restores controls"],
        event_loop_and_watchdog="QApplication processEvents with watchdog",
        validator_path="tools/validate_large_file_refactor_workbench_real_widget_attemptability_v1.py",
        expected_markers=["REAL_WIDGET_STAGE_PASS: QApplication"],
        environment_requirement="USER_LOCAL_PYSIDE6_REQUIRED",
    )
    static_case = _base_case("prompt_metadata_text")
    static_case.update(
        behaviors=["pure_source_contract"],
        static_or_mock_limitations=[
            "no QObject, signal, thread, event loop, or widget behavior is changed",
        ],
        validator_path="tools/validate_brick_wall_q19_real_qt_qsignalspy_decision_v1.py",
        expected_markers=["Q19_NOT_APPLICABLE_RECORD_ACCEPTED: PASS"],
    )
    return {
        "identity_basis": "current Q18 and changed-file inventory",
        "primary_box": "kanda_prompt_workspace/prompt_library",
        "qt_behavior_affected": True,
        "no_qt_evidence": [],
        "cases": [signal_case, widget_case, static_case],
        "unresolved_cases": [],
        "blockers": [],
        "tests": ["required mode matrix", "static substitution rejection"],
        "decision": "COMPLETE",
        "may_proceed_to_q20": True,
        "may_begin_coding": False,
        "may_write_source": False,
    }


def valid_not_applicable_record() -> dict[str, object]:
    """Return an evidence-backed not-applicable Q19 fixture."""
    record = valid_required_record()
    record.update(
        qt_behavior_affected=False,
        no_qt_evidence=[
            "bounded prompt metadata task changes no QObject, signal, or widget",
        ],
        cases=[],
        decision="NOT_APPLICABLE",
    )
    return record


def mutated_record() -> dict[str, object]:
    """Return an independent required fixture for negative tests."""
    return deepcopy(valid_required_record())
