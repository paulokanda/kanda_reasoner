"""Final governance/status checks for Tab 3 manual review workflow."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = (
    ROOT
    / "_project_reference"
    / "ACTIVE_PROJECT_ GOVERNANCE"
    / "TAB3_MANUAL_REVIEW_FINAL_STATUS.md"
)
HELP = (
    ROOT
    / 'ask_' 'ai_project_reasoner'
    / "insert_missing_docstrings_gui"
    / "insert_missing_docstrings_gui_help"
)


EXPECTED_WARNING_FILES = {
    "layout_builder.py",
    "manual_docstring_review_batch.py",
    "manual_docstring_review_editor.py",
    "manual_docstring_review_export.py",
    "manual_docstring_review_support.py",
    "report_review_panel.py",
}


def test_final_status_report_documents_expected_warning_state() -> None:
    text = STATUS.read_text(encoding="utf-8")

    assert "Errors: 0" in text
    assert "Warnings: 6" in text
    assert "MIXED_RESPONSIBILITY_FILE only" in text
    assert "Workflow: pass=8 fail=0 warn=0 skip=3" in text
    for file_name in EXPECTED_WARNING_FILES:
        assert file_name in text


def test_manual_review_feature_files_exist() -> None:
    expected_helpers = {
        "manual_docstring_review_ai.py",
        "manual_docstring_review_batch.py",
        "manual_docstring_review_export.py",
        "manual_docstring_review_heuristic.py",
        "manual_docstring_review_preview.py",
        "manual_docstring_review_support.py",
        "manual_docstring_review_editor.py",
    }

    missing = [name for name in expected_helpers if not (HELP / name).is_file()]
    assert not missing


def test_final_feature_surface_is_present() -> None:
    editor = (HELP / "manual_docstring_review_editor.py").read_text(encoding="utf-8")
    batch = (HELP / "manual_docstring_review_batch.py").read_text(encoding="utf-8")
    preview = (HELP / "manual_docstring_review_preview.py").read_text(encoding="utf-8")
    ai = (HELP / "manual_docstring_review_ai.py").read_text(encoding="utf-8")
    heuristic = (HELP / "manual_docstring_review_heuristic.py").read_text(encoding="utf-8")

    assert 'QPushButton("Apply approved batch")' in editor
    assert 'QPushButton("Preview approved only")' in editor
    assert "def apply_approved_review_batch(" in batch
    assert "py_compile.compile(str(path), doraise=True)" in batch
    assert "def build_approved_review_preview(" in preview
    assert "def suggest_manual_review_docstring(" in ai
    assert "def suggest_manual_review_heuristic(" in heuristic


def test_touched_modules_remain_under_size_threshold() -> None:
    for path in HELP.glob("manual_docstring_review_*.py"):
        assert len(path.read_text(encoding="utf-8").splitlines()) < 500, path


if __name__ == "__main__":
    test_final_status_report_documents_expected_warning_state()
    test_manual_review_feature_files_exist()
    test_final_feature_surface_is_present()
    test_touched_modules_remain_under_size_threshold()
    print("T3R022 Tab 3 manual review final status tests passed.")
