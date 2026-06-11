
from __future__ import annotations

from pathlib import Path
import unittest

from kanda_reasoner_app.insert_missing_docstrings_gui.insert_missing_docstrings_gui_help.tab1_audit_docstring_source import (
    MISSING_DOCSTRING_CODE,
    TAB1_AUDIT_SOURCE_LABEL,
    extract_missing_docstring_findings,
    read_missing_docstrings_from_tab1_audit,
)


class Tab1AuditDocstringSourceRadioTests(unittest.TestCase):
    """Validate the Tab 1 audit docstring source option."""

    def test_extracts_missing_docstring_findings_from_tab1_output(self) -> None:
        output = '\nARCHITECTURE VALIDATION SUMMARY\nWARNING MISSING_DOCSTRING          ask_' 'ai_project_reasoner' '/foo.py :: Missing module docstring.\nERROR MISSING_DOCSTRING            ask_' 'ai_project_reasoner' '/bar.py :: Missing function docstring: do_work\nWARNING MIXED_RESPONSIBILITY_FILE  ask_' 'ai_project_reasoner' '/other.py :: Ignore this.\nWARNING MISSING_DOCSTRING          ask_' 'ai_project_reasoner' '/foo.py :: Missing module docstring.\n'

        findings = extract_missing_docstring_findings(output)

        self.assertEqual(2, len(findings))
        self.assertEqual('ask_' 'ai_project_reasoner' '/foo.py', findings[0].path)
        self.assertEqual("module", findings[0].target_kind)
        self.assertEqual("function", findings[1].target_kind)

    def test_read_missing_docstrings_uses_command_runner_contract(self) -> None:
        captured = {}

        def runner(command, tool_root):
            captured["command"] = command
            captured["tool_root"] = tool_root
            return (
                0,
                "WARNING MISSING_DOCSTRING          pkg/mod.py :: Missing class docstring: Widget\n",
            )

        result = read_missing_docstrings_from_tab1_audit(Path("E:/fake_project"), runner)

        self.assertEqual(1, len(result.findings))
        self.assertIn("--validate", result.command)
        self.assertIn("pkg/mod.py", result.findings[0].path)
        self.assertEqual("class", result.findings[0].target_kind)
        self.assertTrue(captured["command"])

    def test_window_state_creates_red_bold_default_on_radio(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/window_state.py'
        ).read_text(encoding="utf-8")

        self.assertIn("QRadioButton", source)
        self.assertIn("_tab1_audit_docstring_radio", source)
        self.assertIn(TAB1_AUDIT_SOURCE_LABEL, source)
        self.assertIn("setChecked", source)
        self.assertIn("font.setBold(True)", source)
        self.assertIn("color: red; font-weight: bold;", source)

    def test_layout_places_radio_to_right_of_mode_combo(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/layout_builder.py'
        ).read_text(encoding="utf-8")

        self.assertIn("mode_row.addWidget(self._mode_combo)", source)
        self.assertIn("mode_row.addWidget(self._tab1_audit_docstring_radio)", source)
        self.assertIn('form.addRow("Mode", mode_row_widget)', source)

    def test_event_wiring_reads_tab1_audit_when_radio_clicked(self) -> None:
        source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/layout_builder.py'
        ).read_text(encoding="utf-8")

        self.assertIn("_tab1_audit_docstring_radio.clicked.connect", source)
        self.assertIn("refresh_tab1_audit_docstring_source", source)

    def test_safe_mode_remains_independent_from_tab1_audit_source(self) -> None:
        safe_mode_source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/guided_folder_mode/actual_tab3_wiring.py'
        ).read_text(encoding="utf-8")
        audit_source = Path(
            'ask_' 'ai_project_reasoner' '/insert_missing_docstrings_gui/insert_missing_docstrings_gui_help/tab1_audit_docstring_source.py'
        ).read_text(encoding="utf-8")

        self.assertNotIn("safe_mode_radio.setChecked(False)", audit_source)
        self.assertNotIn("_safe_mode_radio.setChecked(False)", audit_source)
        self.assertIn("safe_mode_radio_is_enabled", safe_mode_source)

    def test_missing_docstring_code_constant_is_stable(self) -> None:
        self.assertEqual("MISSING_DOCSTRING", MISSING_DOCSTRING_CODE)


if __name__ == "__main__":
    unittest.main()
