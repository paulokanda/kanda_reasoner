from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.engineering_safety.risk_radar import (  # noqa: E402
    RiskChangeRadarInput,
    build_risk_change_radar_report,
    infer_risk_change_affected_boxes,
    normalize_risk_change_path,
    score_risk_change,
)
from kanda_reasoner_app.engineering_safety.report_writer import (  # noqa: E402
    write_engineering_safety_report,
)


def test_normalize_risk_change_path() -> None:
    assert normalize_risk_change_path('.\\ask_' 'ai_project_reasoner' '\\engineering_safety\\risk_radar.py') == 'ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py'


def test_infer_boxes_from_paths() -> None:
    boxes = infer_risk_change_affected_boxes([
        'ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py',
        "tests/test_es002_risk_change_radar.py",
    ])
    assert "engineering_safety" in boxes
    assert "tests" in boxes


def test_score_and_build_report() -> None:
    input_data = RiskChangeRadarInput(
        project_root=str(PROJECT_ROOT),
        changed_files=[
            'ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py',
            "tests/test_es002_risk_change_radar.py",
        ],
        validation_output_text="No validation issues.",
    )
    risk_level, score, evidence = score_risk_change(input_data)
    assert risk_level in {"low", "medium", "high", "critical"}
    assert score >= 1
    assert evidence
    report = build_risk_change_radar_report(input_data)
    assert report.report_type == "risk_change_radar"
    assert report.project_root
    assert report.affected_files
    assert "engineering_safety" in report.owning_box
    assert report.tests_to_run
    assert report.evidence


def test_write_risk_radar_report(tmp_path: Path) -> None:
    report = build_risk_change_radar_report(
        RiskChangeRadarInput(
            project_root=str(PROJECT_ROOT),
            changed_files=["_project_reference/ACTIVE_PROJECT_ GOVERNANCE/REASONER_PROJECT_CANON.json"],
            bundle_manifest_text="governance update",
        )
    )
    written = write_engineering_safety_report(report, tmp_path)
    json_path = Path(written["json_path"])
    markdown_path = Path(written["markdown_path"])
    assert json_path.exists()
    assert markdown_path.exists()
    assert "risk_change_radar" in json_path.read_text(encoding="utf-8")
    assert "Engineering Safety Report" in markdown_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_normalize_risk_change_path()
    test_infer_boxes_from_paths()
    test_score_and_build_report()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_write_risk_radar_report(Path(tmp_dir))
    print("ES002 Risk Change Radar tests passed.")
