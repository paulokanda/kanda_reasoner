
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED,
    SAFE_MODE_ACTUAL_WIRING_STATUS_NOT_AVAILABLE,
    SAFE_MODE_HOST_HOOK_STATUS_REFRESHED,
    SafeModeButtonState,
    SafeModeGuiSnapshot,
    build_safe_mode_actual_button_state,
    build_safe_mode_actual_callbacks,
    build_safe_mode_actual_snapshot,
    install_safe_mode_actual_tab3_wiring,
    refresh_safe_mode_actual_tab3_wiring,
    refresh_safe_mode_tab3_host_hook,
)


class FakeLayout:
    """Collect widgets mounted by the actual wiring path."""

    def __init__(self) -> None:
        self.widgets = []

    def addWidget(self, widget) -> None:
        self.widgets.append(widget)


class FakeLabel:
    """Small label double."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, text) -> None:
        self.text = text


class FakeButton:
    """Small button double."""

    def __init__(self) -> None:
        self.enabled = False
        self.text = ""

    def setText(self, text) -> None:
        self.text = text

    def setEnabled(self, enabled) -> None:
        self.enabled = bool(enabled)


class FakePanel:
    """Small Safe Mode panel double."""

    def __init__(self) -> None:
        self._safe_mode_panel_parts = {
            "folder_label": FakeLabel(),
            "progress_label": FakeLabel(),
            "pending_label": FakeLabel(),
            "review_label": FakeLabel(),
            "status_label": FakeLabel(),
            "buttons": {
                "accept": FakeButton(),
                "edit": FakeButton(),
                "regenerate": FakeButton(),
                "fallback": FakeButton(),
                "skip": FakeButton(),
                "reject": FakeButton(),
                "clear": FakeButton(),
                "apply_folder": FakeButton(),
                "next_folder": FakeButton(),
            },
        }


class FakeRadio:
    """Small radio button double."""

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
    """Small worker path field double."""

    def __init__(self, parent: object | None = None) -> None:
        self._parent = parent

    def parent(self) -> object | None:
        return self._parent


class FakeBoxLayout:
    """Layout double using indexOf and insertWidget."""

    def __init__(self, worker: object | None = None) -> None:
        self.items = []
        if worker is not None:
            self.items.append(worker)

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


class FakeLayoutItem:
    """QLayoutItem-like double."""

    def __init__(self, widget: object) -> None:
        self._widget = widget

    def widget(self) -> object:
        return self._widget


class FakeHost:
    """Fake Tab 3 host."""

    def __init__(self, with_worker: bool = False) -> None:
        if with_worker:
            self._worker_path_edit = FakeWorkerEdit()
            self.main_layout = FakeBoxLayout(self._worker_path_edit)
        else:
            self.main_layout = FakeLayout()
        self.accept_called = False

    def _build_safe_mode_gui_snapshot(self) -> SafeModeGuiSnapshot:
        return SafeModeGuiSnapshot(
            current_index=0,
            total_folders=1,
            folder_relative_path="pkg",
            python_file_count=1,
            pending_count=0,
            accepted_count=1,
            skipped_count=0,
            rejected_count=0,
            can_apply_folder=True,
            can_continue_to_next_folder=False,
            status_message="Ready.",
        )

    def _build_safe_mode_button_state(self) -> SafeModeButtonState:
        return SafeModeButtonState(
            can_apply_folder=True,
            can_continue_to_next_folder=False,
            can_regenerate=True,
            can_fallback=True,
            can_edit=True,
            message="Ready.",
        )

    def _on_safe_mode_accept(self) -> None:
        self.accept_called = True


class SafeModeActualTab3WiringTests(unittest.TestCase):
    """Validate the actual Tab 3 Safe Mode wiring helper."""

    def test_actual_wiring_uses_host_snapshot_and_button_providers(self) -> None:
        host = FakeHost()

        result = install_safe_mode_actual_tab3_wiring(host)

        self.assertIn(
            result.status,
            {
                SAFE_MODE_ACTUAL_WIRING_STATUS_INSTALLED,
                SAFE_MODE_ACTUAL_WIRING_STATUS_NOT_AVAILABLE,
            },
        )

        snapshot = build_safe_mode_actual_snapshot(host)
        buttons = build_safe_mode_actual_button_state(host)
        callbacks = build_safe_mode_actual_callbacks(host)

        self.assertEqual("pkg", snapshot.folder_relative_path)
        self.assertTrue(buttons.can_apply_folder)
        self.assertIsNotNone(callbacks.on_accept)
        callbacks.on_accept()
        self.assertTrue(host.accept_called)

    def test_actual_wiring_returns_default_snapshot_when_host_has_no_state(self) -> None:
        host = object()

        snapshot = build_safe_mode_actual_snapshot(host)
        buttons = build_safe_mode_actual_button_state(host)

        self.assertEqual(0, snapshot.total_folders)
        self.assertFalse(buttons.can_apply_folder)
        self.assertIn("no active folder", buttons.message.lower())

    def test_actual_wiring_installs_radio_when_worker_script_field_exists(self) -> None:
        from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
            install_safe_mode_radio_button,
            safe_mode_radio_is_enabled,
        )

        host = FakeHost(with_worker=True)
        result = install_safe_mode_radio_button(
            host,
            radio_factory=lambda label, parent: FakeRadio(label, parent),
        )

        self.assertTrue(result.success)
        self.assertTrue(safe_mode_radio_is_enabled(host))
        self.assertFalse(hasattr(host, "_safe_mode_panel_widget"))

        host._safe_mode_radio.setChecked(False)
        refresh = refresh_safe_mode_actual_tab3_wiring(host)
        self.assertTrue(refresh.success)
        self.assertTrue(host._safe_mode_radio.checked)

    def test_panel_host_hook_refresh_still_works_but_actual_wiring_uses_radio(self) -> None:
        from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
            install_safe_mode_tab3_host_hook,
        )

        host = FakeHost()
        panel = FakePanel()

        hook_result = install_safe_mode_tab3_host_hook(
            host,
            callbacks=build_safe_mode_actual_callbacks(host),
            snapshot_provider=lambda: build_safe_mode_actual_snapshot(host),
            button_state_provider=lambda: build_safe_mode_actual_button_state(host),
            panel_factory=lambda _parent, _callbacks: panel,
        )
        refresh_result = refresh_safe_mode_tab3_host_hook(host)

        self.assertTrue(hook_result.success)
        self.assertTrue(refresh_result.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_REFRESHED, refresh_result.status)
        self.assertEqual("pkg", panel._safe_mode_panel_parts["folder_label"].text)
        self.assertTrue(panel._safe_mode_panel_parts["buttons"]["apply_folder"].enabled)


if __name__ == "__main__":
    unittest.main()
