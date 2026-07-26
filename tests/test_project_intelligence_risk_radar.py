"""Validation for Project Intelligence Risk Change Radar v1."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_intelligence import (  # noqa: E402
    ADVISORY_SOURCE_TRUTH_WARNING,
    RiskChangeRadar,
    RiskRadarResult,
)


def _snapshot(root: Path) -> set[str]:
    """Return all existing paths below root as relative slash paths."""
    return {path.relative_to(root).as_posix() for path in root.rglob("*")}


def _assert(condition: bool, message: str) -> None:
    """Raise AssertionError with a readable message when condition is false."""
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Run direct validation script."""
    with tempfile.TemporaryDirectory() as tmp_name:
        project_root = Path(tmp_name) / "sample_project"
        project_root.mkdir()
        before = _snapshot(project_root)

        changed_paths = [
            "kanda_prompt_workspace/prompt_library/ACTIVE_PROMPTS/02_prompt_routing_and_indexing/prompt_router.md",
            "kanda_reasoner_app/freeze_after_update/templates.py",
            "kanda_reasoner_app/error_memory/intake.py",
            "scripts/validate_patch_zip.py",
            "tests/test_project_intelligence_risk_radar.py",
            "kanda_reasoner_app/reasoner_tools_gui_shell/tool_specs.py",
            "E:/sample_project/kanda_reasoner_app/project_intelligence/risk_radar.py",
            "E:/sample_project/kanda_reasoner_app/project_intelligence/risk_radar.py",
            "normal_module.py",
        ]

        radar = RiskChangeRadar()
        result = radar.run_scan(project_root, changed_paths)
        _assert(isinstance(result, RiskRadarResult), "run_scan must return RiskRadarResult")
        data = result.to_dict()
        report = data["report"]
        findings = report["findings"]
        categories = {finding["category"] for finding in findings}

        _assert("prompt-routing" in categories, "prompt-routing risk not detected")
        _assert("freeze-memory" in categories, "freeze-memory risk not detected")
        _assert("error-memory" in categories, "error-memory risk not detected")
        _assert("patch-delivery" in categories, "patch-delivery risk not detected")
        _assert("validation-contract" in categories, "validation-contract risk not detected")
        _assert("gui-workflow" in categories, "gui-workflow risk not detected")
        _assert(report["status"] == "completed_with_findings", "report status should show findings")
        _assert(report["metadata"]["mode"] == "path_based_v1", "metadata mode missing")
        _assert(len(result.scanned_paths) == 8, "changed paths should be deduplicated")
        _assert(ADVISORY_SOURCE_TRUTH_WARNING in report["ai_must_not_assume"], "advisory warning missing")

        text = radar.to_markdown(result)
        _assert("Project Intelligence Risk Change Radar v1" in text, "markdown title missing")
        _assert("What an AI must not assume" in text, "standard section missing")
        _assert("ZIP contract" in text or "ZIP CONTRACT" in text, "validation guidance missing")
        _assert(ADVISORY_SOURCE_TRUTH_WARNING in text, "markdown advisory warning missing")

        empty_result = radar.run_scan(project_root, [])
        _assert(empty_result.report.status == "ok", "empty scan should not fail")
        _assert(empty_result.report.warnings, "empty scan should warn about missing paths")

        json.dumps(data, sort_keys=True)
        after = _snapshot(project_root)
        _assert(before == after, "Risk Radar must not write files to the target project root")

    print("VALIDATION OK: project-intelligence-risk-radar-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
