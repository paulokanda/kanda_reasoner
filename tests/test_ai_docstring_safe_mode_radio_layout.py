
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED,
    SAFE_MODE_ACTUAL_WIRING_STATUS_NOT_AVAILABLE,
    SAFE_MODE_RADIO_LABEL,
    install_safe_mode_actual_tab3_wiring,
    install_safe_mode_radio_button,
    refresh_safe_mode_actual_tab3_wiring,
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


class FakeWorkerEdit:
    """Small worker-script field double."""

    def __init__(self, parent: object | None = None) -> None:
        self._parent = parent

    def parent(self) -> object | None:
        return self._parent


class FakeBoxLayout:
    """Layout double using indexOf and insertWidget."""

    def __init__(self, worker: object) -> None:
        self.items = [worker]

    def indexOf(self, widget: object) -> int:
        try:
            return self.items.index(widget)
        except ValueError:
            return -1

    def insertWidget(self, index: int, widget: object) -> None:
        self.items.insert(index, widget)

    def addWidget(self, widget: object) -> None:
        self.items.append(widget)

    def count(self) -> int:
        return len(self.items)

    def itemAt(self, index: int):
        return FakeLayoutItem(self.items[index])


class FakeGridLayout(FakeBoxLayout):
    """Layout double using getItemPosition and grid addWidget."""

    def __init__(self, worker: object) -> None:
        super().__init__(worker)
        self.added = []

    def getItemPosition(self, index: int):
        if index < 0:
            raise IndexError(index)
        return 0, index, 1, 1

    def addWidget(self, widget: object, row: int = 0, column: int = 0, *_args) -> None:
        self.added.append((widget, row, column))


class FakeLayoutItem:
    """QLayoutItem-like double."""

    def __init__(self, widget: object) -> None:
        self._widget = widget

    def widget(self) -> object:
        return self._widget


class FakeHost:
    """Host double with Worker Script field and a layout."""

    def __init__(self, layout_kind: str = "box") -> None:
        self._worker_path_edit = FakeWorkerEdit()
        if layout_kind == "grid":
            self.main_layout = FakeGridLayout(self._worker_path_edit)
        else:
            self.main_layout = FakeBoxLayout(self._worker_path_edit)


class SafeModeRadioLayoutRepairTests(unittest.TestCase):
    """Validate the compact Safe Mode radio layout repair."""

    def test_radio_button_is_added_after_worker_script_field_and_checked(self) -> None:
        host = FakeHost()

        result = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED, result.status)
        self.assertIsNotNone(result.radio)
        self.assertEqual(SAFE_MODE_RADIO_LABEL, result.radio.label)
        self.assertTrue(result.radio.checked)
        self.assertIs(host.main_layout.items[1], result.radio)
        self.assertTrue(safe_mode_radio_is_enabled(host))

    def test_actual_wiring_installs_compact_radio_without_panel_mount(self) -> None:
        host = FakeHost()

        result = install_safe_mode_actual_tab3_wiring(host)

        self.assertIn(
            result.status,
            {
                SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED,
                SAFE_MODE_ACTUAL_WIRING_STATUS_NOT_AVAILABLE,
            },
        )
        self.assertFalse(hasattr(host, "_safe_mode_panel_widget"))

    def test_radio_install_is_idempotent_and_stays_checked(self) -> None:
        host = FakeHost()

        first = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )
        first.radio.setChecked(False)
        second = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertIs(first.radio, second.radio)
        self.assertTrue(second.radio.checked)
        self.assertEqual(2, len(host.main_layout.items))

    def test_grid_layout_places_radio_to_the_right_of_worker_field(self) -> None:
        host = FakeHost(layout_kind="grid")

        result = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(result.success)
        self.assertEqual(1, len(host.main_layout.added))
        radio, row, column = host.main_layout.added[0]
        self.assertIs(radio, result.radio)
        self.assertEqual(0, row)
        self.assertEqual(1, column)

    def test_missing_worker_field_fails_safely(self) -> None:
        host = object()

        result = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertFalse(result.success)
        self.assertEqual(SAFE_MODE_ACTUAL_WIRING_STATUS_NOT_AVAILABLE, result.status)

    def test_refresh_rechecks_existing_radio(self) -> None:
        host = FakeHost()
        install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )
        host._safe_mode_radio.setChecked(False)

        result = refresh_safe_mode_actual_tab3_wiring(host)

        self.assertTrue(result.success)
        self.assertTrue(host._safe_mode_radio.checked)


if __name__ == "__main__":
    unittest.main()
