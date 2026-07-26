# project-path: tools/validate_project_web_ai_governed_apply_architecture_v1.py
"""Validate strict architecture gates for Project Web AI Governed Apply."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

TOUCHED_CODE = (
    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_contracts.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_receipts.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_apply_workflow.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_write_broker.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_write_storage.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_switch_guard.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_bridge.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_session.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preview.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_change_preparation.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab.py",
    "kanda_reasoner_app/reasoner_engine/project_web_ai_tab_ui.py",
    "tools/validate_project_web_ai_governed_apply_v1.py",
    "tools/validate_project_web_ai_prepare_changes_v1.py",
    "tools/validate_project_web_ai_project_switch_hygiene_v1.py",
    "tools/validate_project_web_ai_governed_apply_architecture_v1.py",
)


def require(condition: bool, message: str) -> None:
    """Raise one focused architecture validation failure."""
    if not condition:
        raise AssertionError(message)


def main() -> int:
    """Run strict scans and module-size gates for every touched source owner."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    sys.path.insert(0, str(root))
    architecture = importlib.import_module(
        "kanda_reasoner_app.manage_architecture.manage_architecture"
    )
    modules = {}
    for relative in TOUCHED_CODE:
        path = root / relative
        require(path.is_file(), "Touched source is missing: " + relative)
        require(
            len(path.read_text(encoding="utf-8").splitlines()) <= 500,
            relative + " exceeds 500 physical lines",
        )
        module, warnings = architecture.scan_module(root, path, set())
        require(not warnings, relative + " warnings: " + repr(warnings))
        modules[module.module_id] = module
    issues = architecture.detect_symbol_shadowing_issues(root, modules)
    require(not issues, "Symbol shadowing remains: " + repr(issues))
    print("GOVERNED_APPLY_ARCHITECTURE_WARNINGS_ZERO: PASS")
    print("GOVERNED_APPLY_SYMBOL_SHADOWING_ZERO: PASS")
    print("TOUCHED_SOURCE_MODULES_MAX_500_LINES: PASS")
    print("VALIDATION OK: project-web-ai-governed-apply-architecture-v1")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
