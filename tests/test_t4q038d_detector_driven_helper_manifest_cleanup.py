
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import unittest


MAIN_MANIFEST = 'ask_' 'ai_project_reasoner' '/project_reasoner_v10/ai_reasoner_main_window_help.json'
RETRIEVER_MANIFEST = 'ask_' 'ai_project_reasoner' '/project_reasoner_v10/reasoner_retriever_help.json'

STALE_FILES = [
    "tests/test_t4q038_v10_helper_manifest_contract_repair.py",
    "tests/test_t4q039_static_collector_runtime_scenario_payload_facades.py",
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_ze.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zf.py',
    'ask_' 'ai_project_reasoner' '/backend_payloads/payload_zg.py',
]


class T4Q038DDetectorDrivenHelperManifestCleanupTests(unittest.TestCase):
    """Validate detector-driven v10 helper manifest cleanup."""

    def test_stale_failed_artifacts_are_removed(self) -> None:
        for rel_path in STALE_FILES:
            self.assertFalse(Path(rel_path).exists(), rel_path)

    def test_unrelated_helper_exports_are_preserved_when_present(self) -> None:
        data = json.loads(Path(MAIN_MANIFEST).read_text(encoding="utf-8"))
        helpers = data.get("helpers", {})
        analysis = helpers.get("analysis_controller.py")
        if isinstance(analysis, dict) and "exports" in analysis:
            self.assertEqual(analysis["exports"], ["AnalysisController"])

    def test_target_stale_exports_are_absent_from_target_manifests(self) -> None:
        forbidden_by_path = {
            MAIN_MANIFEST: {
                "ProfileController",
                "ProfileRefreshResult",
                "RuntimeController",
            },
            RETRIEVER_MANIFEST: {
                "detect_query_intents",
                "is_code_localized_explanation_question",
                "is_documentation_intent_question",
                "is_explain_chain_question",
                "is_explanatory_question",
                "is_explicit_call_chain_question",
                "is_main_window_show_responsibility_question",
                "is_packaging_metadata_question",
            },
        }

        for rel_path, forbidden in forbidden_by_path.items():
            text = Path(rel_path).read_text(encoding="utf-8")
            data = json.loads(text)
            self.assert_no_forbidden_export(data, forbidden, rel_path)

    def assert_no_forbidden_export(
        self,
        value: object,
        forbidden: set[str],
        rel_path: str,
    ) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "exports" and isinstance(child, list):
                    overlap = forbidden.intersection(str(item) for item in child)
                    self.assertFalse(overlap, rel_path + " has " + repr(sorted(overlap)))
                self.assert_no_forbidden_export(child, forbidden, rel_path)
        elif isinstance(value, list):
            for item in value:
                self.assert_no_forbidden_export(item, forbidden, rel_path)

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
        self.assertTrue(
            "Errors: 0" in output or "No validation issues." in output,
            output,
        )
        self.assertNotIn("HELPER_MANIFEST_CONTRACT", output)


if __name__ == "__main__":
    unittest.main()
