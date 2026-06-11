
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_MOUNT_STATUS_ALREADY_MOUNTED,
    SAFE_MODE_MOUNT_STATUS_MOUNTED,
    SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE,
    SAFE_MODE_MOUNT_STATUS_REFRESHED,
    SafeModeButtonState,
    SafeModeGuiSnapshot,
    mount_safe_mode_panel,
    refresh_safe_mode_panel,
    safe_mode_panel_is_mounted,
)


class FakeLayout:
    """Collect mounted widgets for mount-adapter tests."""

    def __init__(self) -> None:
        self.widgets = []

    def addWidget(self, widget) -> None:
        self.widgets.append(widget)


class FakePanel:
    """Store applied panel data for refresh tests."""

    def __init__(self) -> None:
        self.applied = False


class FakeHost:
    """Host with a standard layout attribute."""

    def __init__(self) -> None:
        self.main_layout = FakeLayout()


class FakeMethodLayoutHost:
    """Host exposing layout through a method."""

    def __init__(self) -> None:
        self._layout = FakeLayout()

    def layout(self):
        return self._layout


class SafeModeGuiMountAdapterTests(unittest.TestCase):
    """Validate Safe Mode GUI mount adapter without requiring PySide."""

    def test_mounts_panel_into_named_layout_once(self) -> None:
        host = FakeHost()

        def factory(parent, callbacks):
            self.assertIs(parent, host)
            self.assertIsNone(callbacks)
            return FakePanel()

        result = mount_safe_mode_panel(host, panel_factory=factory)

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_MOUNTED, result.status)
        self.assertEqual("main_layout", result.layout_attr)
        self.assertTrue(safe_mode_panel_is_mounted(host))
        self.assertEqual(1, len(host.main_layout.widgets))

        second = mount_safe_mode_panel(host, panel_factory=factory)
        self.assertTrue(second.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_ALREADY_MOUNTED, second.status)
        self.assertEqual(1, len(host.main_layout.widgets))

    def test_mounts_panel_into_method_layout(self) -> None:
        host = FakeMethodLayoutHost()

        result = mount_safe_mode_panel(host, panel_factory=lambda _parent, _callbacks: FakePanel())

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_MOUNTED, result.status)
        self.assertEqual("layout()", result.layout_attr)
        self.assertEqual(1, len(host._layout.widgets))

    def test_missing_layout_fails_safely(self) -> None:
        host = object()

        result = mount_safe_mode_panel(host, panel_factory=lambda _parent, _callbacks: FakePanel())

        self.assertFalse(result.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE, result.status)

    def test_refresh_requires_mounted_panel(self) -> None:
        host = object()
        snapshot, buttons = self._snapshot_and_buttons()

        result = refresh_safe_mode_panel(host, snapshot, buttons)

        self.assertFalse(result.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_NOT_AVAILABLE, result.status)

    def test_refreshes_mounted_panel_with_panel_model(self) -> None:
        host = FakeHost()
        panel = self._fake_panel_with_parts()
        mount_safe_mode_panel(host, panel_factory=lambda _parent, _callbacks: panel)

        snapshot, buttons = self._snapshot_and_buttons()
        result = refresh_safe_mode_panel(host, snapshot, buttons)

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_REFRESHED, result.status)
        self.assertEqual("pkg", panel._safe_mode_panel_parts["folder_label"].text)
        self.assertEqual("Folder 1 of 1", panel._safe_mode_panel_parts["progress_label"].text)
        self.assertFalse(panel._safe_mode_panel_parts["buttons"]["apply_folder"].enabled)

    def _snapshot_and_buttons(self):
        snapshot = SafeModeGuiSnapshot(
            current_index=0,
            total_folders=1,
            folder_relative_path="pkg",
            python_file_count=1,
            pending_count=1,
            accepted_count=0,
            skipped_count=0,
            rejected_count=0,
            can_apply_folder=False,
            can_continue_to_next_folder=False,
            status_message="Safe Mode folder has pending rows.",
        )
        buttons = SafeModeButtonState(
            can_apply_folder=False,
            can_continue_to_next_folder=False,
            can_regenerate=True,
            can_fallback=True,
            can_edit=True,
            message="1 row still needs review.",
        )
        return snapshot, buttons

    def _fake_panel_with_parts(self):
        class FakeLabel:
            def __init__(self):
                self.text = ""

            def setText(self, text):
                self.text = text

        class FakeButton:
            def __init__(self):
                self.text = ""
                self.enabled = False

            def setText(self, text):
                self.text = text

            def setEnabled(self, enabled):
                self.enabled = bool(enabled)

        panel = FakePanel()
        panel._safe_mode_panel_parts = {
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
        return panel


if __name__ == "__main__":
    unittest.main()
