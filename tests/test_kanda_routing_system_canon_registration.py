from __future__ import annotations

import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
ROUTING_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "kanda_routing_system_canon.md"
ROUTING_META = PROMPT_ROOT / "METADATA" / "kanda_routing_system_canon.meta.json"
AI_PROMPT_REQUEST_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md"
ACTIVE_NAV = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
FOLDER_CARD = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "_FOLDER_ASSIMILATION.md"
ROUTING_NAV = PROMPT_ROOT / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md"
GROUP_INDEX = PROMPT_ROOT / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md"
FOLDER_INDEX = PROMPT_ROOT / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
PROMPT_NAV_JSON = PROMPT_ROOT / "ROUTING" / "prompt_navigation_index.json"
GROUP_JSON = PROMPT_ROOT / "ROUTING" / "group_assimilation_index.json"
FOLDER_JSON = PROMPT_ROOT / "ROUTING" / "folder_assimilation_cards_index.json"
SOURCE_MAP = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"


class KandaRoutingSystemCanonRegistrationTests(unittest.TestCase):
    def test_routing_canon_prompt_exists_and_is_adapted_from_review_handoff(self) -> None:
        text = ROUTING_CANON.read_text(encoding="utf-8")
        self.assertIn("# KANDA Routing System Canon", text)
        self.assertIn("Purpose and authority", text)
        self.assertIn("context-selection operating system", text)
        self.assertIn("Prompt Registration v2", text)
        self.assertIn("Context Package Manifest", text)
        self.assertIn("Routing Signal Scorer v2 Similarity Layer", text)
        self.assertIn("KANDA Box Shielding Canon", text)
        self.assertIn("Register prompts as routable context assets", text)
        self.assertNotIn("## Role requested", text)
        self.assertNotIn("Please return:", text)

    def test_metadata_registers_routing_canon_as_on_request_prompt(self) -> None:
        data = json.loads(ROUTING_META.read_text(encoding="utf-8"))
        self.assertEqual(data["prompt_id"], "kanda_routing_system_canon")
        self.assertEqual(data["category"], "02_prompt_routing_and_indexing")
        self.assertEqual(data["load_type"], "on_request")
        self.assertTrue(data["on_request_not_startup_always_loaded"])
        self.assertTrue(data["requires_context_package_manifest_for_routed_work"])
        self.assertIn("automatic_prompt_loading", data["forbidden_authority"])
        self.assertIn("router_override", data["forbidden_authority"])

    def test_human_readable_routing_assets_register_the_canon(self) -> None:
        for path in [AI_PROMPT_REQUEST_CANON, ACTIVE_NAV, FOLDER_CARD, ROUTING_NAV, GROUP_INDEX, FOLDER_INDEX]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("kanda_routing_system_canon", text, msg=str(path))
            self.assertTrue(
                "KANDA Routing System Canon" in text or "routing-system canon" in text,
                msg=str(path),
            )

    def test_prompt_request_canon_requires_exact_context_for_routing_system_changes(self) -> None:
        text = AI_PROMPT_REQUEST_CANON.read_text(encoding="utf-8")
        self.assertIn("Routing-system canon exact context package", text)
        self.assertIn("Do not insert prompts globally. Register prompts as routable context assets.", text)
        self.assertIn("May proceed now: NO for implementation", text)
        self.assertIn("Do not auto-load the full routing canon at startup", text)

    def test_machine_readable_prompt_navigation_registers_single_routing_canon_entry(self) -> None:
        data = json.loads(PROMPT_NAV_JSON.read_text(encoding="utf-8"))
        entries = data["entries"]
        self.assertEqual(data["prompt_count"], len(entries))
        matches = [entry for entry in entries if entry.get("prompt_id") == "kanda_routing_system_canon"]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["relative_path"], "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md")
        self.assertEqual(entry["priority"], 3)
        self.assertIn("Context Package Manifest", entry["trigger_phrases"])
        self.assertIn("ai_prompt_request_canon", entry["required_companion_prompts"])
        self.assertIn("GROUP_ASSIMILATION_INDEX", entry["required_companion_prompts"])

    def test_group_and_folder_machine_indexes_count_and_include_routing_canon(self) -> None:
        group_data = json.loads(GROUP_JSON.read_text(encoding="utf-8"))
        group = next(item for item in group_data["groups"] if item["group_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(group["prompt_count"], len(group["main_prompts"]))
        self.assertGreaterEqual(group["prompt_count"], 5)
        self.assertIn("kanda_routing_system_canon.md", group["main_prompts"])
        self.assertIn("Context Package Manifest", group["required_for"])

        folder_data = json.loads(FOLDER_JSON.read_text(encoding="utf-8"))
        folder = next(item for item in folder_data["folders"] if item["folder_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(folder["prompt_count"], len(folder["main_prompt_ids"]))
        self.assertGreaterEqual(folder["prompt_count"], 5)
        self.assertIn("kanda_routing_system_canon", folder["main_prompt_ids"])
        self.assertIn("kanda_routing_system_canon", folder["minimum_viable_context"])

    def test_routing_canon_remains_on_request_not_startup_always_loaded(self) -> None:
        data = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
        generated_names = {entry["generated_filename"] for entry in data["startup_sources"]}
        canonical_sources = {entry["canonical_source"] for entry in data["startup_sources"]}
        self.assertNotIn("kanda_routing_system_canon.md", generated_names)
        self.assertNotIn(
            "prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/kanda_routing_system_canon.md",
            canonical_sources,
        )

    def test_canon_preserves_similarity_advisory_boundary_and_prompt_registration_rule(self) -> None:
        text = ROUTING_CANON.read_text(encoding="utf-8")
        self.assertIn("The similarity scorer may suggest candidate context.", text)
        self.assertIn("The deterministic routing canon decides what is required.", text)
        self.assertIn("Prompts are registered, indexed, validated, and called on demand.", text)
        self.assertIn("Do not build stronger ML before routing_signal_scorer_v2_similarity_box_shield_v1 is frozen.", text)


if __name__ == "__main__":
    unittest.main()
