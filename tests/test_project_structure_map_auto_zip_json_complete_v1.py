from __future__ import annotations

import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.project_analysis_evidence_paths import analysis_json_complete_dir
from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import generate_ai_context_bundle
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (
    ALLOWED_PART_SIZE_MB_OPTIONS,
    export_json_handoff_zip_parts,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import bundle_artifact_paths
from kanda_reasoner_app.reasoner_tools_shell.runner_help import zip_json_files_private_impl


def _make_generated_bundle(project_root: Path) -> None:
    project_root.mkdir(parents=True, exist_ok=True)
    source_dir = project_root / "src"
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "main.py").write_text('print("hello")\n', encoding="utf-8")

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
    assert result["ok"] is True


def test_exporter_accepts_new_size_options_and_writes_to_show_project_to_ai_folder() -> None:
    assert ALLOWED_PART_SIZE_MB_OPTIONS == (100, 200, 300, 400, 500)
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_name:
        temp_root = Path(temp_name)
        project_root = temp_root / "demo_project"
        _make_generated_bundle(project_root)

        destination = analysis_json_complete_dir(project_root)
        destination.mkdir(parents=True, exist_ok=True)
        result = export_json_handoff_zip_parts(
            project_root,
            destination,
            part_size_mb=500,
            part_size_bytes=999999999,
        )

        assert result["ok"] is True, result
        assert result["destination_folder"] == str(destination)
        assert result["part_size_mb"] == 500
        assert result["package_count"] == 3
        assert result["zip_count"] == 3
        assert "json_splitted" not in result["destination_folder"]
        assert "architecture_audit" not in result["destination_folder"]
        assert "json_complete" not in result["destination_folder"]
        assert all(
            Path(str(item["path"])).parent == destination
            or str(item["path"]).startswith("show_project_to_AI/second_prompt_files/")
            for item in result["zip_parts"]
        )
        assert any(path.name.endswith("__ai_handoff_upload.zip") for path in destination.glob("*.zip"))
        with zipfile.ZipFile(next(destination.glob("*__ai_handoff_upload.zip"))) as archive:
            names = archive.namelist()
        assert any("show_project_to_AI/second_prompt_files" in name for name in names)
        assert any(name.endswith("__ai_briefing.json") for name in names)


def test_collector_ui_has_extended_zip_sizes_and_auto_zip_hook() -> None:
    methods = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_methods_private_impl.py"
    ).read_text(encoding="utf-8")
    process = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_process_private_impl.py"
    ).read_text(encoding="utf-8")
    zipper = (
        PROJECT_ROOT
        / "kanda_reasoner_app"
        / "reasoner_tools_shell"
        / "runner_help"
        / "zip_json_files_private_impl.py"
    ).read_text(encoding="utf-8")

    for label in ("100 MB", "200 MB", "300 MB", "400 MB", "500 MB"):
        assert label in methods
    assert "Conservative 25 MB" not in methods
    assert "Default 40 MB" not in methods
    assert "Zip JSON files" not in methods
    assert "clear_second_prompt_files_building_dir" in process
    assert "publish_second_prompt_files_building_dir" in zipper
    assert "auto_zip_json_complete" in process
    assert "manual ZIP button removed" in zipper
    assert "analysis_json_complete_dir" in zipper
    assert "second_prompt_files" in zipper
    assert "second_prompt_files_building" in zipper
    assert zip_json_files_private_impl.ALLOWED_ZIP_SIZE_MB_OPTIONS == (100, 200, 300, 400, 500)


def main() -> int:
    test_exporter_accepts_new_size_options_and_writes_to_show_project_to_ai_folder()
    test_collector_ui_has_extended_zip_sizes_and_auto_zip_hook()
    print("VALIDATION OK: project_structure_map_auto_zip_json_complete_v1")
    print("VALIDATION OK: project structure map auto zip json complete")
    print("STATUS: IN_SYNC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
