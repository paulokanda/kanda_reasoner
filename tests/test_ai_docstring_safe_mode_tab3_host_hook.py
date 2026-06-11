
from __future__ import annotations

import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.guided_folder_mode import (
    SAFE_MODE_HOST_HOOK_STATUS_ALREADY_INSTALLED,
    SAFE_MODE_HOST_HOOK_STATUS_INSTALLED,
    SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE,
    SAFE_MODE_HOST_HOOK_STATUS_REFRESHED,
    SAFE_MODE_HOST_HOOK_STATUS_UNINSTALLED,
    SAFE_MODE_MOUNT_STATUS_MOUNTED,
    SafeModeButtonState,
    SafeModeGuiSnapshot,
    install_safe_mode_tab3_host_hook,
    refresh_safe_mode_tab3_host_hook,
    tab3_host_hook_is_installed,
    uninstall_safe_mode_tab3_host_hook,
)


class FakeLayout:
    """Collect mounted widgets for host hook tests."""

    def __init__(self) -> None:
        self.widgets = []

    def addWidget(self, widget) -> None:
        self.widgets.append(widget)


class FakePanel:
    """Store panel parts used by the refresh path."""

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


class FakeLabel:
    """Small label double."""

    def __init__(self) -> None:
        self.text = ""

    def setText(self, text) -> None:
        self.text = text


class FakeButton:
    """Small button double."""

    def __init__(self) -> None:
        self.text = ""
        self.enabled = False

    def setText(self, text) -> None:
        self.text = text

    def setEnabled(self, enabled) -> None:
        self.enabled = bool(enabled)


class FakeHost:
    """Host with a compatible Safe Mode layout."""

    def __init__(self) -> None:
        self.safe_mode_layout = FakeLayout()


class SafeModeTab3HostHookTests(unittest.TestCase):
    """Validate the Safe Mode Tab 3 host hook."""

    def test_installs_panel_and_marks_host_installed(self) -> None:
        host = FakeHost()
        panel = FakePanel()

        result = install_safe_mode_tab3_host_hook(
            host,
            panel_factory=lambda _parent, _callbacks: panel,
        )

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_INSTALLED, result.status)
        self.assertIsNotNone(result.mount_result)
        self.assertEqual(SAFE_MODE_MOUNT_STATUS_MOUNTED, result.mount_result.status)
        self.assertTrue(tab3_host_hook_is_installed(host))
        self.assertEqual(1, len(host.safe_mode_layout.widgets))

    def test_install_is_idempotent(self) -> None:
        host = FakeHost()
        panel = FakePanel()

        first = install_safe_mode_tab3_host_hook(
            host,
            panel_factory=lambda _parent, _callbacks: panel,
        )
        second = install_safe_mode_tab3_host_hook(
            host,
            panel_factory=lambda _parent, _callbacks: FakePanel(),
        )

        self.assertTrue(first.success)
        self.assertTrue(second.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_ALREADY_INSTALLED, second.status)
        self.assertEqual(1, len(host.safe_mode_layout.widgets))

    def test_missing_layout_returns_safe_noop(self) -> None:
        host = object()

        result = install_safe_mode_tab3_host_hook(
            host,
            panel_factory=lambda _parent, _callbacks: FakePanel(),
        )

        self.assertFalse(result.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_NOT_AVAILABLE, result.status)

    def test_refresh_uses_installed_providers(self) -> None:
        host = FakeHost()
        panel = FakePanel()

        result = install_safe_mode_tab3_host_hook(
            host,
            snapshot_provider=self._snapshot,
            button_state_provider=self._buttons,
            panel_factory=lambda _parent, _callbacks: panel,
        )

        self.assertTrue(result.success)
        refresh_result = refresh_safe_mode_tab3_host_hook(host)

        self.assertTrue(refresh_result.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_REFRESHED, refresh_result.status)
        self.assertEqual("pkg", panel._safe_mode_panel_parts["folder_label"].text)
        self.assertEqual("Folder 1 of 1", panel._safe_mode_panel_parts["progress_label"].text)
        self.assertTrue(panel._safe_mode_panel_parts["buttons"]["apply_folder"].enabled)

    def test_uninstall_removes_host_attributes(self) -> None:
        host = FakeHost()
        install_safe_mode_tab3_host_hook(
            host,
            snapshot_provider=self._snapshot,
            button_state_provider=self._buttons,
            panel_factory=lambda _parent, _callbacks: FakePanel(),
        )

        result = uninstall_safe_mode_tab3_host_hook(host)

        self.assertTrue(result.success)
        self.assertEqual(SAFE_MODE_HOST_HOOK_STATUS_UNINSTALLED, result.status)
        self.assertFalse(tab3_host_hook_is_installed(host))
        self.assertFalse(hasattr(host, "_safe_mode_panel_widget"))

    def _snapshot(self) -> SafeModeGuiSnapshot:
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
            status_message="Safe Mode folder is ready to apply.",
        )

    def _buttons(self) -> SafeModeButtonState:
        return SafeModeButtonState(
            can_apply_folder=True,
            can_continue_to_next_folder=False,
            can_regenerate=True,
            can_fallback=True,
            can_edit=True,
            message="Folder can be applied.",
        )


if __name__ == "__main__":
    unittest.main()
