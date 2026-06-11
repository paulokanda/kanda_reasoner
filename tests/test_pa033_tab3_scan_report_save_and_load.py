"""Regression tests for Tab 3 scan report path selection contracts."""

from __future__ import annotations

from pathlib import Path

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


class _Combo:
    """Minimal combo-box fake."""

    def __init__(self) -> None:
        self.text = ""
        self.enabled = True
        self.hidden = False

    def clear(self) -> None:
        self.text = ""

    def addItem(self, value: str) -> None:
        self.text = value

    def setCurrentText(self, value: str) -> None:
        self.text = value

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

    def hide(self) -> None:
        self.hidden = True


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

    def setChecked(self, checked: bool) -> None:
        self.checked = bool(checked)

    def setEnabled(self, enabled: bool) -> None:
        self.enabled = bool(enabled)

    def hide(self) -> None:
        self.hidden = True


class _Owner:
    """Minimal Tab 3 owner fake."""

    def __init__(self, project: Path, report: Path | None = None) -> None:
        self._root_path_edit = _LineEdit(str(project))
        self._report_path_edit = _LineEdit(str(report or ""))
        self._target_path_edit = _LineEdit("stale-target.py")
        self._scope_combo = _Combo()
        self._mode_combo = _Combo()
        self._run_button = _Button()
        self._confirm_write_checkbox = _CheckBox()
        self._file_address_checkbox = _CheckBox()
        self.output: list[str] = []
        self.loaded_count = 0

    def _append_text(self, text: str) -> None:
        self.output.append(text)

    def _load_report_rows(self) -> None:
        self.loaded_count += 1


def test_legacy_chooser_sets_report_path_outside_project(tmp_path: Path) -> None:
    """The old chooser injection contract must still set a report path."""
    project = tmp_path / "project"
    project.mkdir()
    report = tmp_path / "reports" / "legacy_report.jsonl"
    report.parent.mkdir()
    owner = _Owner(project)

    ok = scan_only_workflow.ensure_scan_report_path(
        owner,
        chooser=lambda _owner, _default: report,
    )

    assert ok is True
    assert owner._report_path_edit.text() == str(report)


def test_legacy_chooser_rejects_report_path_inside_project(tmp_path: Path) -> None:
    """Legacy chooser compatibility must still reject reports inside project."""
    project = tmp_path / "project"
    project.mkdir()
    report = project / "inside.jsonl"
    owner = _Owner(project)

    ok = scan_only_workflow.ensure_scan_report_path(
        owner,
        chooser=lambda _owner, _default: report,
    )

    assert ok is False
    assert owner._report_path_edit.text() == ""


def test_run_scan_with_legacy_chooser_uses_scan_mode(tmp_path: Path) -> None:
    """A supplied chooser keeps old tests free of Qt dialogs and runs scan mode."""
    project = tmp_path / "project"
    project.mkdir()
    report = tmp_path / "report.jsonl"
    owner = _Owner(project)
    calls: list[str] = []

    scan_only_workflow.run_scan_selected_mode(
        owner,
        lambda _owner, mode: calls.append(mode),
        chooser=lambda _owner, _default: report,
    )

    assert calls == [scan_only_workflow.SCAN_MODE]
    assert owner._scope_combo.text == "Full project"
    assert owner._target_path_edit.text() == ""


if __name__ == "__main__":
    test_root = Path(__file__).resolve().parent / "_tmp_pa033"
    if test_root.exists():
        import shutil

        shutil.rmtree(test_root)
    test_root.mkdir(parents=True)
    tests = [
        test_legacy_chooser_sets_report_path_outside_project,
        test_legacy_chooser_rejects_report_path_inside_project,
        test_run_scan_with_legacy_chooser_uses_scan_mode,
    ]
    for index, test in enumerate(tests, start=1):
        case_dir = test_root / str(index)
        case_dir.mkdir(parents=True)
        test(case_dir)
    print("PA033 Tab 3 scan report save/load tests passed.")
