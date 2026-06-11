"""Focused tests for PA012 facade versus real-owner resolver."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.facade_owner_resolver import (
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW,
    PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE,
    ProjectSymbolAtlasFacadeOwnerOptions,
    build_reasoner_symbol_atlas_facade_owner_report,
    resolve_reasoner_symbol_atlas_facade_owner,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_pa012_detects_facade_and_real_owner() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write(
            project_root / "reasoner_tools_gui.py",
            "from kanda_reasoner_app.reasoner_tools_gui_shell.tool_specs import TOOLS\n"
            "__all__ = ['TOOLS']\n",
        )
        _write(project_root / 'ask_' 'ai_project_reasoner' / "__init__.py", "")
        _write(project_root / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "__init__.py", "")
        _write(
            project_root / 'ask_' 'ai_project_reasoner' / "reasoner_tools_gui_shell" / "tool_specs.py",
            "TOOLS = ()\n",
        )
        decision = resolve_reasoner_symbol_atlas_facade_owner(
            ProjectSymbolAtlasFacadeOwnerOptions(
                project_root=str(project_root),
                target_path="reasoner_tools_gui.py",
                symbol_name="TOOLS",
            )
        )
        assert decision.target_is_facade is True
        assert decision.should_patch_target is False
        assert decision.status == PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NEEDS_OWNER_REVIEW
        assert decision.likely_real_owner_path.endswith("tool_specs.py")


def test_pa012_allows_non_facade_target() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write(project_root / "package" / "__init__.py", "")
        _write(
            project_root / "package" / "implementation.py",
            "def run_task():\n"
            "    return 'ok'\n",
        )
        decision = resolve_reasoner_symbol_atlas_facade_owner(
            ProjectSymbolAtlasFacadeOwnerOptions(
                project_root=str(project_root),
                target_path="package/implementation.py",
                symbol_name="run_task",
            )
        )
        assert decision.target_is_facade is False
        assert decision.should_patch_target is True
        assert decision.status == PROJECT_SYMBOL_ATLAS_FACADE_STATUS_NO_FACADE


def test_pa012_builds_report() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write(project_root / "facade.py", "from owner import VALUE\n__all__ = ['VALUE']\n")
        _write(project_root / "owner.py", "VALUE = 1\n")
        report = build_reasoner_symbol_atlas_facade_owner_report(
            ProjectSymbolAtlasFacadeOwnerOptions(
                project_root=str(project_root),
                target_path="facade.py",
                symbol_name="VALUE",
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "facade" in data["summary"].lower()


def main() -> int:
    test_pa012_detects_facade_and_real_owner()
    test_pa012_allows_non_facade_target()
    test_pa012_builds_report()
    print("PA012 Facade owner resolver tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
