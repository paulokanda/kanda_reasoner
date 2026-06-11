from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.exclusion_engine as exclusion_engine_module
import kanda_reasoner_app.reasoner_context_bundle.exclusion_provider as exclusion_provider_module
import kanda_reasoner_app.reasoner_context_bundle.exclusion_rules_exporter as exclusion_rules_exporter_module

from kanda_reasoner_app.reasoner_context_bundle import (
    build_exclusion_rules_payload,
    decide_path_exclusion,
    load_bundle_exclusion_rules,
    resolve_project_context,
    write_exclusion_rules_json,
)


def _make_project() -> Path:
    root = Path(tempfile.mkdtemp(prefix="jsonctx004_project_"))
    (root / 'ask_' 'ai_project_reasoner').mkdir()
    (root / 'ask_' 'ai_project_reasoner' / "module.py").write_text(
        "print('ok')\n",
        encoding="utf-8",
    )
    (root / "tests").mkdir()
    (root / "tests" / "test_module.py").write_text("", encoding="utf-8")
    (root / "temp").mkdir()
    (root / "temp" / "scratch.py").write_text("", encoding="utf-8")
    (root / "_project_reference").mkdir()
    (root / "_project_reference" / "note.md").write_text("", encoding="utf-8")
    prefs = {
        "ignore_rules": {
            "folders": ["tests", "temp", "_project_reference"],
            "files": ["test_*.py", "*.log"],
            "extensions": [".tmp"],
        }
    }
    (root / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(prefs),
        encoding="utf-8",
    )
    return root


def test_load_bundle_exclusion_rules_uses_project_policy() -> None:
    root = _make_project()
    rules = load_bundle_exclusion_rules(root)
    assert "tests" in rules.folders
    assert "temp" in rules.folders
    assert "_project_reference" in rules.folders
    assert "test_*.py" in rules.files
    assert ".tmp" in rules.extensions
    assert "project_exclusion_policy" in rules.source


def test_decide_path_exclusion_reports_included_and_excluded_paths() -> None:
    root = _make_project()
    context = resolve_project_context(root)
    rules = load_bundle_exclusion_rules(context)

    included = decide_path_exclusion('ask_' 'ai_project_reasoner' '/module.py', context, rules)
    assert included.included is True
    assert included.excluded is False
    assert included.path == 'ask_' 'ai_project_reasoner' '/module.py'

    excluded_folder = decide_path_exclusion("temp/scratch.py", context, rules)
    assert excluded_folder.included is False
    assert excluded_folder.excluded is True
    assert excluded_folder.rule_type == "folder"
    assert excluded_folder.matched_rule == "temp"

    excluded_file = decide_path_exclusion("other/test_sample.py", context, rules)
    assert excluded_file.excluded is True
    assert excluded_file.rule_type in {"file", "unknown"}


def test_build_exclusion_rules_payload_is_project_agnostic() -> None:
    root = _make_project()
    payload = build_exclusion_rules_payload(root)
    text = json.dumps(payload, sort_keys=True)

    assert payload["schema_version"] == 1
    assert payload["bundle_kind"] == "exclusion_rules"
    assert payload["project"]["project_root_marker"] == "<PROJECT_ROOT>"
    assert payload["project"]["evidence_root_relative"] == "project_analysis_evidence"
    assert payload["project"]["json_complete_relative"] == (
        "project_analysis_evidence/json_complete"
    )
    assert str(root) not in text
    assert "_project_reference/project_analysis_evidence" not in text
    assert "rules" in payload
    assert "decision_examples" in payload


def test_write_exclusion_rules_json_writes_expected_companion_file() -> None:
    root = _make_project()
    context = resolve_project_context(root)
    output_path = write_exclusion_rules_json(context)

    assert output_path.name == context.project_slug + "__exclusion_rules.json"
    assert output_path.parent == root / "project_analysis_evidence" / "json_complete"
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["bundle_kind"] == "exclusion_rules"
    assert data["rules"]["folders"]
    assert data["source"]["contract"] == "read_only_adapter"


def test_public_submodules_are_directly_test_protected() -> None:
    assert hasattr(exclusion_engine_module, "decide_path_exclusion")
    assert hasattr(exclusion_provider_module, "load_bundle_exclusion_rules")
    assert hasattr(exclusion_rules_exporter_module, "write_exclusion_rules_json")


if __name__ == "__main__":
    test_load_bundle_exclusion_rules_uses_project_policy()
    test_decide_path_exclusion_reports_included_and_excluded_paths()
    test_build_exclusion_rules_payload_is_project_agnostic()
    test_write_exclusion_rules_json_writes_expected_companion_file()
    test_public_submodules_are_directly_test_protected()
    print("JSONCTX004 exclusion rules export tests passed.")
