"""JSONCTX014D quality gates for canonical JSON handoff artifacts."""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

PROJECT_ROOT_FOR_TEST = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT_FOR_TEST) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT_FOR_TEST))

from kanda_reasoner_app.reasoner_context_bundle.active_snapshot_builder import (
    build_active_snapshot_payload,
)
from kanda_reasoner_app.reasoner_context_bundle.cli import main as bundle_cli_main
from kanda_reasoner_app.reasoner_context_bundle.file_manifest_builder import (
    build_file_manifest_payload,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths
from kanda_reasoner_app.reasoner_context_bundle.validation_state_builder import (
    build_validation_state_payload,
    run_validation_commands,
)


def _write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def _write_text(path: Path, content: str) -> None:
    _write_bytes(path, content.encode("utf-8"))


def _create_validation_scripts(project_root: Path) -> None:
    architecture_script = (
        project_root
        / 'ask_' 'ai_project_reasoner'
        / "manage_architecture"
        / "manage_architecture.py"
    )
    workflow_script = (
        project_root
        / 'ask_' 'ai_project_reasoner'
        / "manage_workflows"
        / "manage_workflows.py"
    )
    script_text = (
        "from __future__ import annotations\n"
        "import sys\n"
        "print('No validation issues.')\n"
        "raise SystemExit(0)\n"
    )
    _write_text(architecture_script, script_text)
    _write_text(workflow_script, script_text)


def test_file_manifest_snapshot_alignment_is_exact() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _write_text(project_root / "README.md", "hello\r\n")
        _write_text(project_root / 'ask_' 'ai_project_reasoner' / "module.py", "print('ok')\n")
        _write_text(project_root / "notes.unknown", "active but unsupported\n")
        _write_bytes(project_root / "binary.dat", b"abc\x00def")
        _write_text(
            project_root
            / "project_analysis_evidence"
            / "json_complete"
            / "developer_tools__complete.json",
            "{}\n",
        )

        manifest = build_file_manifest_payload(project_root)
        snapshot = build_active_snapshot_payload(project_root)

        manifest_files = manifest["files"]
        snapshot_files = snapshot["files"]
        included_paths = sorted(
            item["path"] for item in manifest_files if item["included_in_active_snapshot"]
        )
        snapshot_paths = sorted(item["path"] for item in snapshot_files)

        assert manifest["counts"]["included_in_active_snapshot"] == len(snapshot_files)
        assert included_paths == snapshot_paths

        by_path = {item["path"]: item for item in manifest_files}
        assert by_path["notes.unknown"]["kind"] == "text"
        assert by_path["notes.unknown"]["included_in_active_snapshot"] is False
        assert by_path["notes.unknown"]["snapshot_omission_reason"] == (
            "extension_not_in_snapshot_text_policy"
        )
        assert by_path["binary.dat"]["included_in_active_snapshot"] is False

        omitted_by_path = {item["path"]: item for item in snapshot["omitted_files"]}
        assert omitted_by_path["notes.unknown"]["reason"] == (
            "extension_not_in_snapshot_text_policy"
        )
        assert omitted_by_path["binary.dat"]["reason"] == "binary_file_omitted"


def test_validation_state_can_capture_local_validation_results() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _create_validation_scripts(project_root)

        results = run_validation_commands(project_root)
        payload = build_validation_state_payload(
            project_root,
            command_results=results,
            commands_run_by_bundle=True,
        )

        assert payload["capture_mode"]["mode"] == "local_commands_run"
        assert payload["capture_mode"]["runs_commands"] is True
        assert payload["capture_mode"]["internet_or_ai_contact"] is False
        assert payload["overall"]["freeze_ready_required_commands"] is True
        assert payload["overall"]["required_status"] == "pass"
        assert payload["overall"]["status"] == "pass"

        by_name = {item["name"]: item for item in payload["commands"]}
        assert by_name["architecture_validate"]["status"] == "pass"
        assert by_name["workflow_validate"]["status"] == "pass"
        assert by_name["architecture_diff"]["status"] == "not_run"


def test_cli_can_write_bundle_with_validation_capture() -> None:
    with TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir)
        _create_validation_scripts(project_root)
        _write_text(project_root / "README.md", "hello\n")
        _write_text(project_root / 'ask_' 'ai_project_reasoner' / "module.py", "print('ok')\n")
        paths = bundle_artifact_paths(project_root)
        paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
        _write_text(paths.complete_json, "{}\n")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = bundle_cli_main(
                [
                    "--root",
                    str(project_root),
                    "--write",
                    "--run-validation",
                    "--no-check",
                    "--compact",
                ]
            )

        assert exit_code == 0
        result = json.loads(output.getvalue())
        assert result["ok"] is True
        validation_state = json.loads(paths.validation_state_json.read_text(encoding="utf-8"))
        assert validation_state["capture_mode"]["mode"] == "local_commands_run"
        assert validation_state["overall"]["freeze_ready_required_commands"] is True


if __name__ == "__main__":
    test_file_manifest_snapshot_alignment_is_exact()
    test_validation_state_can_capture_local_validation_results()
    test_cli_can_write_bundle_with_validation_capture()
    print("JSONCTX014D JSON handoff quality tests passed.")
