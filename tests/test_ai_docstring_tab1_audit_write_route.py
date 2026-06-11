
from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.tab1_audit_write_support import planning


class FakeRadio:
    """Small radio double."""

    def __init__(self, checked: bool) -> None:
        self._checked = checked

    def isChecked(self) -> bool:
        return self._checked


class FakeHost:
    """Small host double."""

    def __init__(self, checked: bool) -> None:
        self._tab1_audit_docstring_radio = FakeRadio(checked)


class Tab1AuditWriteRouteTests(unittest.TestCase):
    """Validate the Tab 1 audit write route hook."""

    def test_route_handles_only_write_mode_with_radio_on(self) -> None:
        self.assertTrue(
            planning.tab1_audit_write_route_should_handle(
                FakeHost(True),
                "write",
            )
        )
        self.assertFalse(
            planning.tab1_audit_write_route_should_handle(
                FakeHost(False),
                "write",
            )
        )
        self.assertFalse(
            planning.tab1_audit_write_route_should_handle(
                FakeHost(True),
                "scan",
            )
        )

    def test_run_controls_contains_existing_boundary_hook(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/run_controls.py"
        ).read_text(encoding="utf-8")

        self.assertIn("_run_tab1_audit_write_route_from_run_controls", source)
        self.assertIn("kanda_reasoner_app.tab1_audit_write_support", source)
        self.assertIn('if mode == "write":', source)

    def test_planning_public_surface_is_planning_only(self) -> None:
        exported = set(planning.__all__)

        self.assertIn("build_tab1_audit_write_plan", exported)
        self.assertIn("module_name_from_python_file", exported)
        self.assertIn("tab1_audit_write_route_should_handle", exported)

        self.assertNotIn("run_tab1_audit_write_route", exported)
        self.assertNotIn("Tab1AuditWriteRouteWorker", exported)
        self.assertNotIn("Tab1AuditWritePlan", exported)
        self.assertNotIn("Tab1AuditWriteTarget", exported)

    def test_old_mixed_route_helper_removed(self) -> None:
        path = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/'
            "insert_missing_docstrings_gui_help/tab1_audit_write_route.py"
        )
        self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
