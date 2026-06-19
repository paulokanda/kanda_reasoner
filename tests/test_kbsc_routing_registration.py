from __future__ import annotations

import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
KBSC_PROMPT = PROMPT_ROOT / "ACTIVE_PROMPTS" / "04_box_architecture_and_boundaries" / "kanda_box_shielding_canon.md"
KBSC_META = PROMPT_ROOT / "METADATA" / "kanda_box_shielding_canon.meta.json"
AI_PROMPT_REQUEST_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md"
ACTIVE_NAV = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
ROUTING_NAV = PROMPT_ROOT / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md"
GROUP_INDEX = PROMPT_ROOT / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md"
FOLDER_INDEX = PROMPT_ROOT / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
FOLDER_CARD = PROMPT_ROOT / "ACTIVE_PROMPTS" / "04_box_architecture_and_boundaries" / "_FOLDER_ASSIMILATION.md"
PROMPT_NAV_JSON = PROMPT_ROOT / "ROUTING" / "prompt_navigation_index.json"
GROUP_JSON = PROMPT_ROOT / "ROUTING" / "group_assimilation_index.json"
FOLDER_JSON = PROMPT_ROOT / "ROUTING" / "folder_assimilation_cards_index.json"


class KbscRoutingRegistrationTests(unittest.TestCase):
    def test_kbsc_prompt_exists_and_restores_method(self) -> None:
        text = KBSC_PROMPT.read_text(encoding="utf-8")
        required_phrases = [
            "# KANDA BOX SHIELDING CANON (KBSC) v1.0",
            "KBSC RESTORE MODE ACTIVE",
            "architectural fitness-function suite for a bounded context",
            "The machine may suggest.",
            "The canon decides.",
            "No other box logic is invaded.",
            "Tests-first rule",
            "No Placeholder Commitment Rule",
            "Dependency ceiling rule",
            "Routing Signal Scorer application",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_metadata_registers_kbsc_as_on_request_box_architecture_prompt(self) -> None:
        data = json.loads(KBSC_META.read_text(encoding="utf-8"))
        self.assertEqual(data["prompt_id"], "kanda_box_shielding_canon")
        self.assertEqual(data["category"], "04_box_architecture_and_boundaries")
        self.assertEqual(data["load_type"], "on_request")
        self.assertTrue(data["requires_tests_first"])
        self.assertTrue(data["pre_stronger_ml_shield_required"])
        self.assertIn("final_route", data["forbidden_authority"])
        self.assertIn("automatic_prompt_loading", data["forbidden_authority"])

    def test_human_readable_indexes_route_to_kbsc(self) -> None:
        for path in [AI_PROMPT_REQUEST_CANON, ACTIVE_NAV, ROUTING_NAV, GROUP_INDEX, FOLDER_INDEX, FOLDER_CARD]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("kanda_box_shielding_canon", text, msg=str(path))
            self.assertTrue(
                "KBSC" in text or "KANDA Box Shielding Canon" in text,
                msg=str(path),
            )

    def test_machine_readable_prompt_navigation_registers_kbsc(self) -> None:
        data = json.loads(PROMPT_NAV_JSON.read_text(encoding="utf-8"))
        entries = data["entries"]
        self.assertEqual(data["prompt_count"], len(entries))
        kbsc_entries = [entry for entry in entries if entry.get("prompt_id") == "kanda_box_shielding_canon"]
        self.assertEqual(len(kbsc_entries), 1)
        entry = kbsc_entries[0]
        self.assertEqual(entry["relative_path"], "ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md")
        self.assertEqual(entry["priority"], 4)
        self.assertIn("box_architecture_canon", entry["required_companion_prompts"])
        self.assertIn("bundle_gated_development_workflow", entry["required_companion_prompts"])

    def test_group_and_folder_machine_indexes_include_kbsc(self) -> None:
        group_data = json.loads(GROUP_JSON.read_text(encoding="utf-8"))
        group = next(item for item in group_data["groups"] if item["group_id"] == "04_box_architecture_and_boundaries")
        self.assertEqual(group["prompt_count"], 5)
        self.assertIn("kanda_box_shielding_canon.md", group["main_prompts"])
        self.assertIn("box shielding", group["required_for"])

        folder_data = json.loads(FOLDER_JSON.read_text(encoding="utf-8"))
        folder = next(item for item in folder_data["folders"] if item["folder_id"] == "04_box_architecture_and_boundaries")
        self.assertEqual(folder["prompt_count"], 5)
        self.assertIn("kanda_box_shielding_canon", folder["main_prompt_ids"])
        self.assertIn("kanda_box_shielding_canon", folder["minimum_viable_context"])

    def test_kbsc_route_blocks_stronger_ml_until_shield_freeze(self) -> None:
        text = AI_PROMPT_REQUEST_CANON.read_text(encoding="utf-8")
        self.assertIn("Do not continue to stronger ML", text)
        self.assertIn("May proceed now: NO for implementation", text)
        self.assertIn("installed, validated, and frozen", text)

    def test_kbsc_remains_on_request_not_startup_always_loaded(self) -> None:
        source_map = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
        data = json.loads(source_map.read_text(encoding="utf-8"))
        generated_names = {entry["generated_filename"] for entry in data["startup_sources"]}
        canonical_sources = {entry["canonical_source"] for entry in data["startup_sources"]}
        self.assertNotIn("kanda_box_shielding_canon.md", generated_names)
        self.assertNotIn(
            "prompt_library/ACTIVE_PROMPTS/04_box_architecture_and_boundaries/kanda_box_shielding_canon.md",
            canonical_sources,
        )


if __name__ == "__main__":
    unittest.main()
