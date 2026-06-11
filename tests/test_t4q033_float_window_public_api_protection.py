
from __future__ import annotations

import unittest

import kanda_reasoner_app.templates.floating_windows.float_window as float_window


class T4Q033FloatWindowPublicApiProtectionTests(unittest.TestCase):
    """Protect the public floating-window helper API."""

    def test_public_api_exports_are_stable(self) -> None:
        self.assertEqual(
            sorted(float_window.__all__),
            ["HoverFloatingWindowController", "attach_floating_window"],
        )

    def test_public_api_names_resolve(self) -> None:
        self.assertTrue(hasattr(float_window, "HoverFloatingWindowController"))
        self.assertTrue(hasattr(float_window, "attach_floating_window"))

    def test_public_api_objects_are_callable(self) -> None:
        self.assertTrue(callable(float_window.HoverFloatingWindowController))
        self.assertTrue(callable(float_window.attach_floating_window))


if __name__ == "__main__":
    unittest.main()
