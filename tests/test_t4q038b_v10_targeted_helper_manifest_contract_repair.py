
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest


TARGET_MANIFESTS = [
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/ai_reasoner_main_window_help.json',
    'ask_' 'ai_project_reasoner' '/project_reasoner_v10/reasoner_retriever_help.json',
]

STALE_TEST = "tests/test_t4q038_v10_helper_manifest_contract_repair.py"


class T4Q038BV10TargetedHelperManifestContractRepairTests(unittest.TestCase):
    """Validate targeted v10 helper manifest repair."""

    def test_stale_failed_t4q038_test_removed(self) -> None:
        self.assertFalse(Path(STALE_TEST).exists(), STALE_TEST)

    def test_unrelated_helper_exports_are_preserved_when_present(self) -> None:
        manifest_path = Path(TARGET_MANIFESTS[0])
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        helpers = data.get("helpers", {})
        analysis = helpers.get("analysis_controller.py")
        if isinstance(analysis, dict) and "exports" in analysis:
            self.assertEqual(analysis["exports"], ["AnalysisController"])

    def test_architecture_validation_has_no_helper_manifest_contract_warning(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                'ask_' 'ai_project_reasoner' '/manage_architecture/manage_architecture.py',
                "--root",
                str(Path.cwd()),
                "--validate",
            ],
            cwd=str(Path.cwd()),
            capture_output=True,
            text=True,
            errors="replace",
        )

        output = (completed.stdout or "") + (completed.stderr or "")
        self.assertEqual(completed.returncode, 0, output)
        self.assertNotIn("HELPER_MANIFEST_CONTRACT", output)


if __name__ == "__main__":
    unittest.main()
