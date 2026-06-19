"""Focused tests for JSONCTX008 bundle manifest and checker."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.bundle_checker as checker_module
import kanda_reasoner_app.reasoner_context_bundle.bundle_manifest_builder as manifest_module

from kanda_reasoner_app.reasoner_context_bundle import (
    BUNDLE_ARTIFACT_ORDER,
    build_bundle_manifest_payload,
    check_ai_context_bundle,
    raise_for_ai_context_bundle_errors,
    resolve_project_context,
    write_active_snapshot_json,
    write_bundle_manifest_json,
    write_exclusion_rules_json,
    write_file_manifest_json,
    write_reconstruction_payload_json,
    write_validation_state_json,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths


def _make_project(prefix: str = "jsonctx008_project_") -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text("VALUE = 1\n", encoding="utf-8")
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    ignored = root / "ignored"
    ignored.mkdir()
    (ignored / "skip.py").write_text("SKIP = True\n", encoding="utf-8")
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


def _write_complete_json(root: Path) -> None:
    context = resolve_project_context(root)
    paths = bundle_artifact_paths(context)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text(
        json.dumps({"bundle_kind": "complete_graph", "project": context.project_slug}),
        encoding="utf-8",
    )


def _write_required_companion_jsons(root: Path) -> None:
    _write_complete_json(root)
    write_exclusion_rules_json(root)
    write_file_manifest_json(root)
    write_active_snapshot_json(root)
    write_validation_state_json(
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
    write_reconstruction_payload_json(root)


def test_bundle_manifest_records_required_artifacts_without_absolute_root() -> None:
    root = _make_project()
    _write_required_companion_jsons(root)
    payload = build_bundle_manifest_payload(root)
    text = json.dumps(payload, sort_keys=True)
    artifacts = payload["artifacts"]

    assert payload["schema_version"] == 1
    assert payload["bundle_kind"] == "bundle_manifest"
    assert payload["project"]["project_root_marker"] == "<PROJECT_ROOT>"
    assert payload["project"]["evidence_root_relative"] == "project_analysis_evidence"
    assert str(root) not in text
    assert "_project_reference" not in text
    assert payload["complete_json_contract"]["status"] == "protected_existing_consumer"
    assert payload["complete_json_contract"]["schema_changed_by_this_bundle"] is False
    assert payload["compatibility"]["additive_bundle"] is True
    assert payload["compatibility"]["hardcoded_project_root"] is False

    names = [item["name"] for item in artifacts]
    assert names == list(BUNDLE_ARTIFACT_ORDER)
    assert payload["counts"]["required_artifacts_missing"] == 0
    assert payload["counts"]["artifacts_existing"] == len(BUNDLE_ARTIFACT_ORDER)
    assert names[-1] == "bundle_manifest_json"
    assert artifacts[-1]["self_reference"] is True
    assert artifacts[-1]["hash_status"] == "self_hash_not_embedded"


def test_write_bundle_manifest_and_checker_pass_for_complete_bundle() -> None:
    root = _make_project()
    _write_required_companion_jsons(root)
    manifest_path = write_bundle_manifest_json(root)

    assert manifest_path.exists()
    result = check_ai_context_bundle(root)
    assert result["ok"] is True
    assert result["failures"] == []
    assert result["checked_artifacts"] == len(BUNDLE_ARTIFACT_ORDER)


def test_checker_detects_hash_mismatch() -> None:
    root = _make_project()
    _write_required_companion_jsons(root)
    write_bundle_manifest_json(root)
    paths = bundle_artifact_paths(resolve_project_context(root))
    paths.complete_json.write_text('{"changed": true}\n', encoding="utf-8")

    result = check_ai_context_bundle(root)
    assert result["ok"] is False
    assert any("hash mismatch" in failure for failure in result["failures"])


def test_checker_detects_missing_artifact() -> None:
    root = _make_project()
    _write_required_companion_jsons(root)
    write_bundle_manifest_json(root)
    paths = bundle_artifact_paths(resolve_project_context(root))
    paths.active_snapshot_json.unlink()

    result = check_ai_context_bundle(root)
    assert result["ok"] is False
    assert any("active_snapshot" in failure for failure in result["failures"])


def test_public_submodule_contracts_are_test_protected() -> None:
    assert hasattr(manifest_module, "build_bundle_manifest_payload")
    assert hasattr(manifest_module, "write_bundle_manifest_json")
    assert hasattr(checker_module, "check_ai_context_bundle")
    assert hasattr(checker_module, "raise_for_ai_context_bundle_errors")

    root = _make_project()
    _write_required_companion_jsons(root)
    write_bundle_manifest_json(root)
    raise_for_ai_context_bundle_errors(root)


if __name__ == "__main__":
    test_bundle_manifest_records_required_artifacts_without_absolute_root()
    test_write_bundle_manifest_and_checker_pass_for_complete_bundle()
    test_checker_detects_hash_mismatch()
    test_checker_detects_missing_artifact()
    test_public_submodule_contracts_are_test_protected()
    print("JSONCTX008 bundle manifest and checker tests passed.")
