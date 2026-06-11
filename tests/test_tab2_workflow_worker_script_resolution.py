"""Regression tests for Tab 2 workflow worker script resolution."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


def _load_history_module():
    module_path = Path(
        "kanda_reasoner_app/manage_workflows/manage_workflows_gui_help"
        "/workflow_gui_history.py"
    )
    spec = importlib.util.spec_from_file_location(
        "workflow_gui_history_under_test",
        module_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load workflow_gui_history module spec.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Tab2WorkflowWorkerScriptResolutionTests(unittest.TestCase):
    def test_default_script_path_points_to_canonical_workflow_worker(self):
        workflow_gui_history = _load_history_module()
        default_path = Path(workflow_gui_history.get_default_script_path())

        self.assertEqual(default_path.name, "manage_workflows.py")
        self.assertEqual(default_path.parent.name, "manage_workflows")
        self.assertTrue(default_path.exists())

    def test_recent_scripts_filters_missing_legacy_developer_tools_path(self):
        workflow_gui_history = _load_history_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            history_file = Path(temp_dir) / ".manage_gui_history.json"
            legacy_path = (
                r"E:\developer_tools\ask_ai_project_reasoner"
                r"\manage_workflows.py"
            )
            payload = {"scripts": [legacy_path]}
            history_file.write_text(str(payload).replace("'", '"'), encoding="utf-8")

            scripts = workflow_gui_history.get_recent_scripts(
                history_file=history_file,
            )

        self.assertGreaterEqual(len(scripts), 1)
        self.assertNotIn(legacy_path, scripts)
        first_script = scripts[0].replace("\\", "/")
        self.assertTrue(first_script.endswith("manage_workflows/manage_workflows.py"))
        self.assertTrue(Path(scripts[0]).exists())


if __name__ == "__main__":
    unittest.main()
