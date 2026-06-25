"""Focused tests for external runtime evidence path redirection."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    analysis_json_complete_dir,
    analysis_json_parts_dir,
    ensure_project_analysis_evidence_dirs,
    primary_evidence_json_path,
    project_analysis_evidence_root,
)


def _text(path: Path) -> str:
    return str(path).replace("\\", "/")


class ProjectAnalysisEvidenceExternalRoutingTests(unittest.TestCase):
    def test_primary_runtime_evidence_path_resolves_to_external_audit_root(self) -> None:
        root = Path(r"E:\clinic_ai")

        path = primary_evidence_json_path(root)

        self.assertTrue(
            _text(path).endswith(
                "clinic_ai_show_project_to_AI/clinic_ai__complete.json"
            )
        )
        self.assertNotIn("clinic_ai/project_analysis_evidence", _text(path))

    def test_root_and_children_are_external_to_selected_project(self) -> None:
        root = Path(r"D:\other_project")

        evidence_root = project_analysis_evidence_root(root)

        self.assertTrue(_text(evidence_root).endswith("other_project_show_project_to_AI"))
        self.assertEqual(analysis_json_complete_dir(root), evidence_root)
        self.assertEqual(analysis_json_parts_dir(root), evidence_root / "json_splitted")

    def test_ensure_does_not_recreate_in_source_project_analysis_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "sample_project"
            root.mkdir()

            evidence_root = ensure_project_analysis_evidence_dirs(root)

            self.assertTrue(evidence_root.exists())
            self.assertTrue(analysis_json_complete_dir(root).is_dir())
            self.assertTrue(analysis_json_parts_dir(root).is_dir())
            self.assertFalse((root / "project_analysis_evidence").exists())

    def test_source_has_no_hardcoded_project_paths(self) -> None:
        source_path = PROJECT_ROOT / "kanda_reasoner_app" / "project_analysis_evidence_paths.py"
        source = source_path.read_text(encoding="utf-8")

        self.assertNotIn("E:\\kanda_reasoner", source)
        self.assertNotIn("E:/kanda_reasoner", source)
        self.assertNotIn("E:\\developer_tools", source)
        self.assertNotIn("<PROJECT_ROOT>", source)


if __name__ == "__main__":
    unittest.main()
