from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import (
    analysis_json_complete_dir,
    primary_evidence_json_path,
    project_analysis_evidence_root,
)
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import generate_ai_context_bundle
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import export_json_handoff_zip_parts
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths


def _make_generated_bundle(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    src = project_root / "src"
    src.mkdir(parents=True, exist_ok=True)
    (src / "main.py").write_text('print("hello")\n', encoding="utf-8")

    paths = bundle_artifact_paths(project_root)
    paths.complete_json.parent.mkdir(parents=True, exist_ok=True)
    paths.complete_json.write_text('{"bundle_kind":"complete_graph"}', encoding="utf-8")
    paths.complete_json.with_name(project_root.name + "__complete_runtime_trace.json").write_text(
        '{"trace_info":{"trace_version":"test"}}',
        encoding="utf-8",
    )
    result = generate_ai_context_bundle(
        project_root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 0,
                "status": "pass",
                "summary": "Architecture validation passed.",
            }
        },
        commands_run_by_bundle=True,
    )
    assert result["ok"] is True, result


def test_project_structure_map_uses_show_project_to_ai_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        project_root.mkdir()

        evidence_root = project_analysis_evidence_root(project_root)
        complete_dir = analysis_json_complete_dir(project_root)
        primary = primary_evidence_json_path(project_root)

        assert complete_dir == evidence_root / "second_prompt_files"
        assert evidence_root.name == "demo_project_show_project_to_AI"
        assert complete_dir.name == "second_prompt_files"
        assert "architecture_audit" not in str(complete_dir)
        assert "json_complete" not in str(complete_dir)
        assert primary == complete_dir / "demo_project__complete.json"
        assert not (project_root / "project_analysis_evidence").exists()


def test_bundle_and_auto_zip_destination_use_show_project_to_ai_folder() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        _make_generated_bundle(project_root)

        destination = analysis_json_complete_dir(project_root)
        result = export_json_handoff_zip_parts(
            project_root,
            destination,
            part_size_mb=100,
            part_size_bytes=999999999,
        )

        assert result["ok"] is True, result
        assert result["destination_folder"] == str(destination)
        assert destination.name == "second_prompt_files"
        assert destination.parent.name == "demo_project_show_project_to_AI"
        assert "architecture_audit" not in result["destination_folder"]
        assert "json_complete" not in result["destination_folder"]
        assert any(path.name.endswith("__ai_handoff_upload.zip") for path in destination.glob("*.zip"))
        with zipfile.ZipFile(next(destination.glob("*__ai_handoff_upload.zip"))) as archive:
            names = archive.namelist()
        assert any("show_project_to_AI/second_prompt_files" in name for name in names)
        assert not any("project_analysis_evidence/json_complete" in name for name in names)


def test_source_mentions_new_contract_not_old_output_contract() -> None:
    files = [
        PROJECT_ROOT / "kanda_reasoner_app" / "project_analysis_evidence_paths.py",
        PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "bundle_orchestrator.py",
        PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_context_bundle" / "bundle_manifest_builder.py",
        PROJECT_ROOT / "kanda_reasoner_app" / "reasoner_tools_shell" / "runner_help" / "zip_json_files_private_impl.py",
    ]
    joined = "\n".join(path.read_text(encoding="utf-8") for path in files)
    assert "_show_project_to_AI" in joined
    assert "_architecture_audit\\\\current\\\\json_complete" not in joined
    assert "_architecture_audit/current/json_complete" not in joined


def main() -> int:
    test_project_structure_map_uses_show_project_to_ai_folder()
    test_bundle_and_auto_zip_destination_use_show_project_to_ai_folder()
    test_source_mentions_new_contract_not_old_output_contract()
    print("VALIDATION OK: project_structure_map_show_project_to_ai_folder_v1")
    print("VALIDATION OK: project structure map show project to AI folder")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
