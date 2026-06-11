from __future__ import annotations

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
)
from kanda_reasoner_app.reasoner_context_bundle.output_paths import (  # noqa: E402
    bundle_artifact_paths,
)


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


def _zip_names(destination: Path) -> set[str]:
    return {path.name for path in destination.glob("*.zip")}


def _archive_names(zip_path: Path) -> list[str]:
    with zipfile.ZipFile(zip_path) as archive:
        return archive.namelist()


def test_multi_profile_export_creates_three_zip_profiles_and_readme(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    destination = tmp_path / "outside_exports"
    destination.mkdir(parents=True)
    _make_generated_bundle(project_root)

    result = export_json_handoff_zip_parts(
        project_root,
        destination,
        part_size_mb=DEFAULT_PART_SIZE_MB,
        part_size_bytes=999999999,
    )

    assert result["ok"] is True
    assert result["package_count"] == 3
    assert result["zip_count"] == 3
    assert result["artifact_count"] == 8
    assert Path(str(result["readme_file"]["path"])).name == "developer_tools__ai_handoff_upload_readme.txt"
    assert Path(str(result["readme_file"]["path"])).exists()

    names = _zip_names(destination)
    assert "developer_tools__ai_handoff_upload.zip" in names
    assert "developer_tools__ai_handoff_reconstruction.zip" in names
    assert "developer_tools__ai_handoff_all_in_one.zip" in names

    upload_names = _archive_names(destination / "developer_tools__ai_handoff_upload.zip")
    reconstruction_names = _archive_names(destination / "developer_tools__ai_handoff_reconstruction.zip")
    all_in_one_names = _archive_names(destination / "developer_tools__ai_handoff_all_in_one.zip")

    assert any(name.endswith("UPLOAD_README.txt") for name in upload_names)
    assert any(name.endswith("RECONSTRUCTION_README.txt") for name in reconstruction_names)
    assert not any(name.endswith("__reconstruction_payload.json") for name in upload_names)
    assert any(name.endswith("__reconstruction_payload.json") for name in reconstruction_names)
    assert any(name.endswith("__reconstruction_payload.json") for name in all_in_one_names)
    assert any(name.endswith("__active_snapshot.json") for name in upload_names)
    assert any(name.endswith("__complete_runtime_trace.json") for name in upload_names)


def test_multi_profile_export_splits_each_profile_as_standalone_zip_parts(tmp_path: Path) -> None:
    project_root = tmp_path / "developer_tools"
    destination = tmp_path / "outside_exports"
    destination.mkdir(parents=True)
    _make_generated_bundle(project_root)

    result = export_json_handoff_zip_parts(
        project_root,
        destination,
        part_size_mb=DEFAULT_PART_SIZE_MB,
        part_size_bytes=2500,
    )

    assert result["ok"] is True
    assert result["zip_count"] > 3
    names = _zip_names(destination)
    assert any(name.startswith("developer_tools__ai_handoff_upload_part") for name in names)
    assert any(name.startswith("developer_tools__ai_handoff_all_in_one_part") for name in names)

    for record in result["zip_parts"]:
        zip_path = Path(str(record["path"]))
        assert zip_path.exists()
        assert zipfile.is_zipfile(zip_path)
        assert zip_path.parent == destination


def main() -> int:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        test_multi_profile_export_creates_three_zip_profiles_and_readme(root / "case1")
        test_multi_profile_export_splits_each_profile_as_standalone_zip_parts(root / "case2")
    print("JSONCTX014K multi-profile ZIP export tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
