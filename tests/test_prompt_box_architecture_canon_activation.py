"""Validate the Box Architecture Canon prompt and routing activation metadata.

These tests protect the prompt as an architecture-governance box. They avoid
runtime side effects and only inspect prompt-library text/metadata files.
"""

from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROMPT_ROOT = PROJECT_ROOT / "kanda_prompt_workspace" / "prompt_library"
BOX_FOLDER = (
    PROMPT_ROOT
    / "ACTIVE_PROMPTS"
    / "04_box_architecture_and_boundaries"
)
BOX_CANON = BOX_FOLDER / "box_architecture_canon.md"
BOX_META = PROMPT_ROOT / "METADATA" / "box_architecture_canon.meta.json"
FOLDER_META = (
    PROMPT_ROOT
    / "METADATA"
    / "folder_assimilation_04_box_architecture_and_boundaries.meta.json"
)
FOLDER_CARD = BOX_FOLDER / "_FOLDER_ASSIMILATION.md"
ROUTING_JSON = PROMPT_ROOT / "ROUTING" / "prompt_navigation_index.json"
ROUTING_MD = PROMPT_ROOT / "ROUTING" / "PROMPT_NAVIGATION_INDEX.md"
ROUTE_COVERAGE = PROMPT_ROOT / "ROUTING" / "prompt_route_coverage_table.csv"


class BoxArchitectureCanonActivationTests(unittest.TestCase):
    """Focused tests for Box Architecture Canon activation and routing metadata."""

    def test_prompt_file_contains_required_canon_sections(self) -> None:
        text = BOX_CANON.read_text(encoding="utf-8")
        required_fragments = [
            "# REASONER BOX ARCHITECTURE CANON v1.1",
            "First-Position Box Logic Requirement",
            "Box Boundary Audit",
            "Minimal Pre-Code Checklist",
            "Brain Navigator Example",
            "Do not solve a local problem by contaminating another box.",
            "Project-agnostic rule",
            "Closed-Box Product Delivery Addendum",
        ]
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_prompt_file_protects_boundary_anti_patterns(self) -> None:
        text = BOX_CANON.read_text(encoding="utf-8")
        required_fragments = [
            "God Box",
            "No Private Reach-In",
            "Leaking Registry",
            "GUI-Domain Mixing",
            "Event Bus Fog",
            "State Belongs to One Box",
            "Registry Is a Phone Book, Not a Brain",
            "One Patch Targets One Primary Box",
        ]
        for fragment in required_fragments:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_metadata_marks_canon_as_on_request_box_governance_prompt(self) -> None:
        meta = json.loads(BOX_META.read_text(encoding="utf-8"))
        self.assertEqual(meta["prompt_id"], "box_architecture_canon")
        self.assertEqual(meta["status"], "active")
        self.assertEqual(meta["load_type"], "on_request")
        self.assertTrue(meta["box_logic_required"])
        self.assertTrue(meta["requires_box_boundary_audit"])
        self.assertTrue(meta["pre_code_audit_required_for_project_changes"])
        self.assertEqual(meta["box_architecture_canon_version"], "1.1")
        for trigger in [
            "box architecture",
            "box boundary audit",
            "private reach-in",
            "god box",
            "leaking registry",
            "one primary box",
        ]:
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, meta["trigger_phrases"])

    def test_folder_card_and_folder_metadata_route_to_boundary_audit(self) -> None:
        card = FOLDER_CARD.read_text(encoding="utf-8")
        folder_meta = json.loads(FOLDER_META.read_text(encoding="utf-8"))
        for fragment in [
            "Box Boundary Audit",
            "private internals",
            "anti-contamination rules",
            "box_architecture_canon",
        ]:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, card)
        for trigger in ["box boundary audit", "private reach-in", "one primary box"]:
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, folder_meta["trigger_phrases"])

    def test_prompt_navigation_indexes_include_hardened_box_triggers(self) -> None:
        routing = json.loads(ROUTING_JSON.read_text(encoding="utf-8"))
        entries = []

        def collect(node: object) -> None:
            if isinstance(node, dict):
                if node.get("prompt_id") == "box_architecture_canon":
                    entries.append(node)
                for value in node.values():
                    collect(value)
            elif isinstance(node, list):
                for value in node:
                    collect(value)

        collect(routing)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        for trigger in ["box architecture", "box boundary audit", "private reach-in"]:
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, entry["trigger_phrases"])
        self.assertIn("box boundary audit", entry["aliases"])
        self.assertIn("GUI ownership change", entry["when_to_load"])

        routing_md = ROUTING_MD.read_text(encoding="utf-8")
        self.assertIn("box boundary audit", routing_md)
        self.assertIn("private reach-in", routing_md)
        self.assertIn("GUI ownership change", routing_md)

    def test_route_coverage_table_matches_box_canon_triggers(self) -> None:
        with ROUTE_COVERAGE.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        row = next(row for row in rows if row["prompt_id"] == "box_architecture_canon")
        self.assertIn("box boundary audit", row["trigger_phrases"])
        self.assertIn("private reach-in", row["trigger_phrases"])
        self.assertIn("GUI ownership change", row["when_to_load"])
        self.assertIn("pure explanation", row["when_not_to_load"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
