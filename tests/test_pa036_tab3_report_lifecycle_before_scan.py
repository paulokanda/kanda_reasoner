"""Focused tests for PA036 Tab 3 report lifecycle before scan."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from kanda_reasoner_app.tab3_manual_review_runtime import scan_only_workflow


class _LineEdit:
    """Minimal line-edit fake."""

    def __init__(self, value: str = "") -> None:
        self.value = value

    def text(self) -> str:
        return self.value

    def setText(self, value: str) -> None:
        self.value = value

    def clear(self) -> None:
        self.value = ""


class _Combo:
    """Minimal combo fake."""

    def __init__(self) -> None:
        self.text = ""
        self.items: list[str] = []

    def clear(self) -> None:
        self.items.clear()

    def addItem(self, value: str) -> None:
        self.items.append(value)

    def setCurrentText(self, value: str) -> None:
        self.text = value


class _Button:
    """Minimal button fake."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, value: str) -> None:
        self.text = value


class _CheckBox:
    """Minimal checkbox fake."""

    def __init__(self) -> None:
        self.checked = True
        self.enabled = True
        self.hidden = False

    def setChecked(self, value: bool) -> None:
        self.checked = bool(value)

    def setEnabled(self, value: bool) -> None:
        self.enabled = bool(value)

    def hide(self) -> None:
        self.hidden = True


class _Owner:
    """Minimal Tab 3 owner fake."""

    def __init__(self, root: Path, report: Path | None = None) -> None:
        self._root_path_edit = _LineEdit(str(root))
        self._report_path_edit = _LineEdit(str(report or ""))
        self._target_path_edit = _LineEdit("stale-target")
        self._scope_combo = _Combo()
        self._mode_combo = _Combo()
        self._run_button = _Button()
        self._confirm_write_checkbox = _CheckBox()
        self._file_address_checkbox = _CheckBox()
        self.output: list[str] = []
        self.loaded_count = 0
        self.saved_count = 0

    def _append_text(self, text: str) -> None:
        self.output.append(text)

    def _load_report_rows(self) -> None:
        self.loaded_count += 1

    def _save_prefs(self) -> None:
        self.saved_count += 1


def test_yes_loads_previous_report_without_scan(tmp_path: Path) -> None:
    """Choosing yes must load the previous report and skip scanning."""
    project = tmp_path / "fake_project"
    project.mkdir()
    report = tmp_path / "old_missing_docstrings.jsonl"
    report.write_text('{"ok": true}\n', encoding="utf-8")
    owner = _Owner(project, report)
    calls: list[str] = []

    result = scan_only_workflow.run_scan_selected_mode(
        owner,
        lambda _owner, mode: calls.append(mode),
        reuse_prompt=lambda _owner, _path: True,
    )

    assert result is None
    assert calls == []
    assert owner.loaded_count == 1
    assert owner._report_path_edit.text() == str(report)
    assert owner._scope_combo.text == "Full project"
    assert owner._target_path_edit.text() == ""


def test_no_leave_then_scan_uses_project_timestamp_name(tmp_path: Path) -> None:
    """Choosing no and leave must scan into a new project/date report name."""
    project = tmp_path / "My Fake Project"
    project.mkdir()
    old_report = tmp_path / "old_missing_docstrings.jsonl"
    old_report.write_text('{"old": true}\n', encoding="utf-8")
    reports = tmp_path / "reports"
    reports.mkdir()
    owner = _Owner(project, old_report)
    calls: list[str] = []

    scan_only_workflow.run_scan_selected_mode(
        owner,
        lambda _owner, mode: calls.append(mode),
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "leave",
        folder_chooser=lambda _owner, _default: reports,
    )

    expected = reports / "my_fake_project_missing_docstrings_20260606_160405.jsonl"
    # Use direct lifecycle check for deterministic timestamp.
    owner2 = _Owner(project, old_report)
    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner2,
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "leave",
        folder_chooser=lambda _owner, _default: reports,
        now_provider=lambda: datetime(2026, 6, 6, 16, 4, 5),
    )

    assert lifecycle == "ready"
    assert owner2._report_path_edit.text() == str(expected)
    assert old_report.exists()


def test_no_delete_removes_previous_then_sets_new_report_path(tmp_path: Path) -> None:
    """Choosing delete must remove the old report before a new scan."""
    project = tmp_path / "demo"
    project.mkdir()
    old_report = tmp_path / "old.jsonl"
    old_report.write_text("old\n", encoding="utf-8")
    reports = tmp_path / "reports"
    reports.mkdir()
    owner = _Owner(project, old_report)

    lifecycle = scan_only_workflow.prepare_scan_report_lifecycle(
        owner,
        reuse_prompt=lambda _owner, _path: False,
        previous_action_prompt=lambda _owner, _path: "delete",
        folder_chooser=lambda _owner, _default: reports,
        now_provider=lambda: datetime(2026, 6, 6, 1, 2, 3),
    )

    assert lifecycle == "ready"
    assert not old_report.exists()
    assert owner._report_path_edit.text() == str(
        reports / "demo_missing_docstrings_20260606_010203.jsonl"
    )


def test_cancel_folder_cancels_scan(tmp_path: Path) -> None:
    """Cancelling the report folder selection must cancel the scan."""
    project = tmp_path / "demo"
    project.mkdir()
    owner = _Owner(project)
    calls: list[str] = []

    scan_only_workflow.run_scan_selected_mode(
        owner,
        lambda _owner, mode: calls.append(mode),
        folder_chooser=lambda _owner, _default: None,
    )

    assert calls == []
    assert "cancelled" in "".join(owner.output).lower()


def test_legacy_file_chooser_contract_still_works(tmp_path: Path) -> None:
    """Supplying chooser keeps the legacy PA033/PA035 test contract alive."""
    project = tmp_path / "demo"
    project.mkdir()
    report = tmp_path / "legacy_report.jsonl"
    owner = _Owner(project)

    ok = scan_only_workflow.ensure_scan_report_path(
        owner,
        chooser=lambda _owner, _default: report,
    )

    assert ok is True
    assert owner._report_path_edit.text() == str(report)


if __name__ == "__main__":
    test_root = Path(__file__).resolve().parent / "_tmp_pa036"
    if test_root.exists():
        import shutil

        shutil.rmtree(test_root)
    test_root.mkdir(parents=True)
    for index, test in enumerate(
        [
            test_yes_loads_previous_report_without_scan,
            test_no_leave_then_scan_uses_project_timestamp_name,
            test_no_delete_removes_previous_then_sets_new_report_path,
            test_cancel_folder_cancels_scan,
            test_legacy_file_chooser_contract_still_works,
        ],
        start=1,
    ):
        case_dir = test_root / str(index)
        case_dir.mkdir(parents=True)
        test(case_dir)
    print("PA036 Tab 3 report lifecycle before scan tests passed.")
