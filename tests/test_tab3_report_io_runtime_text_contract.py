"""Behavior tests for the public Tab 3 report IO runtime contract."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.report_io_runtime import (
    report_text_for_export,
    set_current_report_path,
)


class _Edit:
    def __init__(self, text: str = "") -> None:
        self._text = text

    def text(self) -> str:
        return self._text

    def setText(self, text: str) -> None:
        self._text = text


class _Owner:
    def __init__(self, report_path: Path | None = None) -> None:
        self._report_path_edit = _Edit(str(report_path or ""))
        self._root_path_edit = _Edit(str(Path.cwd()))
        self._report_rows = []
        self.saved = False
        self.loaded = False
        self.output = ""

    def _effective_report_path(self) -> str:
        return self._report_path_edit.text()

    def _save_prefs(self) -> None:
        self.saved = True

    def _load_report_rows(self) -> None:
        self.loaded = True

    def _append_text(self, text: str) -> None:
        self.output += text


def test_report_text_for_export_prefers_existing_report_file() -> None:
    """Existing report file content is copied exactly."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "report.jsonl"
        path.write_text('{"file":"a.py"}\n', encoding="utf-8")
        owner = _Owner(path)
        assert report_text_for_export(owner) == '{"file":"a.py"}\n'


def test_report_text_for_export_falls_back_to_loaded_rows() -> None:
    """Loaded report rows can be exported when no report file exists."""
    owner = _Owner()
    owner._report_rows = [{"file": "a.py", "name": "alpha"}]
    text = report_text_for_export(owner)
    assert '"file": "a.py"' in text
    assert text.endswith("\n")


def test_set_current_report_path_updates_owner_and_persists_preferences() -> None:
    """Loading or saving a report updates the visible report path."""
    owner = _Owner()
    set_current_report_path(owner, Path("C:/Reports/report.jsonl"))
    assert owner._report_path_edit.text().endswith("report.jsonl")
    assert owner.saved is True


if __name__ == "__main__":
    test_report_text_for_export_prefers_existing_report_file()
    test_report_text_for_export_falls_back_to_loaded_rows()
    test_set_current_report_path_updates_owner_and_persists_preferences()
    print("Tab 3 report IO runtime text contract tests passed.")
