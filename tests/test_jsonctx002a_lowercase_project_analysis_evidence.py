"""Focused tests for the lowercase project_analysis_evidence path contract."""

from __future__ import annotations

import tempfile
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (  # noqa: E402
    PROJECT_ANALYSIS_EVIDENCE_DIR,
    analysis_json_complete_dir,
    analysis_json_parts_dir,
    ensure_project_analysis_evidence_dirs,
    project_analysis_evidence_root,
    relative_primary_evidence_json_path,
)
from kanda_reasoner_app.reasoner_symbol_atlas.evidence_paths import (  # noqa: E402
    get_reasoner_symbol_atlas_canonical_evidence_dir,
)


def _child_directory_names(path: Path) -> set[str]:
    """Return actual child directory names using filesystem casing."""
    return {child.name for child in path.iterdir() if child.is_dir()}


def test_project_analysis_evidence_dir_is_lowercase() -> None:
    assert PROJECT_ANALYSIS_EVIDENCE_DIR == "project_analysis_evidence"


def test_dynamic_project_root_uses_lowercase_project_owned_evidence_folder() -> None:
    root = Path("C:/dynamic_project_root")
    assert project_analysis_evidence_root(root) == root / "project_analysis_evidence"
    assert analysis_json_complete_dir(root) == root / "project_analysis_evidence" / "json_complete"
    assert analysis_json_parts_dir(root) == root / "project_analysis_evidence" / "json_splitted"
    assert str(project_analysis_evidence_root(root)).find("_project_reference") == -1


def test_relative_primary_evidence_path_is_lowercase() -> None:
    relative = relative_primary_evidence_json_path("alpha_project")
    assert relative == "project_analysis_evidence/json_complete/alpha_project__complete.json"
    assert "PROJECT_ANALYSIS_EVIDENCE" not in relative
    assert "_project_reference" not in relative


def test_ensure_project_analysis_evidence_dirs_creates_only_project_owned_path() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "demo_project"
        root.mkdir()
        evidence_root = ensure_project_analysis_evidence_dirs(root)
        assert evidence_root == root / "project_analysis_evidence"
        assert (root / "project_analysis_evidence" / "json_complete").is_dir()
        assert (root / "project_analysis_evidence" / "json_splitted").is_dir()
        child_names = _child_directory_names(root)
        assert "project_analysis_evidence" in child_names
        assert "PROJECT_ANALYSIS_EVIDENCE" not in child_names
        assert not (root / "_project_reference" / "project_analysis_evidence").exists()




def test_ensure_project_analysis_evidence_dirs_renames_legacy_uppercase_folder() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "demo_project"
        legacy = root / "PROJECT_ANALYSIS_EVIDENCE"
        legacy_json = legacy / "json_complete"
        legacy_json.mkdir(parents=True)
        (legacy_json / "demo__complete.json").write_text("{}", encoding="utf-8")

        evidence_root = ensure_project_analysis_evidence_dirs(root)

        assert evidence_root == root / "project_analysis_evidence"
        child_names = _child_directory_names(root)
        assert "project_analysis_evidence" in child_names
        assert "PROJECT_ANALYSIS_EVIDENCE" not in child_names
        assert (evidence_root / "json_complete" / "demo__complete.json").exists()
        assert (evidence_root / "json_splitted").is_dir()

def test_reasoner_symbol_atlas_uses_same_lowercase_canonical_path() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir) / "another_dynamic_project"
        canonical_dir = get_reasoner_symbol_atlas_canonical_evidence_dir(root)
        assert canonical_dir == root.resolve(strict=False) / "project_analysis_evidence"
        assert canonical_dir.name == "project_analysis_evidence"


if __name__ == "__main__":
    test_project_analysis_evidence_dir_is_lowercase()
    test_dynamic_project_root_uses_lowercase_project_owned_evidence_folder()
    test_relative_primary_evidence_path_is_lowercase()
    test_ensure_project_analysis_evidence_dirs_creates_only_project_owned_path()
    test_ensure_project_analysis_evidence_dirs_renames_legacy_uppercase_folder()
    test_reasoner_symbol_atlas_uses_same_lowercase_canonical_path()
    print("JSONCTX002A lowercase project_analysis_evidence tests passed.")
