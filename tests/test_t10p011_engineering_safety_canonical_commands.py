"""Regression tests for Engineering Safety canonical command references."""

from __future__ import annotations

from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENGINEERING_SAFETY_FILES = [
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "crash_triage.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "refactor_playbook.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "risk_radar.py",
    PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "engineering_safety" / "reasoner_symbol_atlas_integration.py",
]
ATLAS_INTEGRATION = (
    PROJECT_ROOT
    / 'ask_' 'ai_project_reasoner'
    / "engineering_safety"
    / "reasoner_symbol_atlas_integration.py"
)


class EngineeringSafetyCanonicalCommandTests(unittest.TestCase):
    """Validate canonical package paths in Engineering Safety guidance."""

    def test_validation_commands_use_canonical_cli_paths(self) -> None:
        for path in ENGINEERING_SAFETY_FILES:
            source = path.read_text(encoding="utf-8")
            self.assertNotIn(
                'python ask_' 'ai_project_reasoner' '\\manage_architecture',
                source,
                path.as_posix(),
            )
            self.assertNotIn(
                'python ask_' 'ai_project_reasoner' '\\manage_workflows',
                source,
                path.as_posix(),
            )
            self.assertNotIn("E:\\developer_tools", source, path.as_posix())

    def test_reasoner_symbol_atlas_imports_use_canonical_package(self) -> None:
        source = ATLAS_INTEGRATION.read_text(encoding="utf-8")
        self.assertIn(
            "from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import",
            source,
        )
        self.assertIn(
            "from kanda_reasoner_app.reasoner_symbol_atlas.pre_patch_gate import",
            source,
        )
        self.assertIn(
            "from kanda_reasoner_app.reasoner_symbol_atlas.schemas import",
            source,
        )
        self.assertNotIn(
            "from kanda_reasoner_app.reasoner_symbol_atlas",
            source,
        )

    def test_observable_risk_radar_report_contains_canonical_validation_commands(self) -> None:
        from kanda_reasoner_app.engineering_safety.risk_radar import (
            RiskChangeRadarInput,
            build_risk_change_radar_report,
        )

        report = build_risk_change_radar_report(
            RiskChangeRadarInput(
                project_root="E:/kanda_reasoner",
                changed_files=['ask_' 'ai_project_reasoner' '/engineering_safety/risk_radar.py'],
            )
        )
        joined = "\n".join(report.tests_to_run)
        self.assertIn("kanda_reasoner_app\\manage_architecture", joined)
        self.assertIn("kanda_reasoner_app\\manage_workflows", joined)
        self.assertNotIn('ask_' 'ai_project_reasoner' '\\manage_architecture', joined)
        self.assertNotIn("E:\\developer_tools", joined)


if __name__ == "__main__":
    unittest.main()
