"""Contract tests for Project Symbol Atlas final status module."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.final_status import (  # noqa: E402
    EXPECTED_CLI_COMMANDS,
    EXPECTED_GUI_COMMANDS,
    EXPECTED_GUI_FILES,
    EXPECTED_SOURCE_FILES,
    ProjectSymbolAtlasFinalStatusOptions,
    build_reasoner_symbol_atlas_final_status,
    write_reasoner_symbol_atlas_final_status,
)


def test_reasoner_symbol_atlas_final_status_public_contract() -> None:
    assert "pre-patch-gate" in EXPECTED_CLI_COMMANDS
    assert "pre-patch-gate" in EXPECTED_GUI_COMMANDS
    assert "reasoner_tools_gui_engineering_safety_panel.py" in EXPECTED_GUI_FILES
    assert any(path.endswith("existing_code_finder.py") for path in EXPECTED_SOURCE_FILES)


def test_reasoner_symbol_atlas_final_status_detects_complete_fixture() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        _create_expected_files(root)
        result = build_reasoner_symbol_atlas_final_status(
            ProjectSymbolAtlasFinalStatusOptions(project_root=root)
        )
        assert result.status == "complete"
        assert result.missing_source_files == []
        assert result.missing_gui_files == []
        assert result.missing_focused_tests == []
        assert result.legacy_evidence_required is False


def test_reasoner_symbol_atlas_final_status_writes_reports() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        _create_expected_files(root)
        output_dir = root / "out"
        result = build_reasoner_symbol_atlas_final_status(
            ProjectSymbolAtlasFinalStatusOptions(project_root=root)
        )
        written = write_reasoner_symbol_atlas_final_status(result, output_dir)
        assert Path(written.json_report_path).exists()
        assert Path(written.markdown_report_path).exists()
        assert "PA022 Project Symbol Atlas Final Status" in Path(
            written.markdown_report_path
        ).read_text(encoding="utf-8")


def _create_expected_files(root: Path) -> None:
    for relative_path in EXPECTED_SOURCE_FILES + EXPECTED_GUI_FILES:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fixture\n", encoding="utf-8")
    from kanda_reasoner_app.reasoner_symbol_atlas.final_status import (  # noqa: E402
        EXPECTED_FOCUSED_TESTS,
    )

    for relative_path in EXPECTED_FOCUSED_TESTS:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fixture\n", encoding="utf-8")
    (root / "project_analysis_evidence").mkdir(parents=True, exist_ok=True)


def main() -> int:
    test_reasoner_symbol_atlas_final_status_public_contract()
    test_reasoner_symbol_atlas_final_status_detects_complete_fixture()
    test_reasoner_symbol_atlas_final_status_writes_reports()
    print("Project Symbol Atlas final status contract tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
