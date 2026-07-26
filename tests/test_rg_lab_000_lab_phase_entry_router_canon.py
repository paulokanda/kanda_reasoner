from __future__ import annotations

import json
import unittest
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
LAB_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "routing_signal_scorer_v3_lab_phase_entry_router_canon.md"
LAB_META = PROMPT_ROOT / "METADATA" / "routing_signal_scorer_v3_lab_phase_entry_router_canon.meta.json"
PILOT_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "routing_signal_scorer_v3_pilot_copilot_phase0_router_canon.md"
AI_PROMPT_REQUEST_CANON = PROMPT_ROOT / "ACTIVE_PROMPTS" / "01_session_start_and_navigation" / "ai_prompt_request_canon.md"
ACTIVE_NAV = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_navigation_index.md"
PROMPT_ROUTER = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "prompt_router.md"
FOLDER_CARD = PROMPT_ROOT / "ACTIVE_PROMPTS" / "02_prompt_routing_and_indexing" / "_FOLDER_ASSIMILATION.md"
ROUTING_NAV = PROMPT_ROOT / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md"
GROUP_INDEX = PROMPT_ROOT / "ROUTING" / "GROUP_ASSIMILATION_INDEX.md"
FOLDER_INDEX = PROMPT_ROOT / "ROUTING" / "FOLDER_ASSIMILATION_CARDS_INDEX.md"
PROMPT_NAV_JSON = PROMPT_ROOT / "ROUTING" / "prompt_navigation_index.json"
GROUP_JSON = PROMPT_ROOT / "ROUTING" / "group_assimilation_index.json"
FOLDER_JSON = PROMPT_ROOT / "ROUTING" / "folder_assimilation_cards_index.json"
SOURCE_MAP = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_tools" / "STARTUP_ROUTING_KERNEL_SOURCES.json"
STARTUP_ZIP = PROJECT_ROOT / "kanda_prompt_workspace" / "first_AI_deliver" / "first_prompts_to_ai.zip"


class RgLab000LabPhaseEntryRouterCanonTests(unittest.TestCase):
    def test_lab_router_canon_exists_and_encodes_post_p12_flux(self) -> None:
        text = LAB_CANON.read_text(encoding="utf-8")
        required = [
            "# RG-LAB-000 - ML LAB Phase Entry Router Canon",
            "After P12, canonize LAB entry first",
            "build and validate the LAB before testing ML router prompt logic",
            "validate ML router prompt logic reliability before continuing ML implementation",
            "LAB-0 - Phase Boundary + Lab Charter / Entry Gate",
            "LAB-0 is documentation-only",
            "ML logic implementation may continue only after all of the following are true",
            "The critical boundary error budget remains zero",
            "Preferred future LAB primary box",
            "Alpha corpus: 60-80 curated, manually reviewed tests",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_lab_router_canon_forbids_runtime_and_direct_ml_shortcuts(self) -> None:
        text = LAB_CANON.read_text(encoding="utf-8")
        forbidden_phrases = [
            "Do not skip directly from P12 to ML implementation.",
            "Do not continue ML implementation directly after P12.",
            "Do not start LAB coding before LAB-0 freezes.",
            "unauthorized prompt loading",
            "provider call",
            "embedding/vector-store call",
            "activation key",
            "field-test mode",
            "Copilot behavior",
            "LAB output become router output",
        ]
        for phrase in forbidden_phrases:
            self.assertIn(phrase, text)

    def test_metadata_registers_lab_canon_as_on_request_and_no_authority(self) -> None:
        data = json.loads(LAB_META.read_text(encoding="utf-8"))
        self.assertEqual(data["prompt_id"], "routing_signal_scorer_v3_lab_phase_entry_router_canon")
        self.assertEqual(data["category"], "02_prompt_routing_and_indexing")
        self.assertEqual(data["load_type"], "on_request")
        self.assertTrue(data["on_request_not_startup_always_loaded"])
        self.assertTrue(data["requires_lab_before_ml_implementation_continuation"])
        self.assertTrue(data["requires_lab_self_validation_before_ml_router_prompt_logic_reliability_claim"])
        self.assertIn("automatic_prompt_loading", data["forbidden_authority"])
        self.assertIn("provider_calls", data["forbidden_authority"])
        self.assertIn("activation_key", data["forbidden_authority"])
        self.assertIn("runner code", data["forbidden_in_lab0"])

    def test_human_readable_routing_assets_register_lab_canon(self) -> None:
        for path in [AI_PROMPT_REQUEST_CANON, ACTIVE_NAV, PROMPT_ROUTER, FOLDER_CARD, ROUTING_NAV, GROUP_INDEX, FOLDER_INDEX]:
            text = path.read_text(encoding="utf-8")
            self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon", text, msg=str(path))
            self.assertTrue("RG-LAB-000" in text or "post-P12 LAB" in text, msg=str(path))

    def test_prompt_request_canon_requires_exact_context_and_blocks_direct_ml(self) -> None:
        text = AI_PROMPT_REQUEST_CANON.read_text(encoding="utf-8")
        self.assertIn("RG-LAB-000 Post-P12 ML LAB phase entry exact context package", text)
        self.assertIn("After P12, canonize LAB entry first", text)
        self.assertIn("Do not continue ML implementation directly after P12", text)
        self.assertIn("NO for ML implementation or LAB coding", text)

    def test_prompt_router_routes_next_after_p12_to_lab_entry_not_ml_implementation(self) -> None:
        text = PROMPT_ROUTER.read_text(encoding="utf-8")
        self.assertIn("### RG-LAB-000 post-P12 ML LAB phase entry", text)
        self.assertIn("After P12, \"next\" does not mean direct ML implementation", text)
        self.assertIn("First canonize LAB entry, then route to LAB-0 only", text)
        self.assertIn("LAB-0 is documentation-only", text)

    def test_machine_readable_prompt_navigation_registers_lab_canon_once(self) -> None:
        data = json.loads(PROMPT_NAV_JSON.read_text(encoding="utf-8"))
        entries = data["entries"]
        self.assertEqual(data["prompt_count"], len(entries))
        matches = [entry for entry in entries if entry.get("prompt_id") == "routing_signal_scorer_v3_lab_phase_entry_router_canon"]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["relative_path"], "ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_lab_phase_entry_router_canon.md")
        self.assertIn("continue after P12", entry["trigger_phrases"])
        self.assertIn("routing_signal_scorer_v3_pilot_copilot_phase0_router_canon", entry["required_companion_prompts"])
        self.assertIn("kanda_box_shielding_canon", entry["required_companion_prompts"])

    def test_group_and_folder_machine_indexes_include_lab_route(self) -> None:
        group_data = json.loads(GROUP_JSON.read_text(encoding="utf-8"))
        group = next(item for item in group_data["groups"] if item["group_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(group["prompt_count"], len(group["main_prompts"]))
        self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon.md", group["main_prompts"])
        self.assertIn("post-P12 LAB phase entry router canonization", group["required_for"])
        route = next(item for item in group_data["task_routes"] if item["task_intent"] == "POST_P12_LAB_PHASE_ENTRY_OR_ML_ROUTER_RELIABILITY")
        self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon", route["required_groups"])
        self.assertEqual(route["fast_path_allowed"], "NO")
        self.assertIn("LAB_0_only_after_RG_LAB_000_freeze", route["missing_behavior"])

        folder_data = json.loads(FOLDER_JSON.read_text(encoding="utf-8"))
        folder = next(item for item in folder_data["folders"] if item["folder_id"] == "02_prompt_routing_and_indexing")
        self.assertEqual(folder["prompt_count"], len(folder["main_prompt_ids"]))
        self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon", folder["main_prompt_ids"])
        self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon", folder["minimum_viable_context"])

    def test_lab_canon_remains_on_request_not_startup_always_loaded(self) -> None:
        data = json.loads(SOURCE_MAP.read_text(encoding="utf-8"))
        generated_names = {entry["generated_filename"] for entry in data["startup_sources"]}
        canonical_sources = {entry["canonical_source"] for entry in data["startup_sources"]}
        self.assertNotIn("routing_signal_scorer_v3_lab_phase_entry_router_canon.md", generated_names)
        self.assertNotIn(
            "prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/routing_signal_scorer_v3_lab_phase_entry_router_canon.md",
            canonical_sources,
        )

    def test_startup_zip_contains_updated_routing_hooks_but_not_full_lab_canon(self) -> None:
        with zipfile.ZipFile(STARTUP_ZIP) as zf:
            names = set(zf.namelist())
            self.assertIn("01_ai_prompt_request_canon.md", names)
            self.assertIn("02_prompt_navigation_index.md", names)
            self.assertIn("03_GROUP_ASSIMILATION_INDEX.md", names)
            self.assertIn("04_FOLDER_ASSIMILATION_CARDS_INDEX.md", names)
            self.assertNotIn("routing_signal_scorer_v3_lab_phase_entry_router_canon.md", names)
            nav = zf.read("02_prompt_navigation_index.md").decode("utf-8")
            group = zf.read("03_GROUP_ASSIMILATION_INDEX.md").decode("utf-8")
            self.assertIn("RG-LAB-000", nav)
            self.assertIn("routing_signal_scorer_v3_lab_phase_entry_router_canon", nav)
            self.assertIn("POST_P12_LAB_PHASE_ENTRY_OR_ML_ROUTER_RELIABILITY", group)

    def test_pilot_canon_points_to_rg_lab_after_p12(self) -> None:
        text = PILOT_CANON.read_text(encoding="utf-8")
        self.assertIn("## Post-P12 LAB handoff addendum", text)
        self.assertIn("RG-LAB-000 - Router Prompt Logic Canon for LAB Phase Entry", text)
        self.assertIn("only then continue ML logic implementation", text)


if __name__ == "__main__":
    unittest.main()
