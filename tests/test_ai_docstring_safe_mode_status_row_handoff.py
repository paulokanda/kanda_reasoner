
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode.actual_tab3_wiring import (
    SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED,
    SAFE_MODE_RADIO_LABEL,
    ensure_safe_mode_radio_button,
    move_safe_mode_radio_to_layout,
    safe_mode_radio_is_enabled,
)


class FakeRadio:
    """Small radio-button double."""

    def __init__(self, label: str, parent: object) -> None:
        self.label = label
        self.parent = parent
        self.checked = False
        self.tooltip = ""

    def setChecked(self, checked: bool) -> None:
        self.checked = bool(checked)

    def isChecked(self) -> bool:
        return self.checked

    def setToolTip(self, text: str) -> None:
        self.tooltip = text

    def setParent(self, parent: object | None) -> None:
        self.parent = parent


class FakeHost:
    """Small host double."""


class FakeStatusLayout:
    """Status/source row layout double."""

    def __init__(self) -> None:
        self.items = []

    def addSpacing(self, value: int) -> None:
        self.items.append(("spacing", value))

    def addWidget(self, widget: object, stretch: int = 0) -> None:
        self.items.append(("widget", widget, stretch))

    def insertSpacing(self, index: int, value: int) -> None:
        self.items.insert(index, ("spacing", value))

    def insertWidget(self, index: int, widget: object, stretch: int = 0) -> None:
        self.items.insert(index, ("widget", widget, stretch))


class SafeModeStatusRowHandoffTests(unittest.TestCase):
    """Validate explicit host-row handoff for the Safe Mode radio button."""

    def test_ensure_radio_creates_checked_radio_without_layout_placement(self) -> None:
        host = FakeHost()

        result = ensure_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED, result.status)
        self.assertEqual(SAFE_MODE_RADIO_LABEL, result.radio.label)
        self.assertTrue(result.radio.checked)
        self.assertTrue(safe_mode_radio_is_enabled(host))

    def test_move_radio_to_status_row_inserts_at_requested_index(self) -> None:
        host = FakeHost()
        layout = FakeStatusLayout()
        layout.items.append(("existing", "source-row-prefix"))

        result = move_safe_mode_radio_to_layout(
            host,
            layout,
            insert_index=1,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(result.success)
        self.assertEqual(("existing", "source-row-prefix"), layout.items[0])
        self.assertEqual(("spacing", 12), layout.items[1])
        self.assertIs(layout.items[2][1], result.radio)
        self.assertTrue(result.radio.checked)

    def test_move_radio_to_status_row_is_idempotent(self) -> None:
        host = FakeHost()
        layout = FakeStatusLayout()

        first = move_safe_mode_radio_to_layout(
            host,
            layout,
            insert_index=None,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )
        second = move_safe_mode_radio_to_layout(
            host,
            layout,
            insert_index=None,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertIs(first.radio, second.radio)
        self.assertEqual(2, len(layout.items))

    def test_lazy_tabs_source_contains_tab3_handoff_call(self) -> None:
        from pathlib import Path

        source = Path(
            'ask_' 'ai_project_reasoner' '/reasoner_tools_gui_shell/lazy_tabs.py'
        ).read_text(encoding="utf-8")

        self.assertIn("_move_tab3_safe_mode_radio_to_status_row", source)
        self.assertIn('ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui.py', source)
        self.assertIn("move_safe_mode_radio_to_layout", source)


if __name__ == "__main__":
    unittest.main()
