"""Focused public-contract tests for PA039 Tab 3 review navigation."""

from __future__ import annotations

from kanda_reasoner_app.tab3_manual_review_runtime import inline_corrector_runtime


class _Signal:
    """Small signal fake that stores connected slots."""

    def __init__(self) -> None:
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self, *args):
        for slot in list(self.slots):
            slot(*args)


class _Button:
    """Small button fake with a clicked signal."""

    def __init__(self) -> None:
        self.clicked = _Signal()


class _Item:
    """Small list item fake carrying row data."""

    def __init__(self, row: dict) -> None:
        self.row_data = row

    def data(self, role=None):
        del role
        return self.row_data


class _ReviewList:
    """Small review list fake with current-row navigation."""

    def __init__(self, rows: list[dict]) -> None:
        self.items = [_Item(row) for row in rows]
        self.current = 0 if rows else -1

    def count(self) -> int:
        return len(self.items)

    def currentRow(self) -> int:
        return self.current

    def setCurrentRow(self, row: int) -> None:
        self.current = row

    def currentItem(self):
        if self.current < 0:
            return None
        return self.items[self.current]


class _Owner:
    """Small owner fake for navigation contracts."""

    def __init__(self) -> None:
        self._review_previous_button = _Button()
        self._review_next_button = _Button()
        self._review_reset_button = _Button()
        self._review_list = _ReviewList([
            {"file": "a.py", "target_name": "first"},
            {"file": "b.py", "target_name": "second"},
            {"file": "c.py", "target_name": "third"},
        ])
        self.refreshed_rows = []


def _capture_refresh(owner: _Owner, row: dict | None) -> None:
    owner.refreshed_rows.append(row)


def test_navigation_buttons_accept_qt_clicked_argument(monkeypatch) -> None:
    """Previous, Next, and Reset slots must accept Qt's clicked(bool) argument."""
    owner = _Owner()
    monkeypatch.setattr(
        inline_corrector_runtime,
        "refresh_inline_corrector_for_selection",
        _capture_refresh,
    )

    inline_corrector_runtime.wire_inline_corrector_events(owner)

    owner._review_next_button.clicked.emit(True)
    assert owner._review_list.currentRow() == 1
    assert owner.refreshed_rows[-1]["target_name"] == "second"

    owner._review_previous_button.clicked.emit(False)
    assert owner._review_list.currentRow() == 0
    assert owner.refreshed_rows[-1]["target_name"] == "first"

    owner._review_next_button.clicked.emit(True)
    owner._review_next_button.clicked.emit(True)
    assert owner._review_list.currentRow() == 2

    owner._review_reset_button.clicked.emit(True)
    assert owner._review_list.currentRow() == 0
    assert owner.refreshed_rows[-1]["target_name"] == "first"


def test_navigation_wraps_and_refreshes_selection(monkeypatch) -> None:
    """Direct navigation must wrap around and refresh preview widgets."""
    owner = _Owner()
    monkeypatch.setattr(
        inline_corrector_runtime,
        "refresh_inline_corrector_for_selection",
        _capture_refresh,
    )

    inline_corrector_runtime.select_next_filtered_review_item(owner, -1)
    assert owner._review_list.currentRow() == 2
    assert owner.refreshed_rows[-1]["target_name"] == "third"

    inline_corrector_runtime.select_next_filtered_review_item(owner, 1)
    assert owner._review_list.currentRow() == 0
    assert owner.refreshed_rows[-1]["target_name"] == "first"


if __name__ == "__main__":
    class _MonkeyPatch:
        def setattr(self, target, name, value):
            setattr(target, name, value)

    monkeypatch = _MonkeyPatch()
    test_navigation_buttons_accept_qt_clicked_argument(monkeypatch)
    test_navigation_wraps_and_refreshes_selection(monkeypatch)
    print("PA039 Tab 3 before-correction navigation tests passed.")
