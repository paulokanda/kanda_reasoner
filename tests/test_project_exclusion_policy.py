"""Focused public contract tests for project_exclusion_policy."""
from __future__ import annotations
import json
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from kanda_reasoner_app.project_exclusion_policy import filter_reasoner_path_strings, load_reasoner_project_exclusion_rules, should_exclude_reasoner_project_path

def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def test_project_exclusion_policy_reads_project_preferences() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rules = {"folders": ["non_project"], "files": ["*.skip.py"], "extensions": [".tmp"]}
        _write(root / ".reasoner_tools_gui_prefs.json", json.dumps({"project_ignore_rules": {str(root): rules}}))
        loaded = load_reasoner_project_exclusion_rules(root)
        assert "non_project" in loaded["folders"]
        assert should_exclude_reasoner_project_path(root / "non_project" / "x.py", root, loaded)
        assert should_exclude_reasoner_project_path(root / "pkg" / "x.skip.py", root, loaded)
        assert not should_exclude_reasoner_project_path(root / "pkg" / "x.py", root, loaded)
        assert filter_reasoner_path_strings(["pkg/x.py", "non_project/x.py"], root, loaded) == ["pkg/x.py"]
if __name__ == "__main__":
    test_project_exclusion_policy_reads_project_preferences()
    print("Project exclusion policy contract tests passed.")
