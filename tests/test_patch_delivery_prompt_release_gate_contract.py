from __future__ import annotations

import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class PatchDeliveryPromptReleaseGateContractTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")

    def test_startup_guardrail_pins_release_gate_validator(self) -> None:
        text = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/01_session_start_and_navigation/"
            "daily_patch_delivery_guardrails.md"
        )
        self.assertIn("PATCH_DELIVERY_RELEASE fail-closed contract", text)
        self.assertIn("python scripts/validate_patch_zip.py <zip_path>", text)
        self.assertIn("CONTRACT NOT MET - PATCH DELIVERY BLOCKED", text)
        self.assertIn("Confirm `KANDA_FREEZE_HINT.json` is at ZIP root", text)
        self.assertIn("contains no Downloads/Desktop fallback", text)

    def test_pre_output_gate_requires_zip_contract_validator(self) -> None:
        text = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/03_governance_freeze_and_handoff/"
            "pre_output_contract_gates.md"
        )
        self.assertIn("PATCH_DELIVERY_RELEASE", text)
        self.assertIn("python scripts/validate_patch_zip.py <zip_path>", text)
        self.assertIn("ZIP contract validator result: PASS", text)
        self.assertIn("same canonical freeze payload", text)
        self.assertIn("CONTRACT NOT MET - PATCH DELIVERY BLOCKED", text)

    def test_router_and_navigation_expose_patch_delivery_release_route(self) -> None:
        router = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/"
            "prompt_router.md"
        )
        navigation = self._read(
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/"
            "prompt_navigation_index.md"
        )
        self.assertIn("### Governed patch ZIP release", router)
        self.assertIn("PATCH_DELIVERY_RELEASE", router)
        self.assertIn("CONTRACT NOT MET - PATCH DELIVERY BLOCKED", router)
        self.assertIn("## Governed patch ZIP release hook", navigation)
        self.assertIn("PATCH_DELIVERY_RELEASE", navigation)
        self.assertIn("Do not emit the ZIP link unless the ZIP contract validator passes", navigation)

    def test_generated_paste_file_contains_output_time_release_hook(self) -> None:
        text = self._read("kanda_prompt_workspace/first_AI_deliver/paste_after_first_prompts_to_ai.md")
        self.assertIn("PATCH_DELIVERY_RELEASE", text)
        self.assertIn("CONTRACT NOT MET - PATCH DELIVERY BLOCKED", text)
        self.assertIn("same freeze payload source", text)


if __name__ == "__main__":
    unittest.main()
