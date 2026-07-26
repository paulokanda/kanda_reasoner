from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

CANON_FILES = [
    ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/daily_patch_delivery_guardrails.md",
    ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/implementation_and_delivery_protocol.md",
    ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/05_patch_delivery_and_validation/bundle_gated_development_workflow.md",
    ROOT / "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md",
]


class RootDriveStagingCanonTests(unittest.TestCase):
    def _read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_strict_root_drive_staging_rule_is_canonical(self) -> None:
        required = [
            "DRIVE_ROOT",
            "PROJECT_ROOT",
            "ROOT_PATCH_ZIP",
            "WORK_PATCH_ZIP",
            "delete_after_daily_work",
            "zip is not in root of drive:\\ where project is",
        ]
        for path in CANON_FILES:
            text = self._read(path)
            missing = [item for item in required if item not in text]
            self.assertEqual([], missing, f"{path} missing {missing}")

    def test_root_copy_deletion_is_mandatory_in_installer_sources(self) -> None:
        for path in CANON_FILES:
            text = self._read(path)
            self.assertTrue(
                "delete the root-drive ZIP copy" in text
                or "Remove-Item -Path $ROOT_PATCH_ZIP" in text,
                f"{path} does not require root ZIP deletion after staging",
            )

    def test_downloads_desktop_first_template_is_forbidden(self) -> None:
        forbidden_phrases = [
            "Downloads/Desktop-first",
            "Downloads` or `Desktop` before",
            "Downloads or Desktop before",
            "Downloads/Desktop before",
        ]
        for path in CANON_FILES:
            text = self._read(path)
            self.assertTrue(
                any(phrase in text for phrase in forbidden_phrases),
                f"{path} does not forbid Downloads/Desktop-first search",
            )

    def test_startup_sync_hook_contains_enforced_rule(self) -> None:
        text = self._read(ROOT / "kanda_prompt_workspace/prompt_tools/sync_startup_routing_kernel_pack.py")
        self.assertIn("delete the root-drive ZIP copy after successful staging", text)
        self.assertIn("Do not use the old generic Downloads/Desktop-first installer search template", text)

    def test_generated_startup_zip_contains_updated_guardrail(self) -> None:
        import zipfile

        zip_path = ROOT / "kanda_prompt_workspace/first_AI_deliver/first_prompts_to_ai.zip"
        self.assertTrue(zip_path.exists())
        with zipfile.ZipFile(zip_path) as archive:
            names = set(archive.namelist())
            self.assertIn("07_daily_patch_delivery_guardrails.md", names)
            text = archive.read("07_daily_patch_delivery_guardrails.md").decode("utf-8")
        self.assertIn("Version: 1.6", text)
        self.assertIn("delete the root-drive ZIP copy after successful staging", text)
        self.assertIn("The words `Downloads` and `Desktop` must not appear", text)


if __name__ == "__main__":
    unittest.main()
