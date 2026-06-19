import ast
import contextlib
import io
import json
import unittest
from dataclasses import FrozenInstanceError, is_dataclass
from pathlib import Path

from kanda_reasoner_app.routing_signal_scorer.adviser_offline.transition_design.shadow_mode_boundary_design import (
    AUTHORITY_DISCLAIMER,
    DESIGN_KIND,
    FEATURE_ID,
    NEXT_ALLOWED_MILESTONE,
    SCHEMA_VERSION,
    build_shadow_mode_boundary_design,
)

ROOT = Path(__file__).resolve().parents[1]
BOX = ROOT / "kanda_reasoner_app" / "routing_signal_scorer"
ADVISER = BOX / "adviser_offline"
TRANSITION = ADVISER / "transition_design"
MODULE = TRANSITION / "shadow_mode_boundary_design.py"
THREAT_MODEL = TRANSITION / "shadow_mode_threat_model.md"
MANIFEST = BOX / "box_manifest.json"


FORBIDDEN_IMPORT_PREFIXES = (
    "os",
    "sys",
    "pathlib",
    "subprocess",
    "socket",
    "threading",
    "multiprocessing",
    "tempfile",
    "importlib",
    "pickle",
    "shelve",
    "sqlite3",
    "requests",
    "httpx",
    "aiohttp",
    "kanda_reasoner_app.routing_signal_scorer.contract",
    "kanda_reasoner_app.routing_signal_scorer.runtime",
    "kanda_reasoner_app.routing_signal_scorer.router",
    "kanda_reasoner_app.prompt_loader",
    "kanda_reasoner_app.freeze_after_update",
    "kanda_reasoner_app.project_freeze_ledger",
)

FORBIDDEN_CALLS = (
    "open",
    "print",
    "eval",
    "exec",
    "compile",
    "__import__",
    "getenv",
    "putenv",
    "system",
    "popen",
    "import_module",
)

UNSAFE_FIELD_NAMES = (
    "confidence",
    "score",
    "probability",
    "approved",
    "enabled",
    "activated",
    "promoted",
    "selected",
    "final_route",
    "recommended_route",
    "suggested_prompt",
    "assistant_transition_relevance",
    "assistant_transition_review_candidate",
    "promotion_ready",
)


class ShadowModeBoundaryDesignTests(unittest.TestCase):
    def _module_ast(self):
        return ast.parse(MODULE.read_text(encoding="utf-8"))

    def _all_field_names(self, value):
        names = set()
        if is_dataclass(value):
            for field_name in value.__dataclass_fields__:
                names.add(field_name)
                names.update(self._all_field_names(getattr(value, field_name)))
        elif isinstance(value, tuple):
            for item in value:
                names.update(self._all_field_names(item))
        return names

    def test_manifest_declares_m18_boundary_without_runtime_behavior(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["shadow_mode_boundary_design_feature_id"], FEATURE_ID)
        self.assertEqual(manifest["shadow_mode_boundary_design_schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            manifest["shadow_mode_boundary_design_status"],
            "immutable_design_only_boundary_no_shadow_activation_no_assistant_behavior_no_runtime_authority",
        )
        for key in (
            "shadow_mode_boundary_design_contains_file_io",
            "shadow_mode_boundary_design_contains_persistence",
            "shadow_mode_boundary_design_contains_logging",
            "shadow_mode_boundary_design_contains_prompt_loading",
            "shadow_mode_boundary_design_contains_source_scanning",
            "shadow_mode_boundary_design_contains_runtime_integration",
            "shadow_mode_boundary_design_contains_router_authority",
            "shadow_mode_boundary_design_contains_candidate_promotion",
            "shadow_mode_boundary_design_contains_shadow_activation",
            "shadow_mode_boundary_design_contains_assistant_behavior",
            "shadow_mode_boundary_design_contains_embeddings_or_providers",
            "shadow_mode_boundary_design_contains_report_writer",
            "shadow_mode_boundary_design_contains_gold_or_registry_mutation",
        ):
            self.assertIs(manifest[key], False, key)
        self.assertEqual(
            manifest["shadow_mode_boundary_design_next_allowed_milestone"],
            NEXT_ALLOWED_MILESTONE,
        )

    def test_boundary_record_is_immutable_static_and_design_only(self):
        first = build_shadow_mode_boundary_design()
        second = build_shadow_mode_boundary_design()
        self.assertIs(first, second)
        self.assertEqual(first.feature_id, FEATURE_ID)
        self.assertEqual(first.schema_version, SCHEMA_VERSION)
        self.assertEqual(first.design_kind, DESIGN_KIND)
        self.assertEqual(first.authority_disclaimer, AUTHORITY_DISCLAIMER)
        self.assertEqual(first.next_allowed_milestone, NEXT_ALLOWED_MILESTONE)
        self.assertEqual(first.phase_assertions.adviser_phase, "closed")
        self.assertEqual(first.phase_assertions.post_adviser_transition_design_phase, "started")
        self.assertEqual(first.phase_assertions.shadow_mode_status, "design_only")
        self.assertEqual(first.phase_assertions.assistant_status, "not_started")
        self.assertEqual(first.phase_assertions.pilot_copilot_status, "not_started")
        self.assertEqual(first.phase_assertions.candidate_promotion_status, "blocked")
        self.assertEqual(first.phase_assertions.runtime_authority_status, "not_granted")
        self.assertEqual(first.phase_assertions.implementation_status, "blocked_by_default")
        with self.assertRaises(FrozenInstanceError):
            first.feature_id = "changed"
        with self.assertRaises(FrozenInstanceError):
            first.phase_assertions.shadow_mode_status = "changed"

    def test_public_exports_do_not_add_side_effect_entry_points(self):
        namespace = {}
        exec(MODULE.read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["__all__"], ["build_shadow_mode_boundary_design"])

    def test_ast_rejects_forbidden_imports_and_calls(self):
        tree = self._module_ast()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prefix in FORBIDDEN_IMPORT_PREFIXES:
                        self.assertFalse(alias.name == prefix or alias.name.startswith(prefix + "."), alias.name)
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for prefix in FORBIDDEN_IMPORT_PREFIXES:
                    self.assertFalse(module == prefix or module.startswith(prefix + "."), module)
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                self.assertNotIn(name, FORBIDDEN_CALLS)

    def test_boundary_builder_has_no_file_or_console_side_effects(self):
        before = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            record = build_shadow_mode_boundary_design()
        after = sorted(str(path.relative_to(ROOT)) for path in ROOT.rglob("*"))
        self.assertEqual(before, after)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(record.phase_assertions.shadow_mode_status, "design_only")

    def test_boundary_record_uses_safe_naming_only(self):
        record = build_shadow_mode_boundary_design()
        field_names = self._all_field_names(record)
        for unsafe in UNSAFE_FIELD_NAMES:
            self.assertNotIn(unsafe, field_names)
        joined_values = "\n".join(record.allowed_capability_principles + record.naming_boundary_rules)
        for unsafe in ("confidence", "score", "probability", "promotion_ready"):
            self.assertNotIn(unsafe, joined_values)

    def test_threat_model_exists_and_keeps_m18_design_only(self):
        text = THREAT_MODEL.read_text(encoding="utf-8")
        required = (
            "M18 is secure design only.",
            "Shadow evidence is not authority.",
            "Critical boundary error budget: zero.",
            "Proceed to M19 only after M18 is installed, validated, frozen",
        )
        for item in required:
            self.assertIn(item, text)

    def test_runtime_package_does_not_export_m18_boundary(self):
        contract_text = (BOX / "contract.py").read_text(encoding="utf-8")
        init_text = (BOX / "__init__.py").read_text(encoding="utf-8")
        for forbidden in (
            "shadow_mode_boundary_design",
            "build_shadow_mode_boundary_design",
            "ShadowModeBoundaryDesign",
        ):
            self.assertNotIn(forbidden, contract_text)
            self.assertNotIn(forbidden, init_text)


if __name__ == "__main__":
    unittest.main()
