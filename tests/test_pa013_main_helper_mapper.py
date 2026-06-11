"""Focused tests for PA013 Project Symbol Atlas main/helper mapper."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas.main_helper_mapper import (  # noqa: E402
    PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY,
    ProjectSymbolAtlasMainHelperOptions,
    build_reasoner_symbol_atlas_main_helper_report,
    map_reasoner_symbol_atlas_main_helpers,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_pa013_maps_main_file_to_helper_files() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(
            root / "panel.py",
            "from panel_commands import build_args\n\n"
            "def create_panel():\n"
            "    return build_args()\n",
        )
        _write(
            root / "panel_commands.py",
            "def build_args():\n"
            "    return ['list-tools']\n",
        )
        _write(
            root / "tests" / "test_panel.py",
            "import panel\n\n"
            "def test_panel():\n"
            "    assert panel.create_panel()\n",
        )
        decision = map_reasoner_symbol_atlas_main_helpers(
            ProjectSymbolAtlasMainHelperOptions(
                project_root=str(root),
                target_path="panel.py",
            )
        )
        assert decision.status == PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY
        assert decision.target_role == "main"
        assert decision.main_path.replace("\\", "/") == "panel.py"
        assert "panel_commands.py" in [item.replace("\\", "/") for item in decision.helper_paths]
        assert decision.public_api_owner_path.replace("\\", "/") == "panel.py"
        assert decision.tests_to_run


def test_pa013_maps_helper_target_back_to_main_file() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(
            root / "feature.py",
            "from feature_helpers import helper\n\n"
            "def run():\n"
            "    return helper()\n",
        )
        _write(
            root / "feature_helpers.py",
            "def helper():\n"
            "    return 'ok'\n",
        )
        decision = map_reasoner_symbol_atlas_main_helpers(
            ProjectSymbolAtlasMainHelperOptions(
                project_root=str(root),
                target_path="feature_helpers.py",
            )
        )
        assert decision.status == PROJECT_SYMBOL_ATLAS_MAIN_HELPER_STATUS_READY
        assert decision.target_role == "helper"
        assert decision.main_path.replace("\\", "/") == "feature.py"
        assert "feature_helpers.py" in [item.replace("\\", "/") for item in decision.helper_paths]


def test_pa013_builds_report_without_source_edits() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "alpha.py", "import alpha_writer\n\ndef run():\n    return alpha_writer.write()\n")
        _write(root / "alpha_writer.py", "def write():\n    return 'ok'\n")
        report = build_reasoner_symbol_atlas_main_helper_report(
            ProjectSymbolAtlasMainHelperOptions(
                project_root=str(root),
                target_path="alpha.py",
            )
        )
        data = report.to_dict()
        assert data["report_type"] == "reasoner_symbol_atlas"
        assert "main_helper_mapper" in data["input_sources"]
        assert "alpha_writer.py" in str(data)


def main() -> int:
    test_pa013_maps_main_file_to_helper_files()
    test_pa013_maps_helper_target_back_to_main_file()
    test_pa013_builds_report_without_source_edits()
    print("PA013 Main/helper mapper tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
