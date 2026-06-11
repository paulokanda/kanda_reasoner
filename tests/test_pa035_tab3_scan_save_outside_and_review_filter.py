"""Regression tests for PA035/PA036 Tab 3 report lifecycle behavior."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime import inline_preview_runtime
from kanda_reasoner_app.tab3_manual_review_runtime import scan_only_workflow


class _LineEdit:
    """Minimal line-edit fake."""

    def __init__(self, value: str = "") -> None:
        self.value = value

    def text(self) -> str:
        return self.value

    def setText(self, value: object) -> None:
        self.value = str(value)

    def clear(self) -> None:
        self.value = ""


class _Owner:
    """Minimal owner fake for report lifecycle tests."""

    def __init__(self, project: Path, report: Path | None = None) -> None:
        self._root_path_edit = _LineEdit(str(project))
        self._report_path_edit = _LineEdit(str(report or ""))
        self.output: list[str] = []
        self.loaded_count = 0

    def _append_text(self, text: str) -> None:
        self.output.append(text)

    def _load_report_rows(self) -> None:
        self.loaded_count += 1


def test_existing_report_yes_loads_without_new_scan(tmp_path: Path) -> None:
    """Choosing yes must load the previous report and skip new scan setup."""
    project = tmp_path / "project"
    project.mkdir()
    report = tmp_path / "previous.jsonl"
    report.write_text("{}\n", encoding="utf-8")
    owner = _Owner(project, report)

    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=lambda _owner, _path: True,
    )

    assert lifecycle == "loaded"
    assert owner.loaded_count == 1
    assert owner._report_path_edit.text() == str(report)


def test_new_scan_uses_project_timestamp_report_name(tmp_path: Path) -> None:
    """New scan reports must use project/date JSONL names in chosen folder."""
    project = tmp_path / "My Project"
    project.mkdir()
    reports = tmp_path / "reports"
    reports.mkdir()
    owner = _Owner(project)

    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner,
        folder_chooser=lambda _owner, _default: reports,
        now_provider=lambda: datetime(2026, 6, 6, 16, 4, 5),
    )

    expected = reports / "my_project_missing_docstrings_20260606_160405.jsonl"
    assert lifecycle == "ready"
    assert owner._report_path_edit.text() == str(expected)


def test_previous_report_can_be_deleted_before_new_scan(tmp_path: Path) -> None:
    """Choosing delete removes the previous report and prepares a new one."""
    project = tmp_path / "demo"
    project.mkdir()
    previous = tmp_path / "previous.jsonl"
    previous.write_text("old\n", encoding="utf-8")
    reports = tmp_path / "reports"
    reports.mkdir()
    owner = _Owner(project, previous)

    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "delete",
        folder_chooser=lambda _owner, _default: reports,
        now_provider=lambda: datetime(2026, 6, 6, 1, 2, 3),
    )

    assert lifecycle == "ready"
    assert not previous.exists()
    assert owner._report_path_edit.text() == str(
        reports / "demo_missing_docstrings_20260606_010203.jsonl"
    )


def test_report_folder_inside_project_is_rejected(tmp_path: Path) -> None:
    """A report destination inside the selected project must cancel setup."""
    project = tmp_path / "project"
    project.mkdir()
    inside = project / "reports"
    inside.mkdir()
    owner = _Owner(project)

    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner,
        folder_chooser=lambda _owner, _default: inside,
    )

    assert lifecycle == "cancelled"
    assert owner._report_path_edit.text() == ""


def test_reviewable_filter_excludes_non_docstring_rows() -> None:
    """Review filter must exclude file-address and already-existing rows."""
    assert inline_preview_runtime.is_reviewable_docstring_row(
        {"action": "inserted", "target_kind": "method"}
    )
    assert not inline_preview_runtime.is_reviewable_docstring_row(
        {"action": "inserted", "target_kind": "file_address"}
    )
    assert not inline_preview_runtime.is_reviewable_docstring_row(
        {"action": "skipped", "target_kind": "function"}
    )
    assert not inline_preview_runtime.is_reviewable_docstring_row(
        {"action": "inserted", "target_kind": "function", "reason": "already exists"}
    )


if __name__ == "__main__":
    test_root = Path(__file__).resolve().parent / "_tmp_pa035"
    if test_root.exists():
        import shutil

        shutil.rmtree(test_root)
    test_root.mkdir(parents=True)
    tests = [
        test_existing_report_yes_loads_without_new_scan,
        test_new_scan_uses_project_timestamp_report_name,
        test_previous_report_can_be_deleted_before_new_scan,
        test_report_folder_inside_project_is_rejected,
    ]
    for index, test in enumerate(tests, start=1):
        case_dir = test_root / str(index)
        case_dir.mkdir(parents=True)
        test(case_dir)
    test_reviewable_filter_excludes_non_docstring_rows()
    print("PA035 Tab 3 scan save outside and review filter tests passed.")
