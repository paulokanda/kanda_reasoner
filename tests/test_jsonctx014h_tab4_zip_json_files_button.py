from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from kanda_reasoner_app.reasoner_context_bundle.bundle_orchestrator import (  # noqa: E402
    generate_ai_context_bundle,
)
from kanda_reasoner_app.reasoner_context_bundle.handoff_zip_exporter import (  # noqa: E402
    DEFAULT_PART_SIZE_MB,
    export_json_handoff_zip_parts,
    is_destination_inside_project_root,
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    bundle_artifact_paths,
)
from kanda_reasoner_app.reasoner_tools_shell.runner_help import (  # noqa: E402
    zip_json_files_private_impl,
)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _make_generated_bundle(project_root: Path) -> None:
    source_dir = project_root / "src"
    source_dir.mkdir(parents=True)
    paths = bundle_artifact_paths(project_root)
    paths.complete_json.parent.mkdir(parents=True)
    paths.complete_json.write_text('{"bundle_kind":"complete_graph"}', encoding="utf-8")
    (paths.complete_json.parent / (project_root.name + "__complete_runtime_trace.json")).write_text(
        '{"trace_info":{"trace_version":"test"}}',
        encoding="utf-8",
    )
    (source_dir / "main.py").write_text('print("hello")\n', encoding="utf-8")
    (source_dir / "asset.bin").write_bytes(b"binary-data")
    generate_ai_context_bundle(
        project_root,
        command_results={
            "architecture_validate": {
                "ran": True,
                "exit_code": 0,
                "status": "pass",
                "summary": "Architecture validation passed.",
            },
            "workflow_validate": {
                "ran": True,
                "exit_code": 0,
                "status": "pass",
                "summary": "Workflow validation passed.",
            },
        },
        commands_run_by_bundle=True,
    )


def test_zip_export_rejects_destination_inside_project_root(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    destination = project_root / "exports"
    destination.mkdir(parents=True)

    assert is_destination_inside_project_root(project_root, destination) is True

    _make_generated_bundle(project_root)
    result = export_json_handoff_zip_parts(project_root, destination)

    assert result["ok"] is False
    assert "inside the active project root" in str(result["failures"])


def test_zip_export_creates_multi_profile_standalone_zip_parts_outside_project(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    destination = tmp_path / "outside_exports"
    destination.mkdir(parents=True)
    _make_generated_bundle(project_root)

    result = export_json_handoff_zip_parts(
        project_root,
        destination,
        part_size_mb=DEFAULT_PART_SIZE_MB,
        part_size_bytes=3500,
    )

    assert result["ok"] is True
    assert result["zip_count"] >= 3
    assert result["artifact_count"] == 8
    assert result["package_count"] == 3
    assert Path(str(result["readme_file"]["path"])).exists()

    zip_parts = result["zip_parts"]
    assert isinstance(zip_parts, list)
    seen_runtime_trace = False
    seen_reconstruction = False
    seen_upload_package = False
    seen_all_in_one_package = False
    for record in zip_parts:
        zip_path = Path(str(record["path"]))
        assert zip_path.exists()
        assert zip_path.parent == destination
        assert zipfile.is_zipfile(zip_path)
        seen_upload_package = seen_upload_package or record.get("package") == "upload"
        seen_all_in_one_package = seen_all_in_one_package or record.get("package") == "all_in_one"
        with zipfile.ZipFile(zip_path) as archive:
            names = archive.namelist()
            assert any(name.endswith("README.txt") for name in names)
            seen_runtime_trace = seen_runtime_trace or any(
                name.endswith("__complete_runtime_trace.json") for name in names
            )
            seen_reconstruction = seen_reconstruction or any(
                name.endswith("__reconstruction_payload.json") for name in names
            )

    assert seen_runtime_trace is True
    assert seen_reconstruction is True
    assert seen_upload_package is True
    assert seen_all_in_one_package is True


def test_tab4_zip_json_files_button_is_wired() -> None:
    methods = _read_text(
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_tools_shell"
        / "runner_help"
        / "window_methods_private_impl.py"
    )
    process = _read_text(
        PROJECT_ROOT
        / 'ask_' 'ai_project_reasoner'
        / "reasoner_tools_shell"
        / "runner_help"
        / "zip_json_files_private_impl.py"
    )

    assert zip_json_files_private_impl.DEFAULT_ZIP_SIZE_MB == 40
    assert zip_json_files_private_impl.CONSERVATIVE_ZIP_SIZE_MB == 25
    assert "Zip JSON files" in methods
    assert "Conservative 25 MB" in methods
    assert "Default 40 MB" in methods
    assert "run_zip_json_files" in methods
    assert "handoff_zip_exporter" in process
    assert "ZIP files cannot be saved inside the active project folder" in process
    assert "--part-size-mb" in process


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        root = Path(temp_dir)
        test_zip_export_rejects_destination_inside_project_root(root / "case1")
        test_zip_export_creates_multi_profile_standalone_zip_parts_outside_project(root / "case2")
    test_tab4_zip_json_files_button_is_wired()
    print("JSONCTX014H Tab 4 ZIP JSON files button tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
