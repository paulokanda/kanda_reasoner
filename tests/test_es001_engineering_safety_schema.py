from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.engineering_safety.schemas as schemas
import kanda_reasoner_app.engineering_safety.report_writer as report_writer
from kanda_reasoner_app.engineering_safety import EngineeringSafetyReport


def test_report_schema_normalizes_core_fields() -> None:
    report = EngineeringSafetyReport(
        report_type="risk_change_radar",
        project_root="E:\\developer_tools",
        risk_level="HIGH",
        confidence="Medium",
        owning_box=" engineering_safety ",
        affected_files=["a.py", "", "b.py"],
        tests_to_run="python tests\\test_example.py",
    )

    payload = report.to_dict()

    assert payload["report_type"] == "risk_change_radar"
    assert payload["risk_level"] == "high"
    assert payload["confidence"] == "medium"
    assert payload["owning_box"] == "engineering_safety"
    assert payload["affected_files"] == ["a.py", "b.py"]
    assert payload["tests_to_run"] == ["python tests\\test_example.py"]
    assert payload["human_decision"] == "pending"
    assert payload["validation_status"] == "not_run"
    assert payload["report_id"].startswith("risk_change_radar_")


def test_invalid_report_type_is_rejected() -> None:
    try:
        EngineeringSafetyReport(report_type="unknown", project_root="E:\\developer_tools")
    except ValueError as exc:
        assert "Unsupported engineering safety report type" in str(exc)
    else:
        raise AssertionError("Expected invalid report type to raise ValueError")


def test_report_writer_creates_json_and_markdown(tmp_path: Path) -> None:
    report = EngineeringSafetyReport(
        report_type="crash_triage",
        project_root=str(tmp_path),
        risk_level="medium",
        affected_files=["module.py"],
        root_cause_or_risk_hypothesis="Crash likely comes from an import boundary.",
        suggested_first_action="Open module.py and inspect imports.",
        tests_to_run=["python -m py_compile module.py"],
        rollback_plan="Restore the previous bundle.",
    )

    result = report_writer.write_engineering_safety_report(report, tmp_path)

    json_path = Path(result["json_path"])
    markdown_path = Path(result["markdown_path"])
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert json_path.exists()
    assert markdown_path.exists()
    assert payload["report_type"] == "crash_triage"
    assert "# Engineering Safety Report" in markdown
    assert "Crash likely comes from an import boundary." in markdown



def test_engineering_safety_constants_are_box_scoped() -> None:
    assert hasattr(schemas, "ENGINEERING_SAFETY_VALID_REPORT_TYPES")
    assert hasattr(schemas, "ENGINEERING_SAFETY_VALID_CONFIDENCE")
    assert not hasattr(schemas, "VALID_REPORT_TYPES")
    assert not hasattr(schemas, "VALID_CONFIDENCE")


def test_public_contract_exports_are_directly_importable() -> None:
    package = importlib.import_module("kanda_reasoner_app.engineering_safety")

    for name in package.__all__:
        assert hasattr(package, name), name

    for name in schemas.__all__:
        assert hasattr(schemas, name), name

    for name in report_writer.__all__:
        assert hasattr(report_writer, name), name


if __name__ == "__main__":
    for test_name, test_func in sorted(globals().items()):
        if test_name.startswith("test_") and callable(test_func):
            if test_name == "test_report_writer_creates_json_and_markdown":
                import tempfile

                with tempfile.TemporaryDirectory() as tmp:
                    test_func(Path(tmp))
            else:
                test_func()
    print("ES001 Engineering Safety schema tests passed.")
