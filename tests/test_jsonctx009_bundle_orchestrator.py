"""Focused tests for JSONCTX009 bundle orchestrator."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator as orchestrator_module

from kanda_reasoner_app.reasoner_context_bundle import (
    check_ai_context_bundle,
    generate_ai_context_bundle,
    resolve_project_context,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths


def _make_project(prefix: str = "jsonctx009_project_") -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    ignored = root / "ignored"
    ignored.mkdir()
    (ignored / "skip.py").write_text("SKIP = True\n", encoding="utf-8")
    generated = root / "project_analysis_evidence" / "json_complete"
    generated.mkdir(parents=True)
    prefs = {
        "ignore_rules": {
            "folders": ["ignored", ".git"],
            "files": ["*.log"],
            "extensions": [".tmp"],
        }
    }
    (root / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(prefs),
        encoding="utf-8",
    )
    return root


def _write_complete_json(root: Path) -> Path:
    context = resolve_project_context(root)
    paths = bundle_artifact_paths(context)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text(
        json.dumps({"bundle_kind": "complete_graph", "project": context.project_slug}) + "\n",
        encoding="utf-8",
    )
    return paths.complete_json


def test_orchestrator_writes_all_companion_jsons_without_touching_complete_json() -> None:
    root = _make_project()
    complete_path = _write_complete_json(root)
    before_text = complete_path.read_text(encoding="utf-8")

    result = generate_ai_context_bundle(
        root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 0,
                "summary": "No validation issues",
            },
            "workflow_validate": {
                "ran": True,
                "exit_code": 0,
                "summary": "Summary pass=8 fail=0 warn=0 skip=3",
            },
        },
    )
    paths = bundle_artifact_paths(resolve_project_context(root))

    assert result["ok"] is True
    assert result["project_root_marker"] == "<PROJECT_ROOT>"
    assert result["evidence_root_relative"] == "project_analysis_evidence"
    assert result["complete_json_contract"]["preserved"] is True
    assert result["complete_json_contract"]["schema_changed_by_this_bundle"] is False
    assert complete_path.read_text(encoding="utf-8") == before_text

    assert paths.exclusion_rules_json.exists()
    assert paths.file_manifest_json.exists()
    assert paths.active_snapshot_json.exists()
    assert paths.validation_state_json.exists()
    assert paths.bundle_manifest_json.exists()

    assert check_ai_context_bundle(root)["ok"] is True


def test_orchestrator_uses_dynamic_project_specific_exclusions() -> None:
    root = _make_project()
    _write_complete_json(root)
    result = generate_ai_context_bundle(root)
    paths = bundle_artifact_paths(resolve_project_context(root))
    manifest = json.loads(paths.file_manifest_json.read_text(encoding="utf-8"))
    snapshot = json.loads(paths.active_snapshot_json.read_text(encoding="utf-8"))
    exclusion_rules = json.loads(paths.exclusion_rules_json.read_text(encoding="utf-8"))
    manifest_paths = {item["path"] for item in manifest["files"]}
    snapshot_paths = {item["path"] for item in snapshot["files"]}
    bundle_text = json.dumps(result, sort_keys=True)

    assert 'ask_' 'ai_project_reasoner' '/module.py' in manifest_paths
    assert "README.md" in manifest_paths
    assert "ignored/skip.py" not in manifest_paths
    assert "ignored/skip.py" not in snapshot_paths
    assert "ignored" in exclusion_rules["rules"]["folders"]
    assert str(root) not in bundle_text
    assert "E:\\developer_tools" not in bundle_text
    assert "_project_reference" not in bundle_text


def test_orchestrator_reports_missing_complete_json_without_generating_it() -> None:
    root = _make_project()
    result = generate_ai_context_bundle(root)
    paths = bundle_artifact_paths(resolve_project_context(root))

    assert paths.complete_json.exists() is False
    assert paths.bundle_manifest_json.exists()
    assert result["ok"] is False
    assert any("complete" in failure for failure in result["failures"])
    assert result["complete_json_contract"]["preserved"] is True


def test_public_submodule_contract_is_test_protected() -> None:
    assert hasattr(orchestrator_module, "generate_ai_context_bundle")


if __name__ == "__main__":
    test_orchestrator_writes_all_companion_jsons_without_touching_complete_json()
    test_orchestrator_uses_dynamic_project_specific_exclusions()
    test_orchestrator_reports_missing_complete_json_without_generating_it()
    test_public_submodule_contract_is_test_protected()
    print("JSONCTX009 bundle orchestrator tests passed.")
