"""Focused tests for JSONCTX007 validation-state generation."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import kanda_reasoner_app.reasoner_context_bundle.validation_state_builder as validation_state_module

from kanda_reasoner_app.reasoner_context_bundle import (
    DEFAULT_VALIDATION_COMMANDS,
    build_validation_state_payload,
    resolve_project_context,
    write_validation_state_json,
)


def _make_project(prefix: str = "jsonctx007_project_") -> Path:
    root = Path(tempfile.mkdtemp(prefix=prefix))
    package = root / 'ask_' 'ai_project_reasoner'
    package.mkdir()
    (package / "module.py").write_text("print('ok')\n", encoding="utf-8")
    prefs = {
        "ignore_rules": {
            "folders": ["ignored"],
            "files": ["*.log"],
            "extensions": [".tmp"],
        }
    }
    (root / ".reasoner_tools_gui_prefs.json").write_text(
        json.dumps(prefs),
        encoding="utf-8",
    )
    return root


def _commands_by_name(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    commands = payload["commands"]
    assert isinstance(commands, list)
    return {str(item["name"]): item for item in commands if isinstance(item, dict)}


def test_default_validation_state_makes_no_false_pass_claims() -> None:
    root = _make_project()
    payload = build_validation_state_payload(root)
    text = json.dumps(payload, sort_keys=True)
    commands = _commands_by_name(payload)

    assert payload["schema_version"] == 1
    assert payload["bundle_kind"] == "validation_state"
    assert payload["project"]["project_root_marker"] == "<PROJECT_ROOT>"
    assert payload["project"]["evidence_root_relative"] == "project_analysis_evidence"
    assert str(root) not in text

    assert payload["capture_mode"]["runs_commands"] is False
    assert payload["overall"]["status"] == "not_run"
    assert payload["overall"]["freeze_ready_required_commands"] is False

    assert commands["architecture_validate"]["status"] == "not_run"
    assert commands["architecture_validate"]["ran"] is False
    assert commands["workflow_validate"]["status"] == "not_run"
    assert commands["architecture_diff"]["required_for_freeze"] is False


def test_validation_state_uses_provided_results_without_absolute_root() -> None:
    root = _make_project()
    payload = build_validation_state_payload(
        root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 0,
                "summary": "No validation issues",
                "stdout_tail": "ARCHITECTURE VALIDATION SUMMARY",
            },
            "workflow_validate": {
                "ran": True,
                "exit_code": 0,
                "summary": "Summary pass=8 fail=0 warn=0 skip=3",
            },
        },
    )
    text = json.dumps(payload, sort_keys=True)
    commands = _commands_by_name(payload)

    assert str(root) not in text
    assert "<PROJECT_ROOT>" in commands["architecture_validate"]["command"]
    assert commands["architecture_validate"]["status"] == "pass"
    assert commands["workflow_validate"]["status"] == "pass"
    assert commands["architecture_diff"]["status"] == "not_run"
    assert payload["overall"]["status"] == "pass"
    assert payload["overall"]["freeze_ready_required_commands"] is True


def test_validation_state_records_failure_when_provided() -> None:
    root = _make_project()
    payload = build_validation_state_payload(
        root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 1,
                "summary": "Errors found",
                "stderr_tail": "failure",
            }
        },
    )
    commands = _commands_by_name(payload)

    assert commands["architecture_validate"]["status"] == "fail"
    assert commands["architecture_validate"]["exit_code"] == 1
    assert payload["overall"]["status"] == "fail"
    assert payload["overall"]["freeze_ready_required_commands"] is False


def test_write_validation_state_json_writes_expected_project_owned_file() -> None:
    root = _make_project()
    context = resolve_project_context(root)
    output_path = write_validation_state_json(context)

    assert output_path.name == context.project_slug + "__validation_state.json"
    assert output_path.parent == root / "project_analysis_evidence" / "json_complete"
    assert output_path.exists()

    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert data["bundle_kind"] == "validation_state"
    assert data["capture_mode"]["runs_commands"] is False


def test_public_submodule_contracts_are_test_protected() -> None:
    names = {item["name"] for item in DEFAULT_VALIDATION_COMMANDS}
    assert "architecture_validate" in names
    assert "workflow_validate" in names
    assert hasattr(validation_state_module, "build_validation_state_payload")
    assert hasattr(validation_state_module, "write_validation_state_json")


if __name__ == "__main__":
    test_default_validation_state_makes_no_false_pass_claims()
    test_validation_state_uses_provided_results_without_absolute_root()
    test_validation_state_records_failure_when_provided()
    test_write_validation_state_json_writes_expected_project_owned_file()
    test_public_submodule_contracts_are_test_protected()
    print("JSONCTX007 validation state builder tests passed.")
