"""PA048 tests for Tab 3 bulk draft generation."""

from __future__ import annotations

import tempfile
from pathlib import Path

from kanda_reasoner_app.tab3_manual_review_runtime.ai_docstring_provider_runtime import (
    AIProviderResult,
)
from kanda_reasoner_app.tab3_manual_review_runtime.review_bulk_drafts_runtime import (
    BulkDraftSummary,
    generate_bulk_drafts,
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


class _Owner:
    def __init__(self, root: Path, rows: list[dict], ai_enabled: bool = False) -> None:
        self._root_path_edit = _TextWidget(str(root))
        self._ai_enabled_checkbox = _CheckBox(ai_enabled)
        self._report_rows = rows
        self._review_list = _ReviewList(rows[0])
        self.output: list[str] = []
        self.summary_refreshed = False
        self.bulk_confirmations: list[tuple[str, int]] = []
        self._review_original_snippet = _PlainText()
        self._review_corrected_snippet = _PlainText()
        self._review_draft_status_label = _Label()

    def _append_text(self, value: str) -> None:
        self.output.append(value)

    def _matches_review_filter(self, row: dict) -> bool:
        return bool(row.get("visible", True))

    def _refresh_review_summary(self) -> None:
        self.summary_refreshed = True

    def _confirm_bulk_draft_generation(self, scope: str, count: int) -> bool:
        self.bulk_confirmations.append((scope, count))
        return True


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


def _row(file_name: str, name: str, visible: bool = True) -> dict:
    return {
        "file": file_name,
        "line": 1,
        "action": "inserted",
        "target_kind": "function",
        "target_name": name,
        "visible": visible,
    }


def test_bulk_generates_heuristic_drafts_for_visible_reviewable_rows() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text(
            "def alpha():\n    return 1\n\ndef beta():\n    return 2\n",
            encoding="utf-8",
        )
        rows = [
            _row("module.py", "alpha", visible=True),
            _row("module.py", "beta", visible=False),
            {"file": "module.py", "line": 1, "action": "skipped", "target_kind": "function"},
        ]
        owner = _Owner(root, rows, ai_enabled=False)

        summary = generate_bulk_drafts(owner, "visible")

        assert isinstance(summary, BulkDraftSummary)
        assert summary.scope == "visible"
        assert summary.generated == 1
        assert summary.skipped == 1
        assert summary.failed == 0
        assert rows[0]["selected_draft_source"] == "heuristic"
        assert rows[0]["draft_docstring"].strip()
        assert "draft_docstring" not in rows[1]
        assert owner.summary_refreshed is True
        assert "generated=1" in "".join(owner.output)


def test_bulk_ai_all_rows_uses_provider_and_counts_fallbacks() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
        rows = [
            _row("module.py", "alpha", visible=True),
            {"file": "module.py", "line": 1, "action": "ignored", "target_kind": "function"},
        ]
        owner = _Owner(root, rows, ai_enabled=True)

        def _failing_provider(request: object) -> AIProviderResult:
            del request
            return AIProviderResult(
                provider_name="fake_local_ai",
                success=False,
                docstring_body="",
                status="failed",
                error_message="offline",
                used_fallback=False,
            )

        owner._ai_docstring_provider = _failing_provider
        summary = generate_bulk_drafts(owner, "all")

        assert summary.generated == 1
        assert summary.fallback == 1
        assert summary.skipped == 1
        assert rows[0]["ai_provider"] == "heuristic_fallback"
        assert rows[0]["ai_used_fallback"] is True
        assert rows[0]["selected_draft_source"] == "heuristic_fallback"
        assert rows[0]["draft_docstring"].strip()
        output_text = "".join(owner.output)
        assert "fallback=1" in output_text
        assert "AI error: offline" in output_text


def test_bulk_selected_scope_uses_current_review_row_only() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "module.py").write_text("def alpha():\n    return 1\n", encoding="utf-8")
        rows = [_row("module.py", "alpha"), _row("module.py", "beta")]
        owner = _Owner(root, rows, ai_enabled=False)

        summary = generate_bulk_drafts(owner, "selected")

        assert summary.generated == 1
        assert rows[0].get("draft_docstring")
        assert not rows[1].get("draft_docstring")


if __name__ == "__main__":
    test_bulk_generates_heuristic_drafts_for_visible_reviewable_rows()
    test_bulk_ai_all_rows_uses_provider_and_counts_fallbacks()
    test_bulk_selected_scope_uses_current_review_row_only()
    print("PA048 Tab 3 AI bulk draft generation tests passed.")
