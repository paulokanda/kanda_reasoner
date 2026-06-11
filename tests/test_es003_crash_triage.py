from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.engineering_safety.crash_triage import (  # noqa: E402
    CrashTriageInput,
    build_crash_triage_report,
    extract_crash_traceback_frames,
    infer_crash_class,
    infer_crash_implicated_files,
)
from kanda_reasoner_app.engineering_safety.report_writer import (  # noqa: E402
    write_engineering_safety_report,
)


def _sample_traceback() -> str:
    return 'Traceback (most recent call last):\n  File "E:\\developer_tools\\ask_' 'ai_project_reasoner' '\\engineering_safety\\risk_radar.py", line 42, in build_risk_change_radar_report\n    raise NameError(\'demo\')\nNameError: demo\n'


def test_extract_frames_from_traceback() -> None:
    frames = extract_crash_traceback_frames(_sample_traceback(), str(PROJECT_ROOT))
    assert frames
    assert any('ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py' in frame for frame in frames)


def test_infer_crash_class() -> None:
    assert infer_crash_class(_sample_traceback()) == "name_error"
    assert infer_crash_class("") == "no_crash_text"


def test_infer_implicated_files() -> None:
    frames = ['ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py:42 in build']
    files = infer_crash_implicated_files(frames)
    assert files == ['ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py']


def test_build_crash_triage_report() -> None:
    report = build_crash_triage_report(
        CrashTriageInput(
            project_root=str(PROJECT_ROOT),
            traceback_text=_sample_traceback(),
        )
    )
    assert report.report_type == "crash_triage"
    assert report.risk_level in {"medium", "high", "critical"}
    assert "engineering_safety" in report.owning_box
    assert report.affected_files
    assert report.tests_to_run
    assert report.evidence


def test_write_crash_triage_report(tmp_path: Path) -> None:
    report = build_crash_triage_report(
        CrashTriageInput(project_root=str(PROJECT_ROOT), traceback_text=_sample_traceback())
    )
    written = write_engineering_safety_report(report, tmp_path)
    json_path = Path(written["json_path"])
    markdown_path = Path(written["markdown_path"])
    assert json_path.exists()
    assert markdown_path.exists()
    assert "crash_triage" in json_path.read_text(encoding="utf-8")
    assert "Engineering Safety Report" in markdown_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    test_extract_frames_from_traceback()
    test_infer_crash_class()
    test_infer_implicated_files()
    test_build_crash_triage_report()
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        test_write_crash_triage_report(Path(tmp_dir))
    print("ES003 Crash Triage tests passed.")
