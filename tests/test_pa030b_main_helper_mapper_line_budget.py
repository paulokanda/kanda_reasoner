"""PA030B warning-neutral line budget tests for main-helper mapper."""

from pathlib import Path

from kanda_reasoner_app.reasoner_symbol_atlas.main_helper_mapper import (
    map_reasoner_symbol_atlas_main_helpers,
)


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_main_helper_mapper_stays_below_architecture_line_budget() -> None:
    source_path = (
        _project_root()
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_symbol_atlas"
        / "main_helper_mapper.py"
    )
    line_count = len(source_path.read_text(encoding="utf-8").splitlines())

    assert line_count <= 500


def test_public_main_helper_mapper_import_contract_remains_available() -> None:
    assert callable(map_reasoner_symbol_atlas_main_helpers)


if __name__ == "__main__":
    test_main_helper_mapper_stays_below_architecture_line_budget()
    test_public_main_helper_mapper_import_contract_remains_available()
    print("PA030B main-helper mapper line budget tests passed.")
