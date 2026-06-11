"""Tests for Engineering Safety Project Symbol Atlas integration."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.engineering_safety.reasoner_symbol_atlas_integration import (  # noqa: E402
    ENGINEERING_SAFETY_ATLAS_STATUS_FAILED,
    EngineeringSafetyProjectSymbolAtlasOptions,
    build_engineering_safety_reasoner_symbol_atlas_context,
    engineering_safety_reasoner_symbol_atlas_evidence_lines,
    format_engineering_safety_reasoner_symbol_atlas_markdown,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_pa020_context_builds_from_live_project() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write(
            root / "app" / "main_panel.py",
            '"""Main panel."""\n\ndef build_panel():\n    return "panel"\n',
        )
        _write(
            root / "app" / "main_panel_commands.py",
            '"""Panel commands."""\n\ndef build_panel_command():\n    return "command"\n',
        )
        _write(
            root / "tests" / "test_main_panel.py",
            "from app.main_panel import build_panel\n\ndef test_build_panel():\n    assert build_panel() == 'panel'\n",
        )
        options = EngineeringSafetyProjectSymbolAtlasOptions(
            project_root=str(root),
            task_description="update panel command helper",
            target_path="app/main_panel_commands.py",
            symbol_name="build_panel_command",
            require_test_protection=False,
        )
        context = build_engineering_safety_reasoner_symbol_atlas_context(options)
        data = context.to_dict()
        assert data["project_root"]
        assert data["symbol_name"] == "build_panel_command"
        assert data["status"] != ENGINEERING_SAFETY_ATLAS_STATUS_FAILED
        assert isinstance(data["related_files_to_inspect"], list)
        assert isinstance(data["tests_to_run"], list)
        assert data["tests_to_run"]
        markdown = format_engineering_safety_reasoner_symbol_atlas_markdown(context)
        assert "Engineering Safety Project Symbol Atlas Context" in markdown
        assert "Pre-patch status" in markdown
        lines = engineering_safety_reasoner_symbol_atlas_evidence_lines(context)
        assert lines
        assert lines[0].startswith("Atlas status:")


def main() -> int:
    test_pa020_context_builds_from_live_project()
    print("PA020 Engineering Safety Project Symbol Atlas integration tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
