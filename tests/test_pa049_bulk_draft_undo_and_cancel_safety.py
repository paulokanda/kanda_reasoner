"""PA049 tests for bulk draft undo and confirmation safety."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.review_bulk_drafts_runtime import (
    generate_bulk_drafts,
    undo_last_bulk_draft_generation,
)


class _TextWidget:
    def __init__(self, value: str) -> None:
        self._value = value

    def text(self) -> str:
        return self._value


class _CheckBox:
    def __init__(self, checked: bool) -> None:
        self._checked = checked

    def isChecked(self) -> bool:
        return self._checked


class _Item:
    def __init__(self, row: dict) -> None:
        self.row_data = row


class _ReviewList:
    def __init__(self, row: dict) -> None:
        self._item = _Item(row)

    def currentItem(self) -> _Item:
        return self._item


class _PlainText:
    def __init__(self) -> None:
        self.value = ""

    def setPlainText(self, value: str) -> None:
        self.value = value


class _Label:
    def __init__(self) -> None:
        self.value = ""

    def setText(self, value: str) -> None:
        self.value = value


class _Owner:
    def __init__(self, root: Path, rows: list[dict]) -> None:
        self._root_path_edit = _TextWidget(str(root))
        self._ai_enabled_checkbox = _CheckBox(False)
        self._report_rows = rows
        self._review_list = _ReviewList(rows[0])
        self._review_original_snippet = _PlainText()
        self._review_corrected_snippet = _PlainText()
        self._review_draft_status_label = _Label()
        self.output: list[str] = []
        self.summary_refreshed = False
        self.confirm_all = True
        self.confirm_calls: list[tuple[str, int]] = []

    def _append_text(self, value: str) -> None:
        self.output.append(value)

    def _matches_review_filter(self, row: dict) -> bool:
        return bool(row.get("visible", True))

    def _refresh_review_summary(self) -> None:
        self.summary_refreshed = True

    def _confirm_bulk_draft_generation(self, scope: str, count: int) -> bool:
        self.confirm_calls.append((scope, count))
        return self.confirm_all


def _row(file_name: str, name: str, visible: bool = True) -> dict:
    return {
        "file": file_name,
        "line": 1,
        "action": "inserted",
        "target_kind": "function",
        "target_name": name,
        "visible": visible,
    }


def test_generate_all_confirmation_cancel_preserves_existing_drafts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
        rows = [_row("module.py", "alpha")]
        rows[0]["draft_docstring"] = "Existing draft."
        owner = _Owner(root, rows)
        owner.confirm_all = False

        summary = generate_bulk_drafts(owner, "all")

        assert summary.generated == 0
        assert rows[0]["draft_docstring"] == "Existing draft."
        assert owner.confirm_calls == [("all", 1)]
        assert getattr(owner, "_last_bulk_draft_snapshot", None) in (None, [])
        assert "cancelled" in "".join(owner.output).lower()


def test_undo_last_bulk_generation_restores_previous_draft_fields() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text(
            "def alpha():\n    return 1\n\ndef beta():\n    return 2\n",
            encoding="utf-8",
        )
        rows = [_row("module.py", "alpha"), _row("module.py", "beta")]
        rows[0]["draft_docstring"] = "Old draft."
        rows[0]["ai_provider"] = "old_provider"
        rows[0]["ai_used_fallback"] = True
        owner = _Owner(root, rows)

        summary = generate_bulk_drafts(owner, "visible")
        assert summary.generated == 2
        assert rows[0]["draft_docstring"] != "Old draft."
        assert rows[1].get("draft_docstring")

        restored = undo_last_bulk_draft_generation(owner)

        assert restored == 2
        assert rows[0]["draft_docstring"] == "Old draft."
        assert rows[0]["ai_provider"] == "old_provider"
        assert rows[0]["ai_used_fallback"] is True
        assert "draft_docstring" not in rows[1]
        assert "selected_draft_source" not in rows[1]
        assert getattr(owner, "_last_bulk_draft_snapshot", []) == []
        assert "restored 2 row" in "".join(owner.output)


def test_undo_without_snapshot_is_safe_noop() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
        owner = _Owner(root, [_row("module.py", "alpha")])

        restored = undo_last_bulk_draft_generation(owner)

        assert restored == 0
        assert "no bulk draft generation" in "".join(owner.output)


if __name__ == "__main__":
    test_generate_all_confirmation_cancel_preserves_existing_drafts()
    test_undo_last_bulk_generation_restores_previous_draft_fields()
    test_undo_without_snapshot_is_safe_noop()
    print("PA049 bulk draft undo and cancel safety tests passed.")
