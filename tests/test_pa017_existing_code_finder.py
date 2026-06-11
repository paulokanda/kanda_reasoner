"""Focused tests for PA017 Existing Code Finder."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.existing_code_finder import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY,
    PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES,
    PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_READY,
    ProjectSymbolAtlasExistingCodeFinderOptions,
    build_reasoner_symbol_atlas_existing_code_report,
    find_reasoner_symbol_atlas_existing_code,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _make_project() -> Path:
    root = Path(tempfile.mkdtemp(prefix="pa017_existing_code_"))
    package = root / "sample_app"
    _write(package / "__init__.py", "")
    _write(
        package / "panel.py",
        "from __future__ import annotations\n\n"
        "def build_panel():\n"
        "    return 'panel'\n\n"
        "class PanelController:\n"
        "    pass\n",
    )
    _write(
        package / "panel_commands.py",
        "from __future__ import annotations\n\n"
        "def build_panel_command():\n"
        "    return 'command'\n",
    )
    _write(
        root / "tests" / "test_panel.py",
        "from sample_app.panel import build_panel\n\n"
        "def test_panel():\n"
        "    assert build_panel() == 'panel'\n",
    )
    return root


def test_pa017_finds_existing_symbol() -> None:
    project_root = _make_project()
    result = find_reasoner_symbol_atlas_existing_code(
        ProjectSymbolAtlasExistingCodeFinderOptions(
            project_root=str(project_root),
            symbol_name="build_panel",
            exact=True,
        )
    )
    assert result.status == PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_READY
    assert result.symbol_matches
    assert any(match.name == "build_panel" for match in result.symbol_matches)
    assert any("panel.py" in path for path in result.owner_paths)


def test_pa017_reports_no_matches() -> None:
    project_root = _make_project()
    result = find_reasoner_symbol_atlas_existing_code(
        ProjectSymbolAtlasExistingCodeFinderOptions(
            project_root=str(project_root),
            symbol_name="does_not_exist",
            exact=True,
        )
    )
    assert result.status == PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_NO_MATCHES
    assert not result.symbol_matches


def test_pa017_reports_invalid_empty_query() -> None:
    project_root = _make_project()
    result = find_reasoner_symbol_atlas_existing_code(
        ProjectSymbolAtlasExistingCodeFinderOptions(project_root=str(project_root))
    )
    assert result.status == PROJECT_SYMBOL_ATLAS_EXISTING_CODE_STATUS_INVALID_QUERY


def test_pa017_builds_report() -> None:
    project_root = _make_project()
    report = build_reasoner_symbol_atlas_existing_code_report(
        ProjectSymbolAtlasExistingCodeFinderOptions(
            project_root=str(project_root),
            query_text="build_panel",
            exact=True,
        )
    )
    payload = report.to_dict()
    assert payload["query_result_count"] == 1
    assert payload["symbol_count"] >= 2


def main() -> int:
    test_pa017_finds_existing_symbol()
    test_pa017_reports_no_matches()
    test_pa017_reports_invalid_empty_query()
    test_pa017_builds_report()
    print("PA017 Existing Code Finder tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
