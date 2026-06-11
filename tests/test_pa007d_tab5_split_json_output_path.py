"""PA007D tests for canonical Tab 5 split JSON evidence paths."""

from __future__ import annotations

import ast
import tempfile
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_parts_dir,
    ensure_project_analysis_evidence_dirs,
    parts_index_file_path,
    parts_manifest_file_path,
    project_analysis_evidence_root,
    relative_parts_index_file_path,
    relative_parts_manifest_file_path,
    relative_route_manifest_file_path,
    route_manifest_file_path,
)


def _assert_canonical(path: Path, project_root: Path) -> None:
    text = str(path).replace("\\", "/")
    root_text = str(project_root).replace("\\", "/")
    assert text.startswith(root_text + "/project_analysis_evidence/")
    assert "/_project_reference/" not in text


def test_pa007d_split_paths_are_canonical_and_dynamic() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        project_root = Path(tmp) / "future_project"
        project_root.mkdir()

        parts_dir = analysis_json_parts_dir(project_root)
        manifest = parts_manifest_file_path(project_root)
        index = parts_index_file_path(project_root)
        route = route_manifest_file_path(project_root)

        assert project_analysis_evidence_root(project_root) == (
            project_root / "project_analysis_evidence"
        )
        assert parts_dir == project_root / "project_analysis_evidence" / "json_splitted"
        assert manifest.name == "future_project_split_manifest.json"
        assert index.name == "future_project_split_index.json"
        assert route.name == "future_project__complete__web_ai_route_manifest.json"

        for path in (parts_dir, manifest, index, route):
            _assert_canonical(path, project_root)

        ensure_project_analysis_evidence_dirs(project_root)
        assert parts_dir.exists()
        assert (project_root / "project_analysis_evidence" / "json_complete").exists()
        assert not (project_root / "_project_reference").exists()


def test_pa007d_relative_split_paths_are_canonical() -> None:
    assert relative_parts_manifest_file_path("alpha") == (
        "project_analysis_evidence/json_splitted/alpha_split_manifest.json"
    )
    assert relative_parts_index_file_path("alpha") == (
        "project_analysis_evidence/json_splitted/alpha_split_index.json"
    )
    assert relative_route_manifest_file_path("alpha") == (
        "project_analysis_evidence/json_splitted/alpha__complete__web_ai_route_manifest.json"
    )


def _function_body_names(source_path: Path, function_name: str) -> set[str]:
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            names: set[str] = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Name):
                    names.add(child.id)
                elif isinstance(child, ast.Attribute):
                    names.add(child.attr)
            return names
    raise AssertionError(f"Function not found: {function_name}")


def test_pa007d_tab5_window_output_paths_use_canonical_helpers() -> None:
    source_path = (
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_tools_gui_shell"
        / "main_window_help"
        / "window_output_paths.py"
    )
    source = source_path.read_text(encoding="utf-8")
    assert "from kanda_reasoner_app.project_analysis_evidence_paths import" in source
    assert "analysis_json_parts_dir" in source
    assert "parts_manifest_file_path" in source
    assert "parts_index_file_path" in source

    split_names = _function_body_names(source_path, "_json_splitted_dir")
    manifest_names = _function_body_names(source_path, "_split_manifest_file")
    index_names = _function_body_names(source_path, "_split_index_file")

    assert "analysis_json_parts_dir" in split_names
    assert "parts_manifest_file_path" in manifest_names
    assert "parts_index_file_path" in index_names


def main() -> int:
    test_pa007d_split_paths_are_canonical_and_dynamic()
    test_pa007d_relative_split_paths_are_canonical()
    test_pa007d_tab5_window_output_paths_use_canonical_helpers()
    print("PA007D Tab 5 split JSON output path tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
