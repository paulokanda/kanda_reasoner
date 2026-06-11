"""PA024 tests for Project Exclusion Rules across Tab 4 and Tab 5."""
from __future__ import annotations
import json
import os
import sys
import tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from kanda_reasoner_app.project_json_scope_filter import filter_project_analysis_json_payload  # noqa: E402
from kanda_reasoner_app.project_exclusion_policy import load_reasoner_project_exclusion_rules, should_exclude_reasoner_project_path  # noqa: E402
from kanda_reasoner_app.reasoner_context_collector import collector_scope  # noqa: E402
from kanda_reasoner_app.reasoner_context_collector.collector_config import CollectorConfig  # noqa: E402
from kanda_reasoner_app.reasoner_context_collector.collector_walker import walk_python_files_filtered  # noqa: E402

def _write(path: Path, text: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def _write_prefs(root: Path) -> None:
    rules = {"folders": ["tests", "workbench", "_project_reference"], "files": ["*.skip.py"], "extensions": [".tmp"]}
    payload = {"active_project_ignore_rules_key": str(root), "ignore_rules": rules, "project_ignore_rules": {str(root): rules, str(root).replace("\\", "/"): rules}}
    _write(root / ".reasoner_tools_gui_prefs.json", json.dumps(payload, indent=2))

def test_pa024_collector_scope_loads_saved_tab8_rules_without_gui_env() -> None:
    old_env = dict(os.environ)
    try:
        for key in ("PROJECT_REASONER_TAB8_IGNORE_RULES_JSON", "PROJECT_REASONER_IGNORE_RULES_JSON", "KANDA_REASONER_TAB8_IGNORE_RULES_JSON"):
            os.environ.pop(key, None)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _write_prefs(root)
            _write(root / "pkg" / "active.py", "x = 1\n")
            _write(root / "tests" / "test_hidden.py", "x = 1\n")
            _write(root / "workbench" / "generated.py", "x = 1\n")
            _write(root / "_project_reference" / "notes.py", "x = 1\n")
            _write(root / "pkg" / "bad.skip.py", "x = 1\n")
            rules = load_reasoner_project_exclusion_rules(root)
            assert "tests" in rules["folders"]
            assert should_exclude_reasoner_project_path(root / "tests" / "test_hidden.py", root, rules)
            paths = [path.relative_to(root).as_posix() for path in collector_scope.iter_project_python_files(root)]
            assert paths == ["pkg/active.py"]
    finally:
        os.environ.clear()
        os.environ.update(old_env)

def test_pa024_collector_walker_uses_same_unified_rules() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_prefs(root)
        _write(root / "pkg" / "active.py", "x = 1\n")
        _write(root / "tests" / "test_hidden.py", "x = 1\n")
        paths = [path.relative_to(root).as_posix() for path in walk_python_files_filtered(root, CollectorConfig())]
        assert paths == ["pkg/active.py"]

def test_pa024_tab5_filters_complete_json_before_split() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_prefs(root)
        payload = {"collector_info": {"project_root": str(root)}, "project_summary": {"project_root": str(root)}, "source_file_index": {"pkg/active.py": {"file": "pkg/active.py"}, "tests/test_hidden.py": {"file": "tests/test_hidden.py"}, "_project_reference/notes.py": {"file": "_project_reference/notes.py"}}, "web_ai_symbol_index": [{"file": "pkg/active.py", "symbols": []}, {"file": "workbench/generated.py", "symbols": []}]}
        filtered, summary = filter_project_analysis_json_payload(payload, project_root=root)
        assert summary["applied"] is True
        assert summary["removed_count"] >= 2
        assert "pkg/active.py" in filtered["source_file_index"]
        assert "tests/test_hidden.py" not in filtered["source_file_index"]
        assert "_project_reference/notes.py" not in filtered["source_file_index"]
        assert filtered["web_ai_symbol_index"] == [{"file": "pkg/active.py", "symbols": []}]

def test_pa024_json_splitter_8_loader_installs_project_filter() -> None:
    text = (ROOT / 'ask_' 'ai_project_reasoner' '/json_splitter/json_splitter_8_help/source_loader_private_impl.py').read_text(encoding="utf-8")
    assert "PA024_PROJECT_EXCLUSION_RULES_SOURCE_INSTALL" in text
    assert "install_json_splitter_project_exclusion_filter" in text

def main() -> int:
    test_pa024_collector_scope_loads_saved_tab8_rules_without_gui_env()
    test_pa024_collector_walker_uses_same_unified_rules()
    test_pa024_tab5_filters_complete_json_before_split()
    test_pa024_json_splitter_8_loader_installs_project_filter()
    print("PA024 Project Exclusion Rules all-tabs tests passed.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
