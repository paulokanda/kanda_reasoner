"""Focused PA007C tests for Tab 4 complete JSON output path contract."""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    ensure_project_analysis_evidence_dirs,
    primary_evidence_json_path,
    project_analysis_evidence_root,
    secondary_evidence_json_path,
)


def test_pa007c_tab4_complete_json_uses_canonical_evidence_root() -> None:
    """Tab 4 complete JSON path helpers should not write under _project_reference."""
    project_root = Path(r"E:\future_project")

    evidence_root = project_analysis_evidence_root(project_root)
    complete_dir = analysis_json_complete_dir(project_root)
    primary_json = primary_evidence_json_path(project_root)
    runtime_json = secondary_evidence_json_path(project_root)

    assert evidence_root == project_root / "project_analysis_evidence"
    assert complete_dir == evidence_root / "json_complete"
    assert primary_json == complete_dir / "future_project__complete.json"
    assert runtime_json == complete_dir / "future_project__complete_runtime_trace.json"
    assert "_project_reference" not in primary_json.as_posix()
    assert "_project_reference" not in runtime_json.as_posix()


def test_pa007c_ensure_dirs_creates_canonical_only(tmp_path: Path) -> None:
    """Directory creation should create canonical folders and not legacy folders."""
    project_root = tmp_path / "sample_project"
    project_root.mkdir()

    evidence_root = ensure_project_analysis_evidence_dirs(project_root)

    assert evidence_root == project_root / "project_analysis_evidence"
    assert (evidence_root / "json_complete").is_dir()
    assert (evidence_root / "json_splitted").is_dir()
    assert not (project_root / "_project_reference" / "project_analysis_evidence").exists()


def main() -> int:
    test_pa007c_tab4_complete_json_uses_canonical_evidence_root()
    with __import__("tempfile").TemporaryDirectory() as temp_dir:
        test_pa007c_ensure_dirs_creates_canonical_only(Path(temp_dir))
    print("PA007C Tab 4 complete JSON output path tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
