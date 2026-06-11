"""Regression tests for T10P066 runtime/data collector canonical refs."""

from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_TOKEN = "_".join(("ask", "ai", "project", "reasoner"))
CANONICAL_TOKEN = "kanda_reasoner_app"
OWNER_DIRS = (
    ROOT / LEGACY_TOKEN / "runtime_scenarios",
    ROOT / LEGACY_TOKEN / "reasoner_context_collector",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _owner_python_files() -> list[Path]:
    files: list[Path] = []
    for owner_dir in OWNER_DIRS:
        files.extend(sorted(owner_dir.rglob("*.py")))
    return files


class RuntimeDataCollectorCanonicalRefsTests(unittest.TestCase):
    """Verify runtime/data collector legacy tokens are dynamic or canonical."""

    def test_owner_python_files_do_not_contain_literal_legacy_package_token(self) -> None:
        offenders = [
            str(path.relative_to(ROOT))
            for path in _owner_python_files()
            if LEGACY_TOKEN in _read(path)
        ]
        self.assertEqual([], offenders)

    def test_runtime_scenarios_use_canonical_runtime_imports(self) -> None:
        traces = _read(ROOT / LEGACY_TOKEN / "runtime_scenarios" / "collector_scenario_traces.py")
        runtime = _read(ROOT / LEGACY_TOKEN / "runtime_scenarios" / "runtime_scenario_runtime.py")

        self.assertIn(f"from {CANONICAL_TOKEN}.runtime_scenarios.runtime_scenario_writer import", traces)
        self.assertIn(f"from {CANONICAL_TOKEN}.runtime_scenarios.runtime_trace_retention import", traces)
        self.assertIn(f"from {CANONICAL_TOKEN}.runtime_scenarios.runtime_scenario_writer import", runtime)

    def test_runtime_hotspot_hooks_use_canonical_module_contracts(self) -> None:
        text = _read(ROOT / LEGACY_TOKEN / "runtime_scenarios" / "runtime_hotspot_hooks.py")

        self.assertIn(f"{CANONICAL_TOKEN}.reasoner_context_collector.collector_main", text)
        self.assertIn(f"{CANONICAL_TOKEN}.reasoner_context_collector.collector_runtime_scenarios", text)
        self.assertIn('"domain_scope": "kanda_reasoner_app"', text)
        self.assertIn('"kanda_reasoner_app/"', text)

    def test_runtime_trace_retention_keeps_staged_path_dynamic(self) -> None:
        text = _read(ROOT / LEGACY_TOKEN / "runtime_scenarios" / "runtime_trace_retention.py")

        self.assertIn('_STAGED_PACKAGE_NAME = "_".join(("ask", "ai", "project", "reasoner"))', text)
        self.assertIn('/ _STAGED_PACKAGE_NAME', text)

    def test_data_collector_uses_canonical_imports_and_dynamic_validators(self) -> None:
        runtime_scenarios = _read(
            ROOT / LEGACY_TOKEN / "reasoner_context_collector" / "collector_runtime_scenarios.py"
        )
        collector_scope = _read(
            ROOT / LEGACY_TOKEN / "reasoner_context_collector" / "collector_scope.py"
        )
        collector_utils = _read(
            ROOT / LEGACY_TOKEN / "reasoner_context_collector" / "collector_utils.py"
        )
        overlap_validator = _read(
            ROOT
            / LEGACY_TOKEN
            / "reasoner_context_collector"
            / "collector_responsibility_overlap_validate_manifests.py"
        )
        widget_validator = _read(
            ROOT
            / LEGACY_TOKEN
            / "reasoner_context_collector"
            / "collector_widget_registry_validate_manifests.py"
        )

        self.assertIn(f"from {CANONICAL_TOKEN}.backend_payloads.loader import", runtime_scenarios)
        self.assertIn('"build_runtime_scenario_index"', runtime_scenarios)
        self.assertIn(f"from {CANONICAL_TOKEN}.project_exclusion_policy import", collector_scope)
        self.assertIn(f"from {CANONICAL_TOKEN}.project_json_scope_filter import", collector_utils)
        self.assertIn("ROOT / _STAGED_PACKAGE_NAME /", overlap_validator)
        self.assertIn("ROOT / _STAGED_PACKAGE_NAME /", widget_validator)


if __name__ == "__main__":
    unittest.main()
