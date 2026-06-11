"""Focused tests for PA015B related file finder split repair."""

from __future__ import annotations

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_symbol_atlas import _related_file_finder_support as support  # noqa: E402
from kanda_reasoner_app.reasoner_symbol_atlas.related_file_finder import (  # noqa: E402
    ProjectSymbolAtlasRelatedFileOptions,
    find_reasoner_symbol_atlas_related_files,
)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def test_pa015b_helper_module_has_private_public_surface() -> None:
    public_names = [name for name in vars(support) if not name.startswith("_")]
    allowed = {"annotations"}
    assert set(public_names) <= allowed
    assert support.__all__ == []


def test_pa015b_public_module_remains_under_large_module_threshold() -> None:
    source_path = PROJECT_ROOT / 'ask_' 'ai_project_reasoner' / "reasoner_symbol_atlas" / "related_file_finder.py"
    line_count = len(source_path.read_text(encoding="utf-8").splitlines())
    assert line_count <= 500


def test_pa015b_split_preserves_related_file_behavior() -> None:
    with TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        _write(root / "alpha_panel.py", "from alpha_panel_commands import build_args\n")
        _write(root / "alpha_panel_commands.py", "def build_args():\n    return []\n")
        _write(root / "tests" / "test_alpha_panel.py", "import alpha_panel\n")
        decision = find_reasoner_symbol_atlas_related_files(
            ProjectSymbolAtlasRelatedFileOptions(
                project_root=str(root),
                target_path="alpha_panel_commands.py",
            )
        )
        assert "alpha_panel.py" in tuple(path.replace("\\", "/") for path in decision.main_files)
        assert "alpha_panel_commands.py" in tuple(path.replace("\\", "/") for path in decision.helper_files)
        assert decision.tests_to_run


def main() -> int:
    test_pa015b_helper_module_has_private_public_surface()
    test_pa015b_public_module_remains_under_large_module_threshold()
    test_pa015b_split_preserves_related_file_behavior()
    print("PA015B Related file finder split repair tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
