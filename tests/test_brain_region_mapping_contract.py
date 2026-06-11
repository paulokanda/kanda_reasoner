"""Focused tests for the Brain Region Mapping Box."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOX_ROOT = (
    PROJECT_ROOT
    / "kanda_reasoner_app"
    / "reasoner_tools_gui_shell"
    / "brain_region_mapping"
)
CONTRACT_PATH = BOX_ROOT / "contract.py"
PRIVATE_DATA_PATH = BOX_ROOT / "_mapping_data.py"
MANIFEST_PATH = BOX_ROOT / "box_manifest.json"
README_PATH = BOX_ROOT / "README.md"

FORBIDDEN_IMPORT_ROOTS = (
    "PySide6",
    "QWebEngineView",
    "main_window",
    "tool_specs",
    "brain_navigator",
    "remember_box",
    "tab_navigation_controller",
)

EXPECTED_REGION_TO_TAB = {
    "frontal_lobe": "architecture_review",
    "parietal_lobe": "workflow_review",
    "brainstem_midbrain": "engineering_safety",
    "cerebellar_folia": "docstring_assistant",
    "occipital_lobe": "project_structure_map",
    "central_sulcus": "ai_import_builder",
    "cerebellum": "refactor_report",
    "temporal_lobe": "project_qa",
    "lateral_sulcus": "exclusion_rules",
    "longitudinal_fissure": "prompt_library",
}


class BrainRegionMappingContractTests(unittest.TestCase):
    """Verify the Brain Region Mapping box is pure, complete, and safe."""

    def test_public_contract_imports_contract_module_directly(self) -> None:
        """The focused test should import the public contract module directly."""

        import kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping.contract as contract_module

        self.assertEqual(
            "brain_region_mapping",
            contract_module.BRAIN_REGION_MAPPING_BOX_ID,
        )
        self.assertEqual(
            "0.1",
            contract_module.BRAIN_REGION_MAPPING_CONTRACT_VERSION,
        )
        self.assertIn(
            "resolve_brain_region",
            contract_module.__all__,
        )

    def test_public_package_imports_without_gui_side_effects(self) -> None:
        """The package facade should import without Qt, WebEngine, or registry."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            BRAIN_REGION_MAPPING_BOX_ID,
            BRAIN_REGION_MAPPING_CONTRACT_VERSION,
        )

        self.assertEqual("brain_region_mapping", BRAIN_REGION_MAPPING_BOX_ID)
        self.assertEqual("0.1", BRAIN_REGION_MAPPING_CONTRACT_VERSION)

    def test_summary_declares_pure_mapping_box_boundary(self) -> None:
        """The summary should describe a pure data mapping box."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            get_brain_region_mapping_summary,
        )

        summary = get_brain_region_mapping_summary()

        self.assertEqual("brain_region_mapping", summary.box_id)
        self.assertEqual("0.1", summary.contract_version)
        self.assertEqual("pure_mapping_box", summary.implementation_state)
        self.assertEqual(10, summary.target_count)
        self.assertIn("resolve_brain_region", summary.public_functions)
        self.assertIn(
            "kanda_reasoner_app/reasoner_tools_gui_shell/brain_region_mapping/",
            summary.owner_paths,
        )

    def test_known_region_ids_are_unique_and_complete(self) -> None:
        """The mapping should expose the expected canonical brain regions."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            list_brain_region_ids,
        )

        region_ids = list_brain_region_ids()

        self.assertEqual(len(region_ids), len(set(region_ids)))
        self.assertEqual(tuple(EXPECTED_REGION_TO_TAB.keys()), region_ids)

    def test_region_targets_map_to_expected_tab_ids(self) -> None:
        """Each canonical region should map to the intended stable tab ID."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            resolve_brain_region,
        )

        for region_id, tab_id in EXPECTED_REGION_TO_TAB.items():
            with self.subTest(region_id=region_id):
                target = resolve_brain_region(region_id)
                self.assertTrue(target.is_known)
                self.assertEqual(region_id, target.region_id)
                self.assertEqual(tab_id, target.target_tab_id)
                self.assertTrue(target.target_tab_label)
                self.assertTrue(target.analogy_text)
                self.assertIn("->", target.tooltip_text)

    def test_all_target_tab_ids_exist_in_dynamic_registry(self) -> None:
        """The pure mapping should stay aligned with the dynamic tab registry."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            list_brain_region_targets,
        )
        from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS

        registry_labels_by_id = {
            spec.tab_id: spec.step_title
            for spec in TOOLS
            if getattr(spec, "tab_id", None)
        }

        for target in list_brain_region_targets():
            with self.subTest(region_id=target.region_id):
                self.assertIn(target.target_tab_id, registry_labels_by_id)
                self.assertEqual(
                    registry_labels_by_id[target.target_tab_id],
                    target.target_tab_label,
                )

    def test_unknown_region_returns_safe_fallback(self) -> None:
        """Unknown regions should not raise or request tab switching."""

        from kanda_reasoner_app.reasoner_tools_gui_shell.brain_region_mapping import (
            is_known_brain_region,
            resolve_brain_region,
        )

        self.assertFalse(is_known_brain_region("not_real"))
        target = resolve_brain_region("not_real")

        self.assertFalse(target.is_known)
        self.assertEqual("not_real", target.region_id)
        self.assertEqual("", target.target_tab_id)
        self.assertEqual("No target tab", target.target_tab_label)
        self.assertEqual("Unmapped", target.category)
        self.assertIn("safe fallback", target.analogy_text)

    def test_manifest_declares_box_architecture_metadata(self) -> None:
        """The manifest should describe ownership, contract, and restrictions."""

        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual("brain_region_mapping", manifest["box_id"])
        self.assertEqual("data", manifest["box_type"])
        self.assertEqual("module", manifest["box_size"])
        self.assertEqual("draft", manifest["health_state"])
        self.assertEqual("0.1", manifest["contract_version"])
        self.assertTrue(manifest["disable_safe"])
        self.assertEqual("optional", manifest["removal_policy"])
        self.assertIn("_mapping_data.py", manifest["private_internals"])
        self.assertIn("PySide6", manifest["forbidden_dependencies"])
        self.assertIn(
            "resolve_brain_region",
            manifest["public_contract"]["provides_functions"],
        )

    def test_mapping_box_has_no_forbidden_imports_or_tab_switch_calls(self) -> None:
        """The mapping box should not import GUI, registry, or navigation boxes."""

        for path in (CONTRACT_PATH, PRIVATE_DATA_PATH):
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                tree = ast.parse(text)
                imported_roots: set[str] = set()
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        imported_roots.update(
                            alias.name.split(".")[0] for alias in node.names
                        )
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imported_roots.add(node.module.split(".")[0])

                for token in FORBIDDEN_IMPORT_ROOTS:
                    self.assertNotIn(token, imported_roots)
                self.assertNotIn("setCurrentIndex", text)

    def test_readme_declares_no_gui_or_navigation_ownership(self) -> None:
        """The README should make the pure data boundary explicit."""

        readme_text = README_PATH.read_text(encoding="utf-8")

        self.assertIn("pure mapping box", readme_text)
        self.assertIn("does not render the brain", readme_text)
        self.assertIn("does not open tabs", readme_text)
        self.assertIn("does not import PySide6", readme_text)


if __name__ == "__main__":
    unittest.main()
