from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class TerminalCleanupCanonV1Tests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")

    def test_canonical_installer_has_success_and_error_cleanup_paths(self) -> None:
        text = self._read("kanda_reasoner_app/patch_governance/installer_template.ps1")

        self.assertIn("try {", text)
        self.assertIn("catch {", text)
        self.assertIn("INSTALL OK. Terminal will clear in 5 seconds...", text)
        self.assertIn("Start-Sleep -Seconds 5", text)
        self.assertIn("INSTALL ERROR. Review the error below before clearing the terminal.", text)
        self.assertIn('Read-Host "Press Enter to clear terminal"', text)
        self.assertIn('Read-Host "Press Enter again to finish"', text)
        self.assertIn("$global:LASTEXITCODE = 1", text)
        self.assertIn("return", text)
        self.assertNotIn("Stop-Process", text)
        self.assertNotIn("Restart-Computer", text)
        self.assertNotIn("exit 1", text.lower())

    def test_daily_guardrail_canonizes_install_error_cleanup(self) -> None:
        text = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/"
            "daily_patch_delivery_guardrails.md"
        )

        self.assertIn("Install blocks must contain a fail-safe error cleanup path", text)
        self.assertIn("A successful install uses 5 seconds then `Clear-Host`", text)
        self.assertIn("any install error must show the error", text)
        self.assertIn("Read-Host \"Press Enter to clear terminal\"", text)
        self.assertIn("Read-Host \"Press Enter again to finish\"", text)
        self.assertIn("Do not close the terminal", text)

    def test_pre_output_gate_requires_try_catch_error_cleanup(self) -> None:
        text = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
            "pre_output_contract_gates.md"
        )

        self.assertIn("INSTALL_ERROR fail-safe wrapper", text)
        self.assertIn("Every install PowerShell block must wrap the install body in `try { ... } catch { ... }`", text)
        self.assertIn("INSTALL ERROR", text)
        self.assertIn("Install errors use Enter, Clear-Host, Enter, Clear-Host", text)
        self.assertIn("keep the terminal open", text)

    def test_router_and_startup_expose_terminal_cleanup_canon(self) -> None:
        router = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/"
            "prompt_router.md"
        )
        navigation = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/"
            "prompt_navigation_index.md"
        )
        paste = self._read("kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md")

        self.assertIn("Terminal cleanup canon", router)
        self.assertIn("Terminal cleanup canon route", navigation)
        self.assertIn("Install errors, validation, diagnostics, validation errors", paste)
        self.assertIn("never close the terminal", paste)
        self.assertIn("fail-safe try/catch", paste)


if __name__ == "__main__":
    unittest.main()
