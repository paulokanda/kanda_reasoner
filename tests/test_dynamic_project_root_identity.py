"""Focused tests for dynamic project-root identity handling."""

from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

from kanda_reasoner_app.project_analysis_evidence_paths import project_name_from_root
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths
from kanda_reasoner_app.project_root_resolver import (
    CANONICAL_PROJECT_ROOT_ENV,
    default_smoke_output_json_path,
    find_reasoner_source_root,
    is_reasoner_project_root,
    resolve_active_project_root,
)
from reasoner_tools_gui_engineering_safety_panel import (
    build_engineering_safety_panel_cli_args,
)


class DynamicProjectRootIdentityTests(unittest.TestCase):
    """Verify project names and paths are derived from the selected root."""

    def test_project_name_from_windows_root_is_dynamic(self) -> None:
        self.assertEqual(project_name_from_root(r"E:\kanda_reasoner"), "kanda_reasoner")
        self.assertEqual(project_name_from_root(r"D:\other_project"), "other_project")

    def test_bundle_artifact_names_use_selected_project_name(self) -> None:
        paths = bundle_artifact_paths(Path(r"E:\kanda_reasoner"))
        names = {
            paths.complete_json.name,
            paths.active_snapshot_json.name,
            paths.file_manifest_json.name,
            paths.validation_state_json.name,
            paths.bundle_manifest_json.name,
            paths.reconstruction_payload_json.name,
        }
        self.assertIn("kanda_reasoner__complete.json", names)
        self.assertIn("kanda_reasoner__file_manifest.json", names)
        self.assertIn("kanda_reasoner__active_snapshot.json", names)
        self.assertIn("kanda_reasoner__validation_state.json", names)
        self.assertIn("kanda_reasoner__bundle_manifest.json", names)
        self.assertIn("kanda_reasoner__reconstruction_payload.json", names)
        for name in names:
            self.assertFalse(name.startswith("developer_tools__"), name)

    def test_reasoner_root_detection_uses_structure_not_folder_name(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "kanda_reasoner"
            package = root / 'ask_' 'ai_project_reasoner'
            package.mkdir(parents=True)
            (package / "__init__.py").write_text("", encoding="utf-8")
            (root / "reasoner_tools_gui.py").write_text("", encoding="utf-8")

            self.assertTrue(is_reasoner_project_root(root))
            self.assertEqual(find_reasoner_source_root(package), root.resolve())

    def test_lowercase_project_root_environment_variable_wins(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "custom_project"
            root.mkdir()
            previous = os.environ.get(CANONICAL_PROJECT_ROOT_ENV)
            os.environ[CANONICAL_PROJECT_ROOT_ENV] = str(root)
            try:
                self.assertEqual(resolve_active_project_root(), root.resolve())
            finally:
                if previous is None:
                    os.environ.pop(CANONICAL_PROJECT_ROOT_ENV, None)
                else:
                    os.environ[CANONICAL_PROJECT_ROOT_ENV] = previous

    def test_engineering_safety_commands_use_explicit_root(self) -> None:
        root = Path(r"E:\kanda_reasoner")
        args = build_engineering_safety_panel_cli_args("evidence-freshness", root)
        self.assertEqual(args, ["evidence-freshness", "--root", str(root)])
        self.assertNotIn(r"<PROJECT_ROOT>", " ".join(args))

    def test_smoke_output_path_uses_active_project_root(self) -> None:
        root = Path(r"E:\kanda_reasoner")
        path = default_smoke_output_json_path(root)
        self.assertEqual(path.name, "real_project_static_context_smoke.json")
        self.assertIn('ask_' 'ai_project_reasoner', str(path))
        self.assertNotIn(r"<PROJECT_ROOT>", str(path))


if __name__ == "__main__":
    unittest.main()
