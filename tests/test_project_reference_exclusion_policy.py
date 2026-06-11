"""Contract test that non-project folders obey Project Exclusion Rules."""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from kanda_reasoner_app.project_exclusion_policy import filter_reasoner_path_strings, load_reasoner_project_exclusion_rules, should_exclude_reasoner_project_path

NON_PROJECT_FOLDERS = ["_project_reference", "tests", "workbench", "snippets"]

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def test_project_reference_and_tab_excluded_folders_are_non_project() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rules = {"folders": NON_PROJECT_FOLDERS, "files": [], "extensions": []}
        _write(root / ".reasoner_tools_gui_prefs.json", json.dumps({"project_ignore_rules": {str(root): rules}}))
        loaded = load_reasoner_project_exclusion_rules(root)
        for folder in NON_PROJECT_FOLDERS:
            assert folder in loaded["folders"]
            assert should_exclude_reasoner_project_path(root / folder / "x.py", root, loaded)
        kept = filter_reasoner_path_strings(["pkg/active.py", "_project_reference/x.py", "tests/test_x.py", "workbench/x.py", "snippets/x.py"], root, loaded)
        assert kept == ["pkg/active.py"]
if __name__ == "__main__":
    test_project_reference_and_tab_excluded_folders_are_non_project()
    print("Project reference exclusion policy tests passed.")
